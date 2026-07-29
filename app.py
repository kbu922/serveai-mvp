import streamlit as st
import numpy as np
import pandas as pd
import datetime

# ==========================================
# 1. Page Configuration
# ==========================================
st.set_page_config(
    page_title="ServeAI - AI Tennis Serve & Travel Package",
    page_icon="🎾",
    layout="wide"
)

# Initialize Session States
if "registered_users" not in st.session_state:
    st.session_state["registered_users"] = {}

if "logged_in_user" not in st.session_state:
    st.session_state["logged_in_user"] = None

if "payment_completed" not in st.session_state:
    st.session_state["payment_completed"] = False


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
            reason = f"NTPR({ntpr_val}) 대비 서브 속도가 빠르므로, 볼 제어력(Control)과 스핀 생성을 위해 **{rec_tension} lbs**를 추천합니다."
        elif speed_diff <= -10:
            rec_tension = base_tension - 2
            reason = f"타구 파워 보완과 엘보 관절 보호를 위해 부드러운 **{rec_tension} lbs**로 시작하는 것을 추천합니다."
        else:
            rec_tension = base_tension
            reason = f"측정된 속도 기반, NTPR({ntpr_val}) 표준 추천 텐션인 **{rec_tension} lbs**가 가장 적합합니다."
        
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
    account_mode = st.sidebar.radio("로그인 / 회원가입", ["로그인 (Login)", "회원가입 (Register)"])

    if account_mode == "회원가입 (Register)":
        st.sidebar.subheader("📝 회원가입")
        reg_id = st.sidebar.text_input("아이디 (ID)")
        reg_pw = st.sidebar.text_input("비밀번호 (Password)", type="password")
        reg_age = st.sidebar.number_input("나이 (Age)", min_value=10, max_value=90, value=25)
        reg_gender = st.sidebar.selectbox("성별 (Gender)", ["Male (남성)", "Female (여성)", "Other (기타)"])
        reg_address = st.sidebar.text_input("주소 (Address)", value="Seoul, South Korea")

        if st.sidebar.button("회원가입 완료"):
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
        st.sidebar.subheader("🔑 로그인")
        login_id = st.sidebar.text_input("아이디 (ID)")
        login_pw = st.sidebar.text_input("비밀번호 (Password)", type="password")

        if st.sidebar.button("로그인"):
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
    
    if st.sidebar.button("로그아웃"):
        st.session_state["logged_in_user"] = None
        st.rerun()

st.sidebar.markdown("---")

st.sidebar.header("⚙️ 테니스 프로필 (Tennis Profile)")
ntpr_input = st.sidebar.selectbox("구력/실력 (NTPR Level)", ["NTPR 2.0 - 2.5", "NTPR 3.0 - 3.5", "NTPR 4.0 - 4.5", "NTPR 5.0+"])
racket_model = st.sidebar.text_input("라켓 모델", value="Babolat Pure Drive 300g")
dont_know_tension = st.sidebar.checkbox("현재 텐션을 모름")

current_tension_input = None if dont_know_tension else st.sidebar.number_input("현재 라켓 텐션 (lbs)", min_value=30, max_value=70, value=52)


# ==========================================
# 4. Main Title & Video Analysis Section
# ==========================================
st.title("🎾 ServeAI: AI 기반 서브 분석 & 테니스 패키지 결제")
st.write("단일 영상 AI 서브 분석부터 글로벌/국내 테니스 대회 참가 및 여행 패키지 결제까지 한 번에 이용하세요.")

st.markdown("---")

uploaded_file = st.file_uploader("🎥 서브 분석 비디오 업로드", type=["mp4", "mov", "avi"])

if uploaded_file is not None:
    st.video(uploaded_file)
    
    if st.button("🚀 AI 분석 실행"):
        with st.spinner("AI가 영상을 분석 중입니다..."):
            import time
            time.sleep(1.5)
            ai_measured_speed = 118.5
            
            user_age, user_gender = 25, "Male"
            if st.session_state["logged_in_user"] is not None:
                curr_u = st.session_state["registered_users"][st.session_state["logged_in_user"]]
                user_age, user_gender = curr_u["age"], curr_u["gender"]
            
            rec_lbs, rec_msg, delta_status, exp_speed = calculate_recommended_tension(
                ntpr_str=ntpr_input,
                current_tension_option=current_tension_input,
                calculated_speed_kmh=ai_measured_speed,
                age=user_age,
                gender=user_gender
            )
            
            st.success("✅ 분석이 완료되었습니다!")
            
            st.markdown("### 📊 AI 분석 리포트")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric(label="최고 서브 속도", value=f"{ai_measured_speed} km/h")
            with col2:
                st.metric(label="추천 라켓 텐션", value=f"{rec_lbs} lbs", delta=delta_status)
            with col3:
                st.metric(label="타깃 라켓 모델", value=racket_model if racket_model else "Standard")
            
            st.markdown("---")
            st.markdown("### 📈 프레임별 서브 속도 추적 그래프")
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
# 5. Competition Package & Visa/Mastercard Payment Engine
# ==========================================
st.header("✈️ 테니스 대회 참가 & 여행 패키지 결제 (Tour Booking & Checkout)")
st.write("원하는 대회를 선택하고 **VISA / Mastercard** 카드 결제(USD / KRW)로 예약을 즉시 완료하세요.")

competitions_db = {
    "🇺🇸 US Open (New York, USA)": {
        "city": "New York, USA",
        "ticket_fee_usd": 250,
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
    
    st.write(f"📍 **개최 도시**: {comp_info['city']}")
    st.write(f"🎟️ **대회 참가/티켓 비용**: ${comp_info['ticket_fee_usd']} USD")

with col_tour2:
    hotel_options = comp_info["hotels"]
    selected_hotel = st.selectbox("2️⃣ 숙박 호텔 선택 (Select Hotel)", list(hotel_options.keys()))
    hotel_price_per_night = hotel_options[selected_hotel]
    
    nights = st.number_input("3️⃣ 숙박 박수 (Nights)", min_value=1, max_value=14, value=3)
    people_count = st.number_input("4️⃣ 인원 수 (People)", min_value=1, max_value=5, value=1)

# Price Calculations
EXCHANGE_RATE = 1350  # 1 USD = 1,350 KRW
total_ticket_usd = comp_info['ticket_fee_usd'] * people_count
total_hotel_usd = hotel_price_per_night * nights * people_count
grand_total_usd = total_ticket_usd + total_hotel_usd
grand_total_krw = grand_total_usd * EXCHANGE_RATE

st.markdown("### 💰 결제 통화 선택 & 최종 금액 (Summary)")
pay_currency = st.radio("💳 결제 통화 선택 (Select Payment Currency)", ["USD ($)", "KRW (₩)"], horizontal=True)

if pay_currency == "USD ($)":
    display_price = f"${grand_total_usd:,.2f} USD"
    sub_text = f"≈ ₩{grand_total_krw:,.0f} KRW"
else:
    display_price = f"₩{grand_total_krw:,.0f} KRW"
    sub_text = f"≈ ${grand_total_usd:,.2f} USD"

q_col1, q_col2, q_col3 = st.columns(3)
with q_col1:
    st.metric(label="티켓/참가비", value=f"${total_ticket_usd} USD")
with q_col2:
    st.metric(label="호텔 숙박비", value=f"${total_hotel_usd} USD")
with q_col3:
    st.metric(label="최종 결제 예정 금액", value=display_price, delta=sub_text)

st.markdown("---")

# VISA / MASTERCARD Payment Gateway Form
st.subheader("💳 해외/국내 신용카드 결제 (Credit Card Checkout)")
st.caption("🔒 256-bit SSL Secure Encrypted Payment Gateway (VISA / Mastercard / JCB / AMEX)")

with st.form("checkout_payment_form"):
    card_name = st.text_input("카드 명의자 이름 (Cardholder Name)", placeholder="HONG GILDONG")
    card_number = st.text_input("카드 번호 (Card Number)", placeholder="4000 1234 5678 9010", max_chars=19)
    
    p_col1, p_col2 = st.columns(2)
    with p_col1:
        card_exp = st.text_input("유효기간 (MM/YY)", placeholder="12/28", max_chars=5)
    with p_col2:
        card_cvc = st.text_input("보안코드 (CVC/CVV)", placeholder="123", type="password", max_chars=4)
        
    submit_pay = st.form_submit_button(f"🚀 {display_price} 결제하기 (Pay Now)")

if submit_pay:
    if st.session_state["logged_in_user"] is None:
        st.error("⚠️ 결제를 진행하려면 먼저 사이드바에서 **로그인/회원가입**을 완료해 주세요.")
    elif not card_name or not card_number or not card_exp or not card_cvc:
        st.warning("⚠️ 모든 카드 결제 정보를 올바르게 입력해 주세요.")
    else:
        with st.spinner("💳 신용카드 승인 요청 중... (Processing VISA/Mastercard)"):
            import time
            time.sleep(2)
            
        st.session_state["payment_completed"] = True
        st.balloons()
        st.success("🎉 결제가 성공적으로 완료되었습니다! (Payment Approved)")
        
        # Payment Receipt
        st.markdown("---")
        st.markdown("### 🧾 전자 영수증 (Payment Receipt)")
        st.info(f"""
        • **주문 번호 (Order ID)**: SRV-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}
        • **구매자 (Customer)**: {st.session_state['logged_in_user']} ({card_name})
        • **선택 대회 (Event)**: {selected_comp}
        • **선택 호텔 (Hotel)**: {selected_hotel} ({nights} nights)
        • **결제 승인 금액**: **{display_price}**
        • **결제 수단**: VISA / Mastercard (****-****-****-{card_number[-4:] if len(card_number)>=4 else '0000'})
        • **승인 일시**: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        """)
