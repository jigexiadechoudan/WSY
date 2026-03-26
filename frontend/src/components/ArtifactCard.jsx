import React, { useRef } from 'react';
import html2canvas from 'html2canvas';

const ArtifactCard = ({ data, onDownload }) => {
  const cardRef = useRef(null);

  if (!data) return null;

  const handleDownload = async () => {
    if (cardRef.current) {
      try {
        const canvas = await html2canvas(cardRef.current, {
          useCORS: true,
          scale: 2, // High resolution
          backgroundColor: '#f5f0e6' // rice-paper color
        });
        const url = canvas.toDataURL('image/png');
        const link = document.createElement('a');
        link.download = `${data.title || 'digital-artifact'}.png`;
        link.href = url;
        link.click();
        if (onDownload) onDownload();
      } catch (error) {
        console.error('Failed to download image', error);
      }
    }
  };

  return (
    <div className="flex flex-col items-center gap-6">
      {/* The Card to be exported */}
      <div 
        ref={cardRef}
        className="w-full max-w-md bg-rice-paper p-8 rounded-sm shadow-2xl relative overflow-hidden"
        style={{ 
          backgroundImage: 'url("https://www.transparenttextures.com/patterns/rice-paper-2.png")',
          border: '1px solid #dcd3b6'
        }}
      >
        {/* Decorative corner borders */}
        <div className="absolute top-4 left-4 w-6 h-6 border-t-2 border-l-2 border-ink-black/40"></div>
        <div className="absolute top-4 right-4 w-6 h-6 border-t-2 border-r-2 border-ink-black/40"></div>
        <div className="absolute bottom-4 left-4 w-6 h-6 border-b-2 border-l-2 border-ink-black/40"></div>
        <div className="absolute bottom-4 right-4 w-6 h-6 border-b-2 border-r-2 border-ink-black/40"></div>

        {/* Title */}
        <div className="text-center mb-6">
          <h2 className="font-xiaowei text-3xl text-ink-black mb-2">{data.title}</h2>
          <div className="w-12 h-0.5 bg-vermilion mx-auto"></div>
        </div>

        {/* Image */}
        <div className="relative mb-6 rounded-sm overflow-hidden border-4 border-ink-black/10 shadow-inner">
          <img 
            src={data.imageUrl} 
            alt={data.title} 
            className="w-full h-auto object-cover aspect-square"
            crossOrigin="anonymous"
          />
        </div>

        {/* Poem */}
        <div className="text-center mb-6 font-calligraphy text-xl text-ink-black/90 leading-relaxed whitespace-pre-line">
          {data.poem.split('。').join('。\n')}
        </div>

        {/* Description */}
        <div className="text-sm font-sans text-charcoal/80 leading-loose text-justify mb-8">
          {data.description}
        </div>

        {/* Footer / Seal */}
        <div className="flex justify-between items-end border-t border-ink-black/10 pt-4 mt-auto">
          <div className="flex flex-col">
            <span className="font-xiaowei text-sm text-ink-black/60">数字传承人</span>
            <span className="text-xs text-charcoal/40 font-sans tracking-widest uppercase">Digital Artifact</span>
          </div>
          <div className="w-10 h-10 border-2 border-vermilion text-vermilion flex items-center justify-center font-calligraphy text-lg rotate-12 opacity-80">
            印
          </div>
        </div>
      </div>

      {/* Download Button */}
      <button 
        onClick={handleDownload}
        className="px-8 py-3 bg-ink-black text-rice-paper font-xiaowei rounded hover:bg-vermilion transition-colors flex items-center gap-2 shadow-lg"
      >
        <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
        </svg>
        保存数字藏品
      </button>
    </div>
  );
};

export default ArtifactCard;