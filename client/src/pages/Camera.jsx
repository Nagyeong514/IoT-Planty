'use client';
import { useNavigate } from 'react-router-dom';
import './Camera.css';

export default function Camera() {
    const navigate = useNavigate();

    return (
        <div className="container">
            <div className="live-card">
                <div className="video-header">
                    <span className="live-indicator">LIVE</span>
                    <h2 className="video-title">실시간 스트리밍</h2>
                </div>
                <img className="video-feed" src="/video_feed" alt="Live stream" />
                <div className="video-controls">
                    <button className="outline-button" onClick={() => navigate('/timelapse')}>
                        타임랩스 보기
                    </button>
                </div>
            </div>
        </div>
    );
}
