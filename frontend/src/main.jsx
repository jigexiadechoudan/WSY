import React from 'react'
import ReactDOM from 'react-dom/client'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Home from './pages/Home'
import CraftLibrary from './pages/CraftLibrary'
import KnowledgeCurator from './pages/KnowledgeCurator'
import MasterWorkshop from './pages/MasterWorkshop'
import MyPractice from './pages/MyPractice'
import VisionMentor from './pages/VisionMentor'
import ShadowPuppet from './pages/ShadowPuppet'
import CreativeWorkshop from './pages/CreativeWorkshop'
import OmniOrchestrator from './components/OmniOrchestrator'
import './index.css'

import Intro from './pages/Intro'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <Router>
      <OmniOrchestrator />
      <Routes>
        <Route path="/" element={<Intro />} />
        <Route path="/home" element={<Home />} />
        <Route path="/craft-library" element={<CraftLibrary />} />
        <Route path="/master-workshop" element={<MasterWorkshop />} />
        <Route path="/my-practice" element={<MyPractice />} />
        <Route path="/vision-mentor" element={<VisionMentor />} />
        <Route path="/knowledge-curator" element={<KnowledgeCurator />} />
        <Route path="/knowledge" element={<KnowledgeCurator />} />
        <Route path="/shadow-puppet" element={<ShadowPuppet />} />
        <Route path="/creative-workshop" element={<CreativeWorkshop />} />
        <Route path="/creative-artisan" element={<CreativeWorkshop />} />
      </Routes>
    </Router>
  </React.StrictMode>,
)
