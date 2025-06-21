import React, { useState, useEffect, useRef } from 'react';
import './Chatbot.css';

const Chatbot = () => {
    const [messages, setMessages] = useState([
        { sender: 'bot', text: '안녕하세요! 식물 챗봇입니다 🌿 무엇을 도와드릴까요?' },
    ]);
    const [input, setInput] = useState('');
    const [face, setFace] = useState('happy.png'); // ✅ 기본 표정 설정
    const [loading, setLoading] = useState(false);
    const chatboxRef = useRef(null);

    const recommendedQuestions = ['지금 화분 상태 어때?', '오늘 기분은 어때?', '마지막으로 물 준 게 언제야?'];

    const handleSend = async () => {
        if (!input.trim()) return;

        const newMessages = [...messages, { sender: 'user', text: input }];
        setMessages(newMessages);
        setInput('');
        setLoading(true);

        try {
            const res = await fetch('/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: input }),
            });

            const data = await res.json();

            setMessages((prev) => [...prev, { sender: 'bot', text: data.reply }]);
            if (data.face) {
                setFace(data.face); // ✅ 표정 이미지 업데이트
            }
        } catch (err) {
            console.error('💥 Chat API 오류:', err);
            setMessages((prev) => [...prev, { sender: 'bot', text: '⚠️ 서버 응답에 실패했어요.' }]);
        } finally {
            setLoading(false);
        }
    };

    // 채팅창 자동 스크롤
    useEffect(() => {
        if (chatboxRef.current) {
            chatboxRef.current.scrollTop = chatboxRef.current.scrollHeight;
        }
    }, [messages]);

    // ✅ 브라우저 확대 대응 vh 계산
    useEffect(() => {
        const setVh = () => {
            const vh = window.innerHeight * 0.01;
            document.documentElement.style.setProperty('--vh', `${vh}px`);
        };
        setVh();
        window.addEventListener('resize', setVh);
        return () => window.removeEventListener('resize', setVh);
    }, []);

    const handleRecommendClick = (text) => {
        setInput(text);
    };

    return (
        <div className="chatbot-container">
            <div className="chatbot-sidebar">
                <div className="wishbot-profile">
                    {/* ✅ 표정 이미지 반영 */}
                    <img className="wishbot-image" src={`/face/${face}`} alt="플랜티 표정" />
                    <div className="wishbot-name">플랜티</div>
                </div>
                <h3>추천 질문</h3>
                {recommendedQuestions.map((q, idx) => (
                    <button key={idx} onClick={() => handleRecommendClick(q)} className="question-btn">
                        {q}
                    </button>
                ))}
            </div>

            <div className="chatbot-main">
                <div className="chatbox" ref={chatboxRef}>
                    {messages.map((msg, idx) => (
                        <div key={idx} className={`chat-message ${msg.sender}`}>
                            <div className="bubble">{msg.text}</div>
                        </div>
                    ))}
                    {loading && (
                        <div className="chat-message bot">
                            <div className="bubble loading">
                                생각 중<span className="dot">.</span>
                                <span className="dot">.</span>
                                <span className="dot">.</span>
                            </div>
                        </div>
                    )}
                </div>

                <div className="input-form">
                    <input
                        type="text"
                        placeholder="메시지를 입력하세요..."
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        onKeyDown={(e) => e.key === 'Enter' && handleSend()}
                    />
                    <button onClick={handleSend}>전송</button>
                </div>
            </div>
        </div>
    );
};

export default Chatbot;
