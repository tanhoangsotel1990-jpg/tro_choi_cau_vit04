<!-- ... existing code ... -->
        let elapsedTime = 0;
        let raceFinished = false;
        let winnerName = "";
        let waveOffset = 0;
        let fireworks = [];
        let fireworkTriggered = false;
        let blinkCounter = 0;

        let audioCtx = null;
<!-- ... existing code ... -->
        function initDucks() {{
            ducks = [];
            winnerName = "";
            fireworks = [];
            fireworkTriggered = false;
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
<!-- ... existing code ... -->
        function triggerSingleFirework() {{
            if (fireworkTriggered) return;
            fireworkTriggered = true;
            
            // Tạo 1 đợt bùng nổ pháo hoa lớn duy nhất với nhiều chùm sáng xung quanh đích
            const burstLocations = [
                {x: 560, y: 150},
                {x: 580, y: 220},
                {x: 540, y: 290}
            ];
            
            const colorsList = ["#ff5252", "#ffeb3b", "#00bcd4", "#ab47bc", "#ff9800", "#ffffff"];
            
            burstLocations.forEach((loc) => {{
                let particles = [];
                for (let i = 0; i < 36; i++) {{
                    const angle = Math.random() * Math.PI * 2;
                    const speed = Math.random() * 5 + 2;
                    particles.push({{
                        x: loc.x, y: loc.y,
                        vx: Math.cos(angle) * speed,
                        vy: Math.sin(angle) * speed,
                        color: colorsList[Math.floor(Math.random() * colorsList.length)],
                        alpha: 1
                    }});
                }}
                fireworks.push(particles);
            }});
            
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
                            triggerSingleFirework();
                        }}
                    }}
                }});
            }}

            // Vẽ hiệu ứng pháo hoa
            if (raceFinished) {{
                fireworks.forEach((particles, index) => {{
                    particles.forEach(p => {{
                        p.x += p.vx;
                        p.y += p.vy;
                        p.alpha -= 0.015;
                        ctx.save();
                        ctx.globalAlpha = Math.max(p.alpha, 0);
                        ctx.fillStyle = p.color;
                        ctx.beginPath();
                        ctx.arc(p.x, p.y, 3.5, 0, Math.PI * 2);
                        ctx.fill();
                        ctx.restore();
                    }});
                }});
            }}

            // 1. VẼ TẤT CẢ CÁC CHÚ VỊT TRƯỚC
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
                    // BIỂU CẢM VỊT ĐANG BƠI / VỀ NHẤT
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

            // 2. VẼ KHUNG THÔNG BÁO NỔI LÊN TRÊN CÙNG (SAU CÙNG) ĐỂ KHÔNG BỊ VỊT ĐÈ LÊN
            if (raceFinished) {{
                ctx.save();
                
                // Đổ bóng nổi đè lên trên tất cả mọi thứ
                ctx.shadowColor = "rgba(0, 0, 0, 0.6)";
                ctx.shadowBlur = 15;
                ctx.shadowOffsetX = 0;
                ctx.shadowOffsetY = 6;

                // Khung viền viền vàng ánh kim
                ctx.fillStyle = "#111827";
                ctx.beginPath();
                ctx.roundRect(100, 180, 500, 75, 12);
                ctx.fill();
                
                ctx.strokeStyle = "#ffeb3b";
                ctx.lineWidth = 4;
                ctx.stroke();
                
                ctx.restore();

                // Dòng chữ chúc mừng đậm rõ nét
                ctx.fillStyle = "#ffeb3b";
                ctx.font = "bold 20px 'Segoe UI', sans-serif";
                ctx.textAlign = "center";
                ctx.textBaseline = "middle";
                ctx.fillText("🎉 Chúc mừng " + winnerName + " vĩ đại đã về nhất! 🎉", 350, 217);
            }}

            requestAnimationFrame(update);
        }}

        update();
    </script>
</body>
</html>
"""

st.components.v1.html(game_code, height=500)
