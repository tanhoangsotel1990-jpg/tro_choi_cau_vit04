import streamlit as st

st.set_page_config(page_title="Cuộc Đua Vịt STEM - Cổ Vũ", page_icon="🦆", layout="centered")

st.title("🦆 Trò Chơi Đua Vịt - Phiên Bản Cổ Vũ Sôi Động")
st.write("Nhập tên các thành viên, bấm 'Bắt đầu cuộc đua' và xem khán giả trên bờ cổ vũ nhé!")

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

    <audio id="bgMusic" loop>
        <source src="https://actions.google.com/sounds/v1/cartoon/silly_chicken.ogg" type="audio/ogg">
    </audio>

    <script>
        const canvas = document.getElementById("gameCanvas");
        const ctx = canvas.getContext("2d");
        const timerEl = document.getElementById("timer");
        const bgMusic = document.getElementById("bgMusic");

        const rawNames = {names_list};
        const colors = ["#ff5252", "#ffeb3b", "#4caf50", "#2196f3", "#ab47bc", "#ff9800", "#e91e63", "#00bcd4"];
        
        let ducks = [];
        let raceStarted = false;
        let isPaused = false;
        let startTime = 0;
        let elapsedTime = 0;
        let raceFinished = false;
        let waveOffset = 0;

        function initDucks() {{
            ducks = [];
            rawNames.forEach((name, index) => {{
                ducks.push({{
                    name: name,
                    x: 40,
                    y: 110 + (index * (290 / Math.max(rawNames.length, 1))),
                    speed: Math.random() * 0.6 + 0.5,
                    color: colors[index % colors.length],
                    size: 28
                }});
            }});
        }}

        initDucks();

        function startRace() {{
            raceStarted = true;
            startTime = Date.now();
            document.getElementById("startBtn").style.display = "none";
            document.getElementById("pauseBtn").style.display = "inline-block";
            bgMusic.play().catch(e => console.log("Audio play blocked"));
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
            raceStarted = false;
            isPaused = false;
            raceFinished = false;
            elapsedTime = 0;
            document.getElementById("startBtn").style.display = "inline-block";
            document.getElementById("pauseBtn").style.display = "none";
            document.getElementById("pauseBtn").innerText = "⏸️ Tạm dừng";
            timerEl.innerText = "⏱️ 00:00";
            bgMusic.pause();
            bgMusic.currentTime = 0;
        }}

        // Vẽ ông mặt trời ở góc trên bên phải
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

        // Vẽ những người đang đứng trên bờ cổ vũ
        function drawCheeringCrowd() {{
            const crowdXPositions = [80, 160, 240, 320, 400, 480];
            crowdXPositions.forEach((x, index) => {{
                // Thân người/áo đủ màu
                ctx.fillStyle = index % 2 === 0 ? "#e91e63" : "#3f51b5";
                ctx.fillRect(x - 8, 45, 16, 20);

                // Đầu người
                ctx.fillStyle = "#ffe0b2";
                ctx.beginPath();
                ctx.arc(x, 34, 7, 0, Math.PI * 2);
                ctx.fill();

                // Tay đang giơ lên cổ vũ (vẫy tay)
                ctx.strokeStyle = "#ffe0b2";
                ctx.lineWidth = 3;
                ctx.beginPath();
                // Tay trái giơ lên
                ctx.moveTo(x - 8, 50);
                ctx.lineTo(x - 16, 36);
                // Tay phải giơ lên
                ctx.moveTo(x + 8, 50);
                ctx.lineTo(x + 16, 36);
                ctx.stroke();
            }});
        }}

        // Vẽ vạch đích caro đen trắng
        function drawCheckeredFinishLine() {{
            const lineX = 560;
            const squareSize = 15;
            for (let y = 60; y < canvas.height; y += squareSize) {{
                for (let x = 0; x < 30; x += squareSize) {{
                    ctx.fillStyle = ((x / squareSize + y / squareSize) % 2 === 0) ? "#000" : "#fff";
                    ctx.fillRect(lineX + x, y, squareSize, squareSize);
                }}
            }}
        }}

        function update() {{
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            // 1. Vẽ dải bờ sông xanh ở phía trên
            ctx.fillStyle = "#689f38";
            ctx.fillRect(0, 0, canvas.width, 65);

            // 2. Vẽ Ông Mặt Trời
            drawSun();

            // 3. Vẽ Khán giả đang cổ vũ trên bờ
            drawCheeringCrowd();

            // 4. Vẽ Hiệu ứng sóng nhấp nhô trên mặt nước (bắt đầu từ y = 65)
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

            // 5. Vẽ Vạch Đích
            drawCheckeredFinishLine();

            if (raceStarted && !isPaused && !raceFinished) {{
                elapsedTime = Date.now() - startTime;
            }}

            let seconds = Math.floor((elapsedTime / 1000) % 60);
            let minutes = Math.floor(elapsedTime / 1000 / 60);
            timerEl.innerText = "⏱️ " + String(minutes).padStart(2, '0') + ":" + String(seconds).padStart(2, '0');

            let allFinished = true;

            ducks.forEach((duck) => {{
                if (raceStarted && !isPaused && !raceFinished) {{
                    duck.x += duck.speed;
                    duck.speed += (Math.random() - 0.5) * 0.04;
                    if (duck.speed < 0.4) duck.speed = 0.4;
                    if (duck.speed > 1.8) duck.speed = 1.8;

                    if (duck.x >= 540) {{
                        duck.x = 540;
                    }}
                }}

                if (duck.x < 540) {{
                    allFinished = false;
                }}

                let floatY = duck.y + Math.sin(duck.x * 0.05 + waveOffset) * 3;

                // --- Vẽ thân vịt ---
                ctx.fillStyle = duck.color;
                ctx.beginPath();
                ctx.ellipse(duck.x, floatY, duck.size, duck.size * 0.75, 0, 0, Math.PI * 2);
                ctx.fill();
                ctx.strokeStyle = "#222";
                ctx.lineWidth = 1.8;
                ctx.stroke();

                // --- Vẽ đầu vịt ---
                ctx.beginPath();
                ctx.arc(duck.x + 16, floatY - 14, duck.size * 0.52, 0, Math.PI * 2);
                ctx.fill();
                ctx.stroke();

                // --- Vẽ mắt vịt ---
                ctx.fillStyle = "#fff";
                ctx.beginPath();
                ctx.arc(duck.x + 20, floatY - 17, 4, 0, Math.PI * 2);
                ctx.fill();
                ctx.fillStyle = "#000";
                ctx.beginPath();
                ctx.arc(duck.x + 21, floatY - 17, 2, 0, Math.PI * 2);
                ctx.fill();

                // --- Vẽ mỏ vịt ---
                ctx.fillStyle = "#ff9800";
                ctx.beginPath();
                ctx.ellipse(duck.x + 28, floatY - 12, 7, 3.5, 0, 0, Math.PI * 2);
                ctx.fill();
                ctx.stroke();

                // --- Hộp tên hiển thị trên đầu vịt ---
                ctx.fillStyle = "rgba(0, 0, 0, 0.7)";
                ctx.fillRect(duck.x - 22, floatY - 42, 50, 18);
                ctx.fillStyle = "#ffffff";
                ctx.font = "bold 12px sans-serif";
                ctx.textAlign = "center";
                ctx.fillText(duck.name, duck.x + 3, floatY - 29);
            }});

            if (raceStarted && allFinished && !raceFinished) {{
                raceFinished = true;
                bgMusic.pause();
            }}

            requestAnimationFrame(update);
        }}

        update();
    </script>
</body>
</html>
"""

st.components.v1.html(game_code, height=500)

