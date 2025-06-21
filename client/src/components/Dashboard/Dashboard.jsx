'use client';
import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import './Dashboard.css';

function Toggle({ isOn, onToggle }) {
    return (
        <label className="switch">
            <input type="checkbox" checked={isOn} onChange={onToggle} />
            <span className="slider"></span>
        </label>
    );
}

function Dashboard() {
    const [sensorData, setSensorData] = useState({
        temperature: 0,
        humidity: 0,
        soilMoisture: 0,
        light: 'bright',
        ledState: false,
        ledMode: false,
    });

    const [faceImg, setFaceImg] = useState(null);
    const [faceText, setFaceText] = useState('');
    const [faceReason, setFaceReason] = useState('');
    const navigate = useNavigate();

    useEffect(() => {
        // 표정 정보 불러오기
        fetch('/api/mood/latest')
            .then((res) => res.json())
            .then((data) => {
                if (!data.error) {
                    setFaceImg(`/face/${data.face}`); // 확장자 포함 경로
                    setFaceText(moodLabel(data.mood));
                    setFaceReason(data.reason || '');
                }
            });

        // 센서 및 LED 상태 불러오기
        fetch('/api/sensor/current')
            .then((res) => res.json())
            .then((data) => {
                setSensorData((prev) => ({
                    ...prev,
                    temperature: data.temperature ?? 0,
                    humidity: data.humidity ?? 0,
                    soilMoisture: data.soilMoisture ?? 0,
                    light: data.light ?? 'bright',
                    ledState: data.led?.state === 'on',
                    ledMode: data.led?.mode === 'auto',
                }));
            });
    }, []);

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
                return '표정';
        }
    };

    const handleLedStateToggle = () => {
        const newState = !sensorData.ledState;
        fetch('/api/led', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ action: newState ? 'on' : 'off' }),
        }).then(() => {
            setSensorData((prev) => ({ ...prev, ledState: newState, ledMode: false }));
        });
    };

    const handleLedModeToggle = () => {
        const newMode = !sensorData.ledMode;
        fetch('/api/led', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ action: newMode ? 'auto' : 'off' }),
        }).then(() => {
            setSensorData((prev) => ({
                ...prev,
                ledMode: newMode,
                ledState: newMode ? prev.ledState : false,
            }));
        });
    };

    return (
        <div style={{ display: 'flex', gap: '20px', height: '100%', width: '100%' }}>
            <div className="main-center" style={{ flex: 1 }}>
                <h1 className="main-title">Smart Plant Control System</h1>
                <div className="grid">
                    {/* 온도 */}
                    <div className="card">
                        <div className="card-title">
                            <img src="/icon/tem.png" alt="온도 아이콘" className="icon" />
                            <h3>온도</h3>
                        </div>
                        <p className="value">{sensorData.temperature}°C</p>
                        <p className="range">적정 온도: 20–26°C</p>
                    </div>

                    {/* 습도 */}
                    <div className="card">
                        <div className="card-title">
                            <img src="/icon/water.png" alt="습도 아이콘" className="icon" />
                            <h3>습도</h3>
                        </div>
                        <p className="value">{sensorData.humidity}%</p>
                        <p className="range">적정 습도: 60–70%</p>
                    </div>

                    {/* 토양 습도 */}
                    <div className="card">
                        <div className="card-title">
                            <img src="/icon/soilwater.png" alt="토양 아이콘" className="icon" />
                            <h3>토양 습도</h3>
                        </div>
                        <p className="value">
                            {sensorData.soilMoisture === true
                                ? '건조함'
                                : sensorData.soilMoisture === false
                                ? '촉촉함'
                                : '-'}
                        </p>
                        <p className="range">적정 수분: 습함 유지</p>
                    </div>

                    {/* LED 제어 */}
                    <div className="card">
                        <div className="card-title">
                            <img src="/icon/led.png" alt="LED 아이콘" className="icon" />
                            <h3>LED 제어</h3>
                        </div>
                        <p className="range">주변 밝기: {sensorData.light === 'dark' ? '어두움' : '밝음'}</p>
                        <div className="row">
                            <span>상태: {sensorData.ledState ? 'ON' : 'OFF'}</span>
                            <Toggle isOn={sensorData.ledState} onToggle={handleLedStateToggle} />
                        </div>
                        <div className="row">
                            <span>자동 모드: {sensorData.ledMode ? 'ON' : 'OFF'}</span>
                            <Toggle isOn={sensorData.ledMode} onToggle={handleLedModeToggle} />
                        </div>
                    </div>

                    {/* 급수 제어 */}
                    <div className="card">
                        <div className="card-title">
                            <img src="/icon/pump.png" alt="펌프 아이콘" className="icon" />
                            <h3>급수 제어</h3>
                        </div>
                        <p className="range">원할 때 즉시 급수</p>
                        <button
                            className="btn-black"
                            onClick={() => {
                                fetch('/api/pump', { method: 'POST' })
                                    .then((res) => res.json())
                                    .then(() => alert('💧 물 주기가 완료되었습니다!'));
                            }}
                        >
                            물 주기 실행
                        </button>
                    </div>

                    {/* 타임랩스 */}
                    <div className="card">
                        <div className="card-title">
                            <img src="/icon/cam.png" alt="타임랩스 아이콘" className="icon" />
                            <h3>플랜트 캠</h3>
                        </div>
                        <p className="range">실시간 플랜트 캠</p>
                        <button className="btn-outline" onClick={() => navigate('/camera')}>
                            플랜트 캠 보러가기
                        </button>
                    </div>
                </div>
            </div>

            {/* 오른쪽 표정 영역 */}
            <aside className="main-right" style={{ flex: 1 }}>
                <h2 className="camera-title">Face</h2>
                <div className="camera-box" style={{ height: '100%' }}>
                    {faceImg ? (
                        <>
                            <img src={faceImg} alt="Plant face" className="camera-image" />
                            <p className="camera-text">{faceText}</p>
                            <p className="camera-update">{faceReason}</p>
                        </>
                    ) : (
                        <p>표정 데이터를 불러오는 중...</p>
                    )}
                </div>
            </aside>
        </div>
    );
}

export default Dashboard;
