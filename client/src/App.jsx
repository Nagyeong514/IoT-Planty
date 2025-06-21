// App.js// client/src/App.js

import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Layout from './components/Layout/Layout';
import Dashboard from './components/Dashboard/Dashboard';
import Chatbot from './components/Chatbot/Chatbot';
import Report from './pages/Report';
import Camera from './pages/Camera';
import Timelapse from './pages/Timelapse';
import VoiceChat from './components/VoiceChat/VoiceChat';

function App() {
    return (
        <Router>
            <Layout>
                <Routes>
                    <Route path="/" element={<Dashboard />} />
                    <Route path="/chatbot" element={<Chatbot />} />
                    <Route path="/report" element={<Report />} />
                    <Route path="/camera" element={<Camera />} />
                    <Route path="/timelapse" element={<Timelapse />} />
                    <Route path="/voicechat" element={<VoiceChat />} />
                </Routes>
            </Layout>
        </Router>
    );
}

export default App;
