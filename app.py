import random
import time
import streamlit as st

st.set_page_config(page_title="Trò Chơi Câu Vịt Nhựa", page_icon="🦆", layout="centered")

# CSS tùy chỉnh để giao diện sinh động, giống như một hồ nước hội chợ
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(to bottom, #e0f7fa, #80deea);
    }
    .duck-pond {
        background-color: #00838f;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        color: white;
        font-size: 20px;
        margin-bottom: 20px;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.2);
    }
    </style>
""",
    unsafe_allow_html=True,
)

# Tiêu đề game
st.title("🦆 Trò Chơi Câu Vịt Nhựa Hội Chợ 🦆")
st.write(
    "Chào mừng bạn đến với hồ câu vịt may mắn! Hãy nhìn đàn vịt đang bơi và"
    " thả cần câu nhé."
)

# Khởi tạo trạng thái game
if "score" not in st.session_state:
  st.session_state.score = 0
if "chances" not in st.session_state:
  st.session_state.chances = 5
if "message" not in st.session_state:
  st.session_state.message = "Hồ nước đang yên bình... Hãy nhấn nút thả cần câu!"
if "last_duck" not in st.session_state:
  st.session_state.last_duck = "❓ Chưa câu con nào"

# Hiển thị điểm số và lượt câu
col1, col2 = st.columns(2)
with col1:
  st.metric(label="🎯 Điểm số của bạn", value=st.session_state.score)
with col2:
  st.metric(label="🎣 Lượt câu còn lại", value=st.session_state.chances)

st.markdown("---")

# 1. Hiển thị "Màn hình hồ nước và đàn vịt đang bơi" bằng hình ảnh minh họa sống động
st.subheader("🌊 Hồ Vịt Đang Bơi Lội")
st.image(
    "https://images.unsplash.com/photo-1555169062-013468b1f4cb?auto=format&fit=crop&w=800&q=80",
    caption="Những chú vịt nhựa đầy màu sắc đang bơi lội tung tăng trong hồ!",
    use_container_width=True,
)

# Thông báo trạng thái
st.info(st.session_state.message)

# 2. Khu vực thao tác câu vịt
if st.session_state.chances > 0:
  if st.button(
      "🎣 THẢ CẦN CÂU XUỐNG HỒ!", type="primary", use_container_width=True
  ):
    # Danh sách phần thưởng dưới hồ
    ducks = [
        {
            "name": "🦆 Vịt vàng thông thường (+10 điểm)",
            "points": 10,
            "img": "https://images.unsplash.com/photo-1555169062-013468b1f4cb?auto=format&fit=crop&w=400&q=80",
        },
        {
            "name": "🟢 Vịt xanh năng động (+20 điểm)",
            "points": 20,
            "img": "https://images.unsplash.com/photo-1535083783855-76ae62b2914e?auto=format&fit=crop&w=400&q=80",
        },
        {
            "name": "👑 Vịt hoàng gia quý hiếm (+50 điểm)",
            "points": 50,
            "img": "https://images.unsplash.com/photo-1517849845537-4d257902454a?auto=format&fit=crop&w=400&q=80",
        },
        {
            "name": "🥾 Ôi không, vớ phải chiếc giày cũ! (0 điểm)",
            "points": 0,
            "img": "https://images.unsplash.com/photo-1560769629-975ec94e6a86?auto=format&fit=crop&w=400&q=80",
        },
    ]

    # Hiệu ứng giả lập cần câu đang hạ xuống và nhấc lên
    with st.spinner("🎣 Đang thả cần câu xuống hồ... Cẩn thận nào..."):
      time.sleep(1.2)

    # Chọn ngẫu nhiên kết quả
    caught = random.choices(ducks, weights=[50, 30, 10, 10], k=1)[0]

    # Cập nhật điểm
    st.session_state.score += caught["points"]
    st.session_state.chances -= 1
    st.session_state.last_duck = caught["name"]
    st.session_state.message = f"🎉 Bạn đã câu lên thành công: **{caught['name']}**!"

    # Hiển thị hình ảnh chú vịt vừa câu được
    st.success(st.session_state.message)
    st.image(
        caught["img"],
        caption=f"Món quà kéo lên: {caught['name']}",
        width=300,
    )

    time.sleep(0.5)
    st.rerun()

else:
  st.warning("🚨 Trò chơi kết thúc! Bạn đã sử dụng hết 5 lượt câu.")
  if st.button("🔄 Chơi lại ván mới", use_container_width=True):
    st.session_state.score = 0
    st.session_state.chances = 5
    st.session_state.message = (
        "Hồ nước đã được làm mới. Hãy thả cần câu tiếp nhé!"
    )
    st.session_state.last_duck = "❓ Chưa câu con nào"
    st.rerun()
