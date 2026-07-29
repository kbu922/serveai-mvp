import streamlit as st
import numpy as np
import pandas as pd

# ==========================================
# 1. Page Configuration
# ==========================================
st.set_page_config(
    page_title="ServeAI - AI Tennis Serve Analysis & Travel",
    page_icon="🎾",
    layout="wide"
)

# Initialize Session States for User Authentication
if "registered_users" not in st.session_state:
    st.session_state["registered_users"] = {}

if "logged_in_user" not in st.session_state:
    st.session_state["logged_in_user"] = None


# ==========================================
# 2. Recommendation Logic Engine
# ==========================================
def calculate_recommended_tension(ntpr_str, current_tension_option, calculated_speed_kmh, age=30, gender="Male"):
    try:
        ntpr_val = float(ntpr_str.split(" ")[1])
    except:
        ntpr_val = 2.5

    standard_baseline_map = {2.0: 48, 2.5: 50, 3.0: 51, 3.5: 52, 4.0: 53, 4.5: 54, 5.0: 55}
    expected_speed_map = {2.0: 80.0, 2.5: 95.0, 3.0: 110.0, 3.5: 125.0, 4.0: 140.0, 4.5: 155.0, 5.0: 170.0}

    base_tension = standard_baseline_map.get(ntpr_val, 50)
    expected_speed = expected_speed_map.get(ntpr_val, 100.0)
    
    if gender == "Female":
        expected_speed -= 10.0
        base_tension -= 2
    if age >= 50:
        base_tension -= 2

    speed_diff = calculated_speed_kmh - expected_speed

    if current_tension_option is None or current_tension_option == 0:
        if speed_diff >= 10:
            rec_tension = base_tension + 2
            reason = f"NTPR({ntpr_val}) 대비 서브 속도가 빠르므로, 볼 제어력(Control)과 스핀 생성을 위해 **{rec_tension} lbs**를 추천합니다.\n\n*(Recommended {rec_tension} lbs for enhanced control.)*"
        elif speed_diff <= -10:
            rec_tension = base_tension - 2
            reason = f"타구 파워 보완과 엘보 관절 보호를 위해 부드러운 **{rec_tension} lbs**로 시작하는 것을 추천합니다.\n\n*(Recommended {rec_tension} lbs to protect elbow joint.)*"
        else:
            rec_tension = base_tension
            reason = f"측정된 속도 기반, NTPR({ntpr_val}) 표준 추천 텐션인 **{rec_tension} lbs**가 가장 적합합니다.\n\n*(Optimal standard tension: {rec_tension} lbs.)*"
        
        return rec_tension, reason, "Standard Guide", expected_speed

    else:
        current_tension = int(current_tension_option)
        if speed_diff >= 15:
            rec_tension = current_tension + 3
            reason = "서브 속도가 매우 빠릅니다! 정밀한 코스 공략을 위해 텐션을 +3 lbs 올려보세요."
        elif 5 <= speed_diff < 15:
            rec_tension = current_tension + 2
            reason = "우수한 타구 파워를 보유하고 있습니다. 안정적인 컨트롤을 위해 +2 lbs를 추천합니다."
        elif -5 <= speed_diff < 5:
            rec_tension = current_tension
            reason = "현재 텐션(lbs)이 사용자의 서브 속도 및 NTPR 레벨과 완벽하게 매칭됩니다!"
        elif -15 <= speed_diff < -5:
            rec_tension = current_tension - 2
            reason = "비거리 확보를 위해 텐션을 -2 lbs 낮춰 라켓의 '트램펄린 효과'를 활용해보세요."
        else:
            rec_tension = current_tension - 3
            reason = "관절 부담을 줄이고 적은 힘으로 비거리를 늘리기 위해 -3 lbs를 추천합니다."
        
        delta_val = rec_tension - current_tension
        delta_str = f"{delta_val:+d} lbs" if delta_val != 0 else "Optimal"
        return rec_tension, reason, delta_str, expected_speed


# ==========================================
# 3. Sidebar: User Account & Profile Registration
# ==========================================
st.sidebar.header("👤 계정 및 프로필 (User Account)")

if st.session_state["logged_in_user"] is None:
    account_mode = st.sidebar.radio("로그인 / 회원가입 (Account)", ["로그인 (Login)", "회원가입 (Register)"])

    if account_mode == "회원가입 (Register)":
        st.sidebar.subheader("📝 회원가입 (Sign Up)")
        reg_id = st.sidebar.text_input("아이디 (ID)")
        reg_pw = st.sidebar.text_input("비밀번호 (Password)", type="password")
        reg_age = st.sidebar.number_input("나이 (Age)", min_value=10, max_value=90, value=25)
        reg_gender = st.sidebar.selectbox("성별 (Gender)", ["Male (남성)", "Female (여성)", "Other (기타)"])
        reg_address = st.sidebar.text_input("주소 (Address)", value="Seoul, South Korea")

        if st.sidebar.button("회원가입 완료 (Register)"):
            if reg_id and reg_pw:
                st.session_state["registered_users"][reg_id] = {
                    "password": reg_pw,
                    "age": reg_age,
                    "gender": "Female" if "Female" in reg_gender else "Male",
                    "address": reg_address
                }
                st.sidebar.success("🎉 회원가입 성공! 로그인 해주세요.")
            else:
                st.sidebar.error("아이디와 비밀번호를 입력해주세요.")

    elif account_mode == "로그인 (Login)":
        st.sidebar.subheader("🔑 로그인 (Login)")
        login_id = st.sidebar.text_input("아이디 (ID)")
        login_pw = st.sidebar.text_input("비밀번호 (Password)", type="password")

        if st.sidebar.button("로그인 (Login)"):
            users = st.session_state["registered_users"]
            if login_id in users and users[login_id]["password"] == login_pw:
                st.session_state["logged_in_user"] = login_id
                st.sidebar.success(f"Welcome back, {login_id}!")
                st.rerun()
            else:
                st.sidebar.error("아이디 또는 비밀번호가 올바르지 않습니다.")

else:
    user_id = st.session_state["logged_in_user"]
    user_info = st.session_state["registered_users"][user_id]
    
    st.sidebar.success(f"🟢 **{user_id}** 님 로그인 중")
    st.sidebar.write(f"• **Age**: {user_info['age']}")
    st.sidebar.write(f"• **Gender**: {user_info['gender']}")
    st.sidebar.write(f"• **Address**: {user_info['address']}")
    
    if st.sidebar.button("로그아웃 (Logout)"):
        st.session_state["logged_in_user"] = None
        st.rerun()

st.sidebar.markdown("---")

# Tennis Profile Sidebar
st.sidebar.header("⚙️ 테니스 프로필 (Tennis Profile)")
ntpr_input = st.sidebar.selectbox("구력/실력 (NTPR Level)", ["NTPR 2.0 - 2.5", "NTPR 3.0 - 3.5", "NTPR 4.0 - 4.5", "NTPR 5.0+"])
racket_model = st.sidebar.text_input("사용 중인 라켓 모델 (Racket Model)", value="Babolat Pure Drive 300g")
dont_know_tension = st.sidebar.checkbox("현재 텐션을 모름 (Don't know current tension)")

if dont_know_tension:
    current_tension_input = None
else:
    current_tension_input = st.sidebar.number_input("현재 라켓 텐션 (Current Tension in lbs)", min_value=30, max_value=70, value=52)


# ==========================================
# 4. Main UI Content
# ==========================================
st.title("🎾 ServeAI: AI 기반 서브 분석 & 테니스 투어 패키지")
st.write("단일 영상 AI 서브 분석부터 글로벌/국내 테니스 대회 참가 및 여행 패키지 견적까지 한 번에 이용하세요.")

st.markdown("---")

# Video Upload Section
uploaded_file = st.file_uploader("🎥 서브 분석 비디오 업로드 (Upload Serve Video)", type=["mp4", "mov", "avi"])

if uploaded_file is not None:
    st.video(uploaded_file)
    
    if st.button("🚀 AI 분석 실행 (Analyze Serve Video)"):
        with st.spinner("AI가 영상을 분석 중입니다..."):
            import time
            time.sleep(2)
            
            ai_measured_speed = 118.5
            
            user_age = 25
            user_gender = "Male"
            if st.session_state["logged_in_user"] is not None:
                curr_u = st.session_state["registered_users"][st.session_state["logged_in_user"]]
                user_age = curr_u["age"]
                user_gender = curr_u["gender"]
            
            rec_lbs, rec_msg, delta_status, exp_speed = calculate_recommended_tension(
                ntpr_str=ntpr_input,
                current_tension_option=current_tension_input,
                calculated_speed_kmh=ai_measured_speed,
                age=user_age,
                gender=user_gender
            )
            
            st.success("✅ 분석이 완료되었습니다!")
            
            # Metric Summary Cards
            st.markdown("### 📊 AI 분석 리포트 (Analysis Summary)")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric(label="최고 서브 속도", value=f"{ai_measured_speed} km/h")
            with col2:
                st.metric(label="추천 라켓 텐션", value=f"{rec_lbs} lbs", delta=delta_status)
            with col3:
                st.metric(label="타깃 라켓 모델", value=racket_model if racket_model else "Standard")
            
            st.markdown("---")
            
            # Graph
            st.markdown("### 📈 프레임별 서브 속도 추적 그래프 (Speed Trajectory)")
            frames = np.arange(0, 30, 1)
            speeds = [0] * 5 + list(np.linspace(20, 118.5, 8)) + list(np.linspace(118.5, 75, 12)) + [0] * 5
            
            chart_data = pd.DataFrame({
                "Frame": frames[:len(speeds)],
                "Ball Speed (km/h)": speeds,
                "NTPR Average Speed": [exp_speed] * len(speeds)
            }).set_index("Frame")
            
            st.line_chart(chart_data)
            st.info(f"💡 **AI 피드백**:\n\n{rec_msg}")

st.markdown("---")

# ==========================================
# 5. NEW FEATURE: Tennis Competition & Travel Calculator
# ==========================================
st.header("✈️ 테니스 대회 참가 & 여행 패키지 견적 (Tennis Tour & Travel Package)")
st.write("세계 주요 그랜드슬램 및 국내 테니스 대회 참가/관람과 도시별 호텔 숙박 패키지 견적을 실시간으로 산출해보세요.")

# Database of Competitions & Hotels
competitions_db = {
    "🇺🇸 US Open (New York, USA)": {
        "city": "New York, USA",
        "ticket_fee_usd": 250, # Ticket / Entry Fee per person
        "hotels": {
            "Grand Hyatt New York (Luxury)": 350,
            "Queens Flushing Hotel (Budget)": 130,
            "Courtyard by Marriott NYC (Mid-Range)": 220
        }
    },
    "🇰🇷 Korea Open ATP/WTA (Seoul, South Korea)": {
        "city": "Seoul, Korea",
        "ticket_fee_usd": 60,
        "hotels": {
            "Grand InterContinental Seoul (Luxury)": 280,
            "L7 Gangnam by LOTTE (Mid-Range)": 140,
            "Seoul Olympic Parktel (Budget)": 80
        }
    },
    "🇰🇷 Korea National Amateur Cup (Busan, South Korea)": {
        "city": "Busan, Korea",
        "ticket_fee_usd": 40,
        "hotels": {
            "Paradise Hotel Busan (Luxury)": 260,
            "Haeundae Centum Hotel (Mid-Range)": 110,
            "Busan Toyoko Inn (Budget)": 65
        }
    }
}

col_tour1, col_tour2 = st.columns(2)

with col_tour1:
    selected_comp = st.selectbox("1️⃣ 대회 선택 (Select Competition)", list(competitions_db.keys()))
    comp_info = competitions_db[selected_comp]
    
    st.write(f"📍 **개최 도시 (City)**: {comp_info['city']}")
    st.write(f"🎟️ **대회 참가/티켓 비용 (Entry/Ticket Fee)**: ${comp_info['ticket_fee_usd']} USD")

with col_tour2:
    hotel_options = comp_info["hotels"]
    selected_hotel = st.selectbox("2️⃣ 숙박 호텔 선택 (Select Hotel)", list(hotel_options.keys()))
    hotel_price_per_night = hotel_options[selected_hotel]
    
    nights = st.number_input("3️⃣ 숙박 박수 (Nights of Stay)", min_value=1, max_value=14, value=3)
    people_count = st.number_input("4️⃣ 인원 수 (Number of People)", min_value=1, max_value=5, value=1)

# Total Package Calculation
total_ticket_cost = comp_info['ticket_fee_usd'] * people_count
total_hotel_cost = hotel_price_per_night * nights * people_count
grand_total_usd = total_ticket_cost + total_hotel_cost

# KRW Conversion Rate (Approx. 1 USD = 1,350 KRW)
grand_total_krw = grand_total_usd * 1350

st.markdown("### 🏷️ 패키지 실시간 견적 산출 (Package Quote Summary)")

q_col1, q_col2, q_col3 = st.columns(3)
with q_col1:
    st.metric(label="티켓/참가비 총액 (Tickets/Entry)", value=f"${total_ticket_cost} USD")
with q_col2:
    st.metric(label="호텔 숙박비 총액 (Hotel Stay)", value=f"${total_hotel_cost} USD")
with q_col3:
    st.metric(
        label="최종 패키지 예상 견적 (Total Package)", 
        value=f"${grand_total_usd} USD", 
        delta=f"≈ ₩{grand_total_krw:,.0f} KRW"
    )

if st.button("📩 이 패키지로 예약 상담 신청 (Request Booking Quote)"):
    if st.session_state["logged_in_user"] is not None:
        user_name = st.session_state["logged_in_user"]
        st.balloons()
        st.success(f"🎉 축하합니다, {user_name}님! **{selected_comp}** 여행 패키지 예약 신청이 접수되었습니다. 담당자 확인 후 연락드리겠습니다.")
    else:
        st.warning("⚠️ 예약 상담 신청을 위해 사이드바에서 먼저 **로그인/회원가입**을 진행해주세요.")
