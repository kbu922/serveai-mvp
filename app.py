import streamlit as st
import datetime
import time

# ==========================================
# 1. Page Configuration
# ==========================================
st.set_page_config(
    page_title="ServeAI - Global Tennis Portal",
    page_icon="🎾",
    layout="wide"
)

# Initialize Session State
if "users" not in st.session_state:
    st.session_state["users"] = {"admin@serveai.com": "password123"}
if "logged_in_user" not in st.session_state:
    st.session_state["logged_in_user"] = None
if "admin_logged_in" not in st.session_state:
    st.session_state["admin_logged_in"] = False

# Global Databases
if "inquiries" not in st.session_state:
    st.session_state["inquiries"] = [
        {
            "title": "Room-share matching for international players",
            "type": "Tournament & Accommodation",
            "content": "Will players of the same gender and similar NTRP be matched?",
            "user": "alex@globaltennis.com",
            "time": "2026-07-28 14:20",
            "reply": "Yes! Same gender and similar NTRP levels are automatically paired."
        }
    ]

if "match_orders" not in st.session_state:
    st.session_state["match_orders"] = []

if "investment_inquiries" not in st.session_state:
    st.session_state["investment_inquiries"] = []

# ==========================================
# 2. Sidebar: Language Switcher & Authentication
# ==========================================
st.sidebar.title("🎾 ServeAI Global")

# Language Switcher
lang = st.sidebar.selectbox("🌐 Language / 언어", ["English", "한국어"])

st.sidebar.markdown("---")

# Dictionary for Multi-language UI Strings
t = {
    "English": {
        "nav_title": "📌 Navigation",
        "nav_1": "⚡ AI Serve Speed Analysis",
        "nav_2": "🎾 AI Tennis Gear Recommender",
        "nav_3": "🏆 Tournaments & Accommodation",
        "nav_4": "🏢 Tennis Real Estate & Investment",
        "nav_5": "💬 Support & Inquiries",
        "nav_6": "🔒 Admin Dashboard",
        "login_sub": "👤 User Account",
        "login_tab": "Login",
        "reg_tab": "Register",
        "email_lbl": "Email Address",
        "pw_lbl": "Password",
        "btn_login": "Login",
        "btn_logout": "Logout",
        "welcome": "Welcome",
        "err_login": "Invalid email or password.",
        "reg_success": "Registration complete! Please log in.",
        "speed_title": "⚡ AI Computer Vision Serve Speed Analysis",
        "speed_desc": "Upload a serve video to analyze trajectory, impact height, and peak speed (km/h).",
        "upload_lbl": "Upload Serve Video (MP4, MOV)",
        "btn_analyze": "🚀 Run AI Analysis",
        "speed_peak": "Peak Speed",
        "speed_height": "Impact Height",
        "speed_rpm": "Spin Rate",
        "tourney_title": "🏆 Global Tennis Tournaments & Booking",
        "tourney_desc": "Browse international and domestic tournaments, register, and book player room-share packages.",
        "back_btn": "⬅️ Back to List",
        "player_info": "1️⃣ Player Information",
        "name_lbl": "Full Name",
        "phone_lbl": "Phone Number",
        "pkg_lbl": "Select Package",
        "pay_sec": "2️⃣ Online Checkout",
        "total_pay": "Total Amount",
        "card_lbl": "Credit Card Number",
        "btn_pay": "🚀 Pay & Register Now",
        "pay_ok": "🎉 Registration & Payment Successful! Recorded in admin database.",
        "estate_title": "🏢 Global Tennis Real Estate & Overseas Academy Investments",
        "estate_desc": "Discover court leases, facility acquisitions, and international tennis academy equity shares.",
        "inq_title": "💬 Customer Support & Inquiries",
        "admin_title": "🔒 Admin Dashboard",
    },
    "한국어": {
        "nav_title": "📌 메뉴 선택",
        "nav_1": "⚡ AI 서브 속도 분석",
        "nav_2": "🎾 AI 테니스 용구 추천",
        "nav_3": "🏆 테니스 대회 & 숙박 예약",
        "nav_4": "🏢 테니스 부동산 & 해외 투자",
        "nav_5": "💬 고객 지원 & 문의",
        "nav_6": "🔒 백엔드 관리자 대시보드",
        "login_sub": "👤 회원 계정",
        "login_tab": "로그인",
        "reg_tab": "회원가입",
        "email_lbl": "이메일 주소",
        "pw_lbl": "비밀번호",
        "btn_login": "로그인",
        "btn_logout": "로그아웃",
        "welcome": "환영합니다",
        "err_login": "이메일 또는 비밀번호가 올바르지 않습니다.",
        "reg_success": "가입 완료! 로그인해 주세요.",
        "speed_title": "⚡ AI 컴퓨터 비전 서브 속도 분석",
        "speed_desc": "서브 동영상을 업로드하면 AI가 최고 속도(km/h)와 궤적을 분석합니다.",
        "upload_lbl": "서브 분석용 영상 업로드 (MP4, MOV)",
        "btn_analyze": "🚀 AI 속도 분석 시작",
        "speed_peak": "최고 속도",
        "speed_height": "임팩트 타점 높이",
        "speed_rpm": "볼 회전수",
        "tourney_title": "🏆 국내외 테니스 대회 & 숙박 예약 포털",
        "tourney_desc": "해외 원정 및 국내 대회 참가 신청과 선수 전용 룸셰어 패키지 결제 서비스를 제공합니다.",
        "back_btn": "⬅️ 전체 목록으로 돌아가기",
        "player_info": "1️⃣ 참가자 정보 입력",
        "name_lbl": "선수 성명",
        "phone_lbl": "연락처",
        "pkg_lbl": "신청 상품 선택",
        "pay_sec": "2️⃣ 온라인 결제",
        "total_pay": "최종 결제 금액",
        "card_lbl": "신용카드 번호",
        "btn_pay": "🚀 결제 및 참가 신청",
        "pay_ok": "🎉 결제 완료! 관리자 대시보드에 정상 등록되었습니다.",
        "estate_title": "🏢 테니스 부동산 & 해외 아카데미 지분 투자",
        "estate_desc": "국내외 테니스장 매매, 임대 및 글로벌 프랜차이즈 지분 투자 기회를 확인하세요.",
        "inq_title": "💬 고객 센터 & 1:1 문의",
        "admin_title": "🔒 백엔드 관리자 대시보드",
    }
}[lang]

# Login Section
if st.session_state["logged_in_user"] is None:
    st.sidebar.subheader(t["login_sub"])
    auth_mode = st.sidebar.radio("Action", [t["login_tab"], t["reg_tab"]], horizontal=True)
    
    if auth_mode == t["login_tab"]:
        email_in = st.sidebar.text_input(t["email_lbl"])
        pw_in = st.sidebar.text_input(t["pw_lbl"], type="password")
        if st.sidebar.button(t["btn_login"]):
            if email_in in st.session_state["users"] and st.session_state["users"][email_in] == pw_in:
                st.session_state["logged_in_user"] = email_in
                st.sidebar.success(f"{t['welcome']}, {email_in}!")
                st.rerun()
            else:
                st.sidebar.error(t["err_login"])
    else:
        reg_email = st.sidebar.text_input(f"New {t['email_lbl']}")
        reg_pw = st.sidebar.text_input(f"New {t['pw_lbl']}", type="password")
        if st.sidebar.button(t["reg_tab"]):
            if reg_email and reg_pw:
                st.session_state["users"][reg_email] = reg_pw
                st.sidebar.success(t["reg_success"])
            else:
                st.sidebar.warning("Fill in all fields.")
else:
    st.sidebar.success(f"🟢 **{st.session_state['logged_in_user']}**")
    if st.sidebar.button(t["btn_logout"]):
        st.session_state["logged_in_user"] = None
        st.rerun()

st.sidebar.markdown("---")

# Dynamic Navigation Options
nav_options = [
    t["nav_1"],
    t["nav_2"],
    t["nav_3"],
    t["nav_4"],
    t["nav_5"],
    t["nav_6"]
]

page_selection = st.sidebar.radio(t["nav_title"], nav_options)

# Localized Tournament Product Database
tournament_products = {
    "match1": {
        "season": "2026 Season #1",
        "title_en": "2026 Seoul International Amateur Tennis Open",
        "title_kr": "2026 서울 국제 아마추어 테니스 오픈",
        "date_en": "August 15, 2026 - August 16, 2026",
        "date_kr": "2026년 8월 15일 ~ 8월 16일",
        "location_en": "Seoul Olympic Park Tennis Center",
        "location_kr": "서울 올림픽공원 테니스장",
        "desc_en": "Includes entry qualification, live AI speed tracking, and foreign athlete hotel room-sharing.",
        "desc_kr": "대회 참가 자격, 현장 AI 서브 측정 및 외국인/원정 선수 전용 호텔 룸셰어 제공.",
        "price_single": "$45 USD (₩60,000)",
        "price_pkg": "$160 USD (₩210,000)",
        "badge": "🟢 OPEN"
    },
    "match2": {
        "season": "2026 Season #2",
        "title_en": "2026 Tokyo-Jeju Global Amateur Exchange Cup",
        "title_kr": "2026 도쿄-제주 글로벌 아마추어 교류전",
        "date_en": "September 12, 2026 - September 13, 2026",
        "date_kr": "2026년 9월 12일 ~ 9월 13일",
        "location_en": "Jeju Seogwipo International Tennis Court",
        "location_kr": "제주 서귀포 국제 테니스장",
        "desc_en": "Jeju away tournament! Entry fee, ocean-view hotel room share, and ServeAI analysis included.",
        "desc_kr": "제주 원정 테니스 대회! 참가비, 오션뷰 호텔 2인 룸셰어 숙박 및 ServeAI 진단 서비스 포함.",
        "price_single": "$50 USD (₩68,000)",
        "price_pkg": "$210 USD (₩280,000)",
        "badge": "🟢 OPEN"
    }
}

query_params = st.query_params
selected_tournament = query_params.get("item", None)

# ==========================================
# 3. Feature 1: AI Speed Analysis
# ==========================================
if page_selection == t["nav_1"]:
    st.title(t["speed_title"])
    st.write(t["speed_desc"])
    
    uploaded_file = st.file_uploader(t["upload_lbl"], type=["mp4", "mov", "avi"])
    
    if uploaded_file is not None:
        st.video(uploaded_file)
        if st.button(t["btn_analyze"]):
            with st.spinner("🔍 Tracking trajectory & speed..."):
                time.sleep(1.5)
            
            st.balloons()
            st.success("Complete!")
            
            col1, col2, col3 = st.columns(3)
            col1.metric(t["speed_peak"], "184 km/h", "+12 km/h")
            col2.metric(t["speed_height"], "2.78 m", "Optimal")
            col3.metric(t["speed_rpm"], "2,450 RPM", "Good Spin")

            st.line_chart([20, 60, 110, 155, 184, 160, 120, 40])

# ==========================================
# 4. Feature 3: Tournament & Booking Sub-Page
# ==========================================
elif page_selection == t["nav_3"]:
    if selected_tournament in tournament_products:
        item = tournament_products[selected_tournament]
        if st.button(t["back_btn"]):
            st.query_params.clear()
            st.rerun()

        title_curr = item["title_en"] if lang == "English" else item["title_kr"]
        date_curr = item["date_en"] if lang == "English" else item["date_kr"]
        loc_curr = item["location_en"] if lang == "English" else item["location_kr"]
        desc_curr = item["desc_en"] if lang == "English" else item["desc_kr"]

        st.markdown(f"## 🏆 {item['season']}: {title_curr}")
        st.info(f"📅 **Date**: {date_curr} | 📍 **Location**: {loc_curr}")
        st.write(desc_curr)
        
        col_info, col_pay = st.columns([1, 1])
        with col_info:
            st.subheader(t["player_info"])
            p_name = st.text_input(t["name_lbl"])
            p_phone = st.text_input(t["phone_lbl"])
            pkg_opt = st.radio(t["pkg_lbl"], ["Entry Only Pass", "Entry + Hotel Room-Share Package"])

        with col_pay:
            st.subheader(t["pay_sec"])
            amt = item["price_single"] if "Only" in pkg_opt else item["price_pkg"]
            st.metric(t["total_pay"], amt)

            with st.form("pay_form"):
                card_num = st.text_input(t["card_lbl"])
                submit_pay = st.form_submit_button(t["btn_pay"])

            if submit_pay:
                if p_name and p_phone and card_num:
                    new_ord_id = f"ORD-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
                    st.session_state["match_orders"].append({
                        "order_id": new_ord_id,
                        "event": title_curr,
                        "name": p_name,
                        "phone": p_phone,
                        "package": pkg_opt,
                        "amount": amt,
                        "card": card_num,
                        "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                    })
                    st.balloons()
                    st.success(t["pay_ok"])
                else:
                    st.error("Please fill in all required fields.")
    else:
        st.title(t["tourney_title"])
        st.write(t["tourney_desc"])
        st.markdown("---")

        for key, item in tournament_products.items():
            title_curr = item["title_en"] if lang == "English" else item["title_kr"]
            date_curr = item["date_en"] if lang == "English" else item["date_kr"]
            loc_curr = item["location_en"] if lang == "English" else item["location_kr"]
            desc_curr = item["desc_en"] if lang == "English" else item["desc_kr"]

            with st.container(border=True):
                c_left, c_right = st.columns([3, 1])
                with c_left:
                    st.subheader(f"{item['season']}: {title_curr}")
                    st.write(f"📅 {date_curr} | 📍 {loc_curr}")
                    st.caption(desc_curr)
                with c_right:
                    if st.button(f"👉 Select {item['season']}", key=f"tourn_{key}"):
                        st.query_params["item"] = key
                        st.rerun()

# ==========================================
# 5. Feature 6: Admin Dashboard
# ==========================================
elif page_selection == t["nav_6"]:
    st.title(t["admin_title"])

    if not st.session_state["admin_logged_in"]:
        with st.form("admin_login"):
            admin_id = st.text_input("Admin ID", placeholder="admin")
            admin_pw = st.text_input("Password", type="password", placeholder="admin")
            if st.form_submit_button("Login to Dashboard"):
                if admin_id == "admin" and admin_pw == "admin":
                    st.session_state["admin_logged_in"] = True
                    st.rerun()
                else:
                    st.error("Invalid credentials (admin/admin)")
    else:
        st.success("🟢 Authenticated as Admin")
        if st.button("Logout Admin"):
            st.session_state["admin_logged_in"] = False
            st.rerun()

        st.markdown("---")
        st.subheader("💳 Registered Orders Database")
        st.dataframe(st.session_state["match_orders"], use_container_width=True)
        
        st.subheader("📩 Messages & Support Requests")
        st.dataframe(st.session_state["inquiries"], use_container_width=True)

# Placeholder fallback for remaining nav items
else:
    st.title(page_selection)
    st.info("Feature active. Selected language: " + lang)
