import random
import time
import streamlit as st

st.set_page_config(page_title="Trò Chơi Câu Vịt Nhựa", page_icon="🦆", layout="centered")

# Tiêu đề game
st.title("🦆 Trò Chơi Câu Vịt Nhựa Hội Chợ 🦆")
st.write("Hãy thử vận may của bạn! Câu được những chú vịt mang điểm số cao nhất nhé.")

# Khởi tạo trạng thái game (Điểm số, lượt câu)
if "score" not in st.session_state:
  st.session_state.score = 0
if "chances" not in st.session_state:
  st.session_state.chances = 5
if "message" not in st.session_state:
  st.session_state.message = (
      "Nhấn nút 'Thả cần câu' bên dưới để bắt đầu câu vịt!"
  )
if "last_duck" not in st.session_state:
  st.session_state.last_duck = "❓"

# Hiển thị thông tin tổng quan
col1, col2 = st.columns(2)
with col1:
  st.metric(label="🎯 Điểm số hiện tại", value=st.session_state.score)
with col2:
  st.metric(label="🎣 Lượt câu còn lại", value=st.session_state.chances)

st.markdown("---")
st.info(st.session_state.message)
st.subheader(f"Chú vịt vừa câu được: {st.session_state.last_duck}")

# Nút thao tác câu vịt
if st.session_state.chances > 0:
  if st.button("🎣 Thả cần câu ngay!", type="primary", use_container_width=True):
    # Danh sách các loại vịt có điểm số khác nhau dưới đáy hồ
    ducks = [
        {"name": "🦆 Vịt vàng thường (10 điểm)", "points": 10, "icon": "🦆"},
        {"name": "🦆 Vịt xanh năng động (20 điểm)", "points": 20, "icon": "🟢"},
        {"name": "👑 Vịt hoàng gia quý hiếm (50 điểm)", "points": 50, "icon": "👑"},
        {
            "name": "🥾 Ôi không, vớ phải chiếc giày cũ! (0 điểm)",
            "points": 0,
            "icon": "🥾",
        },
    ]

    # Hiệu ứng giả lập đang câu
    with st.spinner("Đang thả mồi và chờ vịt cắn câu..."):
      time.sleep(1)

    # Chọn ngẫu nhiên vịt
    caught_duck = random.choices(
        ducks, weights=[50, 30, 10, 10], k=1
    )[0]  # Tỷ lệ xuất hiện khác nhau

    # Cập nhật điểm và số lượt
    st.session_state.score += caught_duck["points"]
    st.session_state.chances -= 1
    st.session_state.last_duck = caught_duck["name"]
    st.session_state.message = (
        f"Bạn vừa câu trúng: **{caught_duck['name']}** (+{caught_duck['points']}"
        " điểm)!"
    )
    st.rerun()

else:
  st.warning(
      "Trò chơi đã kết thúc! Bạn đã hết lượt câu. Hãy bấm chơi lại bên dưới nhé."
  )
  if st.button("🔄 Chơi lại từ đầu", use_container_width=True):
    st.session_state.score = 0
    st.session_state.chances = 5
    st.session_state.message = (
        "Đã làm mới hồ nước! Hãy thả cần câu để thử vận may."
    )
    st.session_state.last_duck = "❓"
    st.rerun()
