// clinet/src/index.js

import React from 'react';
import ReactDOM from 'react-dom/client';
import './styles/index.css'; // 글로벌 스타일
import App from './App';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
    <React.StrictMode>
        <App />
    </React.StrictMode>
);
