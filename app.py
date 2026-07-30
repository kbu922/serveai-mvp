import streamlit as st
import pandas as pd
import datetime
import time

# ==========================================
# 1. PAGE CONFIG (MUST BE FIRST STREAMLIT CALL)
# ==========================================
st.set_page_config(
    page_title="Global Tennis Platform & AI Suite",
    page_icon="🎾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# 2. COMPLETE MULTI-LANGUAGE TRANSLATION SYSTEM
# ==========================================
TEXTS = {
    "EN": {
        # Nav & Top Header
        "app_header_title": "🎾 Global Tennis Platform & AI Suite",
        "app_header_sub": "Live Stats: **12,400+ Serves Analyzed** | 4,200+ Active Members Globally",
        "select_module": "Select Module:",
        "user_portal": "🔐 User Portal",
        "login": "🔑 Login",
        "register": "📝 Register",
        "email": "Email",
        "password": "Password",
        "login_btn": "Log In",
        "logout_btn": "Log Out",
        "full_name": "Full Name",
        "ntrp_skill": "NTRP Skill",
        "create_account": "Create Account",
        "logged_in_as": "Logged in as:",
        "membership_label": "Membership:",
        "ntrp_label": "NTRP Rating:",
        "status": "Status:",

        # Menu Options
        "m1_title": "⚡ 1. AI Serve Velocity & Biomechanics Analyzer",
        "m2_title": "🎯 2. AI Racket & String Tension Recommendation Engine",
        "m3_title": "💳 3. Membership & Subscriptions",
        "m4_title": "🏆 4. Tournaments & Lodging (US Open / Korea)",
        "m5_title": "🏛️ 5. Residency & Academy Programs",
        "m6_title": "🤝 6. Matchmaking & Coach Directory",
        "m7_title": "🎧 7. Support & Ticket Receipts",
        "m8_title": "🔒 8. Admin Control Panel",
        "m9_title": "📞 9. Contact Us",

        # Module 1
        "m1_sub": "Upload high-speed footage to run computer-vision motion vector tracking, shoulder axis analysis, and kinetic chain evaluation.",
        "m1_upload": "Upload Serve Video Footage (MP4/MOV)",
        "m1_cam_angle": "Camera Angle",
        "m1_fps": "Frame Rate (FPS)",
        "m1_run_btn": "Run Deep AI Velocity & Motion Analysis",
        "m1_benchmarks": "📊 AI Motion Vector Benchmarks",
        "m1_trophy_target": "Trophy Angle Target: 25° - 35°",
        "m1_pronation_target": "Pronation Speed Target: >1,300°/sec",
        "m1_kinetic_target": "Kinetic Efficiency Target: >85%",
        "m1_report_hdr": "📈 Biomechanical Diagnostic Report",
        "m1_peak_speed": "Peak Serve Speed",
        "m1_spin_rate": "Spin Rate",
        "m1_impact_height": "Impact Height",
        "m1_kinetic_transfer": "Kinetic Transfer",

        # Module 2
        "m2_sub": "Input your playstyle profile, injury history, and performance requirements to generate customized frame specs and string tension matrixes.",
        "m2_ntrp_label": "Your NTRP Skill Rating",
        "m2_serve_speed": "Average First Serve Speed (mph)",
        "m2_playstyle": "Primary Playstyle",
        "m2_sessions_week": "Playing Frequency (Sessions / Week)",
        "m2_elbow_issue": "Suffer from Tennis Elbow / Wrist Strain?",
        "m2_priority": "Main Priority",
        "m2_frame_weight": "Frame Weight Preference",
        "m2_gen_btn": "Generate Detailed Setup & Tension Recommendations",
        "m2_spec_hdr": "🛠️ Customized Equipment & Tension Specification",
        "m2_head_size": "Recommended Head Size",
        "m2_target_weight": "Target Frame Weight",
        "m2_tension": "String Tension (Mains / Crosses)",
        "m2_material": "String Material",

        # Module 3
        "m3_sub": "Unlock elite AI biomechanics features, coach messaging, and group discount thresholds.",
        "m3_free_title": "🆓 Free Athlete",
        "m3_free_btn": "Current Base Plan",
        "m3_pro_title": "⚡ PRO Pass",
        "m3_pro_btn": "Subscribe PRO ($19.99/mo)",
        "m3_vip_title": "🏆 VIP Gold Residency",
        "m3_vip_btn": "Subscribe VIP Gold ($149/yr)",
        "m3_checkout": "🔒 Secure Checkout:",
        "m3_card_name": "Cardholder Full Name *",
        "m3_card_num": "Credit Card Number *",
        "m3_card_exp": "Expiration Date (MM/YY) *",
        "m3_card_cvv": "CVV Security Code *",
        "m3_pay_btn": "Confirm Payment & Activate Subscription",

        # Module 4 & 5
        "m4_sub": "📍 Select Target Competition:",
        "gallery_tab": "🖼️ Competition Infrastructure & Residence Gallery",
        "group_tab": "👥 Member Group Buying ($85 Discount)",
        "indiv_tab": "👤 Individual Registration & Checkout",
        "passport": "Passport / Gov ID *",
        "indiv_pay_btn": "Pay & Confirm Individual Booking ($300.00)",

        # Module 6
        "m6_sub": "Connect with local hitting partners or book certified tour coaches. Direct messaging requires an active PRO Pass or VIP Gold membership.",
        "m6_warn": "🔒 **Membership Required:** You are currently on `{tier}`. Direct messaging with players and coaches is exclusive to PRO Pass and VIP Gold members.",
        "tab_partners": "🎾 Find Partners",
        "tab_coaches": "👨‍🏫 Certified Coaches",
        "chat_now": "💬 Chat Now",
        "locked": "🔒 Locked (Upgrade)",
        "book_session": "📅 Book Session",

        # Module 7
        "m7_title_text": "🎧 Support Center & Billing Receipts",
        "m7_sub_text": "Manage your support inquiries, request equipment service updates, and access official tax invoices/receipts.",
        "tab_tickets": "📋 My Support Tickets",
        "tab_receipts": "🧾 Transaction Receipts & Invoices",
        "tab_new_ticket": "📩 Submit New Inquiry",
        "active_tickets": "🎫 Active & Past Support Requests",
        "login_info": "💡 Please log in to view your personalized support history.",
        "billing_history": "💳 Billing History & Official Receipts",
        "generate_receipt": "📄 Generate Detailed Digital Receipt",
        "select_order": "Select Order ID to View Receipt:",
        "submit_ticket_hdr": "📩 Create a Support Ticket",
        "category": "Inquiry Category:",
        "subject": "Subject / Title *",
        "details": "Provide details about your inquiry *",
        "submit_btn": "Submit Support Ticket",
        "success_msg": "🎉 Ticket **{id}** submitted successfully! Our team will respond within 24 hours.",
        "no_orders": "No transaction records found.",

        # Module 8 & 9
        "admin_title": "🔒 Platform Administration Panel",
        "admin_restricted": "⛔ Access Restricted: Admin credentials or VIP Gold management status required.",
        "contact_title": "📞 Contact Global Tennis Platform",
        "contact_sub": "Have questions? Reach out directly to our operations team or headquarters.",
        "contact_btn": "Send Direct Message"
    },
    "KR": {
        # Nav & Top Header
        "app_header_title": "🎾 글로벌 테니스 플랫폼 & AI 스위트",
        "app_header_sub": "실시간 통계: **12,400+ 서브 분석 완료** | 전 세계 4,200+ 활성 회원",
        "select_module": "모듈 선택:",
        "user_portal": "🔐 사용자 포털",
        "login": "🔑 로그인",
        "register": "📝 회원가입",
        "email": "이메일",
        "password": "비밀번호",
        "login_btn": "로그인",
        "logout_btn": "로그아웃",
        "full_name": "성명",
        "ntrp_skill": "NTRP 레벨",
        "create_account": "계정 생성",
        "logged_in_as": "로그인 계정:",
        "membership_label": "멤버십 등급:",
        "ntrp_label": "NTRP 점수:",
        "status": "상태:",

        # Menu Options
        "m1_title": "⚡ 1. AI 서브 속도 및 바이오매카닉스 분석기",
        "m2_title": "🎯 2. AI 라켓 및 스트링 적정 적정 수치 추천 엔진",
        "m3_title": "💳 3. 멤버십 및 구독 관리",
        "m4_title": "🏆 4. 토너먼트 및 숙박 (US 오픈 / 한국)",
        "m5_title": "🏛️ 5. 레지던시 및 아카데미 프로그램",
        "m6_title": "🤝 6. 매칭 & 전문 코치 디렉토리",
        "m7_title": "🎧 7. 고객 지원 센터 및 결제 영수증",
        "m8_title": "🔒 8. 관리자 제어 패널",
        "m9_title": "📞 9. 문의하기",

        # Module 1
        "m1_sub": "고속 서브 영상을 업로드하여 컴퓨터 비전 운동 벡터 추적, 어깨 축 분석 및 운동 체인 평가를 진행하세요.",
        "m1_upload": "서브 영상 파일 업로드 (MP4/MOV)",
        "m1_cam_angle": "카메라 촬영 각도",
        "m1_fps": "프레임 레이트 (FPS)",
        "m1_run_btn": "AI 정밀 속도 및 모션 분석 실행",
        "m1_benchmarks": "📊 AI 모션 벡터 벤치마크 Target",
        "m1_trophy_target": "트로피 자세 목표 각도: 25° - 35°",
        "m1_pronation_target": "회내(Pronation) 속도 Target: >1,300°/초",
        "m1_kinetic_target": "운동 에너지 전달 효율 Target: >85%",
        "m1_report_hdr": "📈 바이오매카닉 정밀 진단 리포트",
        "m1_peak_speed": "최고 서브 속도",
        "m1_spin_rate": "스핀 회전수",
        "m1_impact_height": "타구점 높이",
        "m1_kinetic_transfer": "에너지 전달률",

        # Module 2
        "m2_sub": "플레이 스타일, 부상 이력 및 성능 목표를 입력하여 맞춤형 프레임 스펙과 스트링 텐션 매트릭스를 추천받으세요.",
        "m2_ntrp_label": "본인의 NTRP 실력 등급",
        "m2_serve_speed": "평균 첫 번째 서브 속도 (mph)",
        "m2_playstyle": "주요 플레이 스타일",
        "m2_sessions_week": "주간 플레이 빈도 (회 / 주)",
        "m2_elbow_issue": "테니스 엘보 또는 손목 통증이 있으신가요?",
        "m2_priority": "최우선 고려 사항",
        "m2_frame_weight": "선호하는 라켓 프레임 무게",
        "m2_gen_btn": "상세 장비 조합 및 텐션 추천 생성",
        "m2_spec_hdr": "🛠️ 맞춤형 장비 및 스트링 텐션 명세서",
        "m2_head_size": "추천 헤드 사이즈",
        "m2_target_weight": "목표 라켓 무게",
        "m2_tension": "스트링 텐션 (메인 / 크로스)",
        "m2_material": "추천 스트링 소재",

        # Module 3
        "m3_sub": "프리미엄 AI 바이오매카닉스 기능, 코치 직접 메시지, 그룹 할인 혜택을 이용해 보세요.",
        "m3_free_title": "🆓 무료 일반 회원",
        "m3_free_btn": "현재 기본 플랜 이용 중",
        "m3_pro_title": "⚡ PRO 패스",
        "m3_pro_btn": "PRO 패스 구독 ($19.99/월)",
        "m3_vip_title": "🏆 VIP 골드 레지던시",
        "m3_vip_btn": "VIP 골드 구독 ($149/년)",
        "m3_checkout": "🔒 결제하기:",
        "m3_card_name": "카드 소유자 성명 *",
        "m3_card_num": "신용카드 번호 *",
        "m3_card_exp": "유효기간 (MM/YY) *",
        "m3_card_cvv": "CVV 보안코드 *",
        "m3_pay_btn": "결제 승인 및 멤버십 활성화",

        # Module 4 & 5
        "m4_sub": "📍 참가 대회 선택:",
        "gallery_tab": "🖼️ 대회 인프라 및 숙소 갤러리",
        "group_tab": "👥 회원 공동 구매 ($85 할인)",
        "indiv_tab": "👤 개인 참가 신청 및 결제",
        "passport": "여권 번호 또는 신분증 번호 *",
        "indiv_pay_btn": "개인 참가 결제 및 확정 ($300.00)",

        # Module 6
        "m6_sub": "지역 랠리 파트너를 찾거나 검증된 전문 코치 레슨을 예약하세요. 1:1 메시지는 PRO 패스 또는 VIP 골드 회원 전용입니다.",
        "m6_warn": "🔒 **멤버십 필요:** 현재 `{tier}` 이용 중입니다. 파트너 및 코치와의 직접 메시지는 PRO 패스 및 VIP 골드 회원 전용 기능입니다.",
        "tab_partners": "🎾 파트너 찾기",
        "tab_coaches": "👨‍🏫 전문 코치진",
        "chat_now": "💬 대화하기",
        "locked": "🔒 잠김 (업그레이드 필요)",
        "book_session": "📅 레슨 예약하기",

        # Module 7
        "m7_title_text": "🎧 고객 지원 센터 및 결제 영수증",
        "m7_sub_text": "문의 내역 관리, 장비 서비스 업데이트 요청 및 공식 세금 계산서/영수증을 확인하세요.",
        "tab_tickets": "📋 내 지원 티켓",
        "tab_receipts": "🧾 거래 내역 및 영수증",
        "tab_new_ticket": "📩 새 문의 제출하기",
        "active_tickets": "🎫 진행 중 및 지난 문의 내역",
        "login_info": "💡 개인 맞춤 지원 내역을 확인하려면 로그인해 주세요.",
        "billing_history": "💳 결제 내역 및 공식 영수증",
        "generate_receipt": "📄 상세 디지털 영수증 발급",
        "select_order": "영수증을 조회할 주문 ID를 선택하세요:",
        "submit_ticket_hdr": "📩 지원 티켓 작성",
        "category": "문의 유형:",
        "subject": "제목 *",
        "details": "문의 내용을 자세히 작성해 주세요 *",
        "submit_btn": "지원 티켓 제출",
        "success_msg": "🎉 티켓 **{id}**이(가) 성공적으로 접수되었습니다! 24시간 이내에 답변해 드리겠습니다.",
        "no_orders": "거래 내역이 없습니다.",

        # Module 8 & 9
        "admin_title": "🔒 플랫폼 관리자 제어 패널",
        "admin_restricted": "⛔ 접근 제한: 관리자 권한 또는 VIP 골드 계정이 필요합니다.",
        "contact_title": "📞 글로벌 테니스 플랫폼 문의하기",
        "contact_sub": "궁금한 점이 있으신가요? 운영팀 또는 본사에 직접 문의하세요.",
        "contact_btn": "문의 메시지 전송"
    }
}

def get_text(key, lang="EN"):
    """Helper function to safely retrieve localized strings."""
    lang_code = "KR" if lang == "한국어" else "EN"
    return TEXTS.get(lang_code, TEXTS["EN"]).get(key, key)


# ==========================================
# 3. LUXURY SAND THEME STYLING
# ==========================================
st.markdown("""
    <style>
    .stApp {
        background-color: #F5F2EB;
        color: #211F1D;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    h1, h2, h3, h4, h5 {
        color: #211F1D !important;
        font-weight: 600;
        letter-spacing: -0.02em;
    }
    .stCard, div[data-testid="stExpander"], div[data-testid="stForm"] {
        background-color: #FAF8F5;
        border: 1px solid #E5E0D8;
        border-radius: 12px;
        padding: 24px;
        box-shadow: 0 4px 12px rgba(33, 31, 29, 0.03);
    }
    .stButton > button, div[data-testid="stForm"] button {
        background-color: #211F1D !important;
        color: #FAF8F5 !important;
        border-radius: 8px !important;
        border: none !important;
        font-weight: 600 !important;
        padding: 12px 24px !important;
        transition: all 0.2s ease;
        width: 100%;
    }
    .stButton > button:hover {
        background-color: #383430 !important;
        box-shadow: 0 4px 8px rgba(0,0,0,0.12);
    }
    div[data-testid="stMetricValue"] {
        color: #211F1D !important;
        font-weight: 700;
    }
    .stTextInput>div>div>input, .stSelectbox>div>div>div, .stTextArea>div>div>textarea, .stNumberInput>div>div>input {
        background-color: #FFFFFF !important;
        border: 1px solid #D6D0C4 !important;
        border-radius: 8px !important;
        color: #211F1D !important;
    }
    button[data-baseweb="tab"] {
        font-weight: 600 !important;
        color: #5C544D !important;
    }
    button[aria-selected="true"] {
        color: #211F1D !important;
        border-bottom-color: #211F1D !important;
    }
    .badge-membership {
        background-color: #E2DCD0;
        color: #211F1D;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 700;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 4. STATE INITIALIZATION & AUTH SYSTEM
# ==========================================
if "language" not in st.session_state:
    st.session_state["language"] = "English"

if "registered_users" not in st.session_state:
    st.session_state["registered_users"] = {
        "alex@tennis.org": {"password": "password123", "name": "Alex Mercer", "tier": "PRO Pass", "ntrp": 4.5},
        "sarah@tennis.org": {"password": "password123", "name": "Sarah Kim", "tier": "VIP Gold", "ntrp": 5.0}
    }

if "is_logged_in" not in st.session_state:
    st.session_state["is_logged_in"] = False

if "current_user" not in st.session_state:
    st.session_state["current_user"] = None

# Databases
if "players_db" not in st.session_state:
    st.session_state["players_db"] = [
        {"Name": "Marcus Vance", "NTRP": 4.5, "City": "Seoul", "Style": "Aggressive Baseline", "Contact": "m.vance@tennis.org"},
        {"Name": "Elena Rostova", "NTRP": 5.0, "City": "Busan", "Style": "Serve & Volley", "Contact": "elena.r@tennis.org"},
        {"Name": "Jin-woo Park", "NTRP": 4.0, "City": "Seoul", "Style": "Counter-Puncher", "Contact": "jw.park@tennis.kr"},
        {"Name": "Sarah Jenkins", "NTRP": 3.5, "City": "Incheon", "Style": "All-Court", "Contact": "s.jenkins@tennis.org"}
    ]

if "coaches_db" not in st.session_state:
    st.session_state["coaches_db"] = [
        {"Coach": "Coach Rob", "Level": "USPTR Certified Master", "City": "Seoul", "Hourly": "$80/hr", "Specialty": "Serve Biomechanics", "Contact": "rob@tennis.org"},
        {"Coach": "Coach Sarah", "Level": "Ex-WTA Tour Player", "City": "Incheon", "Hourly": "$120/hr", "Specialty": "Match Strategy", "Contact": "sarah.c@tennis.org"},
        {"Coach": "Coach Min-ho", "Level": "KTA High Performance", "City": "Busan", "Hourly": "$95/hr", "Specialty": "Junior Development", "Contact": "minho@tennis.kr"}
    ]

if "tournament_group_votes" not in st.session_state:
    st.session_state["tournament_group_votes"] = [
        {"Name": "Chris P.", "Tournament": "US Open Tennis Championships", "Status": "Discount Unlocked ($85)"},
        {"Name": "Min-ji K.", "Tournament": "Seoul Open Masters", "Status": "Discount Unlocked ($85)"},
        {"Name": "Kenji S.", "Tournament": "Seoul Open Masters", "Status": "Discount Unlocked ($85)"}
    ]

if "academy_group_votes" not in st.session_state:
    st.session_state["academy_group_votes"] = [
        {"name": "Alex M.", "program": "1-Week Intensive Boot Camp", "discount_tier": "15% Off"},
        {"name": "Sarah K.", "program": "1-Week Intensive Boot Camp", "discount_tier": "15% Off"},
        {"name": "David L.", "program": "1-Month Pro Residency", "discount_tier": "20% Off"}
    ]

if "inquiries" not in st.session_state:
    st.session_state["inquiries"] = [
        {"Ticket ID": "TK-1001", "Subject": "Racket Stringing Order", "Status": "Resolved", "Date": "2026-07-15"}
    ]

if "chat_orders" not in st.session_state:
    st.session_state["chat_orders"] = [
        {"Order ID": "ORD-9921", "Item": "PRO Pass Monthly", "Amount": "$19.99", "Status": "Paid"}
    ]

lang = st.session_state["language"]

# ==========================================
# 5. SIDEBAR AUTH & NAVIGATION PANEL
# ==========================================
st.sidebar.image("https://images.unsplash.com/photo-1595435934249-5df7ed86e1c0?w=400&q=80", caption="Global Tennis Hub")

st.sidebar.markdown(f"### {get_text('user_portal', lang)}")

if not st.session_state["is_logged_in"]:
    auth_tab1, auth_tab2 = st.sidebar.tabs([get_text("login", lang), get_text("register", lang)])
    
    with auth_tab1:
        login_email = st.text_input(get_text("email", lang), key="login_email")
        login_pass = st.text_input(get_text("password", lang), type="password", key="login_pass")
        if st.button(get_text("login_btn", lang), key="btn_login"):
            if login_email in st.session_state["registered_users"] and st.session_state["registered_users"][login_email]["password"] == login_pass:
                st.session_state["is_logged_in"] = True
                st.session_state["current_user"] = st.session_state["registered_users"][login_email]
                st.session_state["current_user"]["email"] = login_email
                st.rerun()
            else:
                st.sidebar.error("Invalid Email or Password.")

    with auth_tab2:
        reg_name = st.text_input(get_text("full_name", lang), key="reg_name")
        reg_email = st.text_input(get_text("email", lang), key="reg_email")
        reg_pass = st.text_input(get_text("password", lang), type="password", key="reg_pass")
        reg_ntrp = st.slider(get_text("ntrp_skill", lang), 1.0, 7.0, 3.5, 0.5, key="reg_ntrp")
        if st.button(get_text("create_account", lang), key="btn_reg"):
            if reg_email and reg_pass and reg_name:
                st.session_state["registered_users"][reg_email] = {
                    "password": reg_pass,
                    "name": reg_name,
                    "tier": "Free Tier",
                    "ntrp": reg_ntrp
                }
                st.session_state["is_logged_in"] = True
                st.session_state["current_user"] = st.session_state["registered_users"][reg_email]
                st.session_state["current_user"]["email"] = reg_email
                st.rerun()
            else:
                st.sidebar.error("Please fill in all fields.")
else:
    u = st.session_state["current_user"]
    st.sidebar.markdown(f"**{get_text('logged_in_as', lang)}** `{u['name']}`")
    st.sidebar.markdown(f"**{get_text('membership_label', lang)}** <span class='badge-membership'>{u['tier']}</span>", unsafe_allow_html=True)
    st.sidebar.markdown(f"**{get_text('ntrp_label', lang)}** `{u['ntrp']}`")
    
    if st.sidebar.button(get_text("logout_btn", lang), key="btn_logout"):
        st.session_state["is_logged_in"] = False
        st.session_state["current_user"] = None
        st.rerun()

st.sidebar.markdown("---")

menu_options = [
    get_text("m1_title", lang),
    get_text("m2_title", lang),
    get_text("m3_title", lang),
    get_text("m4_title", lang),
    get_text("m5_title", lang),
    get_text("m6_title", lang),
    get_text("m7_title", lang),
    get_text("m8_title", lang),
    get_text("m9_title", lang)
]

menu = st.sidebar.radio(get_text("select_module", lang), menu_options)

# ==========================================
# 6. TOP NAVIGATION HEADER
# ==========================================
col_h1, col_h2, col_h3 = st.columns([4, 2, 2])

with col_h1:
    st.markdown(f"### {get_text('app_header_title', lang)}")
    st.caption(get_text('app_header_sub', lang))

with col_h2:
    selected_lang = st.selectbox("🌐 Language / 언어", ["English", "한국어"], index=0 if st.session_state["language"] == "English" else 1)
    if selected_lang != st.session_state["language"]:
        st.session_state["language"] = selected_lang
        st.rerun()

with col_h3:
    current_tier = st.session_state["current_user"]["tier"] if st.session_state["is_logged_in"] else "Guest / Free"
    st.markdown(f"**{get_text('status', lang)}** `{current_tier}`")

st.markdown("---")

# ==========================================
# 7. MODULE FUNCTIONS
# ==========================================

# --- MODULE 1: AI SERVE VELOCITY ---
def render_module_1():
    st.subheader(get_text("m1_title", lang))
    st.write(get_text("m1_sub", lang))

    col1, col2 = st.columns([3, 2])
    with col1:
        video_file = st.file_uploader(get_text("m1_upload", lang), type=["mp4", "mov"])
        c_a, c_b = st.columns(2)
        with c_a:
            angle = st.selectbox(get_text("m1_cam_angle", lang), ["Behind Court (Baseline)", "Side View (Court Level)", "45-Degree Angle"])
        with c_b:
            fps = st.slider(get_text("m1_fps", lang), 30, 240, 120)

        run_analysis = st.button(get_text("m1_run_btn", lang))

    with col2:
        st.markdown(f"""
        <div style="background-color:#FAF8F5; border:1px solid #E5E0D8; border-radius:12px; padding:16px;">
            <h4 style="margin-top:0;">{get_text('m1_benchmarks', lang)}</h4>
            <p style="font-size:13px; color:#5C544D; margin-bottom:8px;"><strong>{get_text('m1_trophy_target', lang)}</strong></p>
            <p style="font-size:13px; color:#5C544D; margin-bottom:8px;"><strong>{get_text('m1_pronation_target', lang)}</strong></p>
            <p style="font-size:13px; color:#5C544D; margin-bottom:0;"><strong>{get_text('m1_kinetic_target', lang)}</strong></p>
        </div>
        """, unsafe_allow_html=True)

    if video_file or run_analysis:
        with st.spinner("Analyzing high-speed frames..."):
            time.sleep(1.0)
            st.markdown("---")
            st.markdown(f"### {get_text('m1_report_hdr', lang)}")
            
            m1, m2, m3, m4 = st.columns(4)
            m1.metric(get_text("m1_peak_speed", lang), "118.4 mph", delta="+4.2 mph")
            m2.metric(get_text("m1_spin_rate", lang), "2,840 RPM", delta="Kick Serve")
            m3.metric(get_text("m1_impact_height", lang), "2.88 m", delta="Optimal Apex")
            m4.metric(get_text("m1_kinetic_transfer", lang), "88.2%", delta="Optimal Drive")

# --- MODULE 2: AI RACKET & STRING TENSION ---
def render_module_2():
    st.subheader(get_text("m2_title", lang))
    st.write(get_text("m2_sub", lang))

    col1, col2 = st.columns(2)
    with col1:
        ntrp = st.slider(get_text("m2_ntrp_label", lang), 1.5, 7.0, 4.0, 0.5)
        serve_speed = st.number_input(get_text("m2_serve_speed", lang), 40, 140, 95)
        playstyle = st.selectbox(get_text("m2_playstyle", lang), ["Baseline Aggressor", "All-Court Counterpuncher", "Touch & Net Specialist"])
        matches_per_week = st.slider(get_text("m2_sessions_week", lang), 1, 7, 3)

    with col2:
        elbow_issue = st.checkbox(get_text("m2_elbow_issue", lang))
        priority = st.select_slider(get_text("m2_priority", lang), options=["Maximum Arm Comfort", "Balanced Feel & Control", "Maximum Spin"])
        racket_weight = st.radio(get_text("m2_frame_weight", lang), ["Light (<300g)", "Standard (300g-315g)", "Heavy (>315g)"])

    if st.button(get_text("m2_gen_btn", lang)):
        st.markdown("---")
        st.markdown(f"### {get_text('m2_spec_hdr', lang)}")

        r1, r2, r3, r4 = st.columns(4)
        r1.metric(get_text("m2_head_size", lang), "98 - 100 sq in")
        r2.metric(get_text("m2_target_weight", lang), "305 g")
        r3.metric(get_text("m2_tension", lang), "50 / 48 lbs" if elbow_issue else "54 / 52 lbs")
        r4.metric(get_text("m2_material", lang), "Multifilament / Gut" if elbow_issue else "Co-Poly Hybrid")

# --- MODULE 3: MEMBERSHIP & SUBSCRIPTIONS ---
def render_module_membership():
    st.subheader(get_text("m3_title", lang))
    st.write(get_text("m3_sub", lang))

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"""
        <div style="background-color:#FAF8F5; border:1px solid #E5E0D8; border-radius:12px; padding:20px; text-align:center;">
            <h3>{get_text('m3_free_title', lang)}</h3>
            <h2>$0</h2>
        </div>
        """, unsafe_allow_html=True)
        st.write("")
        st.button(get_text("m3_free_btn", lang), disabled=True, key="plan_free")

    with col2:
        st.markdown(f"""
        <div style="background-color:#FAF8F5; border:2px solid #211F1D; border-radius:12px; padding:20px; text-align:center;">
            <h3>{get_text('m3_pro_title', lang)}</h3>
            <h2>$19.99 / mo</h2>
        </div>
        """, unsafe_allow_html=True)
        st.write("")
        if st.button(get_text("m3_pro_btn", lang), key="plan_pro"):
            st.session_state["selected_plan"] = ("PRO Pass", "$19.99/mo")

    with col3:
        st.markdown(f"""
        <div style="background-color:#FAF8F5; border:1px solid #E5E0D8; border-radius:12px; padding:20px; text-align:center;">
            <h3>{get_text('m3_vip_title', lang)}</h3>
            <h2>$149.00 / yr</h2>
        </div>
        """, unsafe_allow_html=True)
        st.write("")
        if st.button(get_text("m3_vip_btn", lang), key="plan_vip"):
            st.session_state["selected_plan"] = ("VIP Gold", "$149.00/yr")

    if "selected_plan" in st.session_state:
        plan_name, plan_price = st.session_state["selected_plan"]
        st.markdown("---")
        st.markdown(f"### {get_text('m3_checkout', lang)} **{plan_name} ({plan_price})**")
        
        with st.form("checkout_payment_form"):
            c_a, c_b = st.columns(2)
            with c_a:
                card_name = st.text_input(get_text("m3_card_name", lang))
                card_num = st.text_input(get_text("m3_card_num", lang), type="password")
            with c_b:
                card_exp = st.text_input(get_text("m3_card_exp", lang))
                card_cvv = st.text_input(get_text("m3_card_cvv", lang), type="password")

            if st.form_submit_button(get_text("m3_pay_btn", lang), use_container_width=True):
                if card_name and card_num:
                    if st.session_state["is_logged_in"]:
                        st.session_state["current_user"]["tier"] = plan_name
                    st.success("🎉 Payment Successful!")
                    del st.session_state["selected_plan"]
                    st.rerun()

# --- MODULE 4 & 5: TOURNAMENTS & ACADEMY ---
def render_module_3():
    st.subheader(get_text("m4_title", lang))
    selected_event = st.selectbox(get_text("m4_sub", lang), ["🇺🇸 US Open Championships", "🇰🇷 Seoul Open Masters", "🇰🇷 Busan Clay Court Cup"])

    subpage = st.radio("Pathway:", [get_text("gallery_tab", lang), get_text("group_tab", lang), get_text("indiv_tab", lang)], horizontal=True)
    st.markdown("---")

    if subpage == get_text("gallery_tab", lang):
        col_img1, col_img2 = st.columns(2)
        with col_img1:
            st.image("https://images.unsplash.com/photo-1595435934249-5df7ed86e1c0?w=800&q=80", use_container_width=True)
        with col_img2:
            st.image("https://images.unsplash.com/photo-1566073771259-6a8506099945?w=800&q=80", use_container_width=True)

    elif subpage == get_text("group_tab", lang):
        st.table(pd.DataFrame(st.session_state["tournament_group_votes"]))

    elif subpage == get_text("indiv_tab", lang):
        with st.form("indiv_tourn_form"):
            st.text_input(get_text("full_name", lang))
            st.text_input(get_text("passport", lang))
            st.text_input(get_text("m3_card_num", lang), type="password")
            if st.form_submit_button(get_text("indiv_pay_btn", lang)):
                st.success("🎉 Booking Confirmed!")

def render_module_4():
    st.subheader(get_text("m5_title", lang))
    st.table(pd.DataFrame(st.session_state["academy_group_votes"]))

# --- MODULE 6: MATCHMAKING & COACH DIRECTORY ---
def render_module_5():
    st.subheader(get_text("m6_title", lang))
    st.write(get_text("m6_sub", lang))

    is_logged = st.session_state.get("is_logged_in", False)
    user_tier = st.session_state.get("current_user", {}).get("tier", "Free Tier") if is_logged else "Guest"
    has_chat_access = is_logged and user_tier in ["PRO Pass", "VIP Gold"]

    if not has_chat_access:
        st.warning(get_text("m6_warn", lang).format(tier=user_tier))

    st.markdown("---")
    t1, t2 = st.tabs([get_text("tab_partners", lang), get_text("tab_coaches", lang)])

    with t1:
        for idx, player in enumerate(st.session_state["players_db"]):
            with st.expander(f"🎾 {player['Name']} — NTRP {player['NTRP']} ({player['City']})", expanded=True):
                st.write(f"**Style:** {player['Style']}")
                st.write(f"**Contact:** `{player['Contact'] if has_chat_access else '••••••••@••••.org'}`")
                if has_chat_access:
                    st.button(get_text("chat_now", lang), key=f"chat_{idx}")
                else:
                    st.button(get_text("locked", lang), key=f"lock_{idx}", disabled=True)

    with t2:
        for idx, coach in enumerate(st.session_state["coaches_db"]):
            with st.expander(f"🏆 {coach['Coach']} — {coach['Level']} ({coach['City']})", expanded=True):
                st.write(f"**Specialty:** {coach['Specialty']}")
                st.write(f"**Rate:** {coach['Hourly']}")
                if has_chat_access:
                    st.button(get_text("book_session", lang), key=f"book_{idx}")
                else:
                    st.button(get_text("locked", lang), key=f"lock_c_{idx}", disabled=True)

# --- MODULE 7: SUPPORT & RECEIPTS ---
def render_module_6():
    st.subheader(get_text("m7_title_text", lang))
    st.write(get_text("m7_sub_text", lang))
    st.markdown("---")

    tab1, tab2, tab3 = st.tabs([
        get_text("tab_tickets", lang),
        get_text("tab_receipts", lang),
        get_text("tab_new_ticket", lang)
    ])

    with tab1:
        st.markdown(f"#### {get_text('active_tickets', lang)}")
        if not st.session_state["is_logged_in"]:
            st.info(get_text("login_info", lang))
        st.table(pd.DataFrame(st.session_state["inquiries"]))

    with tab2:
        st.markdown(f"#### {get_text('billing_history', lang)}")
        if st.session_state["chat_orders"]:
            df_orders = pd.DataFrame(st.session_state["chat_orders"])
            st.dataframe(df_orders, use_container_width=True)
            
            st.markdown("---")
            st.markdown(f"#### {get_text('generate_receipt', lang)}")
            selected_order_id = st.selectbox(get_text("select_order", lang), df_orders["Order ID"].tolist())
            
            if st.button("Generate Tax Invoice PDF"):
                st.success("Invoice generated!")
        else:
            st.write(get_text("no_orders", lang))

    with tab3:
        st.markdown(f"#### {get_text('submit_ticket_hdr', lang)}")
        with st.form("support_ticket_form"):
            cat = st.selectbox(get_text("category", lang), ["Billing & Subscriptions", "Racket & Equipment Service", "Tournament Lodging", "General Inquiry"])
            subj = st.text_input(get_text("subject", lang))
            det = st.text_area(get_text("details", lang))
            
            if st.form_submit_button(get_text("submit_btn", lang)):
                if subj and det:
                    new_id = f"TK-{len(st.session_state['inquiries'])+1002}"
                    st.session_state["inquiries"].append({
                        "Ticket ID": new_id,
                        "Subject": subj,
                        "Status": "Open",
                        "Date": str(datetime.date.today())
                    })
                    st.success(get_text("success_msg", lang).format(id=new_id))

# --- MODULE 8: ADMIN CONTROL PANEL ---
def render_module_admin():
    st.subheader(get_text("admin_title", lang))
    if not st.session_state["is_logged_in"] or st.session_state["current_user"]["tier"] != "VIP Gold":
        st.error(get_text("admin_restricted", lang))
        return
    st.json(st.session_state["registered_users"])

# --- MODULE 9: CONTACT US ---
def render_module_contact():
    st.subheader(get_text("contact_title", lang))
    st.write(get_text("contact_sub", lang))

    with st.form("contact_form"):
        st.text_input(get_text("full_name", lang))
        st.text_input(get_text("email", lang))
        st.text_area(get_text("details", lang))
        if st.form_submit_button(get_text("contact_btn", lang)):
            st.success("Message sent!")

# ==========================================
# 8. MAIN ROUTER
# ==========================================
if menu == menu_options[0]:
    render_module_1()
elif menu == menu_options[1]:
    render_module_2()
elif menu == menu_options[2]:
    render_module_membership()
elif menu == menu_options[3]:
    render_module_3()
elif menu == menu_options[4]:
    render_module_4()
elif menu == menu_options[5]:
    render_module_5()
elif menu == menu_options[6]:
    render_module_6()
elif menu == menu_options[7]:
    render_module_admin()
elif menu == menu_options[8]:
    render_module_contact()
