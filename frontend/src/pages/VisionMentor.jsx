import React, { useState, useEffect, useRef } from 'react';
import { useSearchParams } from 'react-router-dom';
import Navbar from '../components/Navbar';
import HandTracking from '../components/HandTracking';

const VisionMentor = () => {
  const [searchParams] = useSearchParams();
  const scenarioParam = searchParams.get('scenario');
  const [activeScenario, setActiveScenario] = useState(scenarioParam || 'embroidery'); // 'embroidery' | 'clay' | 'shadow'

  useEffect(() => {
    if (scenarioParam && ['embroidery', 'clay', 'shadow'].includes(scenarioParam)) {
      setActiveScenario(scenarioParam);
    }
  }, [scenarioParam]);
  
  const [metricValue, setMetricValue] = useState(0); // 0-100
  const [feedbackMessage, setFeedbackMessage] = useState('等待检测...');
  const [aiFeedback, setAiFeedback] = useState('');
  const [isUnlocked, setIsUnlocked] = useState(false);
  
  const lastApiCallTime = useRef(0);
  const highScoreStartTime = useRef(null);

  // Reset states when scenario changes
  useEffect(() => {
    setMetricValue(0);
    setFeedbackMessage('等待检测...');
    setAiFeedback('');
    setIsUnlocked(false);
    highScoreStartTime.current = null;
  }, [activeScenario]);

  // Theme configuration based on scenario
  const theme = {
    embroidery: {
      title: '苏绣 · 捏针手势',
      color: 'cyan-glaze',
      accent: '#5796B3',
      bg: 'bg-cyan-glaze/10',
      border: 'border-cyan-glaze',
      text: 'text-cyan-glaze',
      icon: '🪡',
      instruction: '请将食指与拇指轻轻捏合，模仿拿针的姿势。',
    },
    clay: {
      title: '紫砂 · 拍泥手势',
      color: 'vermilion',
      accent: '#C04851',
      bg: 'bg-vermilion/10',
      border: 'border-vermilion',
      text: 'text-vermilion',
      icon: '🏺',
      instruction: '请伸直五指并拢，展示平整的拍泥手掌。',
    },
    shadow: {
      title: '皮影 · 飞兔手影',
      color: 'amber-600',
      accent: '#D97706',
      bg: 'bg-amber-100/50',
      border: 'border-amber-600',
      text: 'text-amber-700',
      icon: '🐰',
      instruction: '竖起食指中指，捏合其他三指，模仿兔子手影。',
    }
  };

  const currentTheme = theme[activeScenario];

  const handleHandResults = (results) => {
    if (results.multiHandLandmarks && results.multiHandLandmarks.length > 0) {
      const now = Date.now();
      // Throttle API calls to roughly 5 fps
      if (now - lastApiCallTime.current > 200) {
        lastApiCallTime.current = now;
        
        let needFeedback = false;
        if (metricValue >= 85 && !isUnlocked) {
            if (!highScoreStartTime.current) {
                highScoreStartTime.current = now;
            } else if (now - highScoreStartTime.current > 2000) {
                needFeedback = true;
                setIsUnlocked(true); // Prevent multiple unlock calls
            }
        } else if (metricValue < 85) {
            highScoreStartTime.current = null;
        }

        // Call backend API
        fetch('http://localhost:8002/api/v1/vision/analyze-pose', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                landmarks: results.multiHandLandmarks,
                scenario: activeScenario,
                need_feedback: needFeedback
            })
        })
        .then(res => res.json())
        .then(data => {
            if (data.status === 'success') {
                setMetricValue(data.score);
                setFeedbackMessage(data.hint);
                if (data.feedback) {
                    setAiFeedback(data.feedback);
                }
            }
        })
        .catch(err => console.error("Vision API Error:", err));
      }
    } else {
      setMetricValue(0);
      setFeedbackMessage('未检测到手部动作');
      highScoreStartTime.current = null;
    }
  };

  // Helper to determine feedback color based on score
  const getScoreColor = (score) => {
      if (score >= 85) return 'text-green-600 border-green-500 bg-green-50';
      if (score >= 60) return 'text-yellow-600 border-yellow-500 bg-yellow-50';
      if (score > 0) return 'text-red-600 border-red-500 bg-red-50';
      return 'text-gray-500 border-gray-300 bg-gray-50';
  };

  return (
    <div className="min-h-screen bg-rice-paper font-serif text-ink-black selection:bg-vermilion selection:text-white relative overflow-hidden">
      {/* Background Noise Texture */}
      <div className="absolute inset-0 z-0 opacity-30 pointer-events-none bg-noise mix-blend-multiply"></div>

      <Navbar />

      <main className="relative z-10 container mx-auto px-6 py-12 pt-24">
        {/* Header Section */}
        <div className="flex flex-col md:flex-row justify-between items-end mb-12 border-b-2 border-ink-black/10 pb-6">
          <div>
            <h1 className="text-4xl md:text-5xl font-calligraphy text-ink-black mb-4">
              视觉导师 <span className="text-2xl text-ink-black/60 font-serif">Vision Mentor</span>
            </h1>
            <p className="text-lg text-ink-black/70 max-w-2xl">
              挑战大师手势！通过摄像头实时比对您的动作，解锁非遗专属成就。
            </p>
          </div>
          
          {/* Scenario Switcher */}
          <div className="flex flex-wrap gap-4 mt-6 md:mt-0">
            {Object.keys(theme).map((key) => (
                <button
                key={key}
                onClick={() => setActiveScenario(key)}
                className={`px-5 py-2 rounded-full border-2 transition-all duration-300 flex items-center gap-2 font-bold ${
                    activeScenario === key
                    ? `bg-[${theme[key].accent}] text-white border-[${theme[key].accent}] shadow-lg transform -translate-y-1`
                    : 'bg-transparent text-ink-black/60 border-ink-black/20 hover:border-ink-black hover:text-ink-black'
                }`}
                style={{
                    backgroundColor: activeScenario === key ? theme[key].accent : 'transparent',
                    borderColor: activeScenario === key ? theme[key].accent : ''
                }}
                >
                <span>{theme[key].icon}</span> {theme[key].title.split('·')[0]}模式
                </button>
            ))}
          </div>
        </div>

        {/* Main Content Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          
          {/* Left Column: Camera Feed */}
          <div className="lg:col-span-2 space-y-6">
            <div className={`relative p-2 rounded-2xl border-2 ${currentTheme.border} bg-white shadow-xl transition-colors duration-500`}>
              {/* Decorative Corner Accents */}
              <div className={`absolute top-0 left-0 w-8 h-8 border-t-4 border-l-4 ${currentTheme.border} -translate-x-1 -translate-y-1 rounded-tl-lg`}></div>
              <div className={`absolute top-0 right-0 w-8 h-8 border-t-4 border-r-4 ${currentTheme.border} translate-x-1 -translate-y-1 rounded-tr-lg`}></div>
              <div className={`absolute bottom-0 left-0 w-8 h-8 border-b-4 border-l-4 ${currentTheme.border} -translate-x-1 translate-y-1 rounded-bl-lg`}></div>
              <div className={`absolute bottom-0 right-0 w-8 h-8 border-b-4 border-r-4 ${currentTheme.border} translate-x-1 translate-y-1 rounded-br-lg`}></div>

              {/* The Hand Tracking Component */}
              <HandTracking onResults={handleHandResults} scenario={activeScenario} />
              
              <div className="absolute bottom-4 left-4 right-4 bg-black/70 backdrop-blur-md text-white px-4 py-3 rounded-xl text-center text-lg shadow-lg border border-white/20">
                {currentTheme.instruction}
              </div>
            </div>
          </div>

          {/* Right Column: Analysis Panel */}
          <div className="lg:col-span-1 space-y-6">
            
            {/* Status Card */}
            <div className={`bg-white p-6 rounded-xl shadow-lg border-t-4 ${currentTheme.border}`}>
              <h3 className={`text-xl font-bold mb-4 flex items-center gap-2 ${currentTheme.text}`}>
                {currentTheme.icon} 动作匹配度
              </h3>
              
              {/* Circular Progress */}
              <div className="flex justify-center my-8 relative">
                  <div className="relative w-40 h-40 flex items-center justify-center">
                      <svg className="w-full h-full transform -rotate-90 absolute inset-0">
                          <circle cx="80" cy="80" r="70" stroke="currentColor" strokeWidth="10" fill="transparent" className="text-gray-100" />
                          <circle cx="80" cy="80" r="70" stroke="currentColor" strokeWidth="10" fill="transparent" 
                                  strokeDasharray="439.8" strokeDashoffset={439.8 - (metricValue / 100) * 439.8}
                                  className={`transition-all duration-300 ease-out ${
                                      metricValue >= 85 ? 'text-green-500' : metricValue >= 60 ? 'text-yellow-500' : 'text-red-400'
                                  }`} 
                                  strokeLinecap="round" />
                      </svg>
                      <div className="text-center z-10 flex flex-col items-center">
                          <span className="text-4xl font-bold font-mono text-ink-black">{metricValue}</span>
                          <span className="text-sm text-ink-black/50">分</span>
                      </div>
                  </div>
              </div>

              <div className={`text-center py-4 px-2 rounded-lg mb-4 transition-colors duration-300 border ${getScoreColor(metricValue)}`}>
                <div className="font-medium">{feedbackMessage}</div>
                {metricValue >= 85 && !isUnlocked && (
                    <div className="text-xs mt-2 animate-pulse font-bold">保持姿势 2 秒即可解锁成就！</div>
                )}
              </div>
            </div>

            {/* AI Feedback Card */}
            {isUnlocked && aiFeedback && (
              <div className="bg-gradient-to-br from-yellow-50 to-amber-100 p-6 rounded-xl shadow-lg border border-amber-200 animate-fade-in-up">
                <h4 className="text-lg font-bold text-amber-800 mb-3 flex items-center gap-2">
                  <span>🏆</span> 大师寄语
                </h4>
                <p className="text-amber-900 leading-relaxed italic">
                  "{aiFeedback}"
                </p>
                <button 
                  onClick={() => { setIsUnlocked(false); setAiFeedback(''); }}
                  className="mt-4 w-full py-2 bg-amber-600 hover:bg-amber-700 text-white rounded-lg transition-colors text-sm font-bold"
                >
                  继续挑战
                </button>
              </div>
            )}

          </div>
        </div>
      </main>
    </div>
  );
};

export default VisionMentor;
