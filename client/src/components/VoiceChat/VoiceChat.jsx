import { useEffect, useRef, useState } from 'react';
import './VoiceChat.css';

function VoiceChat() {
    const [chatHistory, setChatHistory] = useState([]);
    const [face, setFace] = useState('happy.png');
    const [listening, setListening] = useState(false);
    const chatEndRef = useRef(null);

    // ✅ 중복 메시지 방지용 ref
    const lastTranscriptRef = useRef('');
    const lastReplyRef = useRef('');

    useEffect(() => {
        const eventSource = new EventSource('/api/voice/state');

        eventSource.onmessage = (event) => {
            const data = JSON.parse(event.data);

            const fallbackFace = data.face === 'neutral.png' ? 'happy.png' : data.face;
            setFace(fallbackFace || 'happy.png');
            setListening(data.listening);

            const newEntries = [];

            if (data.transcript && data.transcript !== lastTranscriptRef.current) {
                newEntries.push({ type: 'user', text: data.transcript });
                lastTranscriptRef.current = data.transcript;
            }

            if (data.reply && data.reply !== lastReplyRef.current) {
                newEntries.push({ type: 'planty', text: data.reply });
                lastReplyRef.current = data.reply;
            }

            if (newEntries.length > 0) {
                setChatHistory((prev) => [...prev, ...newEntries]);
            }
        };

        eventSource.onerror = () => eventSource.close();
        return () => eventSource.close();
    }, []);

    useEffect(() => {
        if (chatEndRef.current) {
            chatEndRef.current.scrollIntoView({ behavior: 'smooth' });
        }
    }, [chatHistory]);

    return (
        <div className="voicechat-wrapper">
            <div className="left-panel">
                <div className="mic-visual">
                    <div className={`mic-circle ${listening ? 'active' : ''}`}>
                        <span role="img" aria-label="mic">
                            🎤
                        </span>
                    </div>
                    <div className="mic-status">{listening ? '듣는 중이에요...' : '“플랜티”라고 불러주세요!'}</div>
                </div>

                <div className="chat-box">
                    {chatHistory.length === 0 ? (
                        <div className="message placeholder">대화를 시작해보세요!</div>
                    ) : (
                        chatHistory.map((msg, index) => (
                            <div key={index} className={`message ${msg.type === 'user' ? 'user-msg' : 'planty-msg'}`}>
                                {msg.type === 'user' ? '🧍 ' : '🌿 '}
                                {msg.text}
                            </div>
                        ))
                    )}
                    <div ref={chatEndRef} />
                </div>
            </div>

            <div className="right-panel">
                <h2>플랜티의 표정</h2>
                <img src={`/face/${face}`} alt="표정" className="face-large" />
            </div>
        </div>
    );
}

export default VoiceChat;
