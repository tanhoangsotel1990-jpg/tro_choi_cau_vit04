import streamlit as st

st.set_page_config(page_title="Cuộc Đua Vịt STEM - Âm Thanh & Biểu Cảm", page_icon="🦆", layout="centered")

st.title("🦆 Cuộc Đua Vịt STEM - Âm Thanh & Biểu Cảm Sống Động")
st.write("Nhập tên các chú vịt, bấm **🚀 Bắt đầu cuộc đua** để trọng tài thổi còi khởi tranh!")

names_input = st.text_input("Nhập tên các chú vịt (cách nhau bởi dấu phẩy):", "Tân, Linh, Nam, Lan, An, Long, Vy")
names_list = [name.strip() for name in names_input.split(",") if name.strip()]

game_code = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        body {{ 
            margin: 0; 
            background: #b2ebf2; 
            text-align: center; 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            user-select: none;
        }}
        canvas {{ 
            background: linear-gradient(to bottom, #4fc3f7, #0288d1); 
            display: block; 
            margin: 10px auto; 
            border-radius: 12px; 
            box-shadow: 0 6px 15px rgba(0,0,0,0.3); 
        }}
        #ui-bar {{ 
            display: flex; 
            justify-content: center; 
            gap: 10px; 
            align-items: center; 
            width: 700px; 
            margin: 0 auto; 
            padding: 6px 10px; 
            box-sizing: border-box; 
        }}
        .btn {{ 
            background: #ff9800; 
            color: white; 
            border: none; 
            padding: 8px 16px; 
            border-radius: 20px; 
            font-weight: bold; 
            cursor: pointer; 
            font-size: 14px; 
            box-shadow: 0 3px 6px rgba(0,0,0,0.2); 
            transition: all 0.2s ease; 
        }}
        .btn:hover {{ 
            background: #f57c00; 
            transform: scale(1.05); 
        }}
        .btn-secondary {{ 
            background: #00bcd4; 
        }}
        .btn-secondary:hover {{ 
            background: #00acc1; 
        }}
        .btn-audio {{
            background: #e91e63;
        }}
        .btn-audio:hover {{
            background: #c2185b;
        }}
        #timer {{ 
            background: rgba(255, 255, 255, 0.95); 
            padding: 6px 14px; 
            border-radius: 15px; 
            font-weight: bold; 
            font-size: 15px; 
            color: #333; 
            box-shadow: 0 2px 5px rgba(0,0,0,0.2); 
        }}
    </style>
</head>
<body>
    <div id="ui-bar">
        <button class="btn" id="startBtn" onclick="startRace()">🚀 Bắt đầu</button>
        <button class="btn btn-secondary" id="pauseBtn" onclick="togglePause()" style="display:none;">⏸️ Tạm dừng</button>
        <button class="btn btn-audio" id="muteBtn" onclick="toggleMute()">🔊 Âm thanh: BẬT</button>
        <div id="timer">⏱️ 00:00</div>
        <button class="btn btn-secondary" onclick="resetGame()">🔄 Chơi lại</button>
    </div>

    <canvas id="gameCanvas" width="700" height="440"></canvas>

    <script>
        const canvas = document.getElementById("gameCanvas");
        const ctx = canvas.getContext("2d");
        const timerEl = document.getElementById("timer");

        const rawNames = {names_list};
        const colors = ["#ffeb3b", "#ff5252", "#4caf50", "#2196f3", "#ab47bc", "#ff9800", "#e91e63", "#00bcd4"];

        let ducks = [];
        let raceStarted = false;
        let refereeBlown = false;
        let isPaused = false;
        let isMuted = false;
        let startTime = 0;
        let elapsedTime = 0;
        let raceFinished = false;
        let winnerName = "";
        let waveOffset = 0;
        let fireworks = [];
        let blinkCounter = 0;

        let audioCtx = null;
        let musicInterval = null;

        function getAudioContext() {{
            if (!audioCtx) {{
                audioCtx = new (window.AudioContext || window.webkitAudioContext)();
            }}
            if (audioCtx.state === 'suspended') {{
                audioCtx.resume();
            }}
            return audioCtx;
        }}

        function toggleMute() {{
            isMuted = !isMuted;
            document.getElementById("muteBtn").innerText = isMuted ? "🔇 Âm thanh: TẮT" : "🔊 Âm thanh: BẬT";
            if (isMuted) {{
                stopBackgroundMusic();
            }} else if (raceStarted && !isPaused && !raceFinished) {{
                startBackgroundMusic();
            }}
        }}

        function playWhistleSound() {{
            if (isMuted) return;
            const actx = getAudioContext();
            const osc = actx.createOscillator();
            const gain = actx.createGain();

            osc.type = 'sine';
            osc.frequency.setValueAtTime(2600, actx.currentTime);
            osc.frequency.exponentialRampToValueAtTime(3200, actx.currentTime + 0.15);
            osc.frequency.setValueAtTime(2800, actx.currentTime + 0.3);

            gain.gain.setValueAtTime(0.3, actx.currentTime);
            gain.gain.exponentialRampToValueAtTime(0.01, actx.currentTime + 0.8);

            osc.connect(gain);
            gain.connect(actx.destination);

            osc.start();
            osc.stop(actx.currentTime + 0.8);
        }}

        function playFireworkSound() {{
            if (isMuted || !audioCtx) return;
            const actx = getAudioContext();
            const osc = actx.createOscillator();
            const gain = actx.createGain();

            osc.type = 'triangle';
            osc.frequency.setValueAtTime(180 + Math.random() * 220, actx.currentTime);
            osc.frequency.exponentialRampToValueAtTime(40, actx.currentTime + 0.35);

            gain.gain.setValueAtTime(0.25, actx.currentTime);
            gain.gain.exponentialRampToValueAtTime(0.001, actx.currentTime + 0.35);

            osc.connect(gain);
            gain.connect(actx.destination);

            osc.start();
            osc.stop(actx.currentTime + 0.35);
        }}

        function startBackgroundMusic() {{
            stopBackgroundMusic();
            if (isMuted) return;
            const actx = getAudioContext();
            const notes = [261.63, 329.63, 392.00, 523.25, 392.00, 329.63, 440.00, 349.23]; // Giai điệu bơi lội vui tươi
            let step = 0;

            musicInterval = setInterval(() => {{
                if (isPaused || raceFinished || isMuted) return;
                const osc = actx.createOscillator();
                const gain = actx.createGain();

                osc.type = 'sine';
                osc.frequency.setValueAtTime(notes[step % notes.length], actx.currentTime);

                gain.gain.setValueAtTime(0.07, actx.currentTime);
                gain.gain.exponentialRampToValueAtTime(0.001, actx.currentTime + 0.18);

                osc.connect(gain);
                gain.connect(actx.destination);

                osc.start();
                osc.stop(actx.currentTime + 0.18);

                step++;
            }}, 200);
        }}

        function stopBackgroundMusic() {{
            if (musicInterval) {{
                clearInterval(musicInterval);
                musicInterval = null;
            }}
        }}

        function initDucks() {{
            ducks = [];
            winnerName = "";
            fireworks = [];
            raceStarted = false;
            refereeBlown = false;
            rawNames.forEach((name, index) => {{
                ducks.push({{
                    name: name,
                    x: 40,
                    y: 110 + (index * (280 / Math.max(rawNames.length, 1))),
                    speed: Math.random() * 0.6 + 0.5,
                    color: colors[index % colors.length],
                    size: 26,
                    tearY: 0
                }});
            }});
        }}

        initDucks();

        function startRace() {{
            getAudioContext();
            document.getElementById("startBtn").style.display = "none";
            
            refereeBlown = true;
            playWhistleSound();

            setTimeout(() => {{
                raceStarted = true;
                startTime = Date.now();
                document.getElementById("pauseBtn").style.display = "inline-block";
                startBackgroundMusic();
            }}, 1000);
        }}

        function togglePause() {{
            isPaused = !isPaused;
            document.getElementById("pauseBtn").innerText = isPaused ? "▶️ Tiếp tục" : "⏸️ Tạm dừng";
            if (isPaused) {{
                stopBackgroundMusic();
            }} else {{
                startBackgroundMusic();
                startTime = Date.now() - elapsedTime;
            }}
        }}

        function resetGame() {{
            stopBackgroundMusic();
            initDucks();
            isPaused = false;
            raceFinished = false;
            elapsedTime = 0;
            document.getElementById("startBtn").style.display = "inline-block";
            document.getElementById("pauseBtn").style.display = "none";
            document.getElementById("pauseBtn").innerText = "⏸️ Tạm dừng";
            timerEl.innerText = "⏱️ 00:00";
        }}

        function drawSun() {{
            ctx.save();
            ctx.translate(630, 42);
            ctx.strokeStyle = "rgba(255, 235, 59, 0.4)";
            ctx.lineWidth = 3;
            for (let i = 0; i < 8; i++) {{
                ctx.rotate(Math.PI / 4);
                ctx.beginPath();
                ctx.moveTo(0, 22);
                ctx.lineTo(0, 32);
                ctx.stroke();
            }}
            ctx.fillStyle = "#ffeb3b";
            ctx.beginPath();
            ctx.arc(0, 0, 20, 0, Math.PI * 2);
            ctx.fill();
            ctx.strokeStyle = "#fbc02d";
            ctx.lineWidth = 2;
            ctx.stroke();
            ctx.restore();
        }}

        function drawReferee() {{
            const refX = 35;
            const refY = 32;

            // Thân áo trọng tài sọc đen trắng
            ctx.fillStyle = "#ffffff";
            ctx.fillRect(refX - 8, refY + 8, 16, 20);
            ctx.fillStyle = "#000000";
            ctx.fillRect(refX - 4, refY + 8, 3, 20);
            ctx.fillRect(refX + 2, refY + 8, 3, 20);

            // Đầu trọng tài
            ctx.fillStyle = "#ffe0b2";
            ctx.beginPath();
            ctx.arc(refX, refY, 7, 0, Math.PI * 2);
            ctx.fill();

            // Tay cầm còi
            ctx.strokeStyle = "#ffe0b2";
            ctx.lineWidth = 3;
            ctx.beginPath();
            if (refereeBlown) {{
                ctx.moveTo(refX - 8, refY + 14);
                ctx.lineTo(refX, refY + 4);
            }} else {{
                ctx.moveTo(refX - 8, refY + 14);
                ctx.lineTo(refX - 14, refY + 22);
            }}
            ctx.stroke();

            ctx.fillStyle = "#ffffff";
            ctx.font = "bold 10px sans-serif";
            ctx.textAlign = "left";
            ctx.fillText("Trọng tài 🏁", refX + 12, refY + 4);
        }}

        function drawCheeringCrowd() {{
            const crowdXPositions = [120, 200, 280, 360, 440, 520];
            crowdXPositions.forEach((x, index) => {{
                ctx.fillStyle = index % 2 === 0 ? "#e91e63" : "#3f51b5";
                ctx.fillRect(x - 8, 45, 16, 20);
                ctx.fillStyle = "#ffe0b2";
                ctx.beginPath();
                ctx.arc(x, 34, 7, 0, Math.PI * 2);
                ctx.fill();
                ctx.strokeStyle = "#ffe0b2";
                ctx.lineWidth = 3;
                ctx.beginPath();
                
                // Khán giả vẫy tay nhịp nhàng
                let armOffset = Math.sin(Date.now() * 0.008 + index) * 6;
                ctx.moveTo(x - 8, 50); ctx.lineTo(x - 14, 34 + armOffset);
                ctx.moveTo(x + 8, 50); ctx.lineTo(x + 14, 34 - armOffset);
                ctx.stroke();
            }});
        }}

        function drawCheckeredFinishLine() {{
            const lineX = 560;
            const squareSize = 15;
            for (let y = 65; y < canvas.height; y += squareSize) {{
                for (let x = 0; x < 30; x += squareSize) {{
                    ctx.fillStyle = ((x / squareSize + y / squareSize) % 2 === 0) ? "#000" : "#fff";
                    ctx.fillRect(lineX + x, y, squareSize, squareSize);
                }}
            }}
        }}

        function createFirework() {{
            const fx = 575;
            const fy = 150 + Math.random() * 200;
            const colorsList = ["#ff5252", "#ffeb3b", "#00bcd4", "#ab47bc", "#ff9800"];
            let particles = [];
            for (let i = 0; i < 32; i++) {{
                const angle = Math.random() * Math.PI * 2;
                const speed = Math.random() * 4.5 + 2;
                particles.push({{
                    x: fx, y: fy,
                    vx: Math.cos(angle) * speed,
                    vy: Math.sin(angle) * speed,
                    color: colorsList[Math.floor(Math.random() * colorsList.length)],
                    alpha: 1
                }});
            }}
            fireworks.push(particles);
            playFireworkSound();
        }}

        function update() {{
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            blinkCounter++;

            // Bờ cỏ xanh phía trên
            ctx.fillStyle = "#689f38";
            ctx.fillRect(0, 0, canvas.width, 65);

            drawSun();
            drawReferee();
            drawCheeringCrowd();

            // Mặt nước nhấp nhô sóng
            waveOffset += 0.05;
            ctx.fillStyle = "rgba(255, 255, 255, 0.25)";
            ctx.beginPath();
            ctx.moveTo(0, 65);
            for (let x = 0; x <= canvas.width; x += 20) {{
                let y = 65 + Math.sin(x * 0.03 + waveOffset) * 6;
                ctx.lineTo(x, y);
            }}
            ctx.lineTo(canvas.width, 65);
            ctx.lineTo(0, 65);
            ctx.fill();

            drawCheckeredFinishLine();

            if (raceStarted && !isPaused && !raceFinished) {{
                elapsedTime = Date.now() - startTime;
            }}

            let seconds = Math.floor((elapsedTime / 1000) % 60);
            let minutes = Math.floor(elapsedTime / 1000 / 60);
            timerEl.innerText = "⏱️ " + String(minutes).padStart(2, '0') + ":" + String(seconds).padStart(2, '0');

            if (!raceFinished) {{
                ducks.forEach((duck) => {{
                    if (raceStarted && !isPaused) {{
                        duck.x += duck.speed;
                        duck.speed += (Math.random() - 0.5) * 0.04;
                        if (duck.speed < 0.4) duck.speed = 0.4;
                        if (duck.speed > 1.8) duck.speed = 1.8;

                        if (duck.x >= 540 && !raceFinished) {{
                            raceFinished = true;
                            winnerName = duck.name;
                            duck.x = 540;
                            stopBackgroundMusic();
                        }}
                    }}
                }});
            }}

            // Hiệu ứng pháo hoa chúc mừng
            if (raceFinished) {{
                if (Math.random() < 0.08) {{
                    createFirework();
                }}
                fireworks.forEach((particles, index) => {{
                    particles.forEach(p => {{
                        p.x += p.vx;
                        p.y += p.vy;
                        p.alpha -= 0.02;
                        ctx.save();
                        ctx.globalAlpha = Math.max(p.alpha, 0);
                        ctx.fillStyle = p.color;
                        ctx.beginPath();
                        ctx.arc(p.x, p.y, 3.5, 0, Math.PI * 2);
                        ctx.fill();
                        ctx.restore();
                    }});
                    if (particles[0].alpha <= 0) {{
                        fireworks.splice(index, 1);
                    }}
                }});

                // Khung thông báo chiến thắng
                ctx.fillStyle = "rgba(0, 0, 0, 0.8)";
                ctx.fillRect(150, 185, 400, 70);
                ctx.strokeStyle = "#ffeb3b";
                ctx.lineWidth = 3;
                ctx.strokeRect(150, 185, 400, 70);
                ctx.fillStyle = "#ffeb3b";
                ctx.font = "bold 18px sans-serif";
                ctx.textAlign = "center";
                ctx.fillText("🎉 Chúc mừng " + winnerName + " vĩ đại đã về nhất! 🎉", 350, 227);
            }}

            ducks.forEach((duck) => {{
                let floatY = duck.y + Math.sin(duck.x * 0.05 + waveOffset) * 3;

                // Thân vịt
                ctx.fillStyle = duck.color;
                ctx.beginPath();
                ctx.ellipse(duck.x, floatY, duck.size, duck.size * 0.75, 0, 0, Math.PI * 2);
                ctx.fill();
                ctx.strokeStyle = "#222";
                ctx.lineWidth = 1.8;
                ctx.stroke();

                // Cánh vịt
                ctx.fillStyle = "rgba(255, 255, 255, 0.25)";
                ctx.beginPath();
                ctx.ellipse(duck.x - 6, floatY, 10, 6, -0.2, 0, Math.PI * 2);
                ctx.fill();

                // Đầu vịt
                ctx.fillStyle = duck.color;
                ctx.beginPath();
                ctx.arc(duck.x + 16, floatY - 14, duck.size * 0.52, 0, Math.PI * 2);
                ctx.fill();
                ctx.strokeStyle = "#222";
                ctx.lineWidth = 1.8;
                ctx.stroke();

                if (raceFinished && duck.name !== winnerName) {{
                    // BIỂU CẢM VỊT THUA: Mắt cụp buồn + Giọt nước mắt rơi dễ thương
                    ctx.strokeStyle = "#222";
                    ctx.lineWidth = 2.2;
                    ctx.beginPath();
                    // Mắt híp cụp uốn cong hướng xuống
                    ctx.arc(duck.x + 20, floatY - 14, 4, Math.PI * 1.1, Math.PI * 1.9, false);
                    ctx.stroke();

                    // Mỏ xịu xuống nhẹ nhàng
                    ctx.fillStyle = "#ff9800";
                    ctx.beginPath();
                    ctx.ellipse(duck.x + 27, floatY - 10, 6, 3, 0.2, 0, Math.PI * 2);
                    ctx.fill();
                    ctx.strokeStyle = "#222";
                    ctx.lineWidth = 1.2;
                    ctx.stroke();

                    // Giọt nước mắt long lanh rơi bên má
                    duck.tearY = (duck.tearY || 0) + 0.3;
                    if (duck.tearY > 12) duck.tearY = 0;
                    let tearX = duck.x + 18;
                    let tearActualY = floatY - 10 + duck.tearY;

                    ctx.fillStyle = "#4fc3f7";
                    ctx.beginPath();
                    ctx.arc(tearX, tearActualY, 2.5, 0, Math.PI * 2);
                    ctx.fill();
                    ctx.fillStyle = "#e0f7fa";
                    ctx.beginPath();
                    ctx.arc(tearX - 0.8, tearActualY - 0.8, 1, 0, Math.PI * 2);
                    ctx.fill();

                }} else {{
                    // BIỂU CẢM VỊT ĐANG BƠI / VỀ NHẤT: Mắt tròn xoe long lanh & Chớp mắt nhịp nhàng
                    let isBlinking = (blinkCounter % 120 > 112);
                    
                    if (isBlinking) {{
                        ctx.strokeStyle = "#222";
                        ctx.lineWidth = 2;
                        ctx.beginPath();
                        ctx.moveTo(duck.x + 16, floatY - 17);
                        ctx.lineTo(duck.x + 24, floatY - 17);
                        ctx.stroke();
                    }} else {{
                        // Mắt trắng lớn
                        ctx.fillStyle = "#fff";
                        ctx.beginPath();
                        ctx.arc(duck.x + 20, floatY - 17, 4.5, 0, Math.PI * 2);
                        ctx.fill();
                        ctx.strokeStyle = "#222";
                        ctx.lineWidth = 1;
                        ctx.stroke();

                        // Con ngươi đen
                        ctx.fillStyle = "#000";
                        ctx.beginPath();
                        ctx.arc(duck.x + 21.5, floatY - 17, 2.2, 0, Math.PI * 2);
                        ctx.fill();

                        // Điểm sáng trong mắt
                        ctx.fillStyle = "#fff";
                        ctx.beginPath();
                        ctx.arc(duck.x + 22.5, floatY - 18, 0.9, 0, Math.PI * 2);
                        ctx.fill();
                    }}

                    // Mỏ vươn ra tươi cười
                    ctx.fillStyle = "#ff9800";
                    ctx.beginPath();
                    ctx.ellipse(duck.x + 28, floatY - 12, 7, 3.5, 0, 0, Math.PI * 2);
                    ctx.fill();
                    ctx.strokeStyle = "#222";
                    ctx.lineWidth = 1.2;
                    ctx.stroke();
                }}

                // Bảng tên chú vịt
                ctx.fillStyle = "rgba(0, 0, 0, 0.7)";
                ctx.fillRect(duck.x - 22, floatY - 42, 50, 18);
                ctx.fillStyle = "#ffffff";
                ctx.font = "bold 12px sans-serif";
                ctx.textAlign = "center";
                ctx.fillText(duck.name, duck.x + 3, floatY - 29);
            }});

            requestAnimationFrame(update);
        }}

        update();
    </script>
</body>
</html>
"""

st.components.v1.html(game_code, height=500)
