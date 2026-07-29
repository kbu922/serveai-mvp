import streamlit as st
import datetime
import time

# ==========================================
# 1. Page Configuration & Global Styling
# ==========================================
st.set_page_config(
    page_title="ServeAI - Global Tennis & Sports-Tech Portal",
    page_icon="🎾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for polished layout
st.markdown("""
<style>
    .stMetric {
        background-color: #f8f9fa;
        padding: 12px;
        border-radius: 8px;
        border-left: 4px solid #007bff;
    }
    .stButton>button {
        border-radius: 6px;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. State Management Initialization
# ==========================================
if "users" not in st.session_state:
    st.session_state["users"] = {"admin@serveai.com": "password123", "alex@globaltennis.com": "tennis123"}

if "logged_in_user" not in st.session_state:
    st.session_state["logged_in_user"] = None

if "admin_logged_in" not in st.session_state:
    st.session_state["admin_logged_in"] = False

# Membership Database ($4.99/month Pass Model)
if "memberships" not in st.session_state:
    st.session_state["memberships"] = {
        "alex@globaltennis.com": {
            "status": "Active",
            "plan": "1-Month VIP Pass ($4.99/mo)",
            "expires": "2026-08-29"
        }
    }

# Community Databases
if "players_db" not in st.session_state:
    st.session_state["players_db"] = [
        {"id": "P-101", "name": "Jessica Chen", "ntrp": 3.5, "gender": "Female", "location": "Gangnam Center, Seoul", "bio": "Looking for consistent rally partners on weekends! Topspin baseline player.", "avatar": "👩‍🎾"},
        {"id": "P-102", "name": "Min-woo Park", "ntrp": 3.5, "gender": "Male", "location": "Gangnam Center, Seoul", "bio": "Aggressive serve & volleyer. Available weekday evenings.", "avatar": "👨‍🎾"},
        {"id": "P-103", "name": "Elena Rostova", "ntrp": 4.0, "gender": "Female", "location": "Jeju Ocean Resort", "bio": "Advanced player preparing for local tournaments. Prefers singles.", "avatar": "👩‍🎾"},
        {"id": "P-104", "name": "Kenji Sato", "ntrp": 3.0, "gender": "Male", "location": "Songdo Park, Incheon", "bio": "Intermediate player working on backhand consistency. Friendly games!", "avatar": "👨‍🎾"},
        {"id": "P-105", "name": "Sophia Lee", "ntrp": 4.0, "gender": "Female", "location": "Gangnam Center, Seoul", "bio": "Ex-college club player, great rallies and match play.", "avatar": "👩‍🎾"}
    ]

if "coaches_db" not in st.session_state:
    st.session_state["coaches_db"] = [
        {"id": "C-201", "name": "Coach Daniel Kim", "cert": "USPTA Elite Certified", "exp": "8 Years Pro Coaching", "rate": "$45 / hr", "location": "Gangnam Center, Seoul", "bio": "Specializes in serve biomechanics, AI trajectory fixes, and match strategy."},
        {"id": "C-202", "name": "Coach Hannah Choi", "cert": "KTA Certified Senior Coach", "exp": "12 Years Experience", "rate": "$50 / hr", "location": "Jeju Ocean Resort", "bio": "Former national junior coach. Slice, drop shots, and tactical movement."},
        {"id": "C-203", "name": "Coach Alex Rivera", "cert": "PTR Master Professional", "exp": "10 Years Experience", "rate": "$40 / hr", "location": "Songdo Park, Incheon", "bio": "Focuses on footwork, racket head speed, and beginner-to-advanced progression."}
    ]

if "chat_orders" not in st.session_state:
    st.session_state["chat_orders"] = [
        {
            "order_id": "MSG-20260729-01",
            "sender": "alex@globaltennis.com",
            "recipient": "Jessica Chen (NTRP 3.5)",
            "message": "Hi Jessica! Want to hit at Gangnam court this Saturday at 10 AM?",
            "time": "2026-07-29 14:10"
        }
    ]

if "inquiries" not in st.session_state:
    st.session_state["inquiries"] = [
        {"id": "TK-101", "user": "alex@globaltennis.com", "subject": "Court Booking Issue", "status": "Open", "date": "2026-07-28"}
    ]

# ==========================================
# 3. Sidebar Authentication & Dictionary Translation
# ==========================================
st.sidebar.title("🎾 ServeAI Global")
lang = st.sidebar.selectbox("🌐 Language / 언어", ["English", "한국어"])
st.sidebar.markdown("---")

t = {
    "English": {
        # Nav
        "nav_title": "📌 Navigation",
        "nav_1": "⚡ AI Serve Speed Analysis",
        "nav_2": "🎾 AI Racket & Tension Calculator",
        "nav_3": "🏆 Tournaments & Accommodation Subpage",
        "nav_4": "🏫 Tennis School Service & Training Packages",
        "nav_5": "🤝 NTRP Match & VIP Chat Pass",
        "nav_6": "💬 Support & Inquiries",
        "nav_7": "🔒 Admin / Backend Dashboard",
        # Auth
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
        "vip_active": "⭐ VIP Pass Active (Unlimited Chat)",
        "basic_acct": "⚪ Basic Account (Chat Locked)",
        # Feature 1: Serve AI
        "f1_title": "⚡ AI Serve Speed & Trajectory Analyzer",
        "f1_desc": "Upload a video of your serve. AI will detect ball motion frames and calculate real velocity in MPH and KM/H.",
        "f1_up_lbl": "Upload Serve Video (MP4 / MOV)",
        "f1_cam_lbl": "Camera Angle",
        "f1_fps_lbl": "Recorded FPS",
        "f1_btn": "🚀 Analyze Serve Velocity",
        "f1_analyzing": "Processing ball movement trajectories...",
        "f1_success": "Analysis Complete!",
        "f1_peak": "Peak Speed",
        "f1_metric": "Metric Velocity",
        "f1_spin": "Spin Rate",
        "f1_bio_title": "📊 Biomechanics Feedback",
        "f1_bio_tip": "💡 AI Tip: Racket head acceleration peak was reached 0.08s before impact. Toss height was optimal at 3.2m.",
        "f1_warn": "Please upload a video file first to analyze.",
        # Feature 2: Tension Calc
        "f2_title": "🎾 AI Tennis NTRP & Tension Calculator",
        "f2_desc": "Calculates your optimal string tension (lbs) based on your NTRP level and AI serve speed.",
        "f2_ntrp": "Select your NTRP Level",
        "f2_speed": "Your Average Serve Speed (MPH)",
        "f2_style": "Playing Style",
        "f2_head": "Racket Head Size (sq in)",
        "f2_string": "String Material",
        "f2_btn": "🧮 Calculate Optimal Tension & Setup",
        "f2_res_title": "🎯 Recommended Equipment Specifications",
        "f2_main_ten": "Recommended Main Tension",
        "f2_cross_ten": "Recommended Cross Tension",
        "f2_grip": "Grip Size",
        "f2_msg": "Based on your NTRP {ntrp} level and {speed} MPH serve, a {string} at {tension} lbs will provide maximum precision and control.",
        # Feature 3: Tournaments
        "f3_title": "🏆 Tournaments & Official Match Accommodation",
        "f3_desc": "Browse upcoming amateur and pro-am tournaments. Book official hotel packages with integrated transport.",
        "f3_date": "Date",
        "f3_loc": "Location",
        "f3_prize": "Prize Pool",
        "f3_hotel": "Partner Hotel",
        "f3_btn": "🎟️ Register & Book Package",
        "f3_success": "Entry request initiated! Ticket created in Support tab for booking receipt.",
        # Feature 4: School
        "f4_title": "🏫 Global Tennis Academy & Residency Programs",
        "f4_desc": "Long-term high-performance training packages including accommodation, court access, and video analytics.",
        "f4_w1_title": "🥉 1-Week Intensive Boot Camp",
        "f4_w1_f1": "• 15 Hours Private Coaching",
        "f4_w1_f2": "• Unlimited Ball Machine Access",
        "f4_w1_f3": "• AI Serve Biomechanics Report",
        "f4_w1_f4": "• Hotel Accommodation Included",
        "f4_w1_price": "### $890 / Week",
        "f4_w1_btn": "Enroll in 1-Week Camp",
        "f4_m1_title": "🥇 1-Month Pro Residency Package",
        "f4_m1_f1": "• 50 Hours Private & Group Coaching",
        "f4_m1_f2": "• Daily Tournament Sparring Matches",
        "f4_m1_f3": "• Full Physical Conditioning & Diet Plan",
        "f4_m1_f4": "• Serviced Apartment Residence Included",
        "f4_m1_price": "### $2,950 / Month",
        "f4_m1_btn": "Enroll in 1-Month Residency",
        "f4_res_success": "Residency application submitted! Added to Support Center.",
        # Feature 5: Matching & Pass
        "f5_title": "🤝 Community NTRP Matching & Unlimited VIP Chat Pass",
        "f5_desc": "Subscribe for $4.99/month to get unlimited free direct messaging with local coaches and NTRP hitting partners!",
        "f5_active_banner": "🌟 VIP Pass Active | Expires: {expires} | Unlimited Free Direct Chat Unlocked!",
        "f5_pass_expand": "💳 Get 1-Month VIP Chat Pass ($4.99 / Month) - Click Here to Unlock All Chats",
        "f5_pass_sub": "Unlimited direct chats with all local tennis players & coaches for 30 days!",
        "f5_email_lbl": "Account Email",
        "f5_card_lbl": "Card Number",
        "f5_plan_lbl": "Plan: 1-Month VIP Membership",
        "f5_price_lbl": "Price: $4.99 USD / month",
        "f5_btn_pay": "🚀 Pay $4.99 & Activate Pass",
        "f5_pay_success": "🎉 Membership activated! You can now chat with all players and coaches for free.",
        "f5_pay_err": "Please enter email and card details.",
        "f5_tab1": "🎾 Find Nearby NTRP Players",
        "f5_tab2": "👨‍🏫 Connect with Verified Coaches",
        "f5_tab3": "📝 Coach Registration Portal",
        "f5_loc_filter": "Location Filter",
        "f5_ntrp_filter": "Your NTRP Level Filter",
        "f5_free_chat": "✅ Free Chat (VIP Active)",
        "f5_req_vip": "🔒 Requires VIP Pass",
        "f5_sub_note": "Subscribe above for $4.99/mo",
        "f5_chat_btn": "💬 Chat Now",
        "f5_dm_to": "💬 Direct Message to",
        "f5_msg_ph": "Hi {name}, let's set up a time to play at {loc}!",
        "f5_send_btn": "✉️ Send Message",
        "f5_sent_msg": "Message sent to {name}!",
        "f5_coach_btn": "💬 Contact Coach",
        "f5_coach_ph": "Hi Coach, what are your available lesson times this week?",
        "f5_coach_sent": "Message delivered to {name}!",
        "f5_reg_title": "📝 Register as an Experienced Tennis Teacher",
        "f5_reg_name": "Full Name",
        "f5_reg_cert": "Certification",
        "f5_reg_loc": "Primary Location",
        "f5_reg_rate": "Lesson Rate",
        "f5_reg_bio": "Bio & Philosophy",
        "f5_reg_btn": "🚀 Submit Coach Profile",
        "f5_reg_ok": "Profile submitted and listed!",
        # Feature 6: Support
        "f6_title": "💬 Customer Support & Ticket Center",
        "f6_desc": "Submit your questions regarding membership or app features.",
        "f6_form_title": "📩 Submit a New Ticket",
        "f6_email": "Your Email",
        "f6_subj": "Subject",
        "f6_body": "Details",
        "f6_btn": "Submit Support Ticket",
        "f6_success": "Ticket submitted! Reference ID: ",
        "f6_err": "Please fill in email and subject.",
        "f6_list_title": "📋 Your Submitted Tickets",
        "f6_no_tickets": "No submitted tickets yet.",
        # Feature 7: Admin
        "f7_title": "🔒 Admin Backend Dashboard",
        "f7_auth": "Admin Verification",
        "f7_btn_login": "Login as Admin",
        "f7_btn_logout": "🔒 Logout Admin",
        "f7_tab1": "💳 Active VIP Memberships",
        "f7_tab2": "💬 Delivered Messages",
        "f7_tab3": "📩 Support Tickets"
    },
    "한국어": {
        # Nav
        "nav_title": "📌 메뉴 선택",
        "nav_1": "⚡ AI 서브 속도 분석",
        "nav_2": "🎾 AI 라켓 & 텐션 추천 계산기",
        "nav_3": "🏆 테니스 대회 & 숙박 서브페이지",
        "nav_4": "🏫 글로벌 테니스 스쿨 서비스 & 장기 레지던시",
        "nav_5": "🤝 NTRP 파트너 매칭 & VIP 무제한 채팅",
        "nav_6": "💬 고객 지원 & 문의",
        "nav_7": "🔒 백엔드 관리자 대시보드",
        # Auth
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
        "vip_active": "⭐ VIP 패스 활성화 (무제한 채팅 가능)",
        "basic_acct": "⚪ 일반 계정 (채팅 잠김)",
        # Feature 1: Serve AI
        "f1_title": "⚡ AI 서브 속도 및 궤적 분석기",
        "f1_desc": "서브 동영상을 업로드하세요. AI가 공의 움직임을 감지하여 MPH 및 KM/H 단위로 실제 속도를 계산합니다.",
        "f1_up_lbl": "서브 비디오 업로드 (MP4 / MOV)",
        "f1_cam_lbl": "카메라 촬영 각도",
        "f1_fps_lbl": "녹화 프레임 (FPS)",
        "f1_btn": "🚀 서브 속도 측정 시작",
        "f1_analyzing": "볼 궤적 및 속도 프레임 분석 중...",
        "f1_success": "분석 완료!",
        "f1_peak": "최고 속도",
        "f1_metric": "미터법 속도",
        "f1_spin": "회전수 (Spin Rate)",
        "f1_bio_title": "📊 바이오매카닉 피드백",
        "f1_bio_tip": "💡 AI 팁: 임팩트 0.08초 전에 라켓 헤드 가속도가 최대치에 도달했습니다. 토스 높이는 3.2m로 최적이었습니다.",
        "f1_warn": "먼저 분석할 비디오 파일을 업로드해 주세요.",
        # Feature 2: Tension Calc
        "f2_title": "🎾 AI 테니스 NTRP / 최적 텐션 계산기",
        "f2_desc": "NTRP 레벨과 AI 측정 서브 속도를 바탕으로 최적의 텐션을 정밀 계산합니다.",
        "f2_ntrp": "NTRP 레벨 선택",
        "f2_speed": "평균 서브 속도 (MPH)",
        "f2_style": "플레이 스타일",
        "f2_head": "라켓 헤드 사이즈 (sq in)",
        "f2_string": "스트링 종류",
        "f2_btn": "🧮 최적 텐션 및 스펙 계산하기",
        "f2_res_title": "🎯 추천 장비 세팅 사양",
        "f2_main_ten": "추천 메인(가로) 텐션",
        "f2_cross_ten": "추천 크로스(세로) 텐션",
        "f2_grip": "그립 사이즈",
        "f2_msg": "회원님의 NTRP {ntrp} 레벨과 {speed} MPH 서브 속도를 고려할 때, {string} 스트링을 {tension} lbs로 매매하는 것이 최고의 컨트롤을 제공합니다.",
        # Feature 3: Tournaments
        "f3_title": "🏆 테니스 대회 & 공식 숙박 예약 서브페이지",
        "f3_desc": "다가오는 아마추어 및 프로아마 대회를 확인하고 공식 제휴 호텔 및 교통 패키지를 예약하세요.",
        "f3_date": "일정",
        "f3_loc": "장소",
        "f3_prize": "총 상금",
        "f3_hotel": "제휴 호텔",
        "f3_btn": "🎟️ 대회 참가 및 패키지 신청",
        "f3_success": "참가 신청이 완료되었습니다! [고객 지원] 탭에서 예약 영수증 접수 내역을 확인하실 수 있습니다.",
        # Feature 4: School
        "f4_title": "🏫 글로벌 테니스 스쿨 서비스 & 장기 레지던시",
        "f4_desc": "숙박, 코트 이용, 비디오 분석이 포함된 장기 집중 훈련 패키지입니다.",
        "f4_w1_title": "🥉 1주일 집중 부트캠프",
        "f4_w1_f1": "• 15시간 개인 코칭",
        "f4_w1_f2": "• 볼머신기 무제한 이용",
        "f4_w1_f3": "• AI 서브 생체역학 리포트",
        "f4_w1_f4": "• 호텔 숙박 포함",
        "f4_w1_price": "### 주당 $890 (약 115만원)",
        "f4_w1_btn": "1주 캠프 신청하기",
        "f4_m1_title": "🥇 1개월 프로 레지던시 패키지",
        "f4_m1_f1": "• 50시간 개인 & 그룹 코칭",
        "f4_m1_f2": "• 매일 대회 실전 스파링 매치",
        "f4_m1_f3": "• 피지컬 트레이닝 및 식이요법",
        "f4_m1_f4": "• 레지던스 레지던스 레지던트 제공",
        "f4_m1_price": "### 월 $2,950 (약 380만원)",
        "f4_m1_btn": "1개월 레지던시 신청하기",
        "f4_res_success": "레지던시 신청이 접수되었습니다! [고객 지원] 센터 문의로 추가되었습니다.",
        # Feature 5: Matching & Pass
        "f5_title": "🤝 커뮤니티 NTRP 매칭 & 1개월 무제한 VIP 멤버십",
        "f5_desc": "월 $4.99(약 6,500원) 멤버십 구독 시, 주변 모든 NTRP 파트너 및 검증 코치와 무제한 무료 대화가 가능합니다!",
        "f5_active_banner": "🌟 VIP 패스 활성화됨 | 만료일: {expires} | 무제한 1:1 무료 대화 가능!",
        "f5_pass_expand": "💳 1개월 VIP 채팅 패스 ($4.99 / 월) - 여기를 클릭하여 모든 채팅 열기",
        "f5_pass_sub": "30일 동안 주변 테니스 플레이어 및 코치와 무제한으로 1:1 대화를 나누세요!",
        "f5_email_lbl": "계정 이메일",
        "f5_card_lbl": "카드 번호",
        "f5_plan_lbl": "플랜: 1개월 VIP 멤버십",
        "f5_price_lbl": "가격: 월 $4.99 USD",
        "f5_btn_pay": "🚀 $4.99 결제하고 VIP 패스 활성화",
        "f5_pay_success": "🎉 멤버십이 활성화되었습니다! 이제 모든 플레이어 및 코치와 무료로 메시지를 주고받을 수 있습니다.",
        "f5_pay_err": "이메일과 카드 정보를 입력해 주세요.",
        "f5_tab1": "🎾 주변 NTRP 플레이어 찾기",
        "f5_tab2": "👨‍🏫 검증된 전문 코치 연결",
        "f5_tab3": "📝 전문 코치 프로필 등록",
        "f5_loc_filter": "지역 필터",
        "f5_ntrp_filter": "내 NTRP 레벨 필터",
        "f5_free_chat": "✅ 무료 대화 가능 (VIP 패스)",
        "f5_req_vip": "🔒 VIP 패스 필요",
        "f5_sub_note": "위에서 월 $4.99 구독",
        "f5_chat_btn": "💬 대화하기",
        "f5_dm_to": "💬 다음 사용자에게 메시지 보내기:",
        "f5_msg_ph": "안녕하세요 {name}님, {loc}에서 이번주에 같이 테니스 치실래요?",
        "f5_send_btn": "✉️ 메시지 전송",
        "f5_sent_msg": "{name}님에게 메시지가 성공적으로 전송되었습니다!",
        "f5_coach_btn": "💬 코치 문의하기",
        "f5_coach_ph": "코치님 안녕하세요, 이번 주 레슨 가능하신 시간이 궁금합니다.",
        "f5_coach_sent": "{name} 코치님에게 문의가 전송되었습니다!",
        "f5_reg_title": "📝 테니스 코치/지도자 프로필 등록",
        "f5_reg_name": "성함",
        "f5_reg_cert": "자격증 및 경력",
        "f5_reg_loc": "주요 레슨 지역",
        "f5_reg_rate": "레슨비",
        "f5_reg_bio": "자기소개 및 지도 철학",
        "f5_reg_btn": "🚀 코치 프로필 등록하기",
        "f5_reg_ok": "프로필 등록이 완료되어 목록에 게시되었습니다!",
        # Feature 6: Support
        "f6_title": "💬 고객 지원 & 1:1 문의하기",
        "f6_desc": "멤버십 및 서비스 관련 궁금하신 점을 문의해 주세요.",
        "f6_form_title": "📩 새 문의 티켓 제출",
        "f6_email": "이메일 주소",
        "f6_subj": "제목",
        "f6_body": "문의 내용",
        "f6_btn": "문의 티켓 제출",
        "f6_success": "문의가 성공적으로 접수되었습니다! 티켓 번호: ",
        "f6_err": "이메일과 제목을 입력해 주세요.",
        "f6_list_title": "📋 내 문의 및 대회/캠프 예약 내역",
        "f6_no_tickets": "접수된 문의 내역이 없습니다.",
        # Feature 7: Admin
        "f7_title": "🔒 백엔드 관리자 대시보드",
        "f7_auth": "관리자 인증",
        "f7_btn_login": "관리자로 로그인",
        "f7_btn_logout": "🔒 관리자 로그아웃",
        "f7_tab1": "💳 활성 VIP 멤버십 목록",
        "f7_tab2": "💬 전송된 대화 내역",
        "f7_tab3": "📩 고객 지원 접수 티켓"
    }
}[lang]

# Authentication UI Block
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
    user_mem = st.session_state["memberships"].get(st.session_state["logged_in_user"], None)
    if user_mem and user_mem["status"] == "Active":
        st.sidebar.caption(t["vip_active"])
    else:
        st.sidebar.caption(t["basic_acct"])

    if st.sidebar.button(t["btn_logout"]):
        st.session_state["logged_in_user"] = None
        st.rerun()

st.sidebar.markdown("---")

nav_options = [
    t["nav_1"],
    t["nav_2"],
    t["nav_3"],
    t["nav_4"],
    t["nav_5"],
    t["nav_6"],
    t["nav_7"]
]
page_selection = st.sidebar.radio(t["nav_title"], nav_options)

# ==========================================
# 4. Feature 1: AI Serve Speed Analysis
# ==========================================
if page_selection == t["nav_1"]:
    st.title(t["f1_title"])
    st.write(t["f1_desc"])
    
    col_up, col_res = st.columns([1, 1])
    with col_up:
        uploaded_video = st.file_uploader(t["f1_up_lbl"], type=["mp4", "mov", "avi"])
        camera_angle = st.selectbox(t["f1_cam_lbl"], ["Behind Baseline (Recommended)", "Side Court View", "45-Degree Angle"])
        frame_rate = st.select_slider(t["f1_fps_lbl"], options=[30, 60, 120, 240], value=60)
        
        btn_analyze = st.button(t["f1_btn"], use_container_width=True)

    with col_res:
        if btn_analyze:
            if uploaded_video is not None:
                with st.spinner(t["f1_analyzing"]):
                    time.sleep(1.2)
                
                st.success(t["f1_success"])
                m1, m2, m3 = st.columns(3)
                m1.metric(t["f1_peak"], "104 MPH", "+6 MPH")
                m2.metric(t["f1_metric"], "167 KM/H", "+10 KM/H")
                m3.metric(t["f1_spin"], "2,400 RPM", "Topspin-Slice")
                
                st.markdown(f"#### {t['f1_bio_title']}")
                st.info(t["f1_bio_tip"])
            else:
                st.warning(t["f1_warn"])

# ==========================================
# 5. Feature 2: AI Racket & Tension Calculator
# ==========================================
elif page_selection == t["nav_2"]:
    st.title(t["f2_title"])
    st.write(t["f2_desc"])

    c1, c2 = st.columns(2)
    with c1:
        ntrp_input = st.slider(t["f2_ntrp"], min_value=1.5, max_value=7.0, value=3.5, step=0.5)
        serve_speed_input = st.number_input(t["f2_speed"], min_value=30, max_value=150, value=85)
        play_style = st.selectbox(t["f2_style"], ["Baseline Basher", "All-Court Tactical", "Serve & Volley", "Defensive Counter-puncher"])
    
    with c2:
        racket_head = st.selectbox(t["f2_head"], ["98 sq in (Control)", "100 sq in (Balanced)", "104+ sq in (Power)"])
        string_type = st.selectbox(t["f2_string"], ["Co-Poly / Polyester (Control & Spin)", "Multifilament (Comfort & Power)", "Natural Gut (Maximum Touch)", "Hybrid Blend"])

    if st.button(t["f2_btn"], use_container_width=True):
        base_tension = 52.0
        if serve_speed_input > 100:
            base_tension += 4.0
        elif serve_speed_input > 80:
            base_tension += 2.0
        
        if ntrp_input >= 4.5:
            base_tension += 2.0

        st.markdown("---")
        st.subheader(t["f2_res_title"])
        res_col1, res_col2, res_col3 = st.columns(3)
        res_col1.metric(t["f2_main_ten"], f"{base_tension:.1f} lbs")
        res_col2.metric(t["f2_cross_ten"], f"{base_tension - 2.0:.1f} lbs")
        res_col3.metric(t["f2_grip"], "4 3/8 (L3)")

        formatted_msg = t["f2_msg"].format(ntrp=ntrp_input, speed=serve_speed_input, string=string_type, tension=f"{base_tension:.1f}")
        st.success(formatted_msg)

# ==========================================
# 6. Feature 3: Tournaments Subpage
# ==========================================
elif page_selection == t["nav_3"]:
    st.title(t["f3_title"])
    st.write(t["f3_desc"])

    tourneys = [
        {"name": "2026 Seoul Open Amateur Grand Prix", "date": "2026-08-15", "loc": "Olympic Park, Seoul", "prize": "$5,000 Pool", "hotel": "Gangnam Luxury Stay ($120/night)"},
        {"name": "Jeju Island Tennis & Beach Classic", "date": "2026-09-02", "loc": "Jeju Ocean Courts", "prize": "$3,000 Pool", "hotel": "Jeju Ocean Resort ($150/night)"},
        {"name": "Incheon Songdo National NTRP Series", "date": "2026-09-20", "loc": "Songdo Sports Complex", "prize": "$2,500 Pool", "hotel": "Songdo Park Hotel ($95/night)"}
    ]

    for tour in tourneys:
        with st.container(border=True):
            tc1, tc2 = st.columns([3, 1])
            with tc1:
                st.subheader(tour["name"])
                st.write(f"📅 **{t['f3_date']}**: {tour['date']} | 📍 **{t['f3_loc']}**: {tour['loc']}")
                st.write(f"🏆 **{t['f3_prize']}**: {tour['prize']} | 🏨 **{t['f3_hotel']}**: {tour['hotel']}")
            with tc2:
                if st.button(t["f3_btn"], key=f"t_btn_{tour['name']}"):
                    current_u = st.session_state["logged_in_user"] or "Guest User"
                    ticket_id = f"TK-{len(st.session_state['inquiries'])+101}"
                    
                    # Real connection to Support Tickets Data
                    st.session_state["inquiries"].append({
                        "id": ticket_id,
                        "user": current_u,
                        "subject": f"Registration Receipt: {tour['name']}",
                        "status": "Confirmed / Paid",
                        "date": datetime.datetime.now().strftime("%Y-%m-%d")
                    })
                    st.success(t["f3_success"])

# ==========================================
# 7. Feature 4: Tennis School & Residency
# ==========================================
elif page_selection == t["nav_4"]:
    st.title(t["f4_title"])
    st.write(t["f4_desc"])

    sc1, sc2 = st.columns(2)
    with sc1:
        with st.container(border=True):
            st.subheader(t["f4_w1_title"])
            st.write(t["f4_w1_f1"])
            st.write(t["f4_w1_f2"])
            st.write(t["f4_w1_f3"])
            st.write(t["f4_w1_f4"])
            st.markdown(t["f4_w1_price"])
            if st.button(t["f4_w1_btn"]):
                current_u = st.session_state["logged_in_user"] or "Guest User"
                st.session_state["inquiries"].append({
                    "id": f"TK-{len(st.session_state['inquiries'])+101}",
                    "user": current_u,
                    "subject": "Enrollment: 1-Week Intensive Boot Camp",
                    "status": "Application Pending",
                    "date": datetime.datetime.now().strftime("%Y-%m-%d")
                })
                st.success(t["f4_res_success"])

    with sc2:
        with st.container(border=True):
            st.subheader(t["f4_m1_title"])
            st.write(t["f4_m1_f1"])
            st.write(t["f4_m1_f2"])
            st.write(t["f4_m1_f3"])
            st.write(t["f4_m1_f4"])
            st.markdown(t["f4_m1_price"])
            if st.button(t["f4_m1_btn"]):
                current_u = st.session_state["logged_in_user"] or "Guest User"
                st.session_state["inquiries"].append({
                    "id": f"TK-{len(st.session_state['inquiries'])+101}",
                    "user": current_u,
                    "subject": "Enrollment: 1-Month Pro Residency Package",
                    "status": "Application Pending",
                    "date": datetime.datetime.now().strftime("%Y-%m-%d")
                })
                st.success(t["f4_res_success"])

# ==========================================
# 8. Feature 5: NTRP Match & 1-Month VIP Chat Pass
# ==========================================
elif page_selection == t["nav_5"]:
    st.title(t["f5_title"])
    st.write(t["f5_desc"])
    
    current_user = st.session_state["logged_in_user"]
    user_mem_info = st.session_state["memberships"].get(current_user, None) if current_user else None
    has_active_vip = user_mem_info and user_mem_info["status"] == "Active"

    if has_active_vip:
        st.success(t["f5_active_banner"].format(expires=user_mem_info['expires']))
    else:
        with st.expander(t["f5_pass_expand"], expanded=not has_active_vip):
            st.markdown(f"#### {t['f5_pass_sub']}")
            c_mem1, c_mem2 = st.columns([2, 1])
            with c_mem1:
                mem_email = st.text_input(t["f5_email_lbl"], value=current_user or "")
                card_no = st.text_input(t["f5_card_lbl"], placeholder="4000-0000-0000-0000")
            with c_mem2:
                st.write(f"**{t['f5_plan_lbl']}**")
                st.write(f"**{t['f5_price_lbl']}**")
                if st.button(t["f5_btn_pay"], use_container_width=True):
                    if mem_email and card_no:
                        st.session_state["memberships"][mem_email] = {
                            "status": "Active",
                            "plan": "1-Month VIP Pass ($4.99/mo)",
                            "expires": (datetime.datetime.now() + datetime.timedelta(days=30)).strftime("%Y-%m-%d")
                        }
                        st.balloons()
                        st.success(t["f5_pay_success"])
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error(t["f5_pay_err"])

    st.markdown("---")

    sub_tab1, sub_tab2, sub_tab3 = st.tabs([
        t["f5_tab1"],
        t["f5_tab2"],
        t["f5_tab3"]
    ])

    # TAB 1: PLAYER MATCHING
    with sub_tab1:
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            filter_loc = st.selectbox(t["f5_loc_filter"], ["All Locations (전체)", "Gangnam Center, Seoul", "Jeju Ocean Resort", "Songdo Park, Incheon"])
        with col_f2:
            my_ntrp = st.slider(t["f5_ntrp_filter"], min_value=2.0, max_value=5.0, value=3.5, step=0.5)

        filtered_players = []
        for p in st.session_state["players_db"]:
            match_loc = (filter_loc == "All Locations (전체)") or (p["location"] == filter_loc)
            match_ntrp = abs(p["ntrp"] - my_ntrp) <= 0.5
            if match_loc and match_ntrp:
                filtered_players.append(p)

        st.markdown("---")
        for pl in filtered_players:
            with st.container(border=True):
                p_col1, p_col2 = st.columns([3, 1])
                with p_col1:
                    st.markdown(f"### {pl['avatar']} {pl['name']} *(NTRP {pl['ntrp']})*")
                    st.write(f"📍 **Location**: {pl['location']} | **Gender**: {pl['gender']}")
                    st.caption(f"💬 \"{pl['bio']}\"")
                with p_col2:
                    if has_active_vip:
                        st.success(t["f5_free_chat"])
                        if st.button(t["f5_chat_btn"], key=f"chat_{pl['id']}"):
                            st.session_state[f"open_chat_{pl['id']}"] = True
                    else:
                        st.warning(t["f5_req_vip"])
                        st.caption(t["f5_sub_note"])

            if st.session_state.get(f"open_chat_{pl['id']}", False) and has_active_vip:
                with st.form(key=f"form_msg_{pl['id']}"):
                    st.write(f"{t['f5_dm_to']} **{pl['name']}**")
                    placeholder_text = t["f5_msg_ph"].format(name=pl['name'], loc=pl['location'])
                    free_msg = st.text_area("Write your message", placeholder=placeholder_text)
                    if st.form_submit_button(t["f5_send_btn"]):
                        if free_msg:
                            st.session_state["chat_orders"].append({
                                "order_id": f"MSG-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}",
                                "sender": current_user or "Guest User",
                                "recipient": f"{pl['name']} (NTRP {pl['ntrp']})",
                                "message": free_msg,
                                "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                            })
                            st.success(t["f5_sent_msg"].format(name=pl['name']))
                            st.session_state[f"open_chat_{pl['id']}"] = False
                        else:
                            st.error("Please enter a message.")

    # TAB 2: COACH MESSAGING
    with sub_tab2:
        for ch in st.session_state["coaches_db"]:
            with st.container(border=True):
                c_col1, c_col2 = st.columns([3, 1])
                with c_col1:
                    st.markdown(f"### 🎾 {ch['name']}")
                    st.write(f"📜 **Cert**: {ch['cert']} ({ch['exp']})")
                    st.write(f"📍 **Location**: {ch['location']} | 🏷️ **Rate**: {ch['rate']}")
                    st.caption(f"💡 {ch['bio']}")
                with c_col2:
                    if has_active_vip:
                        st.success(t["f5_free_chat"])
                        if st.button(t["f5_coach_btn"], key=f"coach_btn_{ch['id']}"):
                            st.session_state[f"open_coach_{ch['id']}"] = True
                    else:
                        st.warning(t["f5_req_vip"])
                        st.caption(t["f5_sub_note"])

            if st.session_state.get(f"open_coach_{ch['id']}", False) and has_active_vip:
                with st.form(key=f"form_c_msg_{ch['id']}"):
                    st.write(f"{t['f5_dm_to']} **{ch['name']}**")
                    c_free_msg = st.text_area("Inquiry Notes", placeholder=t["f5_coach_ph"])
                    if st.form_submit_button(t["f5_send_btn"]):
                        if c_free_msg:
                            st.session_state["chat_orders"].append({
                                "order_id": f"MSG-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}",
                                "sender": current_user or "Guest User",
                                "recipient": f"{ch['name']} (Coach)",
                                "message": c_free_msg,
                                "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                            })
                            st.success(t["f5_coach_sent"].format(name=ch['name']))
                            st.session_state[f"open_coach_{ch['id']}"] = False
                        else:
                            st.error("Please enter a message.")

    # TAB 3: COACH REGISTRATION
    with sub_tab3:
        st.subheader(t["f5_reg_title"])
        with st.form("coach_reg_form"):
            new_c_name = st.text_input(t["f5_reg_name"], placeholder="Coach Alex Mercer")
            new_c_cert = st.text_input(t["f5_reg_cert"], placeholder="USPTA Certified / 10 Yrs Exp")
            new_c_loc = st.selectbox(t["f5_reg_loc"], ["Gangnam Center, Seoul", "Jeju Ocean Resort", "Songdo Park, Incheon"])
            new_c_rate = st.text_input(t["f5_reg_rate"], placeholder="$50 / hr")
            new_c_bio = st.text_area(t["f5_reg_bio"], placeholder="Specialized in topspin mechanics and match strategy.")
            if st.form_submit_button(t["f5_reg_btn"]):
                if new_c_name and new_c_cert:
                    st.session_state["coaches_db"].append({
                        "id": f"C-{len(st.session_state['coaches_db'])+201}",
                        "name": new_c_name,
                        "cert": new_c_cert,
                        "exp": "Verified Teacher",
                        "rate": new_c_rate,
                        "location": new_c_loc,
                        "bio": new_c_bio
                    })
                    st.balloons()
                    st.success(t["f5_reg_ok"])

# ==========================================
# 9. Feature 6: Support & Inquiries
# ==========================================
elif page_selection == t["nav_6"]:
    st.title(t["f6_title"])
    st.write(t["f6_desc"])

    with st.form("support_ticket_form"):
        st.subheader(t["f6_form_title"])
        inq_email = st.text_input(t["f6_email"], value=st.session_state["logged_in_user"] or "")
        inq_subject = st.text_input(t["f6_subj"], placeholder="Membership inquiry or app feedback")
        inq_body = st.text_area(t["f6_body"], placeholder="Describe your issue or question...")
        if st.form_submit_button(t["f6_btn"]):
            if inq_email and inq_subject:
                ticket_id = f"TK-{len(st.session_state['inquiries'])+101}"
                st.session_state["inquiries"].append({
                    "id": ticket_id,
                    "user": inq_email,
                    "subject": inq_subject,
                    "status": "Open",
                    "date": datetime.datetime.now().strftime("%Y-%m-%d")
                })
                st.success(f"{t['f6_success']} **{ticket_id}**")
            else:
                st.error(t["f6_err"])

    st.markdown("---")
    st.subheader(t["f6_list_title"])
    if st.session_state["inquiries"]:
        st.dataframe(st.session_state["inquiries"], use_container_width=True)
    else:
        st.info(t["f6_no_tickets"])

# ==========================================
# 10. Feature 7: Admin Dashboard
# ==========================================
elif page_selection == t["nav_7"]:
    st.title(t["f7_title"])
    
    if not st.session_state["admin_logged_in"]:
        with st.form("adm_login"):
            st.subheader(t["f7_auth"])
            a_id = st.text_input("Admin ID")
            a_pw = st.text_input("Password", type="password")
            if st.form_submit_button(t["f7_btn_login"]):
                if a_id == "admin" and a_pw == "admin":
                    st.session_state["admin_logged_in"] = True
                    st.rerun()
                else:
                    st.error("Invalid credentials (Use: admin / admin)")
    else:
        st.success("🟢 Admin Authenticated")
        if st.button(t["f7_btn_logout"]):
            st.session_state["admin_logged_in"] = False
            st.rerun()

        st.markdown("---")
        a_tab1, a_tab2, a_tab3 = st.tabs([t["f7_tab1"], t["f7_tab2"], t["f7_tab3"]])
        
        with a_tab1:
            st.json(st.session_state["memberships"])
        
        with a_tab2:
            st.dataframe(st.session_state["chat_orders"], use_container_width=True)

        with a_tab3:
            st.dataframe(st.session_state["inquiries"], use_container_width=True)
