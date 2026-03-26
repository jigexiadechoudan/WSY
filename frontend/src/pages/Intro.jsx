import React, { useEffect, useRef, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import * as echarts from 'echarts';
import { motion, AnimatePresence } from 'framer-motion';
import chinaMapData from '../assets/china.json';

// Images for ICH
import ShadowPuppetImg from '../assets/Shadow-Puppet.png';
import SuzhouEmbroideryImg from '../assets/Suzhou-embroidery.png';
import BatikImg from '../assets/Batik.png';

// Register map data
echarts.registerMap('china', chinaMapData);

const ichLocations = [
  {
    id: 'start',
    name: '全景',
    title: '非遗新造',
    desc: '以数字之眼，观非遗之美。\n跨越千山万水，寻找文明的印记。',
    coordinates: [104.195397, 35.86166], // Center of China
    zoom: 1.2,
    image: null,
  },
  {
    id: 'shaanxi',
    name: '陕西',
    title: '华县皮影',
    desc: '一口叙说千古事，双手对舞百万兵。光影交错间的千古绝唱。',
    coordinates: [108.948024, 34.263161], // Xi'an
    zoom: 6,
    image: ShadowPuppetImg,
  },
  {
    id: 'jiangsu',
    name: '江苏',
    title: '苏绣',
    desc: '以针作画，巧夺天工。丝丝入扣的江南婉约。',
    coordinates: [120.619585, 31.299379], // Suzhou
    zoom: 6,
    image: SuzhouEmbroideryImg,
  },
  {
    id: 'guizhou',
    name: '贵州',
    title: '丹寨蜡染',
    desc: '冰纹错落，蓝白交织。传承千年的自然印记。',
    coordinates: [106.713478, 26.578343], // Guiyang (approx)
    zoom: 6,
    image: BatikImg,
  },
];

const Intro = () => {
  const chartRef = useRef(null);
  const navigate = useNavigate();
  const [currentIndex, setCurrentIndex] = useState(0);
  const [isPlaying, setIsPlaying] = useState(true);
  const [isExiting, setIsExiting] = useState(false);

  useEffect(() => {
    const chart = echarts.init(chartRef.current);
    
    const option = {
      backgroundColor: 'transparent',
      geo: {
        map: 'china',
        roam: false,
        zoom: ichLocations[0].zoom,
        center: ichLocations[0].coordinates,
        label: {
          show: false,
        },
        itemStyle: {
          areaColor: '#e8e4d9', // rice paper color
          borderColor: '#8b7e66', // subtle ink color
          borderWidth: 1,
        },
        emphasis: {
          itemStyle: {
            areaColor: '#d6d0c4',
          },
          label: {
            show: false,
          }
        }
      },
      series: [
        {
          type: 'effectScatter',
          coordinateSystem: 'geo',
          data: ichLocations.slice(1).map(loc => ({
            name: loc.name,
            value: [...loc.coordinates, 1], // [lng, lat, value]
          })),
          symbolSize: 12,
          itemStyle: {
            color: '#c23531', // vermilion red
            shadowBlur: 10,
            shadowColor: '#c23531'
          },
          showEffectOn: 'render',
          rippleEffect: {
            brushType: 'stroke'
          },
          zlevel: 1
        }
      ]
    };
    
    chart.setOption(option);

    const handleResize = () => {
      chart.resize();
    };
    window.addEventListener('resize', handleResize);

    return () => {
      chart.dispose();
      window.removeEventListener('resize', handleResize);
    };
  }, []);

  useEffect(() => {
    if (!isPlaying) return;

    const timer = setInterval(() => {
      setCurrentIndex((prev) => {
        const next = prev + 1;
        if (next >= ichLocations.length) {
          setIsPlaying(false); // Stop at the end
          return prev;
        }
        return next;
      });
    }, 5000); // 5 seconds per location

    return () => clearInterval(timer);
  }, [isPlaying]);

  useEffect(() => {
    if (!chartRef.current) return;
    const chart = echarts.getInstanceByDom(chartRef.current);
    if (!chart) return;

    const loc = ichLocations[currentIndex];
    
    chart.setOption({
      geo: {
        center: loc.coordinates,
        zoom: loc.zoom,
        animationDurationUpdate: 3000, // Cinematic slow pan
        animationEasingUpdate: 'cubicInOut'
      }
    });
  }, [currentIndex]);

  const handleEnter = () => {
    setIsExiting(true);
    setTimeout(() => {
      navigate('/home');
    }, 1000);
  };

  const currentLocation = ichLocations[currentIndex];

  return (
    <div className="relative w-screen h-screen overflow-hidden bg-[#f4f1ea] font-serif">
      {/* Background Texture Overlay */}
      <div className="absolute inset-0 z-0 pointer-events-none opacity-40 mix-blend-multiply" 
           style={{ backgroundImage: 'radial-gradient(circle, transparent 20%, #d4cebe 100%)' }}></div>
      
      {/* Map Container */}
      <div ref={chartRef} className="absolute inset-0 z-10" />

      {/* Info Overlay */}
      <div className="absolute inset-0 z-20 pointer-events-none flex items-center justify-between p-12 md:p-24">
        
        {/* Left Side: Text Info */}
        <AnimatePresence mode="wait">
          <motion.div
            key={currentLocation.id}
            initial={{ opacity: 0, x: -50, filter: 'blur(10px)' }}
            animate={{ opacity: 1, x: 0, filter: 'blur(0px)' }}
            exit={{ opacity: 0, x: 50, filter: 'blur(10px)' }}
            transition={{ duration: 1, ease: "easeOut" }}
            className="max-w-md pointer-events-auto"
          >
            <div className="mb-4">
              <span className="inline-block border border-[#c23531] text-[#c23531] px-2 py-1 text-sm font-calligraphy tracking-widest rounded-sm backdrop-blur-sm bg-white/30">
                {currentLocation.name}
              </span>
            </div>
            <h1 className="text-5xl md:text-7xl font-calligraphy text-[#2c2826] mb-6 leading-tight drop-shadow-md">
              {currentLocation.title}
            </h1>
            <p className="text-lg md:text-xl text-[#4a4541] leading-relaxed whitespace-pre-line font-xiaowei drop-shadow-sm bg-white/20 p-4 rounded-md backdrop-blur-sm border border-white/40">
              {currentLocation.desc}
            </p>
          </motion.div>
        </AnimatePresence>

        {/* Right Side: Image (if any) */}
        <AnimatePresence mode="wait">
          {currentLocation.image && (
            <motion.div
              key={`img-${currentLocation.id}`}
              initial={{ opacity: 0, scale: 0.9, rotate: -2 }}
              animate={{ opacity: 1, scale: 1, rotate: 0 }}
              exit={{ opacity: 0, scale: 0.9, rotate: 2 }}
              transition={{ duration: 1.2, ease: "easeOut", delay: 0.5 }}
              className="hidden md:block w-1/3 aspect-[4/3] rounded-sm overflow-hidden shadow-2xl pointer-events-auto border-4 border-white/50"
            >
              <img 
                src={currentLocation.image} 
                alt={currentLocation.title}
                className="w-full h-full object-cover filter contrast-110 sepia-50"
              />
              <div className="absolute inset-0 bg-gradient-to-t from-black/50 to-transparent"></div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>

      {/* Controls / Enter Button */}
      <div className="absolute bottom-12 right-12 z-30 flex items-center gap-6">
        <div className="flex gap-2">
          {ichLocations.map((loc, idx) => (
            <button
              key={loc.id}
              onClick={() => {
                setCurrentIndex(idx);
                setIsPlaying(false);
              }}
              className={`w-3 h-3 rounded-full transition-all duration-500 ${
                idx === currentIndex ? 'bg-[#c23531] scale-150' : 'bg-[#2c2826]/30 hover:bg-[#2c2826]/60'
              }`}
              aria-label={`Go to ${loc.name}`}
            />
          ))}
        </div>

        <motion.button
          onClick={handleEnter}
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          className="group relative px-8 py-3 bg-[#2c2826] text-[#e8e4d9] overflow-hidden rounded-sm font-xiaowei tracking-widest shadow-lg"
        >
          <span className="relative z-10 flex items-center gap-2">
            进入探索
            <svg xmlns="http://www.w3.org/2000/svg" className="w-4 h-4 group-hover:translate-x-1 transition-transform" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M14 5l7 7m0 0l-7 7m7-7H3" />
            </svg>
          </span>
          <div className="absolute inset-0 bg-[#c23531] transform scale-x-0 group-hover:scale-x-100 transition-transform origin-left duration-300"></div>
        </motion.button>
      </div>

      {/* Exit Overlay */}
      <AnimatePresence>
        {isExiting && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 1 }}
            className="absolute inset-0 z-50 bg-[#f4f1ea]"
          />
        )}
      </AnimatePresence>
    </div>
  );
};

export default Intro;
