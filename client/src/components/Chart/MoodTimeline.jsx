import React, { useEffect, useState } from 'react';
import { GripVertical, MoreHorizontal } from 'lucide-react';
import './MoodTimeline.css';

function MoodTimeline() {
    const [logs, setLogs] = useState([]);

    useEffect(() => {
        fetch('/api/mood/logs?range=7d')
            .then((res) => res.json())
            .then((data) => {
                const filtered = [];
                let prev = '';
                for (const entry of data) {
                    if (entry.mood_type !== prev) {
                        filtered.push(entry);
                        prev = entry.mood_type;
                    }
                }
                setLogs(filtered);
            });
    }, []);

    const formatDate = (ts) => {
        const date = new Date(ts);
        return date.toLocaleString('ko-KR', {
            month: '2-digit',
            day: '2-digit',
            hour: '2-digit',
            minute: '2-digit',
        });
    };

    return (
        <div className="bar-card">
            <div className="timeline-header">
                <div className="timeline-title-wrap">
                    <GripVertical className="timeline-grip" />
                    <h3 className="bar-title">최근 7일 감정 타임라인</h3>
                </div>
                <MoreHorizontal className="timeline-more" />
            </div>

            <div className="timeline-list">
                {/* 세로선 */}
                <div className="timeline-line" />
                {logs.map((log, idx) => (
                    <div key={idx} className="timeline-entry">
                        <div className="timeline-icon">
                            <img src={`/face/${log.face_expression}`} alt={log.mood_type} className="timeline-avatar" />
                        </div>
                        <div className="timeline-info">
                            <div className="timeline-reason">{log.reason}</div>
                            <div className="timeline-timestamp">{formatDate(log.timestamp)}</div>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
}

export default MoodTimeline;
