import streamlit as st

st.set_page_config(page_title="Trò Chơi Câu Vịt", page_icon="🦆", layout="centered")

st.title("🦆 Trò Chơi Câu Vịt Vui Nhộn")
st.write("Dùng chuột nhấp trực tiếp vào các chú vịt đang bơi để câu lên nhé!")

game_code = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body { margin: 0; background: #e0f7fa; text-align: center; font-family: sans-serif; }
        canvas { background: linear-gradient(to bottom, #81d4fa, #0288d1); display: block; margin: 0 auto; border-radius: 10px; cursor: crosshair; box-shadow: 0 4px 10px rgba(0,0,0,0.3); }
        #score { font-size: 22px; font-weight: bold; color: #d32f2f; margin-bottom: 10px; }
    </style>
</head>
<body>
    <div id="score">Điểm số: 0</div>
    <canvas id="gameCanvas" width="600" height="400"></canvas>
    <script>
        const canvas = document.getElementById("gameCanvas");
        const ctx = canvas.getContext("2d");
        const scoreEl = document.getElementById("score");

        let score = 0;
        let ducks = [];

        // Tạo 5 chú vịt bơi lội
        for (let i = 0; i < 5; i++) {
            ducks.push({
                x: Math.random() * (canvas.width - 60),
                y: Math.random() * 200 + 120,
                speed: (Math.random() * 1.5 + 0.8) * (Math.random() < 0.5 ? 1 : -1),
                size: 40
            });
        }

        // Bắt sự kiện click chuột để câu vịt
        canvas.addEventListener("click", (e) => {
            const rect = canvas.getBoundingClientRect();
            const mouseX = e.clientX - rect.left;
            const mouseY = e.clientY - rect.top;

            ducks.forEach(duck => {
                // Kiểm tra xem click có trúng vịt không
                if (mouseX >= duck.x && mouseX <= duck.x + duck.size &&
                    mouseY >= duck.y && mouseY <= duck.y + duck.size) {
                    score += 10;
                    scoreEl.innerText = "Điểm số: " + score;
                    // Đưa vịt đổi vị trí mới
                    duck.x = Math.random() * (canvas.width - 60);
                    duck.y = Math.random() * 200 + 120;
                }
            });
        });

        function update() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            // Vẽ hiệu ứng gợn sóng mặt nước
            ctx.strokeStyle = "rgba(255, 255, 255, 0.4)";
            ctx.lineWidth = 2;
            ctx.beginPath();
            ctx.moveTo(0, 100); ctx.lineTo(600, 100);
            ctx.stroke();

            // Vẽ từng chú vịt đồ chơi
            ducks.forEach(duck => {
                duck.x += duck.speed;
                if (duck.x < 10 || duck.x > canvas.width - 50) {
                    duck.speed *= -1;
                }

                // Vẽ thân vịt (hình Oval màu vàng)
                ctx.fillStyle = "#ffeb3b";
                ctx.beginPath();
                ctx.ellipse(duck.x + 20, duck.y + 25, 22, 16, 0, 0, Math.PI * 2);
                ctx.fill();
                ctx.strokeStyle = "#fbc02d";
                ctx.lineWidth = 2;
                ctx.stroke();

                // Vẽ đầu vịt
                ctx.beginPath();
                ctx.arc(duck.x + 32, duck.y + 12, 12, 0, Math.PI * 2);
                ctx.fill();
                ctx.stroke();

                // Vẽ mỏ vịt (màu cam)
                ctx.fillStyle = "#ff9800";
                ctx.fillRect(duck.x + 40, duck.y + 9, 10, 6);
            });

            requestAnimationFrame(update);
        }

        update();
    </script>
</body>
</html>
"""

st.components.v1.html(game_code, height=500)
