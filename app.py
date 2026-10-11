import streamlit as st

st.set_page_config(page_title="Bài Học STEM - Trò Chơi Đua Vịt", page_icon="🦆", layout="centered")

st.title("🦆 Bài Học STEM: Trò Chơi Đua Vịt Tương Tác")
st.write("Nhập danh sách tên các bạn trong lớp để tạo những chú vịt thi đua bơi về đích nhé!")

# Khung nhập tên danh sách người chơi
names_input = st.text_input("Nhập tên mọi người (cách nhau bởi dấu phẩy):", "Tân, Hòa, Nam, Lan, An")

# Xử lý chuỗi tên
names_list = [name.strip() for name in names_input.split(",") if name.strip()]

game_code = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ margin: 0; background: #e0f7fa; text-align: center; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }}
        canvas {{ background: linear-gradient(to bottom, #4fc3f7, #0288d1); display: block; margin: 10px auto; border-radius: 12px; cursor: pointer; box-shadow: 0 6px 15px rgba(0,0,0,0.3); }}
        #score {{ font-size: 20px; font-weight: bold; color: #0277bd; margin-top: 5px; }}
    </style>
</head>
<body>
    <div id="score">🎯 Bấm vào các chú vịt để tăng tốc về đích!</div>
    <canvas id="gameCanvas" width="700" height="420"></canvas>
    <script>
        const canvas = document.getElementById("gameCanvas");
        const ctx = canvas.getContext("2d");
        const scoreEl = document.getElementById("score");

        const rawNames = {names_list};
        const colors = ["#ff5252", "#ffeb3b", "#4caf50", "#2196f3", "#ab47bc", "#ff9800", "#e91e63", "#00bcd4"];
        
        let ducks = [];

        // Khởi tạo danh sách vịt dựa trên tên người chơi nhập vào
        rawNames.forEach((name, index) => {{
            ducks.push({{
                name: name,
                x: 70, // Bắt đầu từ vạch xuất phát
                y: 70 + index * 55,
                speed: Math.random() * 0.8 + 0.5,
                color: colors[index % colors.length],
                size: 22,
                finished: false
            }});
        }});

        // Sự kiện click vào vịt
        canvas.addEventListener("click", (e) => {{
            const rect = canvas.getBoundingClientRect();
            const mouseX = e.clientX - rect.left;
            const mouseY = e.clientY - rect.top;

            ducks.forEach(duck => {{
                const dist = Math.hypot((duck.x + 15) - mouseX, (duck.y) - mouseY);
                if (dist < duck.size + 15 && !duck.finished) {{
                    duck.x += 15; // Đẩy vịt tiến lên khi click
                    scoreEl.innerText = "🚀 Bạn vừa giúp chú vịt '" + duck.name + "' tiến lên!";
                }}
            }});
        }});

        function drawScene() {{
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            // 1. Vẽ Vạch Bắt Đầu (Bên trái)
            ctx.fillStyle = "rgba(255, 255, 255, 0.8)";
            ctx.fillRect(50, 0, 15, canvas.height);
            ctx.fillStyle = "#d32f2f";
            ctx.font = "bold 14px sans-serif";
            ctx.save();
            ctx.translate(40, 260);
            ctx.rotate(-Math.PI / 2);
            ctx.fillText("VẠCH BẮT ĐẦU", 0, 0);
            ctx.restore();

            // 2. Vẽ Vạch Chiến Thắng (Bên phải)
            ctx.fillStyle = "#ffd54f";
            ctx.fillRect(620, 0, 15, canvas.height);
            ctx.fillStyle = "#1b5e20";
            ctx.font = "bold 14px sans-serif";
            ctx.save();
            ctx.translate(650, 270);
            ctx.rotate(-Math.PI / 2);
            ctx.fillText("VẠCH CHIẾN THẮNG", 0, 0);
            ctx.restore();

            // 3. Vẽ và cập nhật vị trí từng chú vịt
            ducks.forEach((duck) => {{
                if (!duck.finished) {{
                    duck.x += duck.speed;
                    if (duck.x >= 580) {{
                        duck.finished = true;
                        scoreEl.innerText = "🏆 Chú vịt " + duck.name + " đã CHIẾN THẮNG! 🎉";
                    }}
                }}

                // --- Vẽ Thân Vịt ---
                ctx.fillStyle = duck.color;
                ctx.beginPath();
                ctx.ellipse(duck.x, duck.y, duck.size, duck.size * 0.7, 0, 0, Math.PI * 2);
                ctx.fill();
                ctx.strokeStyle = "#333";
                ctx.lineWidth = 1.5;
                ctx.stroke();

                // --- Vẽ Đầu Vịt ---
                ctx.beginPath();
                ctx.arc(duck.x + 15, duck.y - 12, duck.size * 0.55, 0, Math.PI * 2);
                ctx.fill();
                ctx.stroke();

                // --- Vẽ Mắt ---
                ctx.fillStyle = "#ffffff";
                ctx.beginPath();
                ctx.arc(duck.x + 18, duck.y - 15, 4, 0, Math.PI * 2);
                ctx.fill();
                ctx.fillStyle = "#000000";
                ctx.beginPath();
                ctx.arc(duck.x + 19, duck.y - 15, 2, 0, Math.PI * 2);
                ctx.fill();

                // --- Vẽ Mỏ Vịt (Mũi/Miệng) ---
                ctx.fillStyle = "#ff9800";
                ctx.beginPath();
                ctx.ellipse(duck.x + 25, duck.y - 10, 7, 4, 0, 0, Math.PI * 2);
                ctx.fill();
                ctx.stroke();

                // --- In Tên Người Chơi Lên Thân Vịt ---
                ctx.fillStyle = "#ffffff";
                ctx.font = "bold 12px sans-serif";
                ctx.textAlign = "center";
                ctx.shadowColor = "black";
                ctx.shadowBlur = 3;
                ctx.fillText(duck.name, duck.x, duck.y + 4);
                ctx.shadowBlur = 0; // Reset hiệu ứng bóng
            }});

            requestAnimationFrame(drawScene);
        }}

        drawScene();
    </script>
</body>
</html>
"""

st.components.v1.html(game_code, height=470)
