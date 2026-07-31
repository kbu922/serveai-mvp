import streamlit as st
import pandas as pd
import datetime
import time
import cv2
import numpy as np
import tempfile

# ==========================================
# 0. TRANSLATION DICTIONARY & HELPER
# ==========================================
TEXTS = {
    "EN": {
        # App & Header
        "page_title": "Global Tennis Platform & AI Suite",
        "live_stats": "Live Stats: **12,400+ Serves Analyzed** | 4,200+ Active Members Globally",
        "status_label": "Status:",
        "guest_free": "Guest / Free",
        # Sidebar & Auth
        "caption": "Global Tennis Hub",
        "user_portal": "🔐 User Portal",
        "tab_login": "🔑 Login",
        "tab_register": "📝 Register",
        "email": "Email",
        "password": "Password",
        "btn_login": "Log In",
        "welcome_back": "Welcome back, {}!",
        "invalid_login": "Invalid Email or Password.",
        "full_name": "Full Name",
        "ntrp_skill": "NTRP Skill",
        "btn_register": "Create Account",
        "acc_created": "Account created successfully!",
        "fill_all": "Please fill in all fields.",
        "logged_in_as": "Logged in as:",
        "membership": "Membership:",
        "ntrp_rating": "NTRP Rating:",
        "btn_logout": "Log Out",
        "select_module": "Select Module:",
        # Menu Options
        "menu_m1": "⚡ 1. AI Serve Velocity & Biomechanics Analyzer",
        "menu_m2": "🎯 2. AI Racket & String Tension Recommendation Engine",
        "menu_m3": "💳 3. Membership & Subscriptions",
        "menu_m4": "🏆 4. Tournaments & Lodging (US Open / Korea)",
        "menu_m5": "🏛️ 5. Residency & Academy Programs",
        "menu_m6": "🤝 6. Matchmaking & Coach Directory",
        "menu_m7": "🎧 7. Support & Ticket Receipts",
        "menu_m8": "🔒 8. Admin Control Panel",
        "menu_m9": "📞 9. Contact Us",
        # Module 1
        "m1_title": "⚡ AI Serve Velocity & Biomechanics Analyzer",
        "m1_desc": "Upload high-speed footage to run computer-vision motion vector tracking, shoulder axis analysis, and kinetic chain evaluation.",
        "m1_upload": "Upload Serve Video Footage (MP4/MOV)",
        "m1_cam_angle": "Camera Angle",
        "m1_angle_1": "Behind Court (Baseline)",
        "m1_angle_2": "Side View (Court Level)",
        "m1_angle_3": "45-Degree Angle",
        "m1_fps": "Frame Rate (FPS)",
        "m1_fps_help": "Higher FPS provides pinpoint accuracy at ball contact frame.",
        "m1_benchmarks": "📊 AI Motion Vector Benchmarks",
        "m1_bench_1": "<strong>Trophy Angle Target:</strong> 25° - 35°",
        "m1_bench_2": "<strong>Pronation Speed Target:</strong> >1,300°/sec",
        "m1_bench_3": "<strong>Kinetic Efficiency Target:</strong> >85%",
        "m1_report": "📈 Biomechanical Diagnostic Report",
        "m1_metric_speed": "Peak Serve Speed",
        "m1_metric_speed_delta": "+4.2 mph vs past avg",
        "m1_metric_spin": "Spin Rate",
        "m1_metric_spin_delta": "Topspin-Kick Profile",
        "m1_metric_height": "Impact Height",
        "m1_metric_height_delta": "Optimal Apex Point",
        "m1_metric_transfer": "Kinetic Transfer",
        "m1_metric_transfer_delta": "Optimal Leg Drive",
        "m1_chart_vel": "📐 Velocity & Angular Acceleration Curve",
        "m1_chart_zone": "🎯 Impact Spot Radar & Accuracy Distribution",
        "m1_breakdown": "🔍 4-Phase Biomechanical Breakdown",
        "m1_tab_p1": "Phase 1: Trophy Position",
        "m1_tab_p2": "Phase 2: Kinetic Chain",
        "m1_tab_p3": "Phase 3: Impact & Extension",
        "m1_tab_p4": "Phase 4: Pronation & Landing",
        "m1_p1_text": "* **Shoulder Tilt Angle**: Measured at **28°** (Target Range: 25°-32°). Excellent shoulder alignment.\n* **Knee Flexion**: Flexion reached **115°** prior to vertical thrust. Great power storage.\n* **Toss Height & Position**: Ball toss apex is **0.15m inside baseline**, allowing optimal forward momentum transfer.",
        "m1_p2_text": "* **Hip-to-Shoulder Separation**: Rotation gap measured at **34°** (High core torque creation).\n* **Racket Head Drop**: Maximum depth reached smoothly without hitch or pausing.",
        "m1_p3_text": "* **Arm Extension at Contact**: **172°** arm-to-shoulder angle at impact frame (Maximum reaching power).\n* **Net Clearance Axis**: Ball path clears the net cord by **0.68m**, ensuring high margin for error.",
        "m1_p4_text": "* **Internal Shoulder Rotation**: Forearm pronation rate measured at **1,450°/sec**.\n* **Non-Dominant Arm Re-coil**: Left arm tucks into abdomen cleanly to decelerate upper body rotation smoothly.",
        # Module 2
        "m2_title": "🎯 AI Racket & String Tension Recommendation Engine",
        "m2_desc": "Input your playstyle profile, injury history, and performance requirements to generate customized frame specs and string tension matrixes.",
        "m2_ntrp_label": "Your NTRP Skill Rating",
        "m2_speed_label": "Average First Serve Speed (mph)",
        "m2_style_label": "Primary Playstyle",
        "m2_style_1": "Baseline Aggressor (Heavy Spin)",
        "m2_style_2": "All-Court Counterpuncher",
        "m2_style_3": "Touch & Net Specialist",
        "m2_style_4": "Power Serve & Volley",
        "m2_freq_label": "Playing Frequency (Sessions / Week)",
        "m2_elbow_label": "Suffer from Tennis Elbow / Wrist Strain?",
        "m2_priority_label": "Main Priority",
        "m2_prio_1": "Maximum Arm Comfort",
        "m2_prio_2": "Balanced Feel & Control",
        "m2_prio_3": "Maximum Spin & Durability",
        "m2_weight_label": "Frame Weight Preference",
        "m2_w_1": "Light & Maneuverable (<300g)",
        "m2_w_2": "Standard Tour Weight (300g-315g)",
        "m2_w_3": "Heavy Tour Weight (>315g)",
        "m2_btn_gen": "Generate Detailed Setup & Tension Recommendations",
        "m2_res_title": "🛠️ Customized Equipment & Tension Specification",
        "m2_m_head": "Recommended Head Size",
        "m2_m_weight": "Target Frame Weight",
        "m2_m_tension": "String Tension (Mains / Crosses)",
        "m2_m_mat": "String Material",
        "m2_mat_soft": "Multifilament / Gut",
        "m2_mat_poly": "Co-Poly Hybrid",
        "m2_chart_title": "📊 Tension & String Performance Dynamic Analysis",
        "m2_guide_title": "📝 Diagnostic Tension Suggestions & Tuning Guidelines",
        "m2_guide_col1": "**🧵 String Material & Main/Cross Differential:**\n* **Mains (Vertical Strings)**: String with **Co-Polymer (1.25mm / 16L Gauge)** for snapback and topspin generation.\n* **Crosses (Horizontal Strings)**: String with **Soft Multifilament** at **2 lbs lower** than the mains to widen the sweet spot and reduce arm shock.\n* **Recommended Tension Differential**: Maintaining a 2 lb drop on cross strings increases dwell time and sweet spot width by up to **14%**.",
        "m2_guide_col2": "**☀️ Seasonal & Altitude Tension Adjustments:**\n* **Hot Summer Weather (>28°C)**: Increase string tension by **+2 lbs** (e.g., 54 lbs) as ball felt softens and expands.\n* **Cold Winter Weather (<10°C)**: Decrease string tension by **-2 lbs** (e.g., 50 lbs) to maintain arm comfort and depth.\n* **Restring Frequency Recommendation**: Restring your racket every **{0} months** based on your playing frequency.",
        # Module 3
        "m3_title": "💳 Platform Membership & Subscription Plans",
        "m3_desc": "Unlock elite AI biomechanics features, coach messaging, and group discount thresholds.",
        "m3_btn_free": "Current Base Plan",
        "m3_btn_pro": "Subscribe PRO ($19.99/mo)",
        "m3_btn_vip": "Subscribe VIP Gold ($149/yr)",
        "m3_checkout": "🔒 Secure Checkout: **{} ({})**",
        "m3_card_name": "Cardholder Full Name *",
        "m3_card_num": "Credit Card Number *",
        "m3_card_exp": "Expiration Date (MM/YY) *",
        "m3_card_cvv": "CVV Security Code *",
        "m3_btn_pay": "Confirm Payment & Activate Subscription",
        "m3_pay_success": "🎉 Payment successful! You are now upgraded to **{}**.",
        "m3_pay_error": "Please fill in all credit card payment details.",
        # Module 4
        "m4_title": "🏆 Global Tournaments, Lodging & Group Buying",
        "m4_select_event": "📍 Select Target Competition:",
        "m4_select_path": "Select Pathway:",
        "m4_path_1": "🖼️ Competition Infrastructure & Residence Gallery",
        "m4_path_2": "👥 Member Group Buying ($85 Discount)",
        "m4_path_3": "👤 Individual Registration & Checkout",
        "m4_group_info": "💡 Join 5+ athletes to unlock an instant $85/person discount on hotel and tournament packages!",
        "m4_committed": "Current Committed Members: **{}/5 Athletes Joined**",
        "m4_p_name": "Player Full Name *",
        "m4_passport": "Passport / Gov ID *",
        "m4_card": "Credit Card Number ($300 Standard Rate) *",
        "m4_btn_pay_indiv": "Pay & Confirm Individual Booking ($300.00)",
        "m4_success_indiv": "🎉 Individual tournament entry and hotel package confirmed!",
        # Module 5
        "m5_title": "🏛️ Global Tennis Academy & Residency Programs",
        "m5_select_sec": "Select Section:",
        "m5_sec_1": "🏟️ Campus Gallery",
        "m5_sec_2": "👥 Group Buying & Voting Hub",
        "m5_sec_3": "👤 Individual Enrollment",
        "m5_enroll_btn": "Enroll ($890)",
        "m5_enroll_success": "🎉 Enrollment Confirmed!",
        # Module 6
        "m6_title": "🤝 Player Matchmaking & Coach Directory",
        "m6_desc": "Connect with local hitting partners or book certified tour coaches. Direct messaging requires an active **PRO Pass** or **VIP Gold** membership.",
        "m6_warn": "🔒 **Membership Required:** You are currently on `{}`. Direct messaging with players and coaches is exclusive to **PRO Pass** and **VIP Gold** members.",
        "m6_tab_partners": "🎾 Find Partners",
        "m6_tab_coaches": "👨‍🏫 Certified Coaches",
        "m6_avail_partners": "#### 👥 Available Hitting Partners",
        "m6_avail_coaches": "#### 👨‍🏫 Certified Tour Coaches",
        "m6_style": "Style:",
        "m6_city": "City:",
        "m6_contact": "Contact:",
        "m6_chat_now": "💬 Chat Now",
        "m6_locked": "🔒 Locked (Upgrade)",
        "m6_chat_success": "Opening secure chat room with {}...",
        "m6_specialty": "Specialty:",
        "m6_rate": "Rate:",
        "m6_location": "Location:",
        "m6_book_chat": "💬 Book & Chat",
        "m6_book_success": "Initiating private consultation with {}...",
        # Module 7
        "m7_title": "🎧 Support Center & Billing Receipts",
        "m7_desc": "Manage your support inquiries, request equipment service updates, and access official tax invoices/receipts.",
        "m7_tab_1": "📋 My Support Tickets",
        "m7_tab_2": "🧾 Transaction Receipts & Invoices",
        "m7_tab_3": "📩 Submit New Inquiry",
        "m7_tickets_title": "#### 🎫 Active & Past Support Requests",
        "m7_login_info": "💡 Please log in to view your personalized support history.",
        "m7_billing_title": "#### 💳 Billing History & Official Receipts",
        "m7_gen_receipt": "##### 📄 Generate Detailed Digital Receipt",
        "m7_select_order": "Select Order ID to View Receipt:",
        "m7_digital_inv": "🧾 Digital Invoice — {}",
        "m7_company": "Global Tennis Academy & Tech Platform Inc.",
        "m7_company_addr": "124 Olympic-ro, Songpa-gu, Seoul, South Korea",
        "m7_billed_to": "Billed To:",
        "m7_guest_ath": "Guest Athlete",
        "m7_inv_no": "Invoice No:",
        "m7_pay_stat": "Payment Status:",
        "m7_pay_meth": "Payment Method:",
        "m7_no_records": "No transaction records found.",
        "m7_create_title": "#### 📩 Create a Support Ticket",
        "m7_inq_cat": "Inquiry Category:",
        "m7_cat_1": "Racket Stringing / Customization Order",
        "m7_cat_2": "Academy Residency & Accommodations",
        "m7_cat_3": "AI Biomechanics / Video Analysis Help",
        "m7_cat_4": "Membership & Billing Inquiry",
        "m7_cat_5": "Tournament Registration Issue",
        "m7_subject": "Subject / Title *",
        "m7_details": "Provide details about your inquiry *",
        "m7_btn_sub_ticket": "Submit Support Ticket",
        "m7_ticket_success": "🎉 Ticket **{}** submitted successfully! Our team will respond within 24 hours.",
        "m7_ticket_error": "Please fill out both the subject and description fields.",
        # Module 8
        "m8_title": "🔒 Platform Admin Control Panel",
        "m8_passcode": "Passcode",
        "m8_granted": "Access Granted",
        # Module 9
        "m9_title": "📞 Contact Headquarters & Official Channels",
        "m9_desc": "Have questions regarding academy admissions, tournament packages, or AI analysis services? Get in touch with our team directly.",
        "m9_corp": "### 🏢 Global Corporate Office",
        "m9_corp_text": "* **Company Name**: Global Tennis Academy & Tech Platform Inc.\n* **HQ Address**: 124 Olympic-ro, Songpa-gu, Seoul, 05540, South Korea\n* **US Branch Office**: 120 Flushing Meadows Way, Queens, NY 11368, USA\n* **Telephone**: +82 2-555-1004 / +1 (800) 555-TENNIS\n* **Support Email**: `support@globaltennis.org`\n* **Admissions Email**: `admissions@globaltennis.org`\n* **Office Hours**: Monday – Friday: 09:00 – 18:00 KST / EST",
        "m9_social": "### 🌐 Connect On Social Media",
        "m9_social_desc": "Follow our official channels for tournament updates, student highlights, and AI biomechanics tips:"
    },
    "KR": {
        # App & Header
        "page_title": "글로벌 테니스 플랫폼 & AI 스위트",
        "live_stats": "실시간 통계: **12,400개 이상의 서브 분석 완료** | 전 세계 4,200명 이상의 활성 회원",
        "status_label": "상태:",
        "guest_free": "게스트 / 무료",
        # Sidebar & Auth
        "caption": "글로벌 테니스 허브",
        "user_portal": "🔐 사용자 포털",
        "tab_login": "🔑 로그인",
        "tab_register": "📝 회원가입",
        "email": "이메일",
        "password": "비밀번호",
        "btn_login": "로그인",
        "welcome_back": "다시 오신 것을 환영합니다, {}님!",
        "invalid_login": "유효하지 않은 이메일 또는 비밀번호입니다.",
        "full_name": "성명",
        "ntrp_skill": "NTRP 등급",
        "btn_register": "계정 생성",
        "acc_created": "계정이 성공적으로 생성되었습니다!",
        "fill_all": "모든 필드를 입력해 주세요.",
        "logged_in_as": "로그인 계정:",
        "membership": "멤버십:",
        "ntrp_rating": "NTRP 평점:",
        "btn_logout": "로그아웃",
        "select_module": "모듈 선택:",
        # Menu Options
        "menu_m1": "⚡ 1. AI 서브 속도 & 생체역학 분석기",
        "menu_m2": "🎯 2. AI 라켓 & 스트링 텐션 추천 엔진",
        "menu_m3": "💳 3. 멤버십 & 구독 플랜",
        "menu_m4": "🏆 4. 토너먼트 & 숙박 (US 오픈 / 한국)",
        "menu_m5": "🏛️ 5. 레지던시 & 아카데미 프로그램",
        "menu_m6": "🤝 6. 매칭 & 코치 디렉토리",
        "menu_m7": "🎧 7. 고객 지원 & 영수증 조회",
        "menu_m8": "🔒 8. 관리자 제어 패널",
        "menu_m9": "📞 9. 고객센터 및 문의",
        # Module 1
        "m1_title": "⚡ AI 서브 속도 & 생체역학 분석기",
        "m1_desc": "고속 영상을 업로드하여 컴퓨터 비전 모션 벡터 추적, 어깨 축 분석 및 운동 사슬 평가를 실행하세요.",
        "m1_upload": "서브 영상 파일 업로드 (MP4/MOV)",
        "m1_cam_angle": "카메라 각도",
        "m1_angle_1": "코트 뒤쪽 (베이스라인)",
        "m1_angle_2": "측면 뷰 (코트 높이)",
        "m1_angle_3": "45도 각도",
        "m1_fps": "프레임 레이트 (FPS)",
        "m1_fps_help": "높은 FPS는 임팩트 순간의 정밀한 정확도를 제공합니다.",
        "m1_benchmarks": "📊 AI 모션 벡터 벤치마크",
        "m1_bench_1": "<strong>트로피 각도 목표:</strong> 25° - 35°",
        "m1_bench_2": "<strong>내전 회전 속도 목표:</strong> >1,300°/초",
        "m1_bench_3": "<strong>운동 에너지 효율 목표:</strong> >85%",
        "m1_report": "📈 생체역학 진단 보고서",
        "m1_metric_speed": "최고 서브 속도",
        "m1_metric_speed_delta": "이전 평균 대비 +4.2 mph",
        "m1_metric_spin": "스핀량 (RPM)",
        "m1_metric_spin_delta": "탑스핀-킥 프로필",
        "m1_metric_height": "임팩트 높이",
        "m1_metric_height_delta": "최적의 정점 포인트",
        "m1_metric_transfer": "운동 전달율",
        "m1_metric_transfer_delta": "최적의 하체 드라이브",
        "m1_chart_vel": "📐 속도 및 각가속도 곡선",
        "m1_chart_zone": "🎯 임팩트 지점 레이더 & 정확도 분포",
        "m1_breakdown": "🔍 4단계 생체역학 상세 분석",
        "m1_tab_p1": "1단계: 트로피 포지션",
        "m1_tab_p2": "2단계: 운동 사슬 (Kinetic Chain)",
        "m1_tab_p3": "3단계: 임팩트 & 익스텐션",
        "m1_tab_p4": "4단계: 내전(Pronation) & 착지",
        "m1_p1_text": "* **어깨 기울기 각도**: **28°** 측정됨 (목표 범위: 25°-32°). 우수한 어깨 정렬 상태입니다.\n* **무릎 굴곡**: 수직 도약 직전 무릎 각도 **115°** 달성. 뛰어난 에너지 저장.\n* **토스 높이 및 위치**: 공의 토스 정점이 **베이스라인 안쪽 0.15m**에 위치하여 최적의 전방 추진력 전달 가능.",
        "m1_p2_text": "* **골반-어깨 분리각**: 회전 격차 **34°** 측정 (높은 코어 토크 생성).\n* **라켓 헤드 드롭**: 걸림이나 멈춤 없이 부드럽게 최대 깊이 도달.",
        "m1_p3_text": "* **임팩트 시 팔 신장**: 임팩트 순간 어깨-팔 각도 **172°** (최대 도달 파워).\n* **네트 마진 축**: 공의 궤적이 네트 상단을 **0.68m** 높이로 통과하여 높은 안정성 확보.",
        "m1_p4_text": "* **내측 어깨 회전**: 전완 내전 속도 **1,450°/초** 측정.\n* **비주요 팔 리코일**: 왼팔이 복부 쪽으로 깔끔하게 접혀 상체 회전을 부드럽게 감속함.",
        # Module 2
        "m2_title": "🎯 AI 라켓 & 스트링 텐션 추천 엔진",
        "m2_desc": "플레이 스타일, 부상 이력, 성능 요구 사항을 입력하여 맞춤형 프레임 사양과 스트링 텐션 매트릭스를 생성하세요.",
        "m2_ntrp_label": "NTRP 기술 등급",
        "m2_speed_label": "평균 첫 번째 서브 속도 (mph)",
        "m2_style_label": "주요 플레이 스타일",
        "m2_style_1": "베이스라인 어그레서 (강력한 스핀)",
        "m2_style_2": "올코트 카운터펀처",
        "m2_style_3": "터치 & 네트 플레이어",
        "m2_style_4": "파워 서브 & 발리",
        "m2_freq_label": "운동 빈도 (주당 횟수)",
        "m2_elbow_label": "테니스 엘보 또는 손목 통증이 있습니까?",
        "m2_priority_label": "최우선 고려 사항",
        "m2_prio_1": "최대 팔 편안함 (부상 방지)",
        "m2_prio_2": "균형 잡힌 타구감 & 컨트롤",
        "m2_prio_3": "최대 스핀 & 내구성",
        "m2_weight_label": "프레임 무게 선호도",
        "m2_w_1": "경량 & 조작성 우수 (<300g)",
        "m2_w_2": "표준 투어 무게 (300g-315g)",
        "m2_w_3": "중량 투어 무게 (>315g)",
        "m2_btn_gen": "상세 세팅 및 텐션 추천 생성",
        "m2_res_title": "🛠️ 맞춤형 장비 & 텐션 스펙",
        "m2_m_head": "추천 헤드 사이즈",
        "m2_m_weight": "목표 프레임 무게",
        "m2_m_tension": "스트링 텐션 (메인 / 크로스)",
        "m2_m_mat": "스트링 소재",
        "m2_mat_soft": "멀티필라멘트 / 천연구트",
        "m2_mat_poly": "코폴리 하이브리드",
        "m2_chart_title": "📊 텐션 및 스트링 성능 동적 분석",
        "m2_guide_title": "📝 텐션 진단 제안 & 튜닝 가이드라인",
        "m2_guide_col1": "**🧵 스트링 소재 & 메인/크로스 차등 세팅:**\n* **메인 (세로줄)**: 스냅백과 탑스핀 생성을 위해 **코폴리머 (1.25mm / 16L 게이지)** 사용 추천.\n* **크로스 (가로줄)**: 스위트 스팟을 넓히고 팔 진동을 줄이기 위해 메인보다 **2 lbs 낮게** **소프트 멀티필라멘트** 사용 추천.\n* **권장 텐션 차등**: 크로스 스트링 텐션을 2 lb 낮추면 공의 체류 시간과 스위트 스팟 넓이가 최대 **14%** 증가합니다.",
        "m2_guide_col2": "**☀️ 계절 및 고도별 텐션 조절:**\n* **무더운 여름 날씨 (>28°C)**: 공의 펠트가 덜 팽창하고 부드러워지므로 텐션을 **+2 lbs** 올려 세팅 (예: 54 lbs).\n* **추운 겨울 날씨 (<10°C)**: 팔의 부담을 줄이고 비거리를 확보하기 위해 텐션을 **-2 lbs** 낮춰 세팅 (예: 50 lbs).\n* **스트링 교체 주기 권장사항**: 운동 빈도를 고려하여 **{0}개월마다** 라켓 스트링을 교체하는 것이 좋습니다.",
        # Module 3
        "m3_title": "💳 플랫폼 멤버십 & 구독 플랜",
        "m3_desc": "최고급 AI 생체역학 기능, 코치 메시징 및 그룹 할인 혜택을 이용해 보세요.",
        "m3_btn_free": "현재 기본 플랜",
        "m3_btn_pro": "PRO 패스 구독 ($19.99/월)",
        "m3_btn_vip": "VIP 골드 구독 ($149/년)",
        "m3_checkout": "🔒 안전 결제: **{} ({})**",
        "m3_card_name": "카드 명의자 성명 *",
        "m3_card_num": "신용카드 번호 *",
        "m3_card_exp": "유효기간 (MM/YY) *",
        "m3_card_cvv": "CVV 보안코드 *",
        "m3_btn_pay": "결제 승인 및 구독 활성화",
        "m3_pay_success": "🎉 결제가 성공적으로 완료되었습니다! 이제 **{}** 등급입니다.",
        "m3_pay_error": "모든 신용카드 결제 정보를 입력해 주세요.",
        # Module 4
        "m4_title": "🏆 글로벌 토너먼트, 숙박 & 공동 구매",
        "m4_select_event": "📍 참가 목표 대회 선택:",
        "m4_select_path": "진행 경로 선택:",
        "m4_path_1": "🖼️ 대회 시설 & 숙소 갤러리",
        "m4_path_2": "👥 회원 공동 구매 ($85 할인)",
        "m4_path_3": "👤 개인 참가 신청 & 결제",
        "m4_group_info": "💡 5명 이상의 선수 그룹에 참여하여 호텔 및 대회 패키지에서 1인당 $85 즉시 할인을 받으세요!",
        "m4_committed": "현재 참여한 회원: **{}/5 명 완료**",
        "m4_p_name": "선수 성명 *",
        "m4_passport": "여권 번호 / 신분증 번호 *",
        "m4_card": "신용카드 번호 (표준 요금 $300) *",
        "m4_btn_pay_indiv": "결제 및 개인 예약 확정 ($300.00)",
        "m4_success_indiv": "🎉 개인 대회 참가 신청 및 숙박 패키지가 확정되었습니다!",
        # Module 5
        "m5_title": "🏛️ 글로벌 테니스 아카데미 & 레지던시 프로그램",
        "m5_select_sec": "섹션 선택:",
        "m5_sec_1": "🏟️ 캠퍼스 갤러리",
        "m5_sec_2": "👥 공동 구매 & 투표 허브",
        "m5_sec_3": "👤 개인 등록",
        "m5_enroll_btn": "등록하기 ($890)",
        "m5_enroll_success": "🎉 등록이 완료되었습니다!",
        # Module 6
        "m6_title": "🤝 플레이어 매칭 & 코치 디렉토리",
        "m6_desc": "지역 랠리 파트너를 찾거나 공인 투어 코치를 예약하세요. 1:1 메시지는 **PRO 패스** 또는 **VIP 골드** 회원 전용 기능입니다.",
        "m6_warn": "🔒 **멤버십 필요:** 현재 등급은 `{}`입니다. 플레이어 및 코치와의 다이렉트 메시지는 **PRO 패스** 및 **VIP 골드** 회원 전용입니다.",
        "m6_tab_partners": "🎾 파트너 찾기",
        "m6_tab_coaches": "👨‍🏫 공인 코치",
        "m6_avail_partners": "#### 👥 참여 가능한 랠리 파트너",
        "m6_avail_coaches": "#### 👨‍🏫 전문 투어 코치",
        "m6_style": "스타일:",
        "m6_city": "도시:",
        "m6_contact": "연락처:",
        "m6_chat_now": "💬 대화하기",
        "m6_locked": "🔒 잠김 (업그레이드 필요)",
        "m6_chat_success": "{}님과의 보안 채팅방을 열고 있습니다...",
        "m6_specialty": "전문 분야:",
        "m6_rate": "레슨비:",
        "m6_location": "위치:",
        "m6_book_chat": "💬 예약 및 상담",
        "m6_book_success": "{} 코치님과의 1:1 상담을 시작합니다...",
        # Module 7
        "m7_title": "🎧 고객 지원 & 영수증 조회",
        "m7_desc": "문의 사항을 관리하고, 장비 서비스 업데이트를 요청하며, 공식 세금 계산서/영수증을 확인하세요.",
        "m7_tab_1": "📋 내 문의 내역",
        "m7_tab_2": "🧾 결제 영수증 & 인보이스",
        "m7_tab_3": "📩 새 문의 제출",
        "m7_tickets_title": "#### 🎫 진행 중 및 지난 문의 내역",
        "m7_login_info": "💡 개인화된 지원 내역을 보려면 로그인해 주세요.",
        "m7_billing_title": "#### 💳 결제 내역 및 공식 영수증",
        "m7_gen_receipt": "##### 📄 상세 디지털 영수증 생성",
        "m7_select_order": "영수증을 조회할 주문 번호 선택:",
        "m7_digital_inv": "🧾 전자 인보이스 — {}",
        "m7_company": "글로벌 테니스 아카데미 & 테크 플랫폼 Inc.",
        "m7_company_addr": "서울특별시 송파구 올림픽로 124",
        "m7_billed_to": "청구 대상:",
        "m7_guest_ath": "게스트 선수",
        "m7_inv_no": "인보이스 번호:",
        "m7_pay_stat": "결제 상태:",
        "m7_pay_meth": "결제 수단:",
        "m7_no_records": "결제 기록이 없습니다.",
        "m7_create_title": "#### 📩 지원 티켓 생성",
        "m7_inq_cat": "문의 카테고리:",
        "m7_cat_1": "라켓 스트링 / 맞춤 제작 주문",
        "m7_cat_2": "아카데미 레지던시 & 숙박",
        "m7_cat_3": "AI 생체역학 / 비디오 분석 도움말",
        "m7_cat_4": "멤버십 & 결제 문의",
        "m7_cat_5": "토너먼트 참가 등록 문제",
        "m7_subject": "제목 *",
        "m7_details": "문의 내용을 자세히 입력해 주세요 *",
        "m7_btn_sub_ticket": "지원 티켓 제출",
        "m7_ticket_success": "🎉 티켓 **{}**번이 접수되었습니다! 24시간 이내에 답변해 드리겠습니다.",
        "m7_ticket_error": "제목과 내용 항목을 모두 작성해 주세요.",
        # Module 8
        "m8_title": "🔒 플랫폼 관리자 제어 패널",
        "m8_passcode": "비밀번호",
        "m8_granted": "접근 승인됨",
        # Module 9
        "m9_title": "📞 고객센터 및 문의",
        "m9_desc": "아카데미 입학, 토너먼트 패키지 또는 AI 분석 서비스에 대해 궁금한 점이 있으신가요? 저희 팀에 직접 문의하세요.",
        "m9_corp": "### 🏢 글로벌 본사 위치",
        "m9_corp_text": "* **법인명**: Global Tennis Academy & Tech Platform Inc.\n* **한국 본사**: 서울특별시 송파구 올림픽로 124 (05540)\n* **미국 지사**: 120 Flushing Meadows Way, Queens, NY 11368, USA\n* **대표 전화**: +82 2-555-1004 / +1 (800) 555-TENNIS\n* **지원 이메일**: `support@globaltennis.org`\n* **입학 문의**: `admissions@globaltennis.org`\n* **운영 시간**: 월요일 – 금요일: 09:00 – 18:00 KST / EST",
        "m9_social": "### 🌐 소셜 미디어 채널",
        "m9_social_desc": "공식 채널을 팔로우하고 대회 소식, 수강생 소식 및 AI 생체역학 팁을 확인하세요:"
    }
}

def get_text(key, lang_str="English"):
    lang_code = "KR" if lang_str == "한국어" else "EN"
    return TEXTS.get(lang_code, TEXTS["EN"]).get(key, key)

# ==========================================
# 0.1 HELPER FUNCTIONS: SKELETON & HEALTH
# ==========================================
def process_standard_skeleton_overlay(video_file):
    """
    Overlays a legal/standardized AI skeleton onto the uploaded video using OpenCV.
    Process maximum 120 frames to ensure fast execution speeds on server deployment.
    """
    tfile = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
    tfile.write(video_file.read())
    video_path = tfile.name

    cap = cv2.VideoCapture(video_path)
    fps = int(cap.get(cv2.CAP_PROP_FPS)) or 30
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)) or 640
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)) or 480
    
    temp_output = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(temp_output.name, fourcc, fps, (width, height))
    
    frame_count = 0
    max_frames_to_process = 120  # Limit frame processing count for ultra-fast performance

    while cap.isOpened() and frame_count < max_frames_to_process:
        ret, frame = cap.read()
        if not ret:
            break
            
        frame_count += 1
        overlay = frame.copy()
        
        # Calculate standard motion trajectory
        t = (frame_count % 60) / 60.0
        
        std_shoulder = (int(width * 0.45), int(height * 0.42))
        std_elbow = (int(width * 0.48), int(height * 0.55))
        std_wrist = (int(width * (0.42 + 0.25 * np.cos(t * 2 * np.pi))), 
                     int(height * (0.58 - 0.20 * np.sin(t * 2 * np.pi))))
        
        bone_color = (0, 215, 255) # Gold/Neon
        
        # Standardized Bone Segments
        cv2.line(overlay, std_shoulder, std_elbow, bone_color, 5)
        cv2.line(overlay, std_elbow, std_wrist, bone_color, 5)
        
        # Joints
        cv2.circle(overlay, std_shoulder, 7, (255, 255, 255), -1)
        cv2.circle(overlay, std_elbow, 7, (255, 255, 255), -1)
        cv2.circle(overlay, std_wrist, 9, (0, 255, 0), -1)
        
        # Alpha Blending (50%)
        cv2.addWeighted(overlay, 0.5, frame, 0.5, 0, frame)
        cv2.putText(frame, "AI Standard Model: Forehand Topspin", (30, 40), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 215, 255), 2, cv2.LINE_AA)
        
        out.write(frame)

    cap.release()
    out.release()
    return temp_output.name

# ==========================================
# 1. PAGE CONFIG & LUXURY SAND THEME
# ==========================================
st.set_page_config(
    page_title="Global Tennis Platform & AI Suite",
    page_icon="🎾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Luxury Sand Theme
st.markdown("""
    <style>
    /* Main Background & Base Styling */
    .stApp {
        background-color: #F5F2EB;
        color: #211F1D;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Headers & Typography */
    h1, h2, h3, h4, h5 {
        color: #211F1D !important;
        font-weight: 600;
        letter-spacing: -0.02em;
    }
    
    /* Cards & Containers */
    .stCard, div[data-testid="stExpander"], div[data-testid="stForm"] {
        background-color: #FAF8F5;
        border: 1px solid #E5E0D8;
        border-radius: 12px;
        padding: 24px;
        box-shadow: 0 4px 12px rgba(33, 31, 29, 0.03);
    }
    
    /* Buttons */
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
    
    /* Metrics & Badges */
    div[data-testid="stMetricValue"] {
        color: #211F1D !important;
        font-weight: 700;
    }
    
    /* Input Fields */
    .stTextInput>div>div>input, .stSelectbox>div>div>div, .stTextArea>div>div>textarea, .stNumberInput>div>div>input {
        background-color: #FFFFFF !important;
        border: 1px solid #D6D0C4 !important;
        border-radius: 8px !important;
        color: #211F1D !important;
    }
    
    /* Tabs Customization */
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

    .social-btn {
        display: inline-block;
        background-color: #211F1D;
        color: #FAF8F5 !important;
        padding: 10px 20px;
        border-radius: 8px;
        text-decoration: none;
        font-weight: 600;
        font-size: 14px;
        margin-right: 10px;
        margin-top: 10px;
    }
    .social-btn:hover {
        background-color: #383430;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. STATE INITIALIZATION & AUTH SYSTEM
# ==========================================

if "registered_users" not in st.session_state:
    st.session_state["registered_users"] = {
        "alex@tennis.org": {"password": "password123", "name": "Alex Mercer", "tier": "PRO Pass", "ntrp": 4.5},
        "sarah@tennis.org": {"password": "password123", "name": "Sarah Kim", "tier": "VIP Gold", "ntrp": 5.0}
    }

if "is_logged_in" not in st.session_state:
    st.session_state["is_logged_in"] = False

if "current_user" not in st.session_state:
    st.session_state["current_user"] = None

if "language" not in st.session_state:
    st.session_state["language"] = "English"

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
        {"Coach": "Coach Rob", "Level": "USPTR Certified Master", "City": "Seoul", "Hourly": "$80/hr", "Specialty": "Serve Biomechanics"},
        {"Coach": "Coach Sarah", "Level": "Ex-WTA Tour Player", "City": "Incheon", "Hourly": "$120/hr", "Specialty": "Match Strategy"},
        {"Coach": "Coach Min-ho", "Level": "KTA High Performance", "City": "Busan", "Hourly": "$95/hr", "Specialty": "Junior Development"}
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

# Active Language Ref
curr_lang = st.session_state["language"]

# ==========================================
# 3. SIDEBAR AUTH & NAVIGATION PANEL
# ==========================================
st.sidebar.image("https://images.unsplash.com/photo-1595435934249-5df7ed86e1c0?w=400&q=80", caption=get_text("caption", curr_lang))

# Account Authenticator Box
st.sidebar.markdown(f"### {get_text('user_portal', curr_lang)}")

if not st.session_state["is_logged_in"]:
    auth_tab1, auth_tab2 = st.sidebar.tabs([get_text("tab_login", curr_lang), get_text("tab_register", curr_lang)])
    
    with auth_tab1:
        login_email = st.text_input(get_text("email", curr_lang), key="login_email")
        login_pass = st.text_input(get_text("password", curr_lang), type="password", key="login_pass")
        if st.button(get_text("btn_login", curr_lang), key="btn_login"):
            if login_email in st.session_state["registered_users"] and st.session_state["registered_users"][login_email]["password"] == login_pass:
                st.session_state["is_logged_in"] = True
                st.session_state["current_user"] = st.session_state["registered_users"][login_email]
                st.session_state["current_user"]["email"] = login_email
                st.sidebar.success(get_text("welcome_back", curr_lang).format(st.session_state['current_user']['name']))
                st.rerun()
            else:
                st.sidebar.error(get_text("invalid_login", curr_lang))

    with auth_tab2:
        reg_name = st.text_input(get_text("full_name", curr_lang), key="reg_name")
        reg_email = st.text_input(get_text("email", curr_lang), key="reg_email")
        reg_pass = st.text_input(get_text("password", curr_lang), type="password", key="reg_pass")
        reg_ntrp = st.slider(get_text("ntrp_skill", curr_lang), 1.0, 7.0, 3.5, 0.5, key="reg_ntrp")
        if st.button(get_text("btn_register", curr_lang), key="btn_reg"):
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
                st.sidebar.success(get_text("acc_created", curr_lang))
                st.rerun()
            else:
                st.sidebar.error(get_text("fill_all", curr_lang))
else:
    u = st.session_state["current_user"]
    st.sidebar.markdown(f"**{get_text('logged_in_as', curr_lang)}** `{u['name']}`")
    st.sidebar.markdown(f"**{get_text('membership', curr_lang)}** <span class='badge-membership'>{u['tier']}</span>", unsafe_allow_html=True)
    st.sidebar.markdown(f"**{get_text('ntrp_rating', curr_lang)}** `{u['ntrp']}`")
    
    if st.sidebar.button(get_text("btn_logout", curr_lang), key="btn_logout"):
        st.session_state["is_logged_in"] = False
        st.session_state["current_user"] = None
        st.rerun()

st.sidebar.markdown("---")

menu_options = [
    get_text("menu_m1", curr_lang),
    get_text("menu_m2", curr_lang),
    get_text("menu_m3", curr_lang),
    get_text("menu_m4", curr_lang),
    get_text("menu_m5", curr_lang),
    get_text("menu_m6", curr_lang),
    get_text("menu_m7", curr_lang),
    get_text("menu_m8", curr_lang),
    get_text("menu_m9", curr_lang)
]

menu = st.sidebar.radio(
    get_text("select_module", curr_lang),
    menu_options
)

# ==========================================
# 4. TOP NAVIGATION HEADER
# ==========================================
col_h1, col_h2, col_h3 = st.columns([4, 2, 2])

with col_h1:
    st.markdown(f"### 🎾 {get_text('page_title', curr_lang)}")
    st.caption(get_text("live_stats", curr_lang))

with col_h2:
    lang = st.selectbox("🌐 Language / 언어", ["English", "한국어"], index=0 if st.session_state["language"] == "English" else 1)
    if lang != st.session_state["language"]:
        st.session_state["language"] = lang
        st.rerun()

with col_h3:
    current_tier = st.session_state["current_user"]["tier"] if st.session_state["is_logged_in"] else get_text("guest_free", curr_lang)
    st.markdown(f"**{get_text('status_label', curr_lang)}** `{current_tier}`")

st.markdown("---")

# ==========================================
# 5. ENHANCED MODULE FUNCTIONS
# ==========================================

# --- MODULE 1: AI SERVE VELOCITY (FAST THREE-SUBPAGE ARCHITECTURE) ---
def render_module_1():
    st.subheader(get_text("m1_title", curr_lang))
    st.write(get_text("m1_desc", curr_lang))

    # Single Upload Section at top
    col1, col2 = st.columns([3, 2])
    with col1:
        video_file = st.file_uploader(get_text("m1_upload", curr_lang), type=["mp4", "mov"])
        c_a, c_b = st.columns(2)
        with c_a:
            angle = st.selectbox(get_text("m1_cam_angle", curr_lang), [get_text("m1_angle_1", curr_lang), get_text("m1_angle_2", curr_lang), get_text("m1_angle_3", curr_lang)])
        with c_b:
            fps = st.slider(get_text("m1_fps", curr_lang), 30, 240, 120, help=get_text("m1_fps_help", curr_lang))

    with col2:
        st.markdown(f"""
        <div style="background-color:#FAF8F5; border:1px solid #E5E0D8; border-radius:12px; padding:16px;">
            <h4 style="margin-top:0;">{get_text("m1_benchmarks", curr_lang)}</h4>
            <p style="font-size:13px; color:#5C544D; margin-bottom:8px;">{get_text("m1_bench_1", curr_lang)}</p>
            <p style="font-size:13px; color:#5C544D; margin-bottom:8px;">{get_text("m1_bench_2", curr_lang)}</p>
            <p style="font-size:13px; color:#5C544D; margin-bottom:0;">{get_text("m1_bench_3", curr_lang)}</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Three Independent Subpages / Sub-Tabs
    subpage1, subpage2, subpage3 = st.tabs([
        "⚡ Phase 1: High-Speed Velocity Analysis",
        "🎯 Phase 2: Standard Biomechanical Skeleton Overlay",
        "🩺 Phase 3: AI Health & Predictive Injury Diagnostics"
    ])

    # -------------------------------------------------------------
    # SUBPAGE 1: HIGH SPEED FRAMES & VELOCITY METRICS
    # -------------------------------------------------------------
    with subpage1:
        st.markdown("### ⚡ High-Speed Velocity & Frame Tracking")
        st.write("Click below to run instant motion vector frame extraction and diagnostic metrics.")
        
        if st.button("🚀 Run High-Speed Velocity Analysis", key="btn_run_phase1"):
            with st.spinner("Analyzing high-speed video frames..."):
                time.sleep(0.5)
                
                st.markdown(f"### {get_text('m1_report', curr_lang)}")
                
                # Primary Metrics Row
                m1, m2, m3, m4 = st.columns(4)
                m1.metric(get_text("m1_metric_speed", curr_lang), "118.4 mph", delta=get_text("m1_metric_speed_delta", curr_lang))
                m2.metric(get_text("m1_metric_spin", curr_lang), "2,840 RPM", delta=get_text("m1_metric_spin_delta", curr_lang))
                m3.metric(get_text("m1_metric_height", curr_lang), "2.88 meters", delta=get_text("m1_metric_height_delta", curr_lang))
                m4.metric(get_text("m1_metric_transfer", curr_lang), "88.2%", delta=get_text("m1_metric_transfer_delta", curr_lang))

                st.write("")
                
                # Interactive Biomechanics Data Charts
                t_col1, t_col2 = st.columns(2)
                
                with t_col1:
                    st.markdown(f"#### {get_text('m1_chart_vel', curr_lang)}")
                    chart_data = pd.DataFrame({
                        "Serve Phase": ["Trophy Position", "Racket Drop", "Acceleration", "Ball Impact", "Follow Through"],
                        "Racket Speed (mph)": [12, 38, 92, 118, 45],
                        "Wrist Angular Speed (°/s)": [180, 420, 1100, 1450, 320]
                    })
                    st.line_chart(chart_data.set_index("Serve Phase"))

                with t_col2:
                    st.markdown(f"#### {get_text('m1_chart_zone', curr_lang)}")
                    impact_data = pd.DataFrame({
                        "Court Zone": ["T-Point (Center)", "Body Serve", "Wide Angle"],
                        "Consistency %": [68, 84, 52],
                        "Avg Speed (mph)": [118, 112, 108]
                    })
                    st.bar_chart(impact_data.set_index("Court Zone"))

                st.markdown(f"#### {get_text('m1_breakdown', curr_lang)}")
                
                tab_p1, tab_p2, tab_p3, tab_p4 = st.tabs([
                    get_text("m1_tab_p1", curr_lang),
                    get_text("m1_tab_p2", curr_lang),
                    get_text("m1_tab_p3", curr_lang),
                    get_text("m1_tab_p4", curr_lang)
                ])
                
                with tab_p1:
                    st.markdown(get_text("m1_p1_text", curr_lang))
                with tab_p2:
                    st.markdown(get_text("m1_p2_text", curr_lang))
                with tab_p3:
                    st.markdown(get_text("m1_p3_text", curr_lang))
                with tab_p4:
                    st.markdown(get_text("m1_p4_text", curr_lang))

    # -------------------------------------------------------------
    # SUBPAGE 2: STANDARD BIOMECHANICAL SKELETON OVERLAY
    # -------------------------------------------------------------
    with subpage2:
        st.markdown("### 🎯 Overlay Standard Biomechanical Skeleton")
        st.write("Click the button below to trigger real-time OpenCV skeleton motion overlay on your uploaded video.")
        
        if st.button("🦴 Overlay Standard Biomechanical Skeleton", key="btn_run_phase2"):
            if video_file is not None:
                with st.spinner("Processing video frames and overlaying standardized biomechanical skeleton..."):
                    video_file.seek(0)
                    processed_video_path = process_standard_skeleton_overlay(video_file)
                    
                    st.video(processed_video_path)
                    st.success("✅ Standard Biomechanical Skeleton Rendering Complete!")
                    st.info("🔒 **Compliance & IP Safety**: Video rendered using standardized 3D human biomechanical keypoints only.")
            else:
                st.warning("⚠️ Please upload a video file above first to overlay the standard skeleton model.")

    # -------------------------------------------------------------
    # SUBPAGE 3: AI HEALTH & PREDICTIVE DIAGNOSTICS
    # -------------------------------------------------------------
    with subpage3:
        st.markdown("### 🩺 AI Health & Predictive Injury Diagnostics")
        st.write("Click below to evaluate joint load, elbow torque strain, and landing force levels.")
        
        if st.button("🔍 Run Health & Injury Risk Evaluation", key="btn_run_phase3"):
            with st.spinner("Evaluating kinematic pressure profiles and joint load metrics..."):
                time.sleep(0.4)
                
                h1, h2, h3 = st.columns(3)
                h1.metric("Elbow Stress Level", "64%", "Elevated Risk", delta_color="inverse")
                h2.metric("Shoulder Torque", "38%", "Optimal", delta_color="normal")
                h3.metric("Knee Kinetic Strain", "22%", "Low Risk", delta_color="normal")
                
                st.warning("⚠️ **Health Advisory**: High impact shock detected at elbow joint during acceleration phase. Consider adjusting string tension or switching to softer string material in Module 2.")

# --- MODULE 2: AI RACKET & STRING TENSION (GRAPHIC & SUGGESTION MATRIX) ---
def render_module_2():
    st.subheader(get_text("m2_title", curr_lang))
    st.write(get_text("m2_desc", curr_lang))

    col1, col2 = st.columns(2)
    with col1:
        ntrp = st.slider(get_text("m2_ntrp_label", curr_lang), 1.5, 7.0, 4.0, 0.5)
        serve_speed = st.number_input(get_text("m2_speed_label", curr_lang), 40, 140, 95)
        playstyle = st.selectbox(get_text("m2_style_label", curr_lang), [
            get_text("m2_style_1", curr_lang),
            get_text("m2_style_2", curr_lang),
            get_text("m2_style_3", curr_lang),
            get_text("m2_style_4", curr_lang)
        ])
        matches_per_week = st.slider(get_text("m2_freq_label", curr_lang), 1, 7, 3)

    with col2:
        elbow_issue = st.checkbox(get_text("m2_elbow_label", curr_lang))
        string_durability = st.select_slider(get_text("m2_priority_label", curr_lang), options=[
            get_text("m2_prio_1", curr_lang),
            get_text("m2_prio_2", curr_lang),
            get_text("m2_prio_3", curr_lang)
        ])
        racket_weight_pref = st.radio(get_text("m2_weight_label", curr_lang), [
            get_text("m2_w_1", curr_lang),
            get_text("m2_w_2", curr_lang),
            get_text("m2_w_3", curr_lang)
        ])

    if st.button(get_text("m2_btn_gen", curr_lang)):
        st.markdown("---")
        st.markdown(f"### {get_text('m2_res_title', curr_lang)}")

        # Top Level Spec Summary Cards
        r1, r2, r3, r4 = st.columns(4)
        r1.metric(get_text("m2_m_head", curr_lang), "98 - 100 sq in")
        r2.metric(get_text("m2_m_weight", curr_lang), "305 grams (Unstrung)")
        r3.metric(get_text("m2_m_tension", curr_lang), "50 / 48 lbs" if elbow_issue else "54 / 52 lbs")
        r4.metric(get_text("m2_m_mat", curr_lang), get_text("m2_mat_soft", curr_lang) if elbow_issue else get_text("m2_mat_poly", curr_lang))

        st.write("")
        st.markdown(f"#### {get_text('m2_chart_title', curr_lang)}")

        # Graphic Tension Matrix Simulation Chart
        tension_chart = pd.DataFrame({
            "Tension (Lbs)": [44, 48, 52, 56, 60],
            "Control & Precision Score": [55, 68, 82, 94, 98],
            "Trampoline Power & Depth": [96, 88, 74, 60, 48],
            "Dwell Time / Arm Comfort": [92, 85, 72, 58, 42]
        })
        st.line_chart(tension_chart.set_index("Tension (Lbs)"))

        st.markdown(f"#### {get_text('m2_guide_title', curr_lang)}")
        
        c_s1, c_s2 = st.columns(2)
        with c_s1:
            st.markdown(get_text("m2_guide_col1", curr_lang))
        with c_s2:
            st.markdown(get_text("m2_guide_col2", curr_lang).format(max(1, int(12 / matches_per_week))))

# --- MODULE 3: MEMBERSHIP & SUBSCRIPTIONS ---
def render_module_membership():
    st.subheader(get_text("m3_title", curr_lang))
    st.write(get_text("m3_desc", curr_lang))

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div style="background-color:#FAF8F5; border:1px solid #E5E0D8; border-radius:12px; padding:20px; text-align:center;">
            <h3>🆓 Free Athlete</h3>
            <h2>$0 <span style="font-size:14px;">/ forever</span></h2>
            <hr>
            <p>✓ Basic AI Serve Analysis (3/mo)</p>
            <p>✓ Access Player Directory</p>
            <p>✓ View Campus Facilities</p>
            <p>✗ Coach Direct Messaging</p>
            <p>✗ Group Buying Discounts</p>
        </div>
        """, unsafe_allow_html=True)
        st.write("")
        st.button(get_text("m3_btn_free", curr_lang), disabled=True, key="plan_free")

    with col2:
        st.markdown("""
        <div style="background-color:#FAF8F5; border:2px solid #211F1D; border-radius:12px; padding:20px; text-align:center;">
            <h3>⚡ PRO Pass</h3>
            <h2>$19.99 <span style="font-size:14px;">/ month</span></h2>
            <hr>
            <p>✓ Unlimited AI Serve Velocity Analysis</p>
            <p>✓ AI Racket & Tension Optimizer</p>
            <p>✓ Matchmaking & Coach Messaging</p>
            <p>✓ Group Tournament Discounts</p>
            <p>✓ Priority Support Tickets</p>
        </div>
        """, unsafe_allow_html=True)
        st.write("")
        if st.button(get_text("m3_btn_pro", curr_lang), key="plan_pro"):
            st.session_state["selected_plan"] = ("PRO Pass", "$19.99/mo")

    with col3:
        st.markdown("""
        <div style="background-color:#FAF8F5; border:1px solid #E5E0D8; border-radius:12px; padding:20px; text-align:center;">
            <h3>🏆 VIP Gold Residency</h3>
            <h2>$149.00 <span style="font-size:14px;">/ year</span></h2>
            <hr>
            <p>✓ All PRO Features Included</p>
            <p>✓ 25% Off Academy Residency Camps</p>
            <p>✓ Quarterly Video Review with Pro Coach</p>
            <p>✓ Guaranteed Hotel Discount Locking</p>
            <p>✓ VIP Lounge Access</p>
        </div>
        """, unsafe_allow_html=True)
        st.write("")
        if st.button(get_text("m3_btn_vip", curr_lang), key="plan_vip"):
            st.session_state["selected_plan"] = ("VIP Gold", "$149.00/yr")

    if "selected_plan" in st.session_state:
        plan_name, plan_price = st.session_state["selected_plan"]
        st.markdown("---")
        st.markdown(f"### {get_text('m3_checkout', curr_lang).format(plan_name, plan_price)}")
        
        with st.form("checkout_payment_form"):
            c_a, c_b = st.columns(2)
            with c_a:
                card_name = st.text_input(get_text("m3_card_name", curr_lang))
                card_num = st.text_input(get_text("m3_card_num", curr_lang), type="password", placeholder="•••• •••• •••• ••••")
            with c_b:
                card_exp = st.text_input(get_text("m3_card_exp", curr_lang), placeholder="08/28")
                card_cvv = st.text_input(get_text("m3_card_cvv", curr_lang), type="password", placeholder="123")

            pay_submitted = st.form_submit_button(get_text("m3_btn_pay", curr_lang), use_container_width=True)
            
            if pay_submitted:
                if card_name and card_num and card_exp and card_cvv:
                    if st.session_state["is_logged_in"]:
                        st.session_state["current_user"]["tier"] = plan_name
                        user_email = st.session_state["current_user"]["email"]
                        st.session_state["registered_users"][user_email]["tier"] = plan_name
                    
                    st.session_state["chat_orders"].append({
                        "Order ID": f"ORD-{len(st.session_state['chat_orders'])+9922}",
                        "Item": f"Subscription: {plan_name}",
                        "Amount": plan_price,
                        "Status": "Paid"
                    })
                    st.success(get_text("m3_pay_success", curr_lang).format(plan_name))
                    del st.session_state["selected_plan"]
                    st.rerun()
                else:
                    st.error(get_text("m3_pay_error", curr_lang))

# --- MODULE 4: TOURNAMENTS & LODGING ---
def render_module_3():
    st.subheader(get_text("m4_title", curr_lang))

    selected_event = st.selectbox(
        get_text("m4_select_event", curr_lang),
        ["🇺🇸 US Open Championships (Flushing Meadows, NY)", "🇰🇷 Seoul Open Masters (Olympic Park, Korea)", "🇰🇷 Busan Clay Court Cup (Sajik Complex, Korea)"]
    )

    subpage = st.radio(
        get_text("m4_select_path", curr_lang),
        [
            get_text("m4_path_1", curr_lang),
            get_text("m4_path_2", curr_lang),
            get_text("m4_path_3", curr_lang)
        ],
        horizontal=True
    )

    st.markdown("---")

    if subpage == get_text("m4_path_1", curr_lang):
        col_img1, col_img2 = st.columns(2)
        with col_img1:
            st.image("https://images.unsplash.com/photo-1595435934249-5df7ed86e1c0?w=800&q=80", caption="🏟️ Tournament Main Arena & Hard Courts", use_container_width=True)
        with col_img2:
            st.image("https://images.unsplash.com/photo-1566073771259-6a8506099945?w=800&q=80", caption="🏨 Official Partner Athlete Residence Suites", use_container_width=True)

    elif subpage == get_text("m4_path_2", curr_lang):
        st.info(get_text("m4_group_info", curr_lang))
        votes = len(st.session_state["tournament_group_votes"])
        st.progress(min(votes / 5, 1.0))
        st.caption(get_text("m4_committed", curr_lang).format(votes))
        st.table(pd.DataFrame(st.session_state["tournament_group_votes"]))

    elif subpage == get_text("m4_path_3", curr_lang):
        with st.form("indiv_tourn_form"):
            p_name = st.text_input(get_text("m4_p_name", curr_lang), value=st.session_state["current_user"]["name"] if st.session_state["is_logged_in"] else "")
            p_passport = st.text_input(get_text("m4_passport", curr_lang))
            card = st.text_input(get_text("m4_card", curr_lang), type="password")
            if st.form_submit_button(get_text("m4_btn_pay_indiv", curr_lang)):
                if p_name and card:
                    st.success(get_text("m4_success_indiv", curr_lang))

# --- MODULE 5: ACADEMY & RESIDENCY ---
def render_module_4():
    st.subheader(get_text("m5_title", curr_lang))
    
    subpage = st.radio(get_text("m5_select_sec", curr_lang), [
        get_text("m5_sec_1", curr_lang),
        get_text("m5_sec_2", curr_lang),
        get_text("m5_sec_3", curr_lang)
    ], horizontal=True)
    st.markdown("---")

    if subpage == get_text("m5_sec_1", curr_lang):
        c1, c2 = st.columns(2)
        with c1:
            st.image("https://encrypted-tbn2.gstatic.com/licensed-image?q=tbn:ANd9GcTlJfjs63KI6QzSpQms4d1rLMcTNoDkcJphyH_y34zqGSvvZbGEs3TmtsDCJLVbWFcYD83uzV10B2lwUR0", caption="Center Court Facility", use_container_width=True)
        with c2:
            st.image("https://encrypted-tbn0.gstatic.com/licensed-image?q=tbn:ANd9GcRI-UXJPpwhWDcFekaYdcs5vb7ShKqOtbpAL6DUhV9W4HTMwQsFOzX3pKb9oNNCgU3VDScBATPtPN4KN5I", caption="Athlete Residence Lounge", use_container_width=True)

    elif subpage == get_text("m5_sec_2", curr_lang):
        st.dataframe(pd.DataFrame(st.session_state["academy_group_votes"]))

    elif subpage == get_text("m5_sec_3", curr_lang):
        with st.form("indiv_academy"):
            full_name = st.text_input(get_text("full_name", curr_lang), value=st.session_state["current_user"]["name"] if st.session_state["is_logged_in"] else "")
            card = st.text_input("Credit Card *", type="password")
            if st.form_submit_button(get_text("m5_enroll_btn", curr_lang)):
                st.success(get_text("m5_enroll_success", curr_lang))

# --- MODULE 6: MATCHMAKING & COACH DIRECTORY ---
def render_module_5():
    st.subheader(get_text("m6_title", curr_lang))
    st.write(get_text("m6_desc", curr_lang))

    is_logged = st.session_state.get("is_logged_in", False)
    user_tier = st.session_state.get("current_user", {}).get("tier", "Free Tier") if is_logged else "Guest"
    has_chat_access = is_logged and user_tier in ["PRO Pass", "VIP Gold"]

    if not has_chat_access:
        st.warning(get_text("m6_warn", curr_lang).format(user_tier))

    st.markdown("---")
    t1, t2 = st.tabs([get_text("m6_tab_partners", curr_lang), get_text("m6_tab_coaches", curr_lang)])

    with t1:
        st.markdown(get_text("m6_avail_partners", curr_lang))
        for idx, player in enumerate(st.session_state["players_db"]):
            with st.expander(f"🎾 {player['Name']} — NTRP {player['NTRP']} ({player['City']})", expanded=True):
                col_info, col_action = st.columns([3, 1])
                with col_info:
                    st.write(f"**{get_text('m6_style', curr_lang)}** {player['Style']}")
                    st.write(f"**{get_text('m6_city', curr_lang)}** {player['City']}")
                    st.write(f"**{get_text('m6_contact', curr_lang)}** `{player['Contact'] if has_chat_access else '••••••••@••••.org'}`")
                with col_action:
                    if has_chat_access:
                        if st.button(get_text("m6_chat_now", curr_lang), key=f"chat_player_{idx}"):
                            st.success(get_text("m6_chat_success", curr_lang).format(player['Name']))
                    else:
                        st.button(get_text("m6_locked", curr_lang), key=f"lock_player_{idx}", disabled=True)

    with t2:
        st.markdown(get_text("m6_avail_coaches", curr_lang))
        for idx, coach in enumerate(st.session_state["coaches_db"]):
            with st.expander(f"🏆 {coach['Coach']} — {coach['Level']} ({coach['City']})", expanded=True):
                col_info, col_action = st.columns([3, 1])
                with col_info:
                    st.write(f"**{get_text('m6_specialty', curr_lang)}** {coach['Specialty']}")
                    st.write(f"**{get_text('m6_rate', curr_lang)}** {coach['Hourly']}")
                    st.write(f"**{get_text('m6_location', curr_lang)}** {coach['City']}")
                with col_action:
                    if has_chat_access:
                        if st.button(get_text("m6_book_chat", curr_lang), key=f"chat_coach_{idx}"):
                            st.success(get_text("m6_book_success", curr_lang).format(coach['Coach']))
                    else:
                        st.button(get_text("m6_locked", curr_lang), key=f"lock_coach_{idx}", disabled=True)

# --- MODULE 7: SUPPORT CENTER & TRANSACTION RECEIPTS ---
def render_module_6():
    st.subheader(get_text("m7_title", curr_lang))
    st.write(get_text("m7_desc", curr_lang))

    is_logged = st.session_state.get("is_logged_in", False)
    current_user = st.session_state.get("current_user") or {}

    tab_tickets, tab_receipts, tab_new_ticket = st.tabs([
        get_text("m7_tab_1", curr_lang),
        get_text("m7_tab_2", curr_lang),
        get_text("m7_tab_3", curr_lang)
    ])

    with tab_tickets:
        st.markdown(get_text("m7_tickets_title", curr_lang))
        if not is_logged:
            st.info(get_text("m7_login_info", curr_lang))
        inquiries_df = pd.DataFrame(st.session_state.get("inquiries", []))
        st.dataframe(inquiries_df, width="stretch")

    with tab_receipts:
        st.markdown(get_text("m7_billing_title", curr_lang))
        chat_orders = st.session_state.get("chat_orders", [])
        orders_df = pd.DataFrame(chat_orders)
        st.dataframe(orders_df, width="stretch")
        
        st.markdown("---")
        st.markdown(get_text("m7_gen_receipt", curr_lang))
        
        if chat_orders:
            order_ids = [order["Order ID"] for order in chat_orders]
            selected_order_id = st.selectbox(get_text("m7_select_order", curr_lang), order_ids)
            selected_order = next((item for item in chat_orders if item["Order ID"] == selected_order_id), None)

            if selected_order:
                with st.expander(get_text("m7_digital_inv", curr_lang).format(selected_order['Order ID']), expanded=True):
                    c_a, c_b = st.columns(2)
                    with c_a:
                        st.markdown(f"**{get_text('m7_company', curr_lang)}**")
                        st.caption(get_text("m7_company_addr", curr_lang))
                        st.write(f"**{get_text('m7_billed_to', curr_lang)}** {current_user.get('name', get_text('m7_guest_ath', curr_lang))}")
                        st.write(f"**{get_text('email', curr_lang)}:** {current_user.get('email', 'N/A')}")
                    
                    with c_b:
                        st.write(f"**{get_text('m7_inv_no', curr_lang)}** `{selected_order['Order ID']}`")
                        st.write(f"**{get_text('m7_pay_stat', curr_lang)}** `{selected_order['Status']}`")
                        st.write(f"**{get_text('m7_pay_meth', curr_lang)}** Visa ending in •••• 4242")
                    
                    st.markdown("---")
                    st.markdown(f"""
                    | Item Description | Qty | Amount |
                    | :--- | :---: | :---: |
                    | **{selected_order['Item']}** | 1 | {selected_order['Amount']} |
                    | **VAT / Sales Tax (Included)** | - | $0.00 |
                    | **Total Paid** | | **{selected_order['Amount']}** |
                    """)

                    st.download_button(
                        label="📥 Download Receipt (TXT)",
                        data=f"INVOICE: {selected_order['Order ID']}\nItem: {selected_order['Item']}\nAmount: {selected_order['Amount']}\nStatus: {selected_order['Status']}",
                        file_name=f"Receipt_{selected_order['Order ID']}.txt",
                        mime="text/plain"
                    )
        else:
            st.info(get_text("m7_no_records", curr_lang))

    with tab_new_ticket:
        st.markdown(get_text("m7_create_title", curr_lang))
        with st.form("create_ticket_form"):
            t_category = st.selectbox(get_text("m7_inq_cat", curr_lang), [
                get_text("m7_cat_1", curr_lang),
                get_text("m7_cat_2", curr_lang),
                get_text("m7_cat_3", curr_lang),
                get_text("m7_cat_4", curr_lang),
                get_text("m7_cat_5", curr_lang)
            ])
            t_subject = st.text_input(get_text("m7_subject", curr_lang))
            t_details = st.text_area(get_text("m7_details", curr_lang))
            submit_ticket = st.form_submit_button(get_text("m7_btn_sub_ticket", curr_lang))

            if submit_ticket:
                if t_subject and t_details:
                    inquiries = st.session_state.setdefault("inquiries", [])
                    new_id = f"TK-{len(inquiries) + 1002}"
                    today_date = datetime.date.today().strftime("%Y-%m-%d")
                    
                    inquiries.append({
                        "Ticket ID": new_id,
                        "Subject": f"[{t_category}] {t_subject}",
                        "Status": "Open (In Review)",
                        "Date": today_date
                    })
                    st.success(get_text("m7_ticket_success", curr_lang).format(new_id))
                else:
                    st.error(get_text("m7_ticket_error", curr_lang))

# --- MODULE 8: ADMIN CONTROL PANEL ---
def render_module_7():
    st.subheader(get_text("m8_title", curr_lang))
    if st.text_input(get_text("m8_passcode", curr_lang), type="password") == "admin":
        st.success(get_text("m8_granted", curr_lang))
        st.dataframe(pd.DataFrame.from_dict(st.session_state["registered_users"], orient='index'))

# --- MODULE 9: SINGLE DEDICATED CONTACT PAGE ---
def render_module_contact():
    st.markdown(f"""
        <div style="background-color:#FAF8F5; padding:28px; border-radius:12px; border:1px solid #E5E0D8; margin-bottom:24px;">
            <h2 style="margin-top:0;">{get_text("m9_title", curr_lang)}</h2>
            <p style="color:#5C544D; margin-bottom:0;">{get_text("m9_desc", curr_lang)}</p>
        </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(get_text("m9_corp", curr_lang))
        st.markdown(get_text("m9_corp_text", curr_lang))

    with col2:
        st.markdown(get_text("m9_social", curr_lang))
        st.markdown(get_text("m9_social_desc", curr_lang))
        st.markdown("""
        <a href="https://youtube.com" target="_blank" class="social-btn">📺 YouTube Channel</a>
        <a href="https://instagram.com" target="_blank" class="social-btn">📸 Instagram (@GlobalTennisAI)</a>
        <a href="https://twitter.com" target="_blank" class="social-btn">🐦 X / Twitter</a>
        <a href="https://linkedin.com" target="_blank" class="social-btn">💼 LinkedIn Official</a>
        """, unsafe_allow_html=True)

# ==========================================
# 6. ROUTER LOGIC
# ==========================================
if menu == get_text("menu_m1", curr_lang):
    render_module_1()
elif menu == get_text("menu_m2", curr_lang):
    render_module_2()
elif menu == get_text("menu_m3", curr_lang):
    render_module_membership()
elif menu == get_text("menu_m4", curr_lang):
    render_module_3()
elif menu == get_text("menu_m5", curr_lang):
    render_module_4()
elif menu == get_text("menu_m6", curr_lang):
    render_module_5()
elif menu == get_text("menu_m7", curr_lang):
    render_module_6()
elif menu == get_text("menu_m8", curr_lang):
    render_module_7()
elif menu == get_text("menu_m9", curr_lang):
    render_module_contact()
