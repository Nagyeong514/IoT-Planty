import React, { useEffect, useState } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import './WateringChart.css';

function GroupedBarChart() {
    const [data, setData] = useState([]);

    useEffect(() => {
        fetch('/api/pump/logs?range=7d')
            .then((res) => res.json())
            .then((logs) => {
                // 요일별 데이터 초기화
                const counts = {
                    Sun: { name: 'Sun', auto: 0, manual: 0 },
                    Mon: { name: 'Mon', auto: 0, manual: 0 },
                    Tue: { name: 'Tue', auto: 0, manual: 0 },
                    Wed: { name: 'Wed', auto: 0, manual: 0 },
                    Thu: { name: 'Thu', auto: 0, manual: 0 },
                    Fri: { name: 'Fri', auto: 0, manual: 0 },
                    Sat: { name: 'Sat', auto: 0, manual: 0 },
                };

                logs.forEach((log) => {
                    const date = new Date(log.timestamp);
                    const day = date.toLocaleDateString('en-US', { weekday: 'short' }); // 'Mon', 'Tue', ...
                    const method = log.method;
                    if (counts[day]) {
                        counts[day][method] += 1;
                    }
                });

                setData(Object.values(counts));
            });
    }, []);

    return (
        <div className="bar-card">
            <h3 className="bar-title">요일별 급수 횟수</h3>
            <ResponsiveContainer width="100%" height={300}>
                <BarChart data={data} margin={{ top: 10, right: 20, left: 0, bottom: 0 }}>
                    <CartesianGrid strokeDasharray="3 3" vertical={false} />
                    <XAxis dataKey="name" />
                    <YAxis allowDecimals={false} />
                    <Tooltip />
                    <Legend />
                    <Bar dataKey="auto" name="자동 급수" fill="#10b981" radius={[4, 4, 0, 0]} />
                    <Bar dataKey="manual" name="수동 급수" fill="#3b82f6" radius={[4, 4, 0, 0]} />
                </BarChart>
            </ResponsiveContainer>
        </div>
    );
}

export default GroupedBarChart;
