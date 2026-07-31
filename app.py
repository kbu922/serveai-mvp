import datetime
import os
import tempfile
import time

import cv2
import imageio
import numpy as np
import pandas as pd
import streamlit as st

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
        "m5_sec_1": "Stadium Campus Gallery",
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
        "m9_social_desc": "Follow our official channels for tournament updates, student highlights, and AI biomechanics tips:",
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
        "m5_sec_1": "경기장 캠퍼스 갤러리",
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
        "m9_social_desc": "공식 채널을 팔로우하고 대회 소식, 수강생 소식 및 AI 생체역학 팁을 확인하세요:",
    },
}


def get_text(key, lang_str="English"):
    lang_code = "KR" if lang_str == "한국어" else "EN"
    return TEXTS.get(lang_code, TEXTS["EN"]).get(key, key)


# ==========================================
# 1. PAGE CONFIG & LUXURY SAND THEME
# ==========================================
st.set_page_config(
    page_title="Global Tennis Platform & AI Suite",
    page_icon="🎾",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
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
""",
    unsafe_allow_html=True,
)


# ==========================================
# 2. HELPER FUNCTIONS
# ==========================================
def process_skeleton_to_gif(video_file):
    """Overlays standard AI skeleton and outputs an animated GIF for smooth playback."""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tfile:
        tfile.write(video_file.read())
        input_path = tfile.name

    cap = cv2.VideoCapture(input_path)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)) or 640
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)) or 480

    frames = []
    frame_count = 0
    max_frames_to_process = 60

    while cap.isOpened() and frame_count < max_frames_to_process:
        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1

        frame = cv2.resize(frame, (480, int(480 * (height / width))))
        f_h, f_w, _ = frame.shape
        overlay = frame.copy()

        t = (frame_count % 30) / 30.0

        std_shoulder = (int(f_w * 0.45), int(f_h * 0.42))
        std_elbow = (int(f_w * 0.48), int(f_h * 0.55))
        std_wrist = (
            int(f_w * (0.42 + 0.25 * np.cos(t * 2 * np.pi))),
            int(f_h * (0.58 - 0.20 * np.sin(t * 2 * np.pi))),
        )

        bone_color = (0, 215, 255)

        cv2.line(overlay, std_shoulder, std_elbow, bone_color, 4)
        cv2.line(overlay, std_elbow, std_wrist, bone_color, 4)
        cv2.circle(overlay, std_shoulder, 6, (255, 255, 255), -1)
        cv2.circle(overlay, std_elbow, 6, (255, 255, 255), -1)
        cv2.circle(overlay, std_wrist, 8, (0, 255, 0), -1)

        cv2.addWeighted(overlay, 0.5, frame, 0.5, 0, frame)
        cv2.putText(
            frame,
            "AI Standard Model: Topspin Flash",
            (20, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0, 215, 255),
            2,
            cv2.LINE_AA,
        )

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frames.append(frame_rgb)

    cap.release()

    gif_temp = tempfile.NamedTemporaryFile(delete=False, suffix=".gif")
    gif_path = gif_temp.name
    gif_temp.close()

    imageio.mimsave(gif_path, frames, fps=20, loop=0)

    if os.path.exists(input_path):
        os.remove(input_path)

    return gif_path


# ==========================================
# 3. STATE INITIALIZATION & AUTH SYSTEM
# ==========================================
if "registered_users" not in st.session_state:
    st.session_state["registered_users"] = {
        "alex@tennis.org": {
            "password": "password123",
            "name": "Alex Mercer",
            "tier": "PRO Pass",
            "ntrp": 4.5,
        },
        "sarah@tennis.org": {
            "password": "password123",
            "name": "Sarah Kim",
            "tier": "VIP Gold",
            "ntrp": 5.0,
        },
    }

if "is_logged_in" not in st.session_state:
    st.session_state["is_logged_in"] = False

if "current_user" not in st.session_state:
    st.session_state["current_user"] = None

if "language" not in st.session_state:
    st.session_state["language"] = "English"

if "players_db" not in st.session_state:
    st.session_state["players_db"] = [
        {
            "Name": "Marcus Vance",
            "NTRP": 4.5,
            "City": "Seoul",
            "Style": "Aggressive Baseline",
            "Contact": "m.vance@tennis.org",
        },
        {
            "Name": "Elena Rostova",
            "NTRP": 5.0,
            "City": "Busan",
            "Style": "Serve & Volley",
            "Contact": "elena.r@tennis.org",
        },
        {
            "Name": "Jin-woo Park",
            "NTRP": 4.0,
            "City": "Seoul",
            "Style": "Counter-Puncher",
            "Contact": "jw.park@tennis.kr",
        },
        {
            "Name": "Sarah Jenkins",
            "NTRP": 3.5,
            "City": "Incheon",
            "Style": "All-Court",
            "Contact": "s.jenkins@tennis.org",
        },
    ]

if "coaches_db" not in st.session_state:
    st.session_state["coaches_db"] = [
        {
            "Coach": "Coach Rob",
            "Level": "USPTR Certified Master",
            "City": "Seoul",
            "Hourly": "$80/hr",
            "Specialty": "Serve Biomechanics",
        },
        {
            "Coach": "Coach Sarah",
            "Level": "Ex-WTA Tour Player",
            "City": "Incheon",
            "Hourly": "$120/hr",
            "Specialty": "Match Strategy",
        },
        {
            "Coach": "Coach Min-ho",
            "Level": "KTA High Performance",
            "City": "Busan",
            "Hourly": "$95/hr",
            "Specialty": "Junior Development",
        },
    ]

if "tournament_group_votes" not in st.session_state:
    st.session_state["tournament_group_votes"] = [
        {
            "Name": "Chris P.",
            "Tournament": "US Open Tennis Championships",
            "Status": "Discount Unlocked ($85)",
        },
        {
            "Name": "Min-ji K.",
            "Tournament": "Seoul Open Masters",
            "Status": "Discount Unlocked ($85)",
        },
        {
            "Name": "Kenji S.",
            "Tournament": "Seoul Open Masters",
            "Status": "Discount Unlocked ($85)",
        },
    ]

if "academy_group_votes" not in st.session_state:
    st.session_state["academy_group_votes"] = [
        {
            "name": "Alex M.",
            "program": "1-Week Intensive Boot Camp",
            "discount_tier": "15% Off",
        },
        {
            "name": "Sarah K.",
            "program": "1-Week Intensive Boot Camp",
            "discount_tier": "15% Off",
        },
        {
            "name": "David L.",
            "program": "1-Month Pro Residency",
            "discount_tier": "20% Off",
        },
    ]

if "inquiries" not in st.session_state:
    st.session_state["inquiries"] = [
        {
            "Ticket ID": "TK-1001",
            "Subject": "Racket Stringing Order",
            "Status": "In Progress",
            "Date": "2026-03-28",
            "Category": "Racket Stringing / Customization Order",
        }
    ]

if "orders_db" not in st.session_state:
    st.session_state["orders_db"] = [
        {
            "Order ID": "ORD-88219",
            "Item": "VIP Gold Annual Membership",
            "Date": "2026-01-15",
            "Amount": "$149.00",
            "Status": "Paid",
            "Payment Method": "Visa ending in 4242",
        },
        {
            "Order ID": "ORD-94012",
            "Item": "Seoul Open Masters Package",
            "Date": "2026-02-10",
            "Amount": "$215.00",
            "Status": "Paid",
            "Payment Method": "MasterCard ending in 8819",
        },
    ]

# ==========================================
# 4. SIDEBAR & NAVIGATION
# ==========================================
st.sidebar.title("🎾 Global Tennis")
st.sidebar.caption(get_text("caption", st.session_state["language"]))

lang_selection = st.sidebar.selectbox(
    "🌐 Language / 언어",
    options=["English", "한국어"],
    index=0 if st.session_state["language"] == "English" else 1,
)
st.session_state["language"] = lang_selection

st.sidebar.markdown("---")

st.sidebar.subheader(get_text("user_portal", st.session_state["language"]))

if not st.session_state["is_logged_in"]:
    tab_login, tab_reg = st.sidebar.tabs([
        get_text("tab_login", st.session_state["language"]),
        get_text("tab_register", st.session_state["language"]),
    ])

    with tab_login:
        login_email = st.text_input(
            get_text("email", st.session_state["language"]), key="login_email"
        )
        login_pass = st.text_input(
            get_text("password", st.session_state["language"]),
            type="password",
            key="login_pass",
        )
        if st.button(
            get_text("btn_login", st.session_state["language"]),
            key="btn_login_act",
        ):
            if (
                login_email in st.session_state["registered_users"]
                and st.session_state["registered_users"][login_email][
                    "password"
                ]
                == login_pass
            ):
                st.session_state["is_logged_in"] = True
                st.session_state["current_user"] = {
                    "email": login_email,
                    **st.session_state["registered_users"][login_email],
                }
                st.success(
                    get_text(
                        "welcome_back", st.session_state["language"]
                    ).format(st.session_state["current_user"]["name"])
                )
                st.rerun()
            else:
                st.error(
                    get_text("invalid_login", st.session_state["language"])
                )

    with tab_reg:
        reg_name = st.text_input(
            get_text("full_name", st.session_state["language"])
        )
        reg_email = st.text_input(
            get_text("email", st.session_state["language"]), key="reg_email"
        )
        reg_pass = st.text_input(
            get_text("password", st.session_state["language"]),
            type="password",
            key="reg_pass",
        )
        reg_ntrp = st.slider(
            get_text("ntrp_skill", st.session_state["language"]),
            1.0,
            7.0,
            3.5,
            0.5,
        )
        if st.button(get_text("btn_register", st.session_state["language"])):
            if reg_email and reg_pass and reg_name:
                st.session_state["registered_users"][reg_email] = {
                    "password": reg_pass,
                    "name": reg_name,
                    "tier": "Guest / Free",
                    "ntrp": reg_ntrp,
                }
                st.success(
                    get_text("acc_created", st.session_state["language"])
                )
            else:
                st.warning(get_text("fill_all", st.session_state["language"]))
else:
    u = st.session_state["current_user"]
    st.sidebar.markdown(
        f"**{get_text('logged_in_as', st.session_state['language'])}** {u['name']}"
    )
    st.sidebar.markdown(
        f"**{get_text('membership', st.session_state['language'])}** <span class='badge-membership'>{u['tier']}</span>",
        unsafe_allow_html=True,
    )
    st.sidebar.markdown(
        f"**{get_text('ntrp_rating', st.session_state['language'])}** {u['ntrp']}"
    )
    if st.sidebar.button(get_text("btn_logout", st.session_state["language"])):
        st.session_state["is_logged_in"] = False
        st.session_state["current_user"] = None
        st.rerun()

st.sidebar.markdown("---")

menu_options = [
    get_text("menu_m1", st.session_state["language"]),
    get_text("menu_m2", st.session_state["language"]),
    get_text("menu_m3", st.session_state["language"]),
    get_text("menu_m4", st.session_state["language"]),
    get_text("menu_m5", st.session_state["language"]),
    get_text("menu_m6", st.session_state["language"]),
    get_text("menu_m7", st.session_state["language"]),
    get_text("menu_m8", st.session_state["language"]),
    get_text("menu_m9", st.session_state["language"]),
]

selected_module = st.sidebar.radio(
    get_text("select_module", st.session_state["language"]), menu_options
)

st.title(get_text("page_title", st.session_state["language"]))
st.caption(get_text("live_stats", st.session_state["language"]))
st.markdown("---")

# ==========================================
# MODULE 1: AI SERVE VELOCITY & BIOMECHANICS
# ==========================================
if selected_module == menu_options[0]:
    st.header(get_text("m1_title", st.session_state["language"]))
    st.write(get_text("m1_desc", st.session_state["language"]))

    col1, col2 = st.columns([1, 1])

    with col1:
        uploaded_video = st.file_uploader(
            get_text("m1_upload", st.session_state["language"]),
            type=["mp4", "mov"],
        )
        cam_angle = st.selectbox(
            get_text("m1_cam_angle", st.session_state["language"]),
            [
                get_text("m1_angle_1", st.session_state["language"]),
                get_text("m1_angle_2", st.session_state["language"]),
                get_text("m1_angle_3", st.session_state["language"]),
            ],
        )
        fps_setting = st.slider(
            get_text("m1_fps", st.session_state["language"]),
            30,
            240,
            120,
            help=get_text("m1_fps_help", st.session_state["language"]),
        )

    with col2:
        st.markdown(
            f"### {get_text('m1_benchmarks', st.session_state['language'])}"
        )
        st.markdown(
            f"* {get_text('m1_bench_1', st.session_state['language'])}\n"
            f"* {get_text('m1_bench_2', st.session_state['language'])}\n"
            f"* {get_text('m1_bench_3', st.session_state['language'])}",
            unsafe_allow_html=True,
        )

    if uploaded_video is not None:
        st.markdown("---")
        with st.spinner(
            "Analyzing biomechanical motion vectors & processing high-speed video..."
        ):
            proc_gif_path = process_skeleton_to_gif(uploaded_video)
            time.sleep(1)

        st.subheader(get_text("m1_report", st.session_state["language"]))

        m_col1, m_col2, m_col3, m_col4 = st.columns(4)
        m_col1.metric(
            get_text("m1_metric_speed", st.session_state["language"]),
            "118.4 mph",
            get_text("m1_metric_speed_delta", st.session_state["language"]),
        )
        m_col2.metric(
            get_text("m1_metric_spin", st.session_state["language"]),
            "2,840 RPM",
            get_text("m1_metric_spin_delta", st.session_state["language"]),
        )
        m_col3.metric(
            get_text("m1_metric_height", st.session_state["language"]),
            "2.88 meters",
            get_text("m1_metric_height_delta", st.session_state["language"]),
        )
        m_col4.metric(
            get_text("m1_metric_transfer", st.session_state["language"]),
            "89.2%",
            get_text("m1_metric_transfer_delta", st.session_state["language"]),
        )

        v_col1, v_col2 = st.columns([1.2, 1])
        with v_col1:
            st.markdown("#### 🎥 AI Motion Vector Overlay")
            st.image(proc_gif_path)

        with v_col2:
            st.markdown(
                f"#### {get_text('m1_chart_vel', st.session_state['language'])}"
            )
            chart_data = pd.DataFrame({
                "Frame": list(range(1, 31)),
                "Racket Speed (mph)": [
                    10,
                    15,
                    22,
                    35,
                    50,
                    72,
                    95,
                    112,
                    118,
                    115,
                    90,
                    60,
                    30,
                    20,
                    10,
                    5,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                ],
                "Angular Velocity (°/s)": [
                    100,
                    200,
                    350,
                    500,
                    800,
                    1100,
                    1350,
                    1450,
                    1400,
                    1100,
                    700,
                    400,
                    200,
                    100,
                    50,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                    0,
                ],
            })
            st.line_chart(chart_data.set_index("Frame"))

        st.markdown(
            f"### {get_text('m1_breakdown', st.session_state['language'])}"
        )
        p_tab1, p_tab2, p_tab3, p_tab4 = st.tabs([
            get_text("m1_tab_p1", st.session_state["language"]),
            get_text("m1_tab_p2", st.session_state["language"]),
            get_text("m1_tab_p3", st.session_state["language"]),
            get_text("m1_tab_p4", st.session_state["language"]),
        ])

        with p_tab1:
            st.markdown(get_text("m1_p1_text", st.session_state["language"]))
        with p_tab2:
            st.markdown(get_text("m1_p2_text", st.session_state["language"]))
        with p_tab3:
            st.markdown(get_text("m1_p3_text", st.session_state["language"]))
        with p_tab4:
            st.markdown(get_text("m1_p4_text", st.session_state["language"]))

# ==========================================
# MODULE 2: AI RACKET & STRING TENSION
# ==========================================
elif selected_module == menu_options[1]:
    st.header(get_text("m2_title", st.session_state["language"]))
    st.write(get_text("m2_desc", st.session_state["language"]))

    col1, col2 = st.columns(2)
    with col1:
        ntrp = st.select_slider(
            get_text("m2_ntrp_label", st.session_state["language"]),
            options=[2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0],
            value=4.0,
        )
        serve_speed = st.number_input(
            get_text("m2_speed_label", st.session_state["language"]),
            min_value=50,
            max_value=150,
            value=95,
        )
        playstyle = st.selectbox(
            get_text("m2_style_label", st.session_state["language"]),
            [
                get_text("m2_style_1", st.session_state["language"]),
                get_text("m2_style_2", st.session_state["language"]),
                get_text("m2_style_3", st.session_state["language"]),
                get_text("m2_style_4", st.session_state["language"]),
            ],
        )
    with col2:
        freq = st.slider(
            get_text("m2_freq_label", st.session_state["language"]), 1, 7, 3
        )
        has_elbow = st.radio(
            get_text("m2_elbow_label", st.session_state["language"]),
            ["No", "Yes"],
        )
        priority = st.selectbox(
            get_text("m2_priority_label", st.session_state["language"]),
            [
                get_text("m2_prio_1", st.session_state["language"]),
                get_text("m2_prio_2", st.session_state["language"]),
                get_text("m2_prio_3", st.session_state["language"]),
            ],
        )
        weight_pref = st.selectbox(
            get_text("m2_weight_label", st.session_state["language"]),
            [
                get_text("m2_w_1", st.session_state["language"]),
                get_text("m2_w_2", st.session_state["language"]),
                get_text("m2_w_3", st.session_state["language"]),
            ],
        )

    if st.button(get_text("m2_btn_gen", st.session_state["language"])):
        st.markdown("---")
        st.subheader(get_text("m2_res_title", st.session_state["language"]))

        head_size = "98 sq.in." if ntrp >= 4.0 else "100 sq.in."
        rec_weight = (
            "305g (Unstrung)"
            if "300g-315g" in weight_pref or ntrp >= 4.0
            else "285g (Unstrung)"
        )

        if has_elbow == "Yes":
            tension = "48 / 46 lbs"
            string_mat = get_text("m2_mat_soft", st.session_state["language"])
        else:
            tension = "52 / 50 lbs" if ntrp >= 4.0 else "50 / 48 lbs"
            string_mat = get_text("m2_mat_poly", st.session_state["language"])

        r_col1, r_col2, r_col3, r_col4 = st.columns(4)
        r_col1.metric(
            get_text("m2_m_head", st.session_state["language"]), head_size
        )
        r_col2.metric(
            get_text("m2_m_weight", st.session_state["language"]), rec_weight
        )
        r_col3.metric(
            get_text("m2_m_tension", st.session_state["language"]), tension
        )
        r_col4.metric(
            get_text("m2_m_mat", st.session_state["language"]), string_mat
        )

        c1, c2 = st.columns([1, 1])
        with c1:
            st.markdown(
                f"#### {get_text('m2_chart_title', st.session_state['language'])}"
            )
            tension_df = pd.DataFrame({
                "Tension Range (lbs)": [45, 48, 50, 52, 55, 58, 60],
                "Control Index": [40, 52, 65, 75, 88, 94, 98],
                "Power Index": [98, 90, 80, 72, 60, 48, 38],
                "Comfort Rating": [95, 90, 82, 74, 60, 45, 30],
            })
            st.line_chart(tension_df.set_index("Tension Range (lbs)"))

        with c2:
            st.markdown(
                f"#### {get_text('m2_guide_title', st.session_state['language'])}"
            )
            st.markdown(
                get_text("m2_guide_col1", st.session_state["language"])
            )
            restring_months = max(1, 4 - (freq // 2))
            st.markdown(
                get_text("m2_guide_col2", st.session_state["language"]).format(
                    restring_months
                )
            )

# ==========================================
# MODULE 3: MEMBERSHIP & SUBSCRIPTIONS
# ==========================================
elif selected_module == menu_options[2]:
    st.header(get_text("m3_title", st.session_state["language"]))
    st.write(get_text("m3_desc", st.session_state["language"]))

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("### 🥉 Free Pass")
        st.markdown("#### $0 / month")
        st.markdown(
            "* Basic Serve Tracking\n* Read-Only Forum\n* Standard Directories"
        )
        st.button(
            get_text("m3_btn_free", st.session_state["language"]),
            disabled=True,
        )

    with col2:
        st.markdown("### 🥈 PRO Pass")
        st.markdown("#### $19.99 / month")
        st.markdown(
            "* Full AI Biomechanics Tracking\n* Unlimited Coach Messaging\n*"
            " Group Buying Discounts"
        )
        if st.button(get_text("m3_btn_pro", st.session_state["language"])):
            st.session_state["selected_plan"] = ("PRO Pass", "$19.99/mo")

    with col3:
        st.markdown("### 🥇 VIP Gold Pass")
        st.markdown("#### $149.00 / year")
        st.markdown(
            "* Everything in PRO Pass\n* 1-on-1 Monthly Video Review\n*"
            " Tournament Hospitality Access"
        )
        if st.button(get_text("m3_btn_vip", st.session_state["language"])):
            st.session_state["selected_plan"] = ("VIP Gold", "$149.00/yr")

    if "selected_plan" in st.session_state:
        plan_name, plan_price = st.session_state["selected_plan"]
        st.markdown("---")
        st.subheader(
            get_text("m3_checkout", st.session_state["language"]).format(
                plan_name, plan_price
            )
        )

        c_name = st.text_input(
            get_text("m3_card_name", st.session_state["language"])
        )
        c_num = st.text_input(
            get_text("m3_card_num", st.session_state["language"]),
            placeholder="4532 •••• •••• 8892",
        )
        p_col1, p_col2 = st.columns(2)
        c_exp = p_col1.text_input(
            get_text("m3_card_exp", st.session_state["language"]),
            placeholder="12/28",
        )
        c_cvv = p_col2.text_input(
            get_text("m3_card_cvv", st.session_state["language"]),
            type="password",
            placeholder="123",
        )

        if st.button(get_text("m3_btn_pay", st.session_state["language"])):
            if c_name and c_num and c_exp and c_cvv:
                if st.session_state["is_logged_in"]:
                    st.session_state["current_user"]["tier"] = plan_name
                    user_email = st.session_state["current_user"]["email"]
                    if user_email in st.session_state["registered_users"]:
                        st.session_state["registered_users"][user_email][
                            "tier"
                        ] = plan_name

                order_id = f"ORD-{np.random.randint(10000, 99999)}"
                st.session_state["orders_db"].append({
                    "Order ID": order_id,
                    "Item": f"{plan_name} Subscription",
                    "Date": datetime.date.today().strftime("%Y-%m-%d"),
                    "Amount": plan_price,
                    "Status": "Paid",
                    "Payment Method": (
                        f"Card ending in {c_num[-4:] if len(c_num)>=4 else '4242'}"
                    ),
                })

                st.success(
                    get_text(
                        "m3_pay_success", st.session_state["language"]
                    ).format(plan_name)
                )
            else:
                st.error(
                    get_text("m3_pay_error", st.session_state["language"])
                )

# ==========================================
# MODULE 4: TOURNAMENTS & LODGING
# ==========================================
elif selected_module == menu_options[3]:
    st.header(get_text("m4_title", st.session_state["language"]))

    tournament_choice = st.selectbox(
        get_text("m4_select_event", st.session_state["language"]),
        [
            "US Open Tennis Championships (New York, USA)",
            "Seoul Open Masters (Seoul, Korea)",
            "Busan Challenger Open (Busan, Korea)",
        ],
    )

    pathway = st.radio(
        get_text("m4_select_path", st.session_state["language"]),
        [
            get_text("m4_path_1", st.session_state["language"]),
            get_text("m4_path_2", st.session_state["language"]),
            get_text("m4_path_3", st.session_state["language"]),
        ],
    )

    st.markdown("---")

    if pathway == get_text("m4_path_1", st.session_state["language"]):
        st.subheader("🏟️ Stadium & Hotel Infrastructure")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### Official Tournament Courts")
            st.image(
                "https://images.unsplash.com/photo-1595435934249-5df7ed86e1c0?w=800&q=80",
                caption="Tournament Center Court",
            )
        with col2:
            st.markdown("#### Official Residence Partner")
            st.image(
                "https://images.unsplash.com/photo-1566073771259-6a8506099945?w=800&q=80",
                caption="Official Player Hotel Suite",
            )

    elif pathway == get_text("m4_path_2", st.session_state["language"]):
        st.subheader("👥 Group Buying Hub ($85 Discount Threshold)")
        st.info(get_text("m4_group_info", st.session_state["language"]))

        current_count = len(st.session_state["tournament_group_votes"])
        st.markdown(
            get_text("m4_committed", st.session_state["language"]).format(
                current_count
            )
        )
        st.progress(min(current_count / 5.0, 1.0))

        st.table(pd.DataFrame(st.session_state["tournament_group_votes"]))

        if st.button("➕ Join Current Group Buying Pool"):
            user_name = (
                st.session_state["current_user"]["name"]
                if st.session_state["is_logged_in"]
                else "Guest Athlete"
            )
            st.session_state["tournament_group_votes"].append({
                "Name": user_name,
                "Tournament": tournament_choice,
                "Status": "Discount Unlocked ($85)",
            })
            st.success("You have been added to the group buying pool!")
            st.rerun()

    elif pathway == get_text("m4_path_3", st.session_state["language"]):
        st.subheader("👤 Individual Registration & Package Checkout")
        t_name = st.text_input(
            get_text("m4_p_name", st.session_state["language"])
        )
        t_pass = st.text_input(
            get_text("m4_passport", st.session_state["language"])
        )
        t_card = st.text_input(
            get_text("m4_card", st.session_state["language"])
        )

        if st.button(get_text("m4_btn_pay_indiv", st.session_state["language"])):
            if t_name and t_pass and t_card:
                order_id = f"ORD-{np.random.randint(10000, 99999)}"
                st.session_state["orders_db"].append({
                    "Order ID": order_id,
                    "Item": f"Tournament Package: {tournament_choice}",
                    "Date": datetime.date.today().strftime("%Y-%m-%d"),
                    "Amount": "$300.00",
                    "Status": "Paid",
                    "Payment Method": (
                        f"Card ending in {t_card[-4:] if len(t_card)>=4 else '1111'}"
                    ),
                })
                st.success(
                    get_text("m4_success_indiv", st.session_state["language"])
                )
            else:
                st.error("Please fill in all registration fields.")

# ==========================================
# MODULE 5: RESIDENCY & ACADEMY PROGRAMS
# ==========================================
elif selected_module == menu_options[4]:
    st.header(get_text("m5_title", st.session_state["language"]))

    sec = st.radio(
        get_text("m5_select_sec", st.session_state["language"]),
        [
            get_text("m5_sec_1", st.session_state["language"]),
            get_text("m5_sec_2", st.session_state["language"]),
            get_text("m5_sec_3", st.session_state["language"]),
        ],
    )

    st.markdown("---")

    if sec == get_text("m5_sec_1", st.session_state["language"]):
        st.subheader("🏛️ High-Performance Academy Campus")
        c1, c2 = st.columns(2)
        with c1:
            st.image(
                "https://images.unsplash.com/photo-1622279457486-62dcc4a431d6?w=800&q=80",
                caption="Training Courts & Gym Complex",
            )
        with c2:
            st.image(
                "https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?w=800&q=80",
                caption="Athlete Residency Accommodation",
            )

    elif sec == get_text("m5_sec_2", st.session_state["language"]):
        st.subheader("👥 Academy Group Buying & Voting Hub")
        st.table(pd.DataFrame(st.session_state["academy_group_votes"]))

    elif sec == get_text("m5_sec_3", st.session_state["language"]):
        st.subheader("👤 Direct Academy Enrollment")
        a_name = st.text_input("Athlete Full Name *")
        a_prog = st.selectbox("Select Program", [
            "1-Week Intensive Boot Camp ($890)",
            "1-Month Pro Residency ($2,800)",
        ])
        a_card = st.text_input("Credit Card Number *")

        if st.button(get_text("m5_enroll_btn", st.session_state["language"])):
            if a_name and a_card:
                order_id = f"ORD-{np.random.randint(10000, 99999)}"
                cost = "$890.00" if "1-Week" in a_prog else "$2,800.00"
                st.session_state["orders_db"].append({
                    "Order ID": order_id,
                    "Item": f"Academy Enrollment: {a_prog}",
                    "Date": datetime.date.today().strftime("%Y-%m-%d"),
                    "Amount": cost,
                    "Status": "Paid",
                    "Payment Method": (
                        f"Card ending in {a_card[-4:] if len(a_card)>=4 else '9999'}"
                    ),
                })
                st.success(
                    get_text("m5_enroll_success", st.session_state["language"])
                )
            else:
                st.error("Please fill in required enrollment fields.")

# ==========================================
# MODULE 6: MATCHMAKING & COACH DIRECTORY
# ==========================================
elif selected_module == menu_options[5]:
    st.header(get_text("m6_title", st.session_state["language"]))
    st.write(get_text("m6_desc", st.session_state["language"]))

    user_tier = (
        st.session_state["current_user"]["tier"]
        if st.session_state["is_logged_in"]
        else "Guest / Free"
    )
    can_chat = user_tier in ["PRO Pass", "VIP Gold"]

    if not can_chat:
        st.warning(
            get_text("m6_warn", st.session_state["language"]).format(user_tier)
        )

    tab_p, tab_c = st.tabs([
        get_text("m6_tab_partners", st.session_state["language"]),
        get_text("m6_tab_coaches", st.session_state["language"]),
    ])

    with tab_p:
        st.markdown(
            get_text("m6_avail_partners", st.session_state["language"])
        )
        for p in st.session_state["players_db"]:
            with st.expander(f"🎾 {p['Name']} (NTRP {p['NTRP']}) — {p['City']}"):
                st.write(
                    f"**{get_text('m6_style', st.session_state['language'])}**"
                    f" {p['Style']}"
                )
                st.write(
                    f"**{get_text('m6_city', st.session_state['language'])}**"
                    f" {p['City']}"
                )
                st.write(
                    f"**{get_text('m6_contact', st.session_state['language'])}**"
                    f" {p['Contact']}"
                )
                if can_chat:
                    if st.button(
                        f"{get_text('m6_chat_now', st.session_state['language'])} with {p['Name']}",
                        key=f"p_{p['Name']}",
                    ):
                        st.success(
                            get_text(
                                "m6_chat_success", st.session_state["language"]
                            ).format(p["Name"])
                        )
                else:
                    st.button(
                        get_text("m6_locked", st.session_state["language"]),
                        key=f"p_lock_{p['Name']}",
                        disabled=True,
                    )

    with tab_c:
        st.markdown(get_text("m6_avail_coaches", st.session_state["language"]))
        for c in st.session_state["coaches_db"]:
            with st.expander(f"👨‍🏫 {c['Coach']} — {c['Level']}"):
                st.write(
                    f"**{get_text('m6_specialty', st.session_state['language'])}**"
                    f" {c['Specialty']}"
                )
                st.write(
                    f"**{get_text('m6_rate', st.session_state['language'])}**"
                    f" {c['Hourly']}"
                )
                st.write(
                    f"**{get_text('m6_location', st.session_state['language'])}**"
                    f" {c['City']}"
                )
                if can_chat:
                    if st.button(
                        f"{get_text('m6_book_chat', st.session_state['language'])} with {c['Coach']}",
                        key=f"c_{c['Coach']}",
                    ):
                        st.success(
                            get_text(
                                "m6_book_success", st.session_state["language"]
                            ).format(c["Coach"])
                        )
                else:
                    st.button(
                        get_text("m6_locked", st.session_state["language"]),
                        key=f"c_lock_{c['Coach']}",
                        disabled=True,
                    )

# ==========================================
# MODULE 7: SUPPORT & RECEIPTS
# ==========================================
elif selected_module == menu_options[6]:
    st.header(get_text("m7_title", st.session_state["language"]))
    st.write(get_text("m7_desc", st.session_state["language"]))

    s_tab1, s_tab2, s_tab3 = st.tabs([
        get_text("m7_tab_1", st.session_state["language"]),
        get_text("m7_tab_2", st.session_state["language"]),
        get_text("m7_tab_3", st.session_state["language"]),
    ])

    with s_tab1:
        st.markdown(
            get_text("m7_tickets_title", st.session_state["language"])
        )
        if not st.session_state["is_logged_in"]:
            st.info(get_text("m7_login_info", st.session_state["language"]))
        st.table(pd.DataFrame(st.session_state["inquiries"]))

    with s_tab2:
        st.markdown(
            get_text("m7_billing_title", st.session_state["language"])
        )
        if len(st.session_state["orders_db"]) > 0:
            st.table(pd.DataFrame(st.session_state["orders_db"]))

            st.markdown(
                get_text("m7_gen_receipt", st.session_state["language"])
            )
            order_ids = [o["Order ID"] for o in st.session_state["orders_db"]]
            selected_order_id = st.selectbox(
                get_text("m7_select_order", st.session_state["language"]),
                order_ids,
            )

            order_data = next(
                (
                    item
                    for item in st.session_state["orders_db"]
                    if item["Order ID"] == selected_order_id
                ),
                None,
            )

            if order_data:
                user_name = (
                    st.session_state["current_user"]["name"]
                    if st.session_state["is_logged_in"]
                    else get_text(
                        "m7_guest_ath", st.session_state["language"]
                    )
                )
                user_email = (
                    st.session_state["current_user"]["email"]
                    if st.session_state["is_logged_in"]
                    else "guest@globaltennis.org"
                )

                st.markdown(
                    f"""
                <div style="background-color: #FAF8F5; border: 1px solid #E5E0D8; border-radius: 12px; padding: 24px; margin-top: 15px;">
                    <h3>{get_text("m7_digital_inv", st.session_state["language"]).format(order_data["Order ID"])}</h3>
                    <p><strong>{get_text("m7_company", st.session_state["language"])}</strong><br>
                    {get_text("m7_company_addr", st.session_state["language"])}</p>
                    <hr style="border-top: 1px solid #E5E0D8;">
                    <p><strong>{get_text("m7_billed_to", st.session_state["language"])}</strong> {user_name} ({user_email})<br>
                    <strong>Date:</strong> {order_data["Date"]}<br>
                    <strong>{get_text("m7_inv_no", st.session_state["language"])}</strong> INV-{order_data["Order ID"]}</p>
                    <table style="width:100%; text-align:left; border-collapse: collapse; margin-top: 15px;">
                        <tr style="border-bottom: 1px solid #E5E0D8;">
                            <th style="padding: 8px;">Description</th>
                            <th style="padding: 8px;">Amount</th>
                        </tr>
                        <tr style="border-bottom: 1px solid #E5E0D8;">
                            <td style="padding: 8px;">{order_data["Item"]}</td>
                            <td style="padding: 8px;">{order_data["Amount"]}</td>
                        </tr>
                    </table>
                    <br>
                    <p><strong>{get_text("m7_pay_stat", st.session_state["language"])}</strong> <span style="color:green; font-weight:bold;">{order_data["Status"]}</span><br>
                    <strong>{get_text("m7_pay_meth", st.session_state["language"])}</strong> {order_data["Payment Method"]}</p>
                </div>
                """,
                    unsafe_allow_html=True,
                )
        else:
            st.info(get_text("m7_no_records", st.session_state["language"]))

    with s_tab3:
        st.markdown(get_text("m7_create_title", st.session_state["language"]))
        inq_cat = st.selectbox(
            get_text("m7_inq_cat", st.session_state["language"]),
            [
                get_text("m7_cat_1", st.session_state["language"]),
                get_text("m7_cat_2", st.session_state["language"]),
                get_text("m7_cat_3", st.session_state["language"]),
                get_text("m7_cat_4", st.session_state["language"]),
                get_text("m7_cat_5", st.session_state["language"]),
            ],
        )
        inq_sub = st.text_input(
            get_text("m7_subject", st.session_state["language"])
        )
        inq_body = st.text_area(
            get_text("m7_details", st.session_state["language"])
        )

        if st.button(get_text("m7_btn_sub_ticket", st.session_state["language"])):
            if inq_sub and inq_body:
                new_id = f"TK-{np.random.randint(1000, 9999)}"
                st.session_state["inquiries"].append({
                    "Ticket ID": new_id,
                    "Subject": inq_sub,
                    "Status": "Pending Review",
                    "Date": datetime.date.today().strftime("%Y-%m-%d"),
                    "Category": inq_cat,
                })
                st.success(
                    get_text(
                        "m7_ticket_success", st.session_state["language"]
                    ).format(new_id)
                )
            else:
                st.error(
                    get_text("m7_ticket_error", st.session_state["language"])
                )

# ==========================================
# MODULE 8: ADMIN CONTROL PANEL
# ==========================================
elif selected_module == menu_options[7]:
    st.header(get_text("m8_title", st.session_state["language"]))

    passcode = st.text_input(
        get_text("m8_passcode", st.session_state["language"]), type="password"
    )
    if passcode == "admin123":
        st.success(get_text("m8_granted", st.session_state["language"]))

        st.markdown("### Registered Users Database")
        st.write(st.session_state["registered_users"])

        st.markdown("### System Inquiries")
        st.table(pd.DataFrame(st.session_state["inquiries"]))

        st.markdown("### Platform Order Records")
        st.table(pd.DataFrame(st.session_state["orders_db"]))
    elif passcode:
        st.error("Invalid passcode.")

# ==========================================
# MODULE 9: CONTACT US
# ==========================================
elif selected_module == menu_options[8]:
    st.header(get_text("m9_title", st.session_state["language"]))
    st.write(get_text("m9_desc", st.session_state["language"]))

    st.markdown(get_text("m9_corp", st.session_state["language"]))
    st.markdown(get_text("m9_corp_text", st.session_state["language"]))

    st.markdown("---")
    st.markdown(get_text("m9_social", st.session_state["language"]))
    st.write(get_text("m9_social_desc", st.session_state["language"]))

    st.markdown(
        """
        <a href="https://youtube.com" target="_blank" class="social-btn">📺 YouTube Channel</a>
        <a href="https://instagram.com" target="_blank" class="social-btn">📸 Instagram</a>
        <a href="https://facebook.com" target="_blank" class="social-btn">🌐 Facebook Community</a>
    """,
        unsafe_allow_html=True,
    )
