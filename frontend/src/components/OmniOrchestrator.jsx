import React, { useState, useRef, useEffect } from 'react';
import { Bot, X, Send, Maximize2, Minimize2, Sparkles, Image as ImageIcon, BookOpen } from 'lucide-react';
import TaskPipelineVisualizer from './TaskPipelineVisualizer';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

const OmniOrchestrator = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [isExpanded, setIsExpanded] = useState(false);
  const [query, setQuery] = useState('');
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!query.trim() || isLoading) return;

    const userMessage = { role: 'user', content: query };
    setMessages(prev => [...prev, userMessage]);
    setQuery('');
    setIsLoading(true);

    try {
      const response = await fetch('http://localhost:8002/api/v1/orchestrator/process', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query: userMessage.content, history: messages }),
      });

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      const data = await response.json();
      
      const assistantMessage = {
        role: 'assistant',
        content: data.final_answer,
        intent: data.intent?.intent,
        tasks: data.tasks,
        results: data.results,
        isError: false
      };
      
      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      console.error('Orchestrator Error:', error);
      const errorMessage = {
        role: 'assistant',
        content: '抱歉，系统处理您的请求时遇到了问题，请稍后再试。',
        isError: true
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const toggleOpen = () => {
    setIsOpen(!isOpen);
    if (isExpanded) setIsExpanded(false);
  };

  const renderMessageContent = (msg) => {
    if (msg.role === 'user') {
      return <div className="text-sm whitespace-pre-wrap">{msg.content}</div>;
    }

    return (
      <div className="flex flex-col space-y-3 w-full">
        {/* Render final answer */}
        <div className="text-sm markdown-wrapper">
           <ReactMarkdown remarkPlugins={[remarkGfm]}>{msg.content}</ReactMarkdown>
        </div>
        
        {/* Render generated images if any */}
        {msg.results && Object.entries(msg.results).map(([taskId, result]) => {
          if (typeof result === 'string' && (result.startsWith('http') || result.startsWith('data:image'))) {
             return (
                <div key={taskId} className="mt-2 rounded-md overflow-hidden border border-gray-200">
                   <img src={result} alt="Generated result" className="w-full h-auto object-cover max-h-64" />
                </div>
             );
          }
          return null;
        })}

        {/* Render Task Pipeline if available */}
        {(msg.intent || (msg.tasks && msg.tasks.length > 0)) && (
          <div className="mt-2 border-t border-gray-100 pt-2">
            <details className="group">
              <summary className="text-xs text-gray-500 cursor-pointer hover:text-gray-700 flex items-center">
                <Sparkles size={12} className="mr-1" />
                查看调度详情
              </summary>
              <div className="mt-2">
                <TaskPipelineVisualizer intent={msg.intent} tasks={msg.tasks} />
              </div>
            </details>
          </div>
        )}
      </div>
    );
  };

  return (
    <>
      {/* Floating Action Button */}
      <button
        onClick={toggleOpen}
        className={`fixed bottom-6 right-6 z-[60] w-14 h-14 rounded-full bg-vermilion text-white shadow-xl flex items-center justify-center hover:scale-105 transition-transform duration-300 ${isOpen ? 'scale-0 opacity-0' : 'scale-100 opacity-100'}`}
      >
        <Bot size={28} />
      </button>

      {/* Main Chat Window */}
      <div
        className={`fixed z-[60] bottom-6 right-6 bg-white rounded-lg shadow-2xl border border-gray-200 flex flex-col transition-all duration-300 ease-in-out transform origin-bottom-right
          ${isOpen ? 'scale-100 opacity-100' : 'scale-0 opacity-0 pointer-events-none'}
          ${isExpanded ? 'w-[800px] h-[80vh] max-w-[90vw]' : 'w-[400px] h-[600px] max-w-[90vw]'}
        `}
      >
        {/* Header */}
        <div className="flex items-center justify-between p-4 border-b border-gray-100 bg-gray-50/80 rounded-t-lg">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-full bg-vermilion/10 text-vermilion flex items-center justify-center">
              <Sparkles size={18} />
            </div>
            <div>
              <h3 className="font-xiaowei text-lg text-gray-800">全能智能助理</h3>
              <p className="text-[10px] text-gray-500 font-sans">Multi-Agent Orchestrator</p>
            </div>
          </div>
          <div className="flex items-center gap-2 text-gray-400">
            <button onClick={() => setIsExpanded(!isExpanded)} className="hover:text-gray-700 p-1">
              {isExpanded ? <Minimize2 size={16} /> : <Maximize2 size={16} />}
            </button>
            <button onClick={toggleOpen} className="hover:text-gray-700 p-1">
              <X size={20} />
            </button>
          </div>
        </div>

        {/* Messages Area */}
        <div className="flex-1 overflow-y-auto p-4 bg-slate-50/50">
          {messages.length === 0 ? (
            <div className="h-full flex flex-col items-center justify-center text-center space-y-4 opacity-60">
              <Bot size={48} className="text-gray-300" />
              <div className="text-sm text-gray-500">
                <p>你好！我是您的数字传承人全能助理。</p>
                <p className="mt-1">您可以让我帮您：</p>
                <div className="flex flex-col items-start mt-4 space-y-2 text-xs bg-white p-4 rounded-md shadow-sm">
                  <span className="flex items-center gap-2"><BookOpen size={14} className="text-blue-500"/> 查询非遗知识或历史</span>
                  <span className="flex items-center gap-2"><ImageIcon size={14} className="text-vermilion"/> 创作非遗风格的图像</span>
                  <span className="flex items-center gap-2"><Sparkles size={14} className="text-yellow-500"/> 制定非遗学习计划</span>
                </div>
                <p className="mt-4 text-xs italic">试试发送："我想学苏绣，并生成一张牡丹图"</p>
              </div>
            </div>
          ) : (
            <div className="space-y-6">
              {messages.map((msg, idx) => (
                <div key={idx} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                  {msg.role === 'assistant' && (
                    <div className="w-8 h-8 rounded-full bg-gray-200 flex-shrink-0 mr-2 flex items-center justify-center text-gray-500">
                      <Bot size={16} />
                    </div>
                  )}
                  <div className={`max-w-[85%] rounded-2xl px-4 py-3 shadow-sm ${
                    msg.role === 'user' 
                      ? 'bg-vermilion text-white rounded-tr-sm' 
                      : msg.isError 
                        ? 'bg-red-50 text-red-600 border border-red-100 rounded-tl-sm'
                        : 'bg-white border border-gray-100 rounded-tl-sm text-gray-800'
                  }`}>
                    {renderMessageContent(msg)}
                  </div>
                </div>
              ))}
              
              {isLoading && (
                <div className="flex justify-start">
                  <div className="w-8 h-8 rounded-full bg-gray-200 flex-shrink-0 mr-2 flex items-center justify-center text-gray-500">
                    <Bot size={16} />
                  </div>
                  <div className="bg-white border border-gray-100 rounded-2xl rounded-tl-sm px-4 py-3 shadow-sm flex items-center space-x-2">
                    <div className="flex space-x-1">
                      <div className="w-2 h-2 bg-gray-300 rounded-full animate-bounce"></div>
                      <div className="w-2 h-2 bg-gray-300 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                      <div className="w-2 h-2 bg-gray-300 rounded-full animate-bounce" style={{ animationDelay: '0.4s' }}></div>
                    </div>
                    <span className="text-xs text-gray-500 ml-2">正在协调多个 Agent 处理中...</span>
                  </div>
                </div>
              )}
              <div ref={messagesEndRef} />
            </div>
          )}
        </div>

        {/* Input Area */}
        <div className="p-4 border-t border-gray-100 bg-white rounded-b-lg">
          <form onSubmit={handleSubmit} className="relative flex items-center">
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="输入任何复杂的指令..."
              disabled={isLoading}
              className="w-full bg-gray-100 border-transparent rounded-full pl-4 pr-12 py-3 text-sm focus:bg-white focus:border-vermilion focus:ring-2 focus:ring-vermilion/20 transition-all disabled:opacity-50 outline-none"
            />
            <button
              type="submit"
              disabled={!query.trim() || isLoading}
              className="absolute right-2 p-2 rounded-full text-vermilion hover:bg-vermilion/10 disabled:text-gray-400 disabled:hover:bg-transparent transition-colors"
            >
              <Send size={18} />
            </button>
          </form>
        </div>
      </div>
    </>
  );
};

export default OmniOrchestrator;
