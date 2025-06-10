// static/script.js

function updateDht() {
    fetch('/api/dht')
        .then((response) => response.json())
        .then((data) => {
            document.getElementById('temp').textContent =
                data.temperature !== null ? data.temperature : '에러';
            document.getElementById('humid').textContent =
                data.humidity !== null ? data.humidity : '에러';
        })
        .catch(() => {
            document.getElementById('temp').textContent = '오류';
            document.getElementById('humid').textContent = '오류';
        });
}

function updateSoil() {
    fetch('/api/soil')
        .then((response) => response.json())
        .then((data) => {
            document.getElementById('soil').textContent =
                data.status === 'dry' ? '건조함' : '촉촉함';
        })
        .catch(() => {
            document.getElementById('soil').textContent = '오류';
        });
}

// 최초 실행
updateDht();
updateSoil();

// 5초마다 반복
setInterval(() => {
    updateDht();
    updateSoil();
}, 5000);
