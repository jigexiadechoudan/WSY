"""
RAG 服务 - 基于 Neo4j 知识图谱的检索增强生成
"""

from app.services.neo4j_service import neo4j_service
from app.services.llm_service import LangChainService
from typing import List, Dict, Any
from elasticsearch import Elasticsearch
from app.core.config import settings

class RAGService:
    """RAG 服务 - 结合知识图谱, Elasticsearch和 LLM"""

    def __init__(self):
        self.neo4j = neo4j_service
        self.llm = LangChainService()
        self.es = Elasticsearch([settings.ES_URL])
        self.es_index = settings.ES_INDEX_NAME

    def extract_keywords(self, query: str) -> List[str]:
        """
        从用户问题中提取关键词

        Args:
            query: 用户问题

        Returns:
            关键词列表
        """
        # 使用 LLM 提取关键词
        prompt = f"""从以下问题中提取 2-3 个关键名词或短语，用逗号分隔：

问题：{query}

直接输出关键词，不要其他内容："""

        try:
            response = self.llm.chat([{"role": "user", "content": prompt}])
            keywords = [kw.strip() for kw in response.split(',')]
            return keywords[:3]
        except Exception:
            # 降级：简单分词
            return [query]

    def search_elasticsearch(self, query: str) -> str:
        """
        在 Elasticsearch 中搜索相关文档
        """
        try:
            res = self.es.search(index=self.es_index, body={
                "query": {
                    "multi_match": {
                        "query": query,
                        "fields": ["title^2", "content", "keywords", "category"],
                        "fuzziness": "AUTO"
                    }
                },
                "size": 3
            })
            
            es_context = []
            for hit in res['hits']['hits']:
                source = hit['_source']
                title = source.get('title', '')
                content = source.get('content', '')
                es_context.append(f"【{title}】\n{content}")
                
            return "\n\n".join(es_context)
        except Exception as e:
            print(f"Elasticsearch search error: {e}")
            return ""

    def search_knowledge_graph(self, keywords: List[str]) -> str:
        """
        在知识图谱中搜索相关信息
        """
        if not keywords:
            return "未找到相关信息"

        # 使用 Cypher 匹配相关节点并返回其属性和关系
        # 简化版：通过实体名和常见属性进行模糊匹配
        match_conditions = " OR ".join([f"n.name CONTAINS '{kw}' OR n.description CONTAINS '{kw}' OR n.姓名 CONTAINS '{kw}' OR n.剧名 CONTAINS '{kw}'" for kw in keywords])
        
        query = f"""
        MATCH (n)
        WHERE {match_conditions}
        OPTIONAL MATCH (n)-[r]->(m)
        RETURN labels(n) AS labels, properties(n) AS props, type(r) AS relation, labels(m) AS target_labels, properties(m) AS target_props
        LIMIT 20
        """
        
        try:
            results = self.neo4j.query(query)
            if not results:
                return "未找到相关信息"
                
            context = []
            for record in results:
                node_label = record["labels"][0] if record["labels"] else "节点"
                props = record["props"]
                name = props.get("name", props.get("姓名", props.get("剧名", "未知")))
                
                # 提取有价值的属性，过滤掉内建或无关属性
                useful_props = {k: v for k, v in props.items() if k not in ['id', 'name', 'type'] and v}
                prop_str = ", ".join([f"{k}: {v}" for k, v in useful_props.items()])
                
                node_info = f"[{node_label}] {name}"
                if prop_str:
                    node_info += f" ({prop_str})"
                    
                if record["relation"] and record["target_props"]:
                    target_label = record["target_labels"][0] if record["target_labels"] else "节点"
                    t_props = record["target_props"]
                    t_name = t_props.get("name", t_props.get("姓名", t_props.get("剧名", "未知")))
                    node_info += f" -> {record['relation']} -> [{target_label}] {t_name}"
                    
                context.append(node_info)
                
            # 去重
            context = list(set(context))
            return "\n".join(context)
        except Exception as e:
            print(f"Knowledge Graph search error: {e}")
            return "未找到相关信息"

    def _format_node_info(self, node: Dict) -> str:
        """格式化节点信息"""
        if not node:
            return ""

        name = node.get('name', '未知')
        node_type = node.get('type', node.get('label', '实体'))
        description = node.get('description', '')

        # 收集其他属性
        other_attrs = {k: v for k, v in node.items()
                       if k not in ['name', 'type', 'label', 'description'] and v}

        info = f"**{name}** ({node_type})"
        if description:
            info += f"\n{description}"

        if other_attrs:
            for key, value in other_attrs.items():
                if isinstance(value, list):
                    info += f"\n{key}: {', '.join(value)}"
                elif value:
                    info += f"\n{key}: {value}"

        return info

    def _format_relation_info(self, node: Dict, relation: Dict, related: Dict) -> str:
        """格式化关系信息"""
        if not node or not related:
            return ""

        node_name = node.get('name', '未知')
        related_name = related.get('name', '未知')
        relation_type = relation.get('type', relation.get('label', '相关')) if relation else '相关'

        # 提取关系类型（去掉前缀）
        if isinstance(relation_type, str) and ':' in relation_type:
            relation_type = relation_type.split(':')[1]

        return f"{node_name} → {relation_type} → {related_name}"

    async def aquery_stream(self, question: str, conversation_history: List[Dict] = None):
        """
        异步流式返回 RAG 查询结果
        """
        # 1. 提取关键词
        keywords = self.extract_keywords(question)
        print(f"Extracted keywords: {keywords}")

        # 2. 检索知识图谱
        kg_context = self.search_knowledge_graph(keywords)
        
        # 3. 检索 Elasticsearch
        es_context = self.search_elasticsearch(question)
        
        # 合并上下文
        combined_context = ""
        if kg_context and kg_context != "未找到相关信息":
            combined_context += "【知识图谱结构化信息】\n" + kg_context + "\n\n"
        if es_context:
            combined_context += "【文档资料检索信息】\n" + es_context

        if not combined_context:
            combined_context = "未能检索到相关非遗资料，请根据你自身的知识进行回答，并说明信息可能不够全面。"

        # 4. 提取相关实体（用于前端展示）
        related_entities = self._extract_related_entities(kg_context)
        
        import json
        
        # 先发送实体等元数据
        metadata = {
            "type": "metadata",
            "related_entities": related_entities,
            "keywords": keywords
        }
        yield f"data: {json.dumps(metadata, ensure_ascii=False)}\n\n"

        # 5. 使用 LLM 流式生成回答
        system_prompt = f"""你是一个专业的非遗文化知识助手。请基于以下提供的参考资料，专业、准确地回答用户的问题。
要求：
1. 优先使用提供的参考资料中的信息进行回答。
2. 语言要生动有趣，富有文化底蕴。
3. 如果资料中没有直接答案，你可以结合自身的知识库进行补充，但要说明。
4. 如果回答中包含特定实体（如流派、剧目、人物），尽量保持原名。

参考资料：
{combined_context}"""

        full_answer = ""
        history = conversation_history or []
        async for chunk in self.llm.achat_stream(messages=history + [{"role": "user", "content": question}], system_prompt=system_prompt):
            full_answer += chunk
            chunk_data = {
                "type": "chunk",
                "content": chunk
            }
            yield f"data: {json.dumps(chunk_data, ensure_ascii=False)}\n\n"

        # 6. 生成追问
        follow_ups = self.llm.generate_follow_up_questions(context=combined_context, user_query=question, answer=full_answer)
        
        final_data = {
            "type": "done",
            "follow_up_questions": follow_ups,
            "full_answer": full_answer
        }
        yield f"data: {json.dumps(final_data, ensure_ascii=False)}\n\n"

    def query(self, question: str, conversation_history: List[Dict] = None) -> Dict[str, Any]:
        """
        完整的 RAG 查询流程

        Args:
            question: 用户问题
            conversation_history: 对话历史
            session_id: 会话ID

        Returns:
            包含回答、追问选项等信息的字典
        """
        # 1. 提取关键词
        keywords = self.extract_keywords(question)
        print(f"Extracted keywords: {keywords}")

        # 2. 检索知识图谱
        kg_context = self.search_knowledge_graph(keywords)
        print(f"KG context length: {len(kg_context)}")
        
        # 3. 检索 Elasticsearch
        es_context = self.search_elasticsearch(question)
        print(f"ES context length: {len(es_context)}")
        
        # 合并上下文
        combined_context = ""
        if kg_context and kg_context != "未找到相关信息":
            combined_context += "【知识图谱结构化信息】\n" + kg_context + "\n\n"
        if es_context:
            combined_context += "【文档资料检索信息】\n" + es_context

        if not combined_context:
            combined_context = "未能检索到相关非遗资料，请根据你自身的知识进行回答，并说明信息可能不够全面。"

        # 4. 使用 LLM 生成回答
        system_prompt = f"""你是一个专业的非遗文化知识助手。请基于以下提供的参考资料，专业、准确地回答用户的问题。
要求：
1. 优先使用提供的参考资料中的信息进行回答。
2. 语言要生动有趣，富有文化底蕴。
3. 如果资料中没有直接答案，你可以结合自身的知识库进行补充，但要说明。
4. 如果回答中包含特定实体（如流派、剧目、人物），尽量保持原名。

参考资料：
{combined_context}"""

        if conversation_history is None:
            conversation_history = []
            
        answer = self.llm.chat(messages=conversation_history + [{"role": "user", "content": question}], system_prompt=system_prompt)

        # 5. 生成追问
        follow_ups = self.llm.generate_follow_up_questions(context=combined_context, user_query=question, answer=answer)

        # 6. 提取相关实体（用于前端展示）
        related_entities = self._extract_related_entities(kg_context)

        return {
            "answer": answer,
            "follow_up_questions": follow_ups,
            "related_entities": related_entities,
            "kg_context": kg_context,
            "es_context": es_context,
            "keywords": keywords
        }

    def _extract_related_entities(self, context: str) -> List[str]:
        """从上下文中提取相关实体名称"""
        entities = []
        for line in context.split('\n'):
            if line.startswith('**') and '**' in line[2:]:
                entity = line.split('**')[1]
                if entity and entity not in entities:
                    entities.append(entity)
        return entities[:5]  # 最多返回 5 个


# 全局实例
rag_service = RAGService()
