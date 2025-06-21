// client/src/components/Layout/Layout.jsx
import { Link, useLocation } from 'react-router-dom';
import '../Dashboard/Dashboard.css';

const Layout = ({ children }) => {
    const location = useLocation();
    const current = location.pathname;

    return (
        <div className="dashboard-body">
            <aside className="main-left">
                <h2 className="sidebar-title">🌿 PlantCare</h2>
                <nav>
                    <ul>
                        <li className={current === '/' ? 'active' : ''}>
                            <Link to="/" style={{ textDecoration: 'none', color: 'inherit' }}>
                                Dashboard
                            </Link>
                        </li>

                        <li className={current === '/chatbot' ? 'active' : ''}>
                            <Link to="/chatbot" style={{ textDecoration: 'none', color: 'inherit' }}>
                                Chatbot
                            </Link>
                        </li>
                        <li className={current === '/voicechat' ? 'active' : ''}>
                            <Link to="/voicechat" style={{ textDecoration: 'none', color: 'inherit' }}>
                                Voice Chat
                            </Link>
                        </li>
                        <li className={current === '/camera' ? 'active' : ''}>
                            <Link to="/camera" style={{ textDecoration: 'none', color: 'inherit' }}>
                                Camera
                            </Link>
                        </li>
                        <li className={current === '/report' ? 'active' : ''}>
                            <Link to="/report" style={{ textDecoration: 'none', color: 'inherit' }}>
                                Report
                            </Link>
                        </li>
                    </ul>
                </nav>
            </aside>

            <main className="main-center">{children}</main>
        </div>
    );
};

export default Layout;
