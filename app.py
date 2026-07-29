import streamlit as st
import datetime
import time

# ==========================================
# 1. Page Configuration & Modern SaaS Styling
# ==========================================
st.set_page_config(
    page_title="ServeAI - Global Tennis & Sports-Tech Portal",
    page_icon="🎾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Clean SaaS CSS Theme
st.markdown("""
<style>
    /* Global Page Clean Theme */
    .stApp {
        background-color: #f8fafc;
        color: #0f172a;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }
    
    /* Top Header Bar */
    .top-header {
        background-color: #ffffff;
        border-bottom: 1px solid #e2e8f0;
        padding: 16px 24px;
        border-radius: 12px;
        margin-bottom: 24px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.05);
    }
    
    /* Hero Banner */
    .hero-box {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 16px;
        padding: 32px 24px;
        margin-bottom: 28px;
        text-align: center;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.03);
    }
    
    .hero-title {
        font-size: 2.4rem;
        font-weight: 800;
        color: #0f172a;
        margin-bottom: 8px;
        letter-spacing: -0.025em;
    }
    
    .hero-subtitle {
        color: #475569;
        font-size: 1.1rem;
        max-width: 680px;
        margin: 0 auto 16px auto;
        line-height: 1.5;
    }
    
    /* Stats Bar for Social Proof */
    .stat-badge {
        display: inline-block;
        background-color: #f1f5f9;
        color: #334155;
        font-weight: 600;
        font-size: 0.85rem;
        padding: 6px 14px;
        border-radius: 9999px;
        margin: 4px;
        border: 1px solid #e2e8f0;
    }

    /* Cards & Container Containers */
    div[data-testid="stVerticalBlock"] > div[style*="flex-direction: column"] > div[data-testid="stBlock"] {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 2px 4px 0 rgba(0, 0, 0, 0.02);
    }
    
    /* Clean Primary Buttons */
    .stButton > button {
        background-color: #0f172a !important;
        color: #ffffff !important;
        font-weight: 600 !important;
        border-radius: 8px !important;
        border: none !important;
        padding: 0.5rem 1.1rem !important;
        transition: all 0.15s ease-in-out !important;
    }
    
    .stButton > button:hover {
        background-color: #1e293b !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.08) !important;
    }

    /* Clean Metrics */
    .stMetric {
        background-color: #ffffff !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 10px !important;
        padding: 12px 16px !important;
    }
    
    div[data-testid="stMetricValue"] {
        color: #0f172a !important;
        font-weight: 700 !important;
    }

    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 6px;
        background-color: #f1f5f9;
        padding: 6px;
        border-radius: 10px;
    }

    .stTabs [data-baseweb="tab"] {
        height: 40px;
        border-radius: 6px;
        color: #475569;
        font-weight: 500;
    }

    .stTabs [aria-selected="true"] {
        background-color: #ffffff !important;
        color: #0f172a !important;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.08) !important;
    }

    /* Sidebar Clean styling */
    section[data-testid="stSidebar"] {
        background-color: #ffffff !important;
        border-right: 1px solid #e2e8f0;
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

if "language" not in st.session_state:
    st.session_state["language"] = "English"

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
# 3. Multilingual Dictionary
# ==========================================
t = {
    "English": {
        "nav_title": "Navigation Menu",
        "nav_1": "⚡ AI Serve Velocity",
        "nav_2": "🎾 AI Racket & Tension",
        "nav_3": "🏆 Tournaments & Hotels",
        "nav_4": "🏫 Residency & School",
        "nav_5": "🤝 NTRP Match & Direct Chat",
        "nav_6": "💬 Support & Tickets",
        "nav_7": "🔒 Admin Backend",
        "login_tab": "Login",
        "reg_tab": "Register",
        "email_lbl": "Email Address",
        "pw_lbl": "Password",
        "btn_login": "Sign In",
        "btn_logout": "Sign Out",
        "welcome": "Welcome back",
        "err_login": "Invalid credentials.",
        "reg_success": "Account created! Please sign in.",
        "vip_active": "VIP Pass Active",
        "basic_acct": "Basic Free Account",
        "pay_form_header": "Checkout & Travel Details",
        "full_name": "Full Customer Name",
        "passport_id": "Passport ID Number",
        "contact_phone": "Contact Phone Number",
        "card_type": "Payment Method",
        "card_no": "Card Number (Visa / Mastercard)",
        "exp_date": "Expiration (MM/YY)",
        "cvv": "CVV Code",
        "btn_complete_pay": "Complete Order & Book",
        "pay_err_fields": "Please complete all payment fields.",
        "f1_title": "AI Serve Speed & Trajectory Analyzer",
        "f1_desc": "Upload serve video footage. AI tracks ball frame speed and outputs trajectory metrics.",
        "f1_up_lbl": "Upload Serve Video (MP4 / MOV)",
        "f1_cam_lbl": "Camera Angle",
        "f1_fps_lbl": "Recorded FPS",
        "f1_btn": "Analyze Serve Velocity",
        "f1_analyzing": "Analyzing video motion vectors...",
        "f1_success": "Analysis Complete!",
        "f1_peak": "Peak Speed",
        "f1_metric": "Metric Velocity",
        "f1_spin": "Spin Rate",
        "f1_bio_title": "Biomechanics Analysis",
        "f1_bio_tip": "AI Tip: Racket acceleration peaked 0.08s prior to contact. Ball toss height was optimal at 3.2m.",
        "f1_warn": "Please select a video file to analyze.",
        "f2_title": "AI Racket & Tension Calculator",
        "f2_desc": "Find string tension (lbs) based on your NTRP rating and AI serve metrics.",
        "f2_ntrp": "Select NTRP Rating",
        "f2_speed": "Average Serve Speed (MPH)",
        "f2_style": "Play Style",
        "f2_head": "Racket Head Size (sq in)",
        "f2_string": "String Type",
        "f2_btn": "Calculate Recommended Setup",
        "f2_res_title": "Recommended Racket Setup",
        "f2_main_ten": "Main Tension",
        "f2_cross_ten": "Cross Tension",
        "f2_grip": "Grip Size",
        "f2_msg": "For NTRP {ntrp} at {speed} MPH, using {string} string strung at {tension} lbs provides optimal control.",
        "f3_title": "Tournaments & Official Match Lodging",
        "f3_desc": "Register for verified tournaments and reserve accommodations.",
        "f3_date": "Date",
        "f3_loc": "Location",
        "f3_prize": "Prize Pool",
        "f3_hotel": "Partner Hotel",
        "f3_btn": "Register & Book Package",
        "f3_success": "Booking confirmed! Receipt saved to Support tab.",
        "f4_title": "Global Tennis Academy & Residency Programs",
        "f4_desc": "All-inclusive high-performance training programs with court access and lodging.",
        "f4_w1_title": "1-Week Intensive Boot Camp",
        "f4_w1_f1": "• 15 Hours Private Coaching",
        "f4_w1_f2": "• Unlimited Ball Machine Access",
        "f4_w1_f3": "• AI Serve Biomechanics Report",
        "f4_w1_f4": "• Hotel Accommodation Included",
        "f4_w1_price": "$890 / Week",
        "f4_w1_btn": "Enroll in 1-Week Camp",
        "f4_m1_title": "1-Month Pro Residency Package",
        "f4_m1_f1": "• 50 Hours Coaching & Matches",
        "f4_m1_f2": "• Daily Sparring Matches",
        "f4_m1_f3": "• Conditioning & Diet Program",
        "f4_m1_f4": "• Serviced Apartment Included",
        "f4_m1_price": "$2,950 / Month",
        "f4_m1_btn": "Enroll in 1-Month Residency",
        "f4_res_success": "Enrollment completed! Details saved to Support tab.",
        "f5_title": "NTRP Partner Matchmaking & VIP Chat Pass",
        "f5_desc": "Get direct messaging access to local players and certified coaches for $4.99/month.",
        "f5_active_banner": "VIP Pass Active | Expires: {expires} | Direct Messaging Unlocked",
        "f5_pass_expand": "Get 1-Month VIP Chat Pass ($4.99 / Month)",
        "f5_pass_sub": "Unlimited direct messaging with players and coaches.",
        "f5_email_lbl": "Account Email",
        "f5_card_lbl": "Card Number",
        "f5_plan_lbl": "Plan: 1-Month VIP Pass",
        "f5_price_lbl": "Price: $4.99 USD / month",
        "f5_btn_pay": "Activate $4.99 Pass",
        "f5_pay_success": "VIP Pass activated! Direct messaging unlocked.",
        "f5_pay_err": "Please enter account and card details.",
        "f5_tab1": "Find Nearby Players",
        "f5_tab2": "Connect with Coaches",
        "f5_tab3": "Register as Coach",
        "f5_loc_filter": "Location Filter",
        "f5_ntrp_filter": "Target NTRP Level",
        "f5_free_chat": "Free Direct Chat",
        "f5_req_vip": "Requires VIP Pass",
        "f5_sub_note": "Subscribe for $4.99/mo",
        "f5_chat_btn": "Chat Now",
        "f5_dm_to": "Direct Message to",
        "f5_msg_ph": "Hi {name}, would you like to hit at {loc} this weekend?",
        "f5_send_btn": "Send Message",
        "f5_sent_msg": "Message sent to {name}!",
        "f5_coach_btn": "Contact Coach",
        "f5_coach_ph": "Hi Coach, what lesson times are available this week?",
        "f5_coach_sent": "Inquiry sent to {name}!",
        "f5_reg_title": "Register as a Certified Tennis Coach",
        "f5_reg_name": "Full Name",
        "f5_reg_cert": "Certifications",
        "f5_reg_loc": "Primary Location",
        "f5_reg_rate": "Hourly Rate",
        "f5_reg_bio": "Bio & Methodology",
        "f5_reg_btn": "Submit Coach Profile",
        "f5_reg_ok": "Coach profile registered!",
        "f6_title": "Customer Support & Ticket Portal",
        "f6_desc": "Submit inquiries regarding bookings or account features.",
        "f6_form_title": "Create Support Ticket",
        "f6_email": "Your Email",
        "f6_subj": "Subject",
        "f6_body": "Details",
        "f6_btn": "Submit Ticket",
        "f6_success": "Ticket created! Reference ID: ",
        "f6_err": "Please provide email and subject.",
        "f6_list_title": "Your Support Tickets & Bookings",
        "f6_no_tickets": "No submitted tickets found.",
        "f7_title": "Admin Backend Dashboard",
        "f7_auth": "Admin Authentication",
        "f7_btn_login": "Log In as Admin",
        "f7_btn_logout": "Log Out Admin",
        "f7_tab1": "Active VIP Memberships",
        "f7_tab2": "Delivered Messages",
        "f7_tab3": "Support Tickets"
    },
    "한국어": {
        "nav_title": "메뉴 선택",
        "nav_1": "⚡ AI 서브 속도 분석",
        "nav_2": "🎾 AI 라켓 & 텐션 계산기",
        "nav_3": "🏆 대회 & 숙박 예약",
        "nav_4": "🏫 레지던시 & 스쿨",
        "nav_5": "🤝 NTRP 매칭 & 1:1 대화",
        "nav_6": "💬 고객 지원 & 티켓",
        "nav_7": "🔒 관리자 대시보드",
        "login_tab": "로그인",
        "reg_tab": "회원가입",
        "email_lbl": "이메일 주소",
        "pw_lbl": "비밀번호",
        "btn_login": "로그인",
        "btn_logout": "로그아웃",
        "welcome": "환영합니다",
        "err_login": "로그인 정보가 올바르지 않습니다.",
        "reg_success": "가입 완료! 로그인해 주세요.",
        "vip_active": "VIP 패스 활성화됨",
        "basic_acct": "일반 계정",
        "pay_form_header": "결제 및 예약자 정보 입력",
        "full_name": "예약자 성함",
        "passport_id": "여권 번호",
        "contact_phone": "연락처",
        "card_type": "결제 수단",
        "card_no": "카드 번호",
        "exp_date": "유효기간 (MM/YY)",
        "cvv": "보안코드 (CVV)",
        "btn_complete_pay": "결제 완료 및 예약 확정",
        "pay_err_fields": "모든 결제 및 인적사항 정보를 입력해 주세요.",
        "f1_title": "AI 서브 속도 및 궤적 분석기",
        "f1_desc": "서브 비디오를 업로드하면 AI가 공의 프레임 속도 및 궤적을 측정합니다.",
        "f1_up_lbl": "서브 비디오 업로드 (MP4 / MOV)",
        "f1_cam_lbl": "카메라 각도",
        "f1_fps_lbl": "녹화 FPS",
        "f1_btn": "서브 속도 측정 시작",
        "f1_analyzing": "프레임 모션 분석 중...",
        "f1_success": "분석 완료!",
        "f1_peak": "최고 속도",
        "f1_metric": "미터법 속도",
        "f1_spin": "회전수 (Spin)",
        "f1_bio_title": "바이오매카닉 피드백",
        "f1_bio_tip": "AI 팁: 임팩트 0.08초 전에 라켓 헤드 가속도가 최고치에 도달했습니다.",
        "f1_warn": "분석할 비디오 파일을 업로드해 주세요.",
        "f2_title": "AI 라켓 & 텐션 추천 계산기",
        "f2_desc": "NTRP 레벨과 서브 속도를 바탕으로 최적의 스트링 텐션을 정밀 계산합니다.",
        "f2_ntrp": "NTRP 레벨 선택",
        "f2_speed": "평균 서브 속도 (MPH)",
        "f2_style": "플레이 스타일",
        "f2_head": "라켓 헤드 사이즈 (sq in)",
        "f2_string": "스트링 종류",
        "f2_btn": "최적 텐션 계산하기",
        "f2_res_title": "추천 장비 세팅 사양",
        "f2_main_ten": "메인 텐션",
        "f2_cross_ten": "크로스 텐션",
        "f2_grip": "그립 사이즈",
        "f2_msg": "회원님의 NTRP {ntrp} 레벨과 {speed} MPH 서브 속도에는 {string} 스트링 {tension} lbs 세팅이 적합합니다.",
        "f3_title": "테니스 대회 & 공식 숙박 예약",
        "f3_desc": "대회 참가 및 제휴 호텔 패키지를 예약하세요.",
        "f3_date": "일정",
        "f3_loc": "장소",
        "f3_prize": "총 상금",
        "f3_hotel": "제휴 호텔",
        "f3_btn": "대회 참가 및 패키지 신청",
        "f3_success": "결제가 완료되었습니다! [고객 지원] 탭에서 확인서를 접수했습니다.",
        "f4_title": "글로벌 테니스 스쿨 & 레지던시",
        "f4_desc": "숙박과 집중 훈련이 포함된 선수형 레지던시 프로그램입니다.",
        "f4_w1_title": "1주일 집중 부트캠프",
        "f4_w1_f1": "• 15시간 개인 코칭",
        "f4_w1_f2": "• 볼머신기 무제한 이용",
        "f4_w1_f3": "• AI 서브 리포트",
        "f4_w1_f4": "• 호텔 숙박 포함",
        "f4_w1_price": "주당 $890",
        "f4_w1_btn": "1주 캠프 신청하기",
        "f4_m1_title": "1개월 프로 레지던시 패키지",
        "f4_m1_f1": "• 50시간 개인/그룹 코칭",
        "f4_m1_f2": "• 매일 실전 스파링 매치",
        "f4_m1_f3": "• 컨디셔닝 & 식이요법",
        "f4_m1_f4": "• 레지던스 객실 포함",
        "f4_m1_price": "월 $2,950",
        "f4_m1_btn": "1개월 레지던시 신청하기",
        "f4_res_success": "레지던시 결제가 완료되었습니다!",
        "f5_title": "NTRP 매칭 & 1개월 VIP 무제한 대화",
        "f5_desc": "월 $4.99 멤버십으로 주변 플레이어 및 검증 코치와 무제한 무료 대화를 나누세요.",
        "f5_active_banner": "VIP 패스 활성화 | 만료일: {expires} | 1:1 무제한 대화 가능",
        "f5_pass_expand": "1개월 VIP 채팅 패스 ($4.99 / 월) 구매하기",
        "f5_pass_sub": "30일간 모든 지역 테니스 플레이어 및 코치와 무제한 대화.",
        "f5_email_lbl": "계정 이메일",
        "f5_card_lbl": "카드 번호",
        "f5_plan_lbl": "플랜: 1개월 VIP 패스",
        "f5_price_lbl": "가격: 월 $4.99 USD",
        "f5_btn_pay": "$4.99 결제하고 VIP 패스 시작",
        "f5_pay_success": "VIP 패스가 활성화되었습니다!",
        "f5_pay_err": "이메일과 카드 정보를 입력해 주세요.",
        "f5_tab1": "주변 NTRP 플레이어 찾기",
        "f5_tab2": "검증 코치 연결",
        "f5_tab3": "코치 프로필 등록",
        "f5_loc_filter": "지역 필터",
        "f5_ntrp_filter": "내 NTRP 레벨 필터",
        "f5_free_chat": "무료 대화 가능",
        "f5_req_vip": "VIP 패스 필요",
        "f5_sub_note": "위에서 월 $4.99 구독",
        "f5_chat_btn": "대화하기",
        "f5_dm_to": "메시지 보내기:",
        "f5_msg_ph": "안녕하세요 {name}님, {loc}에서 이번 주에 경기 가능하신가요?",
        "f5_send_btn": "메시지 전송",
        "f5_sent_msg": "{name}님에게 메시지가 전송되었습니다!",
        "f5_coach_btn": "코치 문의하기",
        "f5_coach_ph": "코치님 안녕하세요, 이번 주 레슨 가능 시간이 궁금합니다.",
        "f5_coach_sent": "{name} 코치님에게 문의가 전송되었습니다!",
        "f5_reg_title": "테니스 지도자 프로필 등록",
        "f5_reg_name": "성함",
        "f5_reg_cert": "자격증 및 경력",
        "f5_reg_loc": "주요 지역",
        "f5_reg_rate": "레슨비",
        "f5_reg_bio": "소개 및 레슨 철학",
        "f5_reg_btn": "코치 프로필 등록",
        "f5_reg_ok": "프로필 등록이 완료되었습니다!",
        "f6_title": "고객 지원 & 문의 센터",
        "f6_desc": "예약 및 서비스 관련 궁금하신 점을 제출해 주세요.",
        "f6_form_title": "새 문의 제출",
        "f6_email": "이메일",
        "f6_subj": "제목",
        "f6_body": "내용",
        "f6_btn": "문의 제출",
        "f6_success": "문의가 접수되었습니다! 티켓 ID: ",
        "f6_err": "이메일과 제목을 입력해 주세요.",
        "f6_list_title": "내 문의 및 결제 내역",
        "f6_no_tickets": "접수된 문의 내역이 없습니다.",
        "f7_title": "백엔드 관리자 대시보드",
        "f7_auth": "관리자 로그인",
        "f7_btn_login": "관리자 로그인",
        "f7_btn_logout": "로그아웃",
        "f7_tab1": "VIP 멤버십 목록",
        "f7_tab2": "대화 메시지 내역",
        "f7_tab3": "고객 지원 티켓"
    }
}

# Active translation dictionary alias
L = t[st.session_state["language"]]

# ==========================================
# 4. Top Navigation Header (Login / Register / Language Front-Row)
# ==========================================
header_col1, header_col2 = st.columns([1, 1])

with header_col1:
    st.markdown("### 🎾 **ServeAI Global**")

with header_col2:
    nav_btn_c1, nav_btn_c2, nav_btn_c3 = st.columns([1.5, 1, 1])
    
    with nav_btn_c1:
        selected_lang = st.selectbox(
            "🌐 Language",
            ["English", "한국어"],
            index=0 if st.session_state["language"] == "English" else 1,
            label_visibility="collapsed"
        )
        if selected_lang != st.session_state["language"]:
            st.session_state["language"] = selected_lang
            st.rerun()

    with nav_btn_c2:
        if st.session_state["logged_in_user"] is None:
            if st.button(L["login_tab"], use_container_width=True):
                st.session_state["show_auth_modal"] = "login"
        else:
            st.caption(f"👤 {st.session_state['logged_in_user'].split('@')[0]}")

    with nav_btn_c3:
        if st.session_state["logged_in_user"] is None:
            if st.button(L["reg_tab"], use_container_width=True):
                st.session_state["show_auth_modal"] = "register"
        else:
            if st.button(L["btn_logout"], use_container_width=True):
                st.session_state["logged_in_user"] = None
                st.rerun()

# Authentication Popover / Panel
if st.session_state.get("show_auth_modal"):
    mode = st.session_state["show_auth_modal"]
    with st.expander(f"🔐 {L['login_tab'] if mode=='login' else L['reg_tab']} Panel", expanded=True):
        auth_col1, auth_col2 = st.columns(2)
        with auth_col1:
            in_email = st.text_input(L["email_lbl"], key="auth_email")
        with auth_col2:
            in_pw = st.text_input(L["pw_lbl"], type="password", key="auth_pw")
            
        if mode == "login":
            if st.button(L["btn_login"]):
                if in_email in st.session_state["users"] and st.session_state["users"][in_email] == in_pw:
                    st.session_state["logged_in_user"] = in_email
                    st.session_state["show_auth_modal"] = None
                    st.success(f"{L['welcome']}, {in_email}!")
                    st.rerun()
                else:
                    st.error(L["err_login"])
        else:
            if st.button(L["reg_tab"]):
                if in_email and in_pw:
                    st.session_state["users"][in_email] = in_pw
                    st.session_state["show_auth_modal"] = "login"
                    st.success(L["reg_success"])
                else:
                    st.warning("Please fill in all fields.")

st.markdown("---")

# Navigation Menu
nav_options = [
    L["nav_1"],
    L["nav_2"],
    L["nav_3"],
    L["nav_4"],
    L["nav_5"],
    L["nav_6"],
    L["nav_7"]
]
page_selection = st.sidebar.radio(L["nav_title"], nav_options)

# ==========================================
# 5. Popularity Hero Banner (Clean SaaS Proof)
# ==========================================
st.markdown(f"""
<div class="hero-box">
    <div class="hero-title">ServeAI Sports Engine</div>
    <div class="hero-subtitle">High-performance AI trajectory analysis, global amateur tournaments, and NTRP community match-making.</div>
    <div>
        <span class="stat-badge">⚡ 12,400+ Serves Analyzed</span>
        <span class="stat-badge">🏆 15+ Global Tournaments</span>
        <span class="stat-badge">⭐ 4.9/5 Player Satisfaction</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ==========================================
# 6. Feature 1: AI Serve Speed Analysis
# ==========================================
if page_selection == L["nav_1"]:
    st.title(L["f1_title"])
    st.write(L["f1_desc"])
    
    col_up, col_res = st.columns([1, 1])
    with col_up:
        uploaded_video = st.file_uploader(L["f1_up_lbl"], type=["mp4", "mov", "avi"])
        camera_angle = st.selectbox(L["f1_cam_lbl"], ["Behind Baseline (Recommended)", "Side Court View", "45-Degree Angle"])
        frame_rate = st.select_slider(L["f1_fps_lbl"], options=[30, 60, 120, 240], value=60)
        
        btn_analyze = st.button(L["f1_btn"], use_container_width=True)

    with col_res:
        if btn_analyze:
            if uploaded_video is not None:
                with st.spinner(L["f1_analyzing"]):
                    time.sleep(1.2)
                
                st.success(L["f1_success"])
                m1, m2, m3 = st.columns(3)
                m1.metric(L["f1_peak"], "104 MPH", "+6 MPH")
                m2.metric(L["f1_metric"], "167 KM/H", "+10 KM/H")
                m3.metric(L["f1_spin"], "2,400 RPM", "Topspin-Slice")
                
                st.markdown(f"#### {L['f1_bio_title']}")
                st.info(L["f1_bio_tip"])
            else:
                st.warning(L["f1_warn"])

# ==========================================
# 7. Feature 2: AI Racket & Tension Calculator
# ==========================================
elif page_selection == L["nav_2"]:
    st.title(L["f2_title"])
    st.write(L["f2_desc"])

    c1, c2 = st.columns(2)
    with c1:
        ntrp_input = st.slider(L["f2_ntrp"], min_value=1.5, max_value=7.0, value=3.5, step=0.5)
        serve_speed_input = st.number_input(L["f2_speed"], min_value=30, max_value=150, value=85)
        play_style = st.selectbox(L["f2_style"], ["Baseline Basher", "All-Court Tactical", "Serve & Volley", "Defensive Counter-puncher"])
    
    with c2:
        racket_head = st.selectbox(L["f2_head"], ["98 sq in (Control)", "100 sq in (Balanced)", "104+ sq in (Power)"])
        string_type = st.selectbox(L["f2_string"], ["Co-Poly / Polyester (Control & Spin)", "Multifilament (Comfort & Power)", "Natural Gut (Maximum Touch)", "Hybrid Blend"])

    if st.button(L["f2_btn"], use_container_width=True):
        base_tension = 52.0
        if serve_speed_input > 100:
            base_tension += 4.0
        elif serve_speed_input > 80:
            base_tension += 2.0
        
        if ntrp_input >= 4.5:
            base_tension += 2.0

        st.markdown("---")
        st.subheader(L["f2_res_title"])
        res_col1, res_col2, res_col3 = st.columns(3)
        res_col1.metric(L["f2_main_ten"], f"{base_tension:.1f} lbs")
        res_col2.metric(L["f2_cross_ten"], f"{base_tension - 2.0:.1f} lbs")
        res_col3.metric(L["f2_grip"], "4 3/8 (L3)")

        formatted_msg = L["f2_msg"].format(ntrp=ntrp_input, speed=serve_speed_input, string=string_type, tension=f"{base_tension:.1f}")
        st.success(formatted_msg)

# ==========================================
# 8. Feature 3: Tournaments Subpage (With Passport & Payment Form)
# ==========================================
elif page_selection == L["nav_3"]:
    st.title(L["f3_title"])
    st.write(L["f3_desc"])

    tourneys = [
        {"id": "TR-01", "name": "2026 Seoul Open Amateur Grand Prix", "date": "2026-08-15", "loc": "Olympic Park, Seoul", "prize": "$5,000 Pool", "hotel": "Gangnam Luxury Stay ($120/night)"},
        {"id": "TR-02", "name": "Jeju Island Tennis & Beach Classic", "date": "2026-09-02", "loc": "Jeju Ocean Courts", "prize": "$3,000 Pool", "hotel": "Jeju Ocean Resort ($150/night)"},
        {"id": "TR-03", "name": "Incheon Songdo National NTRP Series", "date": "2026-09-20", "loc": "Songdo Sports Complex", "prize": "$2,500 Pool", "hotel": "Songdo Park Hotel ($95/night)"}
    ]

    for tour in tourneys:
        with st.container():
            tc1, tc2 = st.columns([3, 1])
            with tc1:
                st.subheader(tour["name"])
                st.write(f"📅 **{L['f3_date']}**: {tour['date']} | 📍 **{L['f3_loc']}**: {tour['loc']}")
                st.write(f"🏆 **{L['f3_prize']}**: {tour['prize']} | 🏨 **{L['f3_hotel']}**: {tour['hotel']}")
            with tc2:
                if st.button(L["f3_btn"], key=f"t_btn_{tour['id']}"):
                    st.session_state[f"book_tour_{tour['id']}"] = not st.session_state.get(f"book_tour_{tour['id']}", False)

            if st.session_state.get(f"book_tour_{tour['id']}", False):
                st.markdown("---")
                st.subheader(f"{L['pay_form_header']} - {tour['name']}")
                with st.form(key=f"pay_form_tour_{tour['id']}"):
                    fc1, fc2 = st.columns(2)
                    with fc1:
                        cust_name = st.text_input(L["full_name"], placeholder="John Doe")
                        passport_no = st.text_input(L["passport_id"], placeholder="M12345678")
                        cust_email = st.text_input(L["email_lbl"], value=st.session_state["logged_in_user"] or "")
                    with fc2:
                        cust_phone = st.text_input(L["contact_phone"], placeholder="+82 10-1234-5678")
                        card_brand = st.selectbox(L["card_type"], ["Mastercard", "Visa", "American Express"])
                        card_no = st.text_input(L["card_no"], placeholder="5412 7500 0000 0000")
                        c_col1, c_col2 = st.columns(2)
                        with c_col1:
                            exp = st.text_input(L["exp_date"], placeholder="12/28")
                        with c_col2:
                            cvv = st.text_input(L["cvv"], type="password", placeholder="123")

                    if st.form_submit_button(L["btn_complete_pay"], use_container_width=True):
                        if cust_name and passport_no and cust_email and cust_phone and card_no:
                            with st.spinner("Processing payment via Gateway..."):
                                time.sleep(1.2)
                            
                            ticket_id = f"TK-{len(st.session_state['inquiries'])+101}"
                            st.session_state["inquiries"].append({
                                "id": ticket_id,
                                "user": cust_email,
                                "subject": f"CONFIRMED PAYMENT: {tour['name']}",
                                "status": "Confirmed / Paid",
                                "date": datetime.datetime.now().strftime("%Y-%m-%d"),
                                "details": f"Passenger: {cust_name} | Passport: {passport_no} | Phone: {cust_phone} | Paid via {card_brand} ending in {card_no[-4:] if len(card_no)>=4 else '****'}"
                            })
                            st.balloons()
                            st.success(L["f3_success"])
                            st.session_state[f"book_tour_{tour['id']}"] = False
                        else:
                            st.error(L["pay_err_fields"])

# ==========================================
# 9. Feature 4: Tennis School & Residency (With Passport & Payment Form)
# ==========================================
elif page_selection == L["nav_4"]:
    st.title(L["f4_title"])
    st.write(L["f4_desc"])

    sc1, sc2 = st.columns(2)
    
    with sc1:
        with st.container():
            st.subheader(L["f4_w1_title"])
            st.write(L["f4_w1_f1"])
            st.write(L["f4_w1_f2"])
            st.write(L["f4_w1_f3"])
            st.write(L["f4_w1_f4"])
            st.markdown(f"### {L['f4_w1_price']}")
            if st.button(L["f4_w1_btn"], key="btn_open_w1"):
                st.session_state["show_w1_pay"] = not st.session_state.get("show_w1_pay", False)

        if st.session_state.get("show_w1_pay", False):
            with st.form("pay_form_w1"):
                st.subheader(f"{L['pay_form_header']} ($890 USD)")
                w1_name = st.text_input(L["full_name"], placeholder="Alex Mercer")
                w1_pass = st.text_input(L["passport_id"], placeholder="P98765432")
                w1_email = st.text_input(L["email_lbl"], value=st.session_state["logged_in_user"] or "")
                w1_phone = st.text_input(L["contact_phone"], placeholder="+1 555-0192")
                w1_card_type = st.selectbox(L["card_type"], ["Mastercard", "Visa", "American Express"])
                w1_card_no = st.text_input(L["card_no"], placeholder="4000 1234 5678 9010")
                if st.form_submit_button(L["btn_complete_pay"], use_container_width=True):
                    if w1_name and w1_pass and w1_email and w1_card_no:
                        with st.spinner("Processing registration..."):
                            time.sleep(1.2)
                        st.session_state["inquiries"].append({
                            "id": f"TK-{len(st.session_state['inquiries'])+101}",
                            "user": w1_email,
                            "subject": "CONFIRMED PAYMENT: 1-Week Intensive Boot Camp ($890)",
                            "status": "Paid & Enrolled",
                            "date": datetime.datetime.now().strftime("%Y-%m-%d"),
                            "details": f"Student: {w1_name} | Passport: {w1_pass} | Phone: {w1_phone}"
                        })
                        st.balloons()
                        st.success(L["f4_res_success"])
                        st.session_state["show_w1_pay"] = False
                    else:
                        st.error(L["pay_err_fields"])

    with sc2:
        with st.container():
            st.subheader(L["f4_m1_title"])
            st.write(L["f4_m1_f1"])
            st.write(L["f4_m1_f2"])
            st.write(L["f4_m1_f3"])
            st.write(L["f4_m1_f4"])
            st.markdown(f"### {L['f4_m1_price']}")
            if st.button(L["f4_m1_btn"], key="btn_open_m1"):
                st.session_state["show_m1_pay"] = not st.session_state.get("show_m1_pay", False)

        if st.session_state.get("show_m1_pay", False):
            with st.form("pay_form_m1"):
                st.subheader(f"{L['pay_form_header']} ($2,950 USD)")
                m1_name = st.text_input(L["full_name"], placeholder="Alex Mercer")
                m1_pass = st.text_input(L["passport_id"], placeholder="P98765432")
                m1_email = st.text_input(L["email_lbl"], value=st.session_state["logged_in_user"] or "")
                m1_phone = st.text_input(L["contact_phone"], placeholder="+1 555-0192")
                m1_card_type = st.selectbox(L["card_type"], ["Mastercard", "Visa", "American Express"])
                m1_card_no = st.text_input(L["card_no"], placeholder="5412 0000 1111 2222")
                if st.form_submit_button(L["btn_complete_pay"], use_container_width=True):
                    if m1_name and m1_pass and m1_email and m1_card_no:
                        with st.spinner("Processing residency booking..."):
                            time.sleep(1.2)
                        st.session_state["inquiries"].append({
                            "id": f"TK-{len(st.session_state['inquiries'])+101}",
                            "user": m1_email,
                            "subject": "CONFIRMED PAYMENT: 1-Month Pro Residency ($2,950)",
                            "status": "Paid & Enrolled",
                            "date": datetime.datetime.now().strftime("%Y-%m-%d"),
                            "details": f"Student: {m1_name} | Passport: {m1_pass} | Phone: {m1_phone}"
                        })
                        st.balloons()
                        st.success(L["f4_res_success"])
                        st.session_state["show_m1_pay"] = False
                    else:
                        st.error(L["pay_err_fields"])

# ==========================================
# 10. Feature 5: NTRP Match & 1-Month VIP Chat Pass
# ==========================================
elif page_selection == L["nav_5"]:
    st.title(L["f5_title"])
    st.write(L["f5_desc"])
    
    current_user = st.session_state["logged_in_user"]
    user_mem_info = st.session_state["memberships"].get(current_user, None) if current_user else None
    has_active_vip = user_mem_info and user_mem_info["status"] == "Active"

    if has_active_vip:
        st.success(L["f5_active_banner"].format(expires=user_mem_info['expires']))
    else:
        with st.expander(L["f5_pass_expand"], expanded=not has_active_vip):
            st.markdown(f"#### {L['f5_pass_sub']}")
            c_mem1, c_mem2 = st.columns([2, 1])
            with c_mem1:
                mem_email = st.text_input(L["f5_email_lbl"], value=current_user or "")
                card_no = st.text_input(L["f5_card_lbl"], placeholder="4000-0000-0000-0000")
            with c_mem2:
                st.write(f"**{L['f5_plan_lbl']}**")
                st.write(f"**{L['f5_price_lbl']}**")
                if st.button(L["f5_btn_pay"], use_container_width=True):
                    if mem_email and card_no:
                        st.session_state["memberships"][mem_email] = {
                            "status": "Active",
                            "plan": "1-Month VIP Pass ($4.99/mo)",
                            "expires": (datetime.datetime.now() + datetime.timedelta(days=30)).strftime("%Y-%m-%d")
                        }
                        st.balloons()
                        st.success(L["f5_pay_success"])
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error(L["f5_pay_err"])

    st.markdown("---")

    sub_tab1, sub_tab2, sub_tab3 = st.tabs([
        L["f5_tab1"],
        L["f5_tab2"],
        L["f5_tab3"]
    ])

    with sub_tab1:
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            filter_loc = st.selectbox(L["f5_loc_filter"], ["All Locations", "Gangnam Center, Seoul", "Jeju Ocean Resort", "Songdo Park, Incheon"])
        with col_f2:
            my_ntrp = st.slider(L["f5_ntrp_filter"], min_value=2.0, max_value=5.0, value=3.5, step=0.5)

        filtered_players = []
        for p in st.session_state["players_db"]:
            match_loc = (filter_loc == "All Locations") or (p["location"] == filter_loc)
            match_ntrp = abs(p["ntrp"] - my_ntrp) <= 0.5
            if match_loc and match_ntrp:
                filtered_players.append(p)

        st.markdown("---")
        for pl in filtered_players:
            with st.container():
                p_col1, p_col2 = st.columns([3, 1])
                with p_col1:
                    st.markdown(f"### {pl['avatar']} {pl['name']} *(NTRP {pl['ntrp']})*")
                    st.write(f"📍 **Location**: {pl['location']} | **Gender**: {pl['gender']}")
                    st.caption(f"💬 \"{pl['bio']}\"")
                with p_col2:
                    if has_active_vip:
                        st.success(L["f5_free_chat"])
                        if st.button(L["f5_chat_btn"], key=f"chat_{pl['id']}"):
                            st.session_state[f"open_chat_{pl['id']}"] = True
                    else:
                        st.warning(L["f5_req_vip"])
                        st.caption(L["f5_sub_note"])

            if st.session_state.get(f"open_chat_{pl['id']}", False) and has_active_vip:
                with st.form(key=f"form_msg_{pl['id']}"):
                    st.write(f"{L['f5_dm_to']} **{pl['name']}**")
                    placeholder_text = L["f5_msg_ph"].format(name=pl['name'], loc=pl['location'])
                    free_msg = st.text_area("Write your message", placeholder=placeholder_text)
                    if st.form_submit_button(L["f5_send_btn"]):
                        if free_msg:
                            st.session_state["chat_orders"].append({
                                "order_id": f"MSG-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}",
                                "sender": current_user or "Guest User",
                                "recipient": f"{pl['name']} (NTRP {pl['ntrp']})",
                                "message": free_msg,
                                "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                            })
                            st.success(L["f5_sent_msg"].format(name=pl['name']))
                            st.session_state[f"open_chat_{pl['id']}"] = False
                        else:
                            st.error("Please enter a message.")

    with sub_tab2:
        for ch in st.session_state["coaches_db"]:
            with st.container():
                c_col1, c_col2 = st.columns([3, 1])
                with c_col1:
                    st.markdown(f"### 🎾 {ch['name']}")
                    st.write(f"📜 **Cert**: {ch['cert']} ({ch['exp']})")
                    st.write(f"📍 **Location**: {ch['location']} | 🏷️ **Rate**: {ch['rate']}")
                    st.caption(f"💡 {ch['bio']}")
                with c_col2:
                    if has_active_vip:
                        st.success(L["f5_free_chat"])
                        if st.button(L["f5_coach_btn"], key=f"coach_btn_{ch['id']}"):
                            st.session_state[f"open_coach_{ch['id']}"] = True
                    else:
                        st.warning(L["f5_req_vip"])
                        st.caption(L["f5_sub_note"])

            if st.session_state.get(f"open_coach_{ch['id']}", False) and has_active_vip:
                with st.form(key=f"form_c_msg_{ch['id']}"):
                    st.write(f"{L['f5_dm_to']} **{ch['name']}**")
                    c_free_msg = st.text_area("Inquiry Notes", placeholder=L["f5_coach_ph"])
                    if st.form_submit_button(L["f5_send_btn"]):
                        if c_free_msg:
                            st.session_state["chat_orders"].append({
                                "order_id": f"MSG-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}",
                                "sender": current_user or "Guest User",
                                "recipient": f"{ch['name']} (Coach)",
                                "message": c_free_msg,
                                "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                            })
                            st.success(L["f5_coach_sent"].format(name=ch['name']))
                            st.session_state[f"open_coach_{ch['id']}"] = False
                        else:
                            st.error("Please enter a message.")

    with sub_tab3:
        st.subheader(L["f5_reg_title"])
        with st.form("coach_reg_form"):
            new_c_name = st.text_input(L["f5_reg_name"], placeholder="Coach Alex Mercer")
            new_c_cert = st.text_input(L["f5_reg_cert"], placeholder="USPTA Certified / 10 Yrs Exp")
            new_c_loc = st.selectbox(L["f5_reg_loc"], ["Gangnam Center, Seoul", "Jeju Ocean Resort", "Songdo Park, Incheon"])
            new_c_rate = st.text_input(L["f5_reg_rate"], placeholder="$50 / hr")
            new_c_bio = st.text_area(L["f5_reg_bio"], placeholder="Specialized in topspin mechanics and match strategy.")
            if st.form_submit_button(L["f5_reg_btn"]):
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
                    st.success(L["f5_reg_ok"])

# ==========================================
# 11. Feature 6: Support & Inquiries
# ==========================================
elif page_selection == L["nav_6"]:
    st.title(L["f6_title"])
    st.write(L["f6_desc"])

    with st.form("support_ticket_form"):
        st.subheader(L["f6_form_title"])
        inq_email = st.text_input(L["f6_email"], value=st.session_state["logged_in_user"] or "")
        inq_subject = st.text_input(L["f6_subj"], placeholder="Membership inquiry or app feedback")
        inq_body = st.text_area(L["f6_body"], placeholder="Describe your issue or question...")
        if st.form_submit_button(L["f6_btn"]):
            if inq_email and inq_subject:
                ticket_id = f"TK-{len(st.session_state['inquiries'])+101}"
                st.session_state["inquiries"].append({
                    "id": ticket_id,
                    "user": inq_email,
                    "subject": inq_subject,
                    "status": "Open",
                    "date": datetime.datetime.now().strftime("%Y-%m-%d"),
                    "details": inq_body
                })
                st.success(f"{L['f6_success']} **{ticket_id}**")
            else:
                st.error(L["f6_err"])

    st.markdown("---")
    st.subheader(L["f6_list_title"])
    if st.session_state["inquiries"]:
        st.dataframe(st.session_state["inquiries"], use_container_width=True)
    else:
        st.info(L["f6_no_tickets"])

# ==========================================
# 12. Feature 7: Admin Dashboard
# ==========================================
elif page_selection == L["nav_7"]:
    st.title(L["f7_title"])
    
    if not st.session_state["admin_logged_in"]:
        with st.form("adm_login"):
            st.subheader(L["f7_auth"])
            a_id = st.text_input("Admin ID")
            a_pw = st.text_input("Password", type="password")
            if st.form_submit_button(L["f7_btn_login"]):
                if a_id == "admin" and a_pw == "admin":
                    st.session_state["admin_logged_in"] = True
                    st.rerun()
                else:
                    st.error("Invalid credentials (Use: admin / admin)")
    else:
        st.success("🟢 Admin Authenticated")
        if st.button(L["f7_btn_logout"]):
            st.session_state["admin_logged_in"] = False
            st.rerun()

        st.markdown("---")
        a_tab1, a_tab2, a_tab3 = st.tabs([L["f7_tab1"], L["f7_tab2"], L["f7_tab3"]])
        
        with a_tab1:
            st.json(st.session_state["memberships"])
        
        with a_tab2:
            st.dataframe(st.session_state["chat_orders"], use_container_width=True)

        with a_tab3:
            st.dataframe(st.session_state["inquiries"], use_container_width=True)
