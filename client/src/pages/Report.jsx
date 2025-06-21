import React, { useEffect, useState } from 'react';
import SensorChart from '../components/Chart/SensorChart';
import WateringChart from '../components/Chart/WateringChart';
import MoodTimeline from '../components/Chart/MoodTimeline';
import './Report.css';

function Report() {
    const [sensor, setSensor] = useState({});
    const [mood, setMood] = useState({});

    useEffect(() => {
        fetch('/api/sensor/latest')
            .then((res) => res.json())
            .then((data) => setSensor(data));

        fetch('/api/mood/latest')
            .then((res) => res.json())
            .then((data) => setMood(data));
    }, []);

    const now = new Date();
    const day = now.toLocaleDateString('ko-KR', { weekday: 'long' });
    const time = now.toLocaleTimeString('ko-KR', {
        hour: '2-digit',
        minute: '2-digit',
        hour12: true,
    });

    const moodLabel = (mood) => {
        switch (mood) {
            case 'happy':
                return '기쁨';
            case 'angry':
                return '화남';
            case 'cry':
                return '울상';
            case 'hot':
                return '더움';
            case 'cold':
                return '추움';
            case 'confused':
                return '당황';
            case 'lovely':
                return '러블리';
            default:
                return '--';
        }
    };

    return (
        <div className="report-container">
            <div className="metrics-row">
                <div className="metric-card">
                    <div className="metric-label">{day}</div>
                    <div className="metric-value">{time}</div>
                </div>
            </div>

            <h3 className="section-title2">최근 일주일 내 센서 변화 그래프</h3>
            <SensorChart />

            <h3 className="section-title2">최근 일주일 급수 및 감정 변화</h3>
            <div className="chart-row">
                <WateringChart />
                <MoodTimeline />
            </div>
        </div>
    );
}

export default Report;
