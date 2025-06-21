import React, { useEffect, useState } from 'react';
import './SensorChart.css';
import {
    Chart as ChartJS,
    LineElement,
    PointElement,
    CategoryScale,
    LinearScale,
    Title,
    Tooltip,
    Legend,
    Filler,
} from 'chart.js';
import { Line } from 'react-chartjs-2';

// 이미지 아이콘 경로 지정
const tempIcon = '/icon/tem.png';
const humidityIcon = '/icon/water.png';
const soilIcon = '/icon/soilwater.png';

ChartJS.register(LineElement, PointElement, CategoryScale, LinearScale, Title, Tooltip, Legend, Filler);

function SensorChart() {
    const [labels, setLabels] = useState([]);
    const [temperatureData, setTemperatureData] = useState([]);
    const [humidityData, setHumidityData] = useState([]);
    const [soilData, setSoilData] = useState([]);

    useEffect(() => {
        fetch('/api/sensor/logs?range=7d')
            .then((res) => res.json())
            .then((data) => {
                const labelList = data.map((item) =>
                    new Date(item.timestamp).toLocaleDateString('ko-KR', {
                        month: '2-digit',
                        day: '2-digit',
                    })
                );
                const tempList = data.map((item) => item.temperature);
                const humidList = data.map((item) => item.humidity);
                const soilList = data.map((item) => (item.soil_dry ? 1 : 0));

                setLabels(labelList);
                setTemperatureData(tempList);
                setHumidityData(humidList);
                setSoilData(soilList);
            });
    }, []);

    const createChartConfig = (label, data, color, fill = true) => ({
        labels,
        datasets: [
            {
                label,
                data,
                borderColor: color,
                backgroundColor: fill ? color + '33' : 'transparent',
                tension: 0.4,
                pointRadius: 3,
                fill,
            },
        ],
    });

    const chartOptions = {
        responsive: true,
        plugins: {
            legend: { display: false },
            tooltip: {
                callbacks: {
                    label: (context) => `${context.parsed.y}`,
                },
            },
        },
        scales: {
            x: { grid: { display: false } },
            y: { grid: { color: '#f3f4f6' } },
        },
    };

    return (
        <div className="chart-row">
            <div className="chart-card">
                <div className="chart-title">
                    <img src={tempIcon} alt="온도" className="icon" style={{ width: '24px', marginRight: '8px' }} />
                    온도
                </div>
                <Line data={createChartConfig('온도', temperatureData, '#f97316')} options={chartOptions} />
            </div>

            <div className="chart-card">
                <div className="chart-title">
                    <img src={humidityIcon} alt="습도" className="icon" style={{ width: '24px', marginRight: '8px' }} />
                    습도
                </div>
                <Line data={createChartConfig('습도', humidityData, '#3b82f6')} options={chartOptions} />
            </div>

            <div className="chart-card">
                <div className="chart-title">
                    <img src={soilIcon} alt="토양" className="icon" style={{ width: '24px', marginRight: '8px' }} />
                    토양
                </div>
                <Line
                    data={createChartConfig('토양', soilData, '#10b981', false)}
                    options={{
                        ...chartOptions,
                        scales: {
                            ...chartOptions.scales,
                            y: {
                                min: 0,
                                max: 1,
                                ticks: {
                                    callback: (value) => (value === 1 ? '건조함' : '적당함'),
                                },
                                grid: { color: '#f3f4f6' },
                            },
                        },
                    }}
                />
            </div>
        </div>
    );
}

export default SensorChart;
