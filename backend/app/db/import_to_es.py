import json
from elasticsearch import Elasticsearch
from app.core.config import settings

def import_to_es():
    es = Elasticsearch([settings.ES_URL])
    index_name = settings.ES_INDEX_NAME
    
    # Create index if not exists
    if not es.indices.exists(index=index_name):
        es.indices.create(index=index_name, body={
            "mappings": {
                "properties": {
                    "id": {"type": "integer"},
                    "title": {"type": "text", "analyzer": "standard"},
                    "category": {"type": "keyword"},
                    "content": {"type": "text", "analyzer": "standard"},
                    "keywords": {"type": "keyword"}
                }
            }
        })
        print(f"Created index {index_name}")
    else:
        print(f"Index {index_name} already exists")
        
    # Import shadow puppet data
    try:
        with open('../shadow_puppet_rag.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        count = 0
        for chunk in data.get('chunks', []):
            es.index(index=index_name, id=f"shadow_{chunk['id']}", document=chunk)
            count += 1
            
        print(f"Successfully imported {count} documents to Elasticsearch.")
    except Exception as e:
        print(f"Error importing data: {e}")

if __name__ == "__main__":
    import_to_es()
