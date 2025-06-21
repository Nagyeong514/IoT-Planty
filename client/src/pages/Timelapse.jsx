// src/pages/Timelapse.jsx
import './Timelapse.css';

function Timelapse() {
    return (
        <div className="container">
            {' '}
            {/* ✅ 배경 애니메이션 wrapper로 변경 */}
            <div className="live-card">
                <div className="video-header">
                    <h2 className="video-title">플랜티 타임랩스</h2>
                </div>
                <video width="100%" controls className="video-feed">
                    <source src="/static/timelapse.mp4" type="video/mp4" />
                    브라우저가 비디오 태그를 지원하지 않습니다.
                </video>
            </div>
        </div>
    );
}

export default Timelapse;
