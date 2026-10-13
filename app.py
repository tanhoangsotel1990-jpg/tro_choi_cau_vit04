import streamlit as st

st.set_page_config(page_title="Cuộc Đua Vịt STEM - Trọng Tài", page_icon="🦆", layout="centered")

st.title("🦆 Trò Chơi Đua Vịt - Cuộc Đua Sôi Động")
st.write("Nhập tên các thành viên, bấm 'Bắt đầu cuộc đua' để trọng tài thổi còi cho vịt bơi nhé!")

names_input = st.text_input("Nhập tên các chú vịt (cách nhau bởi dấu phẩy):", "Tân, Linh, Nam, Lan, An, Long, Vy")
names_list = [name.strip() for name in names_input.split(",") if name.strip()]

game_code = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ margin: 0; background: #b2ebf2; text-align: center; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }}
        canvas {{ background: linear-gradient(to bottom, #4fc3f7, #0288d1); display: block; margin: 10px auto; border-radius: 12px; box-shadow: 0 6px 15px rgba(0,0,0,0.3); }}
        #ui-bar {{ display: flex; justify-content: center; gap: 15px; align-items: center; width: 700px; margin: 0 auto; padding: 5px 10px; box-sizing: border-box; }}
        .btn {{ background: #ff9800; color: white; border: none; padding: 8px 18px; border-radius: 20px; font-weight: bold; cursor: pointer; font-size: 15px; box-shadow: 0 3px 6px rgba(0,0,0,0.2); transition: 0.2s; }}
        .btn:hover {{ background: #f57c00; transform: scale(1.05); }}
        .btn-secondary {{ background: #00bcd4; }}
        .btn-secondary:hover {{ background: #00acc1; }}
        #timer {{ background: rgba(255, 255, 255, 0.9); padding: 6px 16px; border-radius: 15px; font-weight: bold; font-size: 16px; color: #333; box-shadow: 0 2px 5px rgba(0,0,0,0.2); }}
    </style>
</head>
<body>
    <div id="ui-bar">
        <button class="btn" id="startBtn" onclick="startRace()">🚀 Bắt đầu cuộc đua</button>
        <button class="btn btn-secondary" id="pauseBtn" onclick="togglePause()" style="display:none;">⏸️ Tạm dừng</button>
        <div id="timer">⏱️ 00:00</div>
        <button class="btn btn-secondary" onclick="resetGame()">🔄 Chơi lại</button>
    </div>

    <canvas id="gameCanvas" width="700" height="440"></canvas>

    <!-- Âm thanh còi trọng tài và nhạc nền -->
    <audio id="whistleSound" src="https://actions.google.com/sounds/v1/sports/referee_whistle_1.ogg"></audio>
    <audio id="bgMusic" loop src="https://actions.google.com/sounds/v1/cartoon/silly_chicken.ogg"></audio>

    <script>
        const canvas = document.getElementById("gameCanvas");
        const ctx = canvas.getContext("2d");
        const timerEl = document.getElementById("timer");
        const whistleSound = document.getElementById("whistleSound");
        const bgMusic = document.getElementById("bgMusic");

        const rawNames = {names_list};
        const colors = ["#ff5252", "#ffeb3b", "#4caf50", "#2196f3", "#ab47bc", "#ff9800", "#e91e63", "#00bcd4"];
        
        let ducks = [];
        let raceStarted = false;
        let refereeBlown = false;
        let isPaused = false;
        let startTime = 0;
        let elapsedTime = 0;
        let raceFinished = false;
        let winnerName = "";
        let waveOffset = 0;
        let fireworks = [];

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
                    y: 110 + (index * (290 / Math.max(rawNames.length, 1))),
                    speed: Math.random() * 0.6 + 0.5,
                    color: colors[index % colors.length],
                    size: 28,
                    finished: false
                }});
            }});
        }}

        initDucks();

        function startRace() {{
            document.getElementById("startBtn").style.display = "none";
            
            // Trọng tài thổi còi trước
            whistleSound.play().catch(e => console.log("Audio play blocked"));
            refereeBlown = true;

            // Sau 1.5 giây còi thổi xong thì cuộc đua chính thức bắt đầu
            setTimeout(() => {{
                raceStarted = true;
                startTime = Date.now();
                document.getElementById("pauseBtn").style.display = "inline-block";
                bgMusic.play().catch(e => console.log("Audio play blocked"));
            }}, 1500);
        }}

        function togglePause() {{
            isPaused = !isPaused;
            document.getElementById("pauseBtn").innerText = isPaused ? "▶️ Tiếp tục" : "⏸️ Tạm dừng";
            if (isPaused) {{
                bgMusic.pause();
            }} else {{
                bgMusic.play();
                startTime = Date.now() - elapsedTime;
            }}
        }}

        function resetGame() {{
            initDucks();
            isPaused = false;
            raceFinished = false;
            elapsedTime = 0;
            document.getElementById("startBtn").style.display = "inline-block";
            document.getElementById("pauseBtn").style.display = "none";
            document.getElementById("pauseBtn").innerText = "⏸️ Tạm dừng";
            timerEl.innerText = "⏱️ 00:00";
            bgMusic.pause();
            bgMusic.currentTime = 0;
            whistleSound.currentTime = 0;
        }}

        function drawSun() {{
            ctx.save();
            ctx.translate(630, 45);
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

        // Vẽ trọng tài đứng ở đầu bờ sông cầm còi
        function drawReferee() {{
            const refX = 35;
            const refY = 32;

            // Thân áo trọng tài (áo sọc đen trắng đặc trưng)
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

            // Tay cầm còi hoặc giơ tay
            ctx.strokeStyle = "#ffe0b2";
            ctx.lineWidth = 3;
            ctx.beginPath();
            if (refereeBlown) {{
                // Tay đưa còi lên miệng thổi
                ctx.moveTo(refX - 8, refY + 14);
                ctx.lineTo(refX, refY + 4);
            }} else {{
                // Tay cầm còi xuôi
                ctx.moveTo(refX - 8, refY + 14);
                ctx.lineTo(refX - 14, refY + 22);
            }}
            ctx.stroke();

            // Chữ chú thích "Trọng tài" nhỏ bên cạnh
            ctx.fillStyle = "#333";
            ctx.font = "bold 10px sans-serif";
            ctx.textAlign = "left";
            ctx.fillText("Trọng tài", refX + 12, refY + 4);
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
                ctx.moveTo(x - 8, 50); ctx.lineTo(x - 16, 36);
                ctx.moveTo(x + 8, 50); ctx.lineTo(x + 16, 36);
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
            for (let i = 0; i < 30; i++) {{
                const angle = Math.random() * Math.PI * 2;
                const speed = Math.random() * 4 + 2;
                particles.push({{
                    x: fx, y: fy,
                    vx: Math.cos(angle) * speed,
                    vy: Math.sin(angle) * speed,
                    color: colorsList[Math.floor(Math.random() * colorsList.length)],
                    alpha: 1
                }});
            }}
            fireworks.push(particles);
        }}

        function update() {{
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            ctx.fillStyle = "#689f38";
            ctx.fillRect(0, 0, canvas.width, 65);

            drawSun();
            drawReferee();
            drawCheeringCrowd();

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
                        }}
                    }}
                }});
            }}

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

                ctx.fillStyle = "rgba(0, 0, 0, 0.75)";
                ctx.fillRect(150, 180, 400, 70);
                ctx.fillStyle = "#ffeb3b";
                ctx.font = "bold 18px sans-serif";
                ctx.textAlign = "center";
                ctx.fillText("🎉 Chúc mừng " + winnerName + " đã về đích đầu tiên! 🎉", 350, 222);
            }}

            ducks.forEach((duck) => {{
                let floatY = duck.y + Math.sin(duck.x * 0.05 + waveOffset) * 3;

                ctx.fillStyle = duck.color;
                ctx.beginPath();
                ctx.ellipse(duck.x, floatY, duck.size, duck.size * 0.75, 0, 0, Math.PI * 2);
                ctx.fill();
                ctx.strokeStyle = "#222";
                ctx.lineWidth = 1.8;
                ctx.stroke();

                ctx.beginPath();
                ctx.arc(duck.x + 16, floatY - 14, duck.size * 0.52, 0, Math.PI * 2);
                ctx.fill();
                ctx.stroke();

                if (raceFinished && duck.name !== winnerName) {{
                    ctx.fillStyle = "#000";
                    ctx.font = "bold 12px sans-serif";
                    ctx.fillText("✖ ✖", duck.x + 16, floatY - 18);
                    
                    ctx.strokeStyle = "#000";
                    ctx.lineWidth = 1.5;
                    ctx.beginPath();
                    ctx.arc(duck.x + 28, floatY - 5, 4, Math.PI, 0, false);
                    ctx.stroke();
                }} else {{
                    ctx.fillStyle = "#fff";
                    ctx.beginPath();
                    ctx.arc(duck.x + 20, floatY - 17, 4, 0, Math.PI * 2);
                    ctx.fill();
                    ctx.fillStyle = "#000";
                    ctx.beginPath();
                    ctx.arc(duck.x + 21, floatY - 17, 2, 0, Math.PI * 2);
                    ctx.fill();

                    ctx.fillStyle = "#ff9800";
                    ctx.beginPath();
                    ctx.ellipse(duck.x + 28, floatY - 12, 7, 3.5, 0, 0, Math.PI * 2);
                    ctx.fill();
                    ctx.stroke();
                }}

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
