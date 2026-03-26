import React, { useState } from 'react';
import Navbar from '../components/Navbar';
import ArtifactCard from '../components/ArtifactCard';
import axios from 'axios';

const CRAFT_STYLES = [
  { id: 'su-embroidery', name: '苏绣', desc: '丝线光泽，针法细腻' },
  { id: 'blue-white-porcelain', name: '青花瓷', desc: '白底蓝花，釉面温润' },
  { id: 'shadow-puppet', name: '皮影戏', desc: '牛皮质感，透光色彩' },
  { id: 'paper-cutting', name: '剪纸', desc: '红纸镂空，线条连贯' }
];

const CreativeWorkshop = () => {
  const [idea, setIdea] = useState('');
  const [selectedStyle, setSelectedStyle] = useState(CRAFT_STYLES[0]);
  const [loadingStep, setLoadingStep] = useState(0); // 0: none, 1: enrich, 2: image, 3: story
  const [masterReply, setMasterReply] = useState('');
  const [artifactData, setArtifactData] = useState(null);
  const [error, setError] = useState('');

  const handleGenerate = async () => {
    if (!idea.trim()) {
      setError('请输入您的灵感创意');
      return;
    }

    try {
      setError('');
      setArtifactData(null);
      setMasterReply('');
      
      // Step 1: Enrich Prompt
      setLoadingStep(1);
      const enrichRes = await axios.post('http://localhost:8002/api/v1/creative/enrich-prompt', {
        idea: idea,
        style: selectedStyle.name
      });
      
      const { master_reply, optimized_prompt } = enrichRes.data.data;
      setMasterReply(master_reply);

      // Step 2: Generate Image
      setLoadingStep(2);
      const imgRes = await axios.post('http://localhost:8002/api/v1/creative/generate-image', {
        optimized_prompt: optimized_prompt
      });
      const imageUrl = imgRes.data.image_url;

      // Step 3: Generate Story
      setLoadingStep(3);
      const storyRes = await axios.post('http://localhost:8002/api/v1/creative/generate-story', {
        idea: idea,
        style: selectedStyle.name,
        image_url: imageUrl
      });
      const { title, poem, description } = storyRes.data.data;

      // Finalize
      setArtifactData({
        imageUrl,
        title,
        poem,
        description
      });
      setLoadingStep(0);

    } catch (err) {
      console.error(err);
      setError(err.response?.data?.detail || '生成过程中发生错误，请稍后重试。');
      setLoadingStep(0);
    }
  };

  return (
    <div className="min-h-screen bg-rice-paper font-sans">
      <Navbar />
      
      <main className="pt-24 px-8 pb-12 max-w-7xl mx-auto">
        <div className="text-center mb-12">
          <h1 className="font-xiaowei text-4xl text-ink-black mb-4">云端非遗数字文创工坊</h1>
          <p className="text-charcoal/80 max-w-2xl mx-auto">
            输入一个简单的创意，选择一种非遗技艺，AI 大师将引导您完成创作，并自动生成独一无二的数字藏品卡片。
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12">
          {/* Left Column: Input & Interaction */}
          <div className="bg-white p-8 rounded-lg shadow-sm border border-ink-black/5 flex flex-col gap-6 h-fit">
            
            <div>
              <label className="block font-xiaowei text-xl text-ink-black mb-3">1. 选择非遗流派</label>
              <div className="grid grid-cols-2 gap-3">
                {CRAFT_STYLES.map(style => (
                  <button
                    key={style.id}
                    onClick={() => setSelectedStyle(style)}
                    className={`p-3 text-left border rounded transition-all ${
                      selectedStyle.id === style.id 
                      ? 'border-vermilion bg-vermilion/5 ring-1 ring-vermilion' 
                      : 'border-ink-black/20 hover:border-ink-black/40'
                    }`}
                  >
                    <div className={`font-bold ${selectedStyle.id === style.id ? 'text-vermilion' : 'text-ink-black'}`}>
                      {style.name}
                    </div>
                    <div className="text-xs text-charcoal/60 mt-1">{style.desc}</div>
                  </button>
                ))}
              </div>
            </div>

            <div>
              <label className="block font-xiaowei text-xl text-ink-black mb-3">2. 描述您的创意灵感</label>
              <textarea
                value={idea}
                onChange={(e) => setIdea(e.target.value)}
                placeholder="例如：画一只赛博朋克风格的机械猫..."
                className="w-full h-32 p-4 border border-ink-black/20 rounded focus:outline-none focus:border-vermilion focus:ring-1 focus:ring-vermilion resize-none"
              />
            </div>

            {error && (
              <div className="text-vermilion text-sm bg-vermilion/10 p-3 rounded">
                {error}
              </div>
            )}

            <button
              onClick={handleGenerate}
              disabled={loadingStep !== 0}
              className={`w-full py-4 rounded font-xiaowei text-lg transition-all ${
                loadingStep === 0 
                ? 'bg-ink-black text-rice-paper hover:bg-vermilion shadow-lg' 
                : 'bg-ink-black/50 text-rice-paper cursor-not-allowed'
              }`}
            >
              {loadingStep === 0 ? '开始创作数字藏品' : '大师正在创作中...'}
            </button>

            {/* Master Reply Area */}
            {(loadingStep > 0 || masterReply) && (
              <div className="mt-4 p-5 bg-ink-black/5 rounded border border-ink-black/10 relative">
                <div className="absolute -top-3 left-4 bg-rice-paper px-2 font-xiaowei text-vermilion text-sm">
                  {selectedStyle.name}大师
                </div>
                {loadingStep === 1 && <p className="text-charcoal animate-pulse">大师正在构思您的创意，并转化为专业绘画指令...</p>}
                {loadingStep === 2 && <p className="text-charcoal animate-pulse">正在云端绘制您的非遗风格作品，请稍候...</p>}
                {loadingStep === 3 && <p className="text-charcoal animate-pulse">正在为作品赋诗作词，生成数字藏品卡片...</p>}
                
                {masterReply && loadingStep !== 1 && (
                  <div className="text-charcoal/80 text-sm leading-relaxed whitespace-pre-line">
                    {masterReply}
                  </div>
                )}
              </div>
            )}
          </div>

          {/* Right Column: Result / Artifact Card */}
          <div className="flex items-center justify-center min-h-[600px] bg-ink-black/5 rounded-lg border border-ink-black/10 p-8 relative">
            {loadingStep > 0 && !artifactData && (
              <div className="flex flex-col items-center gap-4">
                <div className="w-16 h-16 border-4 border-vermilion/30 border-t-vermilion rounded-full animate-spin"></div>
                <div className="font-xiaowei text-ink-black">
                  {loadingStep === 1 && "沟通灵感中..."}
                  {loadingStep === 2 && "云端生图中 (可能需要 10-20 秒)..."}
                  {loadingStep === 3 && "文化赋能中..."}
                </div>
              </div>
            )}

            {!loadingStep && !artifactData && (
              <div className="text-center text-charcoal/40 font-xiaowei text-xl">
                您的专属数字藏品将在此展示
              </div>
            )}

            {artifactData && (
              <ArtifactCard data={artifactData} />
            )}
          </div>
        </div>
      </main>
    </div>
  );
};

export default CreativeWorkshop;