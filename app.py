import streamlit as st

st.set_page_config(page_title="Cuộc Đua Vịt Vui Nhộn", page_icon="🦆", layout="centered")

st.title("🦆 Trò Chơi Đua Vịt - Phong Cách STEM")
st.write("Nhập danh sách tên để bắt đầu cuộc đua vượt sông nhé!")

names_input = st.text_input("Nhập tên các chú vịt (cách nhau bởi dấu phẩy):", "Tân, Linh, Nam, Lan, An, Long, Vy")
names_list = [name.strip() for name in names_input.split(",") if name.strip()]

game_code = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ margin: 0; background: #b2ebf2; text-align: center; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }}
        canvas {{ background: linear-gradient(to bottom, #4fc3f7, #0288d1); display: block; margin: 10px auto; border-radius: 12px; box-shadow: 0 6px 15px rgba(0,0,0,0.3); }}
        #ui-bar {{ display: flex; justify-content: space-between; align-items: center; width: 700px; margin: 0 auto; padding: 5px 10px; box-sizing: border-box; }}
        .btn {{ background: rgba(255, 255, 255, 0.8); border: none; padding: 6px 14px; border-radius: 20px; font-weight: bold; cursor: pointer; font-size: 14px; box-shadow: 0 2px 5px rgba(0,0,0,0.2); }}
        .btn:hover {{ background: #ffffff; }}
        #timer {{ background: rgba(255, 255, 255, 0.85); padding: 5px 15px; border-radius: 15px; font-weight: bold; font-size: 16px; color: #333; box-shadow: 0 2px 5px rgba(0,0,0,0.2); }}
    </style>
</head>
<body>
    <div id="ui-bar">
        <button class="btn" id="pauseBtn" onclick="togglePause()">⏸️ Tạm dừng</button>
        <div id="timer">⏱️ 00:00</div>
        <button class="btn" onclick="resetGame()">🔄 Chơi lại</button>
    </div>

    <canvas id="gameCanvas" width="700" height="400"></canvas>

    <script>
        const canvas = document.getElementById("gameCanvas");
        const ctx = canvas.getContext("2d");
        const timerEl = document.getElementById("timer");

        const rawNames = {names_list};
        const colors = ["#ff5252", "#ffeb3b", "#4caf50", "#2196f3", "#ab47bc", "#ff9800", "#e91e63", "#00bcd4"];
        
        let ducks = [];
        let isPaused = false;
        let startTime = Date.now();
        let elapsedTime = 0;
        let raceFinished = false;

        function initDucks() {{
            ducks = [];
            rawNames.forEach((name, index) => {{
                ducks.push({{
                    name: name,
                    x: 40 + Math.random() * 40, // Xuất phát lệch nhau chút cho tự nhiên
                    y: 60 + (index * (280 / Math.max(rawNames.length, 1))),
                    speed: Math.random() * 0.7 + 0.6,
                    color: colors[index % colors.length],
                    size: 20
                }});
            }});
        }}

        initDucks();

        function togglePause() {{
            isPaused = !isPaused;
            document.getElementById("pauseBtn").innerText = isPaused ? "▶️ Tiếp tục" : "⏸️ Tạm dừng";
            if (!isPaused) {{
                startTime = Date.now() - elapsedTime;
            }}
        }}

        function resetGame() {{
            initDucks();
            startTime = Date.now();
            elapsedTime = 0;
            isPaused = false;
            raceFinished = false;
            document.getElementById("pauseBtn").innerText = "⏸️ Tạm dừng";
        }}

        // Vẽ vạch đích caro đen trắng
        function drawCheckeredFinishLine() {{
            const lineX = 550;
            const squareSize = 15;
            for (let y = 0; y < canvas.height; y += squareSize) {{
                for (let x = 0; x < 30; x += squareSize) {{
                    ctx.fillStyle = ((x / squareSize + y / squareSize) % 2 === 0) ? "#000" : "#fff";
                    ctx.fillRect(lineX + x, y, squareSize, squareSize);
                }}
            }}
        }}

        function update() {{
            if (!isPaused && !raceFinished) {{
                elapsedTime = Date.now() - startTime;
            }}

            let seconds = Math.floor((elapsedTime / 1000) % 60);
            let minutes = Math.floor(elapsedTime / 1000 / 60);
            timerEl.innerText = "⏱️ " + String(minutes).padStart(2, '0') + ":" + String(seconds).padStart(2, '0');

            ctx.clearRect(0, 0, canvas.width, canvas.height);

            // Vẽ hiệu ứng mặt nước gợn sóng phía trên
            ctx.fillStyle = "rgba(255,255,255,0.2)";
            ctx.fillRect(0, 0, canvas.width, 40);

            // Vẽ vạch đích
            drawCheckeredFinishLine();

            let allFinished = true;

            // Cập nhật và vẽ từng chú vịt
            ducks.forEach((duck) => {{
                if (!isPaused && !raceFinished) {{
                    duck.x += duck.speed;
                    // Tăng giảm tốc độ ngẫu nhiên để cuộc đua kịch tính
                    duck.speed += (Math.random() - 0.5) * 0.05;
                    if (duck.speed < 0.3) duck.speed = 0.3;
                    if (duck.speed > 2.0) duck.speed = 2.0;

                    if (duck.x >= 530) {{
                        duck.x = 530; // Dừng lại khi chạm đích
                    }}
                }}

                if (duck.x < 530) {{
                    allFinished = false;
                }}

                // --- Vẽ thân vịt ---
                ctx.fillStyle = duck.color;
                ctx.beginPath();
                ctx.ellipse(duck.x, duck.y, duck.size, duck.size * 0.7, 0, 0, Math.PI * 2);
                ctx.fill();
                ctx.strokeStyle = "#222";
                ctx.lineWidth = 1.5;
                ctx.stroke();

                // --- Vẽ đầu vịt ---
                ctx.beginPath();
                ctx.arc(duck.x + 12, duck.y - 10, duck.size * 0.55, 0, Math.PI * 2);
                ctx.fill();
                ctx.stroke();

                // --- Vẽ mắt vịt ---
                ctx.fillStyle = "#fff";
                ctx.beginPath();
                ctx.arc(duck.x + 15, duck.y - 12, 3.5, 0, Math.PI * 2);
                ctx.fill();
                ctx.fillStyle = "#000";
                ctx.beginPath();
                ctx.arc(duck.x + 16, duck.y - 12, 1.5, 0, Math.PI * 2);
                ctx.fill();

                // --- Vẽ mỏ vịt ---
                ctx.fillStyle = "#ff9800";
                ctx.beginPath();
                ctx.ellipse(duck.x + 21, duck.y - 8, 6, 3, 0, 0, Math.PI * 2);
                ctx.fill();
                ctx.stroke();

                // --- Hộp tên hiển thị trên đầu mỗi con vịt ---
                ctx.fillStyle = "rgba(0, 0, 0, 0.6)";
                ctx.fillRect(duck.x - 20, duck.y - 32, 45, 16);
                ctx.fillStyle = "#ffffff";
                ctx.font = "bold 11px sans-serif";
                ctx.textAlign = "center";
                ctx.fillText(duck.name, duck.x + 25, duck.y - 20);
            }});

            if (allFinished && !raceFinished) {{
                raceFinished = true;
            }}

            requestAnimationFrame(update);
        }}

        update();
    </script>
</body>
</html>
"""

st.components.v1.html(game_code, height=470)
