import streamlit as st
import datetime
import time

# ==========================================
# 1. Page Configuration & Initial State
# ==========================================
st.set_page_config(
    page_title="ServeAI - Global Tennis & Real Estate Portal",
    page_icon="🎾",
    layout="wide"
)

# Session State Initialization
if "users" not in st.session_state:
    st.session_state["users"] = {"admin@serveai.com": "password123"}
if "logged_in_user" not in st.session_state:
    st.session_state["logged_in_user"] = None
if "admin_logged_in" not in st.session_state:
    st.session_state["admin_logged_in"] = False

# Backend Databases
if "inquiries" not in st.session_state:
    st.session_state["inquiries"] = [
        {
            "id": "INQ-1001",
            "user_email": "alex@globaltennis.com",
            "subject": "Room-share matching criteria inquiry",
            "category": "Tournament & Accommodation",
            "message": "Are players paired with the same gender and similar NTRP rating for room-sharing?",
            "status": "Answered",
            "created_at": "2026-07-28 14:20",
            "admin_reply": "Yes! We pair players based on the same gender and closely matched NTRP levels."
        }
    ]

if "match_orders" not in st.session_state:
    st.session_state["match_orders"] = [
        {
            "order_id": "TOURN-20260728-01",
            "tournament": "2026 Seoul Amateur Open & Resort Package",
            "player_name": "Sarah Connor",
            "phone": "+1-310-555-0142",
            "email": "sarah@tennis.org",
            "ntrp": "3.5",
            "accommodation": "1 Night Single Room (+ $120)",
            "amount": "$300 USD",
            "time": "2026-07-28 16:45"
        }
    ]

if "estate_orders" not in st.session_state:
    st.session_state["estate_orders"] = [
        {
            "order_id": "EST-20260729-01",
            "property": "Gangnam Teheran-ro Indoor Tennis Academy",
            "buyer_name": "David Miller",
            "phone": "+1-212-555-0199",
            "email": "david@capital.com",
            "option": "Hold Deposit Only (예약 보증금 결제)",
            "tax_service": "Yes (+ $1,200 Tax Advisory)",
            "amount": "$16,200 USD",
            "time": "2026-07-29 11:30"
        }
    ]

# ==========================================
# 2. Language Switcher & Localization
# ==========================================
st.sidebar.title("🎾 ServeAI Global")

# Language Switcher
lang = st.sidebar.selectbox("🌐 Language / 언어", ["English", "한국어"])

st.sidebar.markdown("---")

# UI String Translations
t = {
    "English": {
        "nav_title": "📌 Navigation",
        "nav_1": "⚡ AI Serve Speed Analysis",
        "nav_2": "🎾 AI Racket & Tension Calculator",
        "nav_3": "🏆 Tournaments & Accommodation Subpage",
        "nav_4": "🏢 Tennis Real Estate Subpage & Orders",
        "nav_5": "💬 Support & Inquiries",
        "nav_6": "🔒 Admin / Backend Dashboard",
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
        "back_btn_tourn": "⬅️ Back to Tournaments List",
        "back_btn_estate": "⬅️ Back to Property List",
        "tourn_title": "🏆 Tennis Tournaments & Resort Accommodation Subpage",
        "tourn_desc": "Register for global amateur tournaments, book partner resort stays, or request room-sharing.",
        "estate_title": "🏢 Tennis Real Estate & Academy Investment Subpage",
        "estate_desc": "Browse indoor court deals, submit purchase/lease orders, and place online reservation deposits.",
        "calc_title": "🎾 AI Tennis NTRP, Serve Speed & Optimal Tension Calculator",
        "calc_desc": "Calculates your optimal string tension (lbs) based on your NTRP level, current tension, and measured AI serve speed.",
        "support_title": "💬 Customer Support & Ticket Center",
        "support_desc": "Submit your questions regarding tournaments, real estate, or AI features. Our team will review and reply.",
    },
    "한국어": {
        "nav_title": "📌 메뉴 선택",
        "nav_1": "⚡ AI 서브 속도 분석",
        "nav_2": "🎾 AI 라켓 & 텐션 추천 계산기",
        "nav_3": "🏆 테니스 대회 & 숙박 서브페이지",
        "nav_4": "🏢 테니스 부동산 & 투자 서브페이지",
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
        "back_btn_tourn": "⬅️ 대회 목록으로 돌아가기",
        "back_btn_estate": "⬅️ 전체 부동산 목록으로 돌아가기",
        "tourn_title": "🏆 테니스 대회 & 리조트 숙박 예약 서브페이지",
        "tourn_desc": "국내외 아마추어 테니스 대회 참가 신청, 전용 리조트 예약 및 룸셰어 패키지를 결제하세요.",
        "estate_title": "🏢 테니스 부동산 & 해외 아카데미 매매/임대 서브페이지",
        "estate_desc": "실내외 코트 매물 및 지분 투자 목록을 확인하고, 세무 자문 옵션 선택 및 예약금 결제를 진행하세요.",
        "calc_title": "🎾 AI 테니스 NTRP / 서브 속도 기반 최적 텐션 계산기",
        "calc_desc": "NTRP 레벨, 현재 사용 중인 텐션(모름 포함), AI 측정 서브 속도를 바탕으로 최적의 텐션(lbs)을 정밀 계산합니다.",
        "support_title": "💬 고객 지원 & 1:1 문의하기",
        "support_desc": "대회, 부동산 매물, AI 분석 기능 등 궁금하신 점을 작성해 주세요. 관리자 확인 후 즉시 답변드립니다.",
    }
}[lang]

# Login / Registration Block
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

# Navigation Routing
nav_options = [
    t["nav_1"],
    t["nav_2"],
    t["nav_3"],
    t["nav_4"],
    t["nav_5"],
    t["nav_6"]
]
page_selection = st.sidebar.radio(t["nav_title"], nav_options)

# Tournament Database
tournaments_db = {
    "tourn1": {
        "title_en": "2026 Seoul Amateur Open & Resort Package",
        "title_kr": "2026 서울 아마추어 오픈 & 리조트 숙박 패키지",
        "date": "2026-09-12 ~ 2026-09-14",
        "location_en": "Jangchung Tennis Center & Shilla Hotel Package",
        "location_kr": "장충 테니스장 & 신라호텔 숙박 연계",
        "fee_usd": "$180 USD (₩240,000)",
        "desc_en": "Includes entry fee, tournament jersey, welcome dinner, and 1-night shared twin room at partner hotel.",
        "desc_kr": "대회 참가비, 공식 유니폼, 웰컴 만찬 및 파트너 호텔 2인 1실 1박 포함.",
        "badge": "🔥 Registration Open"
    },
    "tourn2": {
        "title_en": "Jeju Island Coastal Tennis Cup & Resort Stay",
        "title_kr": "제주 오션뷰 테니스 챔피언십 & 해비치 리조트 패키지",
        "date": "2026-10-03 ~ 2026-10-05",
        "location_en": "Jeju Ocean Tennis Complex & Haevichi Resort",
        "location_kr": "제주 해비치 테니스 코트 & 리조트 2박",
        "fee_usd": "$320 USD (₩430,000)",
        "desc_en": "3-day singles/doubles tournament. 2 nights ocean resort stay, airport shuttle, and ServeAI analysis.",
        "desc_kr": "3일간 진행되는 단식/복식 대회. 리조트 2박, 공항 셔틀 및 AI 서브 데이터 분석 포함.",
        "badge": "✈️ Resort Package"
    },
    "tourn3": {
        "title_en": "Tokyo-Seoul Friendly Match & Travel Tour",
        "title_kr": "도쿄-서울 교류전 & 3박 4일 프라이빗 테니스 투어",
        "date": "2026-11-10 ~ 2026-11-13",
        "location_en": "Ariake Tennis Park, Tokyo, Japan",
        "location_kr": "일본 도쿄 아리아케 테니스 파크",
        "fee_usd": "$750 USD (₩1,000,000)",
        "desc_en": "Cross-border amateur match against Japanese clubs with local accommodation & gala party.",
        "desc_kr": "일본 현지 클럽과의 국제 교류전. 고급 호텔 3박, 이동 차편, 갈라 파티 포함.",
        "badge": "🌏 Global Tour"
    }
}

# Real Estate & Investment Database
real_estate_products = {
    "estate1": {
        "title_en": "Gangnam Teheran-ro Indoor Tennis Academy",
        "title_kr": "강남 테헤란로 실내 테니스 아카데미",
        "location_en": "Gangnam-gu, Seoul, South Korea",
        "location_kr": "서울시 강남구 역삼동",
        "size_en": "720 sqm (3 Indoor Courts + Full Amenity Shower Rooms)",
        "size_kr": "전용 220평 (코트 3면 + 풀옵션 샤워실)",
        "desc_en": "Monthly revenue of $35,000. Equipped with ServeAI speed cameras and 300 active members.",
        "desc_kr": "월 매출 4,500만원 입증 완료. AI 서브 측정 장비 및 회원 300명 양도 포함.",
        "price_deposit_num": 15000,
        "price_deposit_usd": "$15,000 (₩20,000,000)",
        "price_full_num": 650000,
        "price_full_usd": "$650,000 (₩850,000,000)",
        "badge": "🔥 Featured Deal"
    },
    "estate2": {
        "title_en": "Bundang Jeongja-dong Modern Indoor Facility Lease",
        "title_kr": "분당 정자동 최신식 실내 테니스장 롱텀 임대",
        "location_en": "Bundang-gu, Seongnam, South Korea",
        "location_kr": "경기도 성남시 분당구 정자동",
        "size_en": "500 sqm (2 Indoor Courts, 8m High Ceiling)",
        "size_kr": "전용 150평 (실내 2면, 높은 층고 8m)",
        "desc_en": "Parking for 50 cars. Soundproofed structure. Ready for immediate academy operation.",
        "desc_kr": "주차 50대 가능. 층간소음 방지 설계 완료. 즉시 아카데미 영업 가능.",
        "price_deposit_num": 7500,
        "price_deposit_usd": "$7,500 (₩10,000,000)",
        "price_full_num": 75000,
        "price_full_usd": "$75,000 (₩100,000,000)",
        "badge": "🟢 Available"
    },
    "estate3": {
        "title_en": "ServeAI Branch #2 'Incheon Songdo Tennis Park' Equity Share",
        "title_kr": "ServeAI 2호점 '인천 송도 테니스 파크' 프랜차이즈 지분 투자",
        "location_en": "Songdo-dong, Incheon, South Korea",
        "location_kr": "인천 연수구 송도동",
        "size_en": "4 Outdoor Courts + 2 Indoor Courts Major Complex",
        "size_kr": "야외 4면 + 실내 2면 대형 클럽",
        "desc_en": "Tennis academy venture equipped with ServeAI computer vision tech. Share investment per slot.",
        "desc_kr": "ServeAI 기술이 탑재된 테니스 전문 학교 설립 사업. 최소 1 구좌부터 지분 참여 가능.",
        "price_deposit_num": 2500,
        "price_deposit_usd": "$2,500 (₩3,300,000)",
        "price_full_num": 25000,
        "price_full_usd": "$25,000 (₩33,000,000)",
        "badge": "💎 Equity Share"
    }
}

# Dynamic URL Params Routing
query_params = st.query_params
selected_tourn = query_params.get("tourn", None)
selected_estate = query_params.get("estate", None)

# ==========================================
# 3. Feature 1: AI Serve Speed Analysis
# ==========================================
if page_selection == t["nav_1"]:
    st.title(t["nav_1"])
    st.write("Upload a tennis serve video to calculate velocity trajectory and impact point.")
    
    uploaded_file = st.file_uploader("Upload Video (MP4, MOV)", type=["mp4", "mov", "avi"])
    if uploaded_file is not None:
        st.video(uploaded_file)
        if st.button("🚀 Run AI Analysis"):
            with st.spinner("🔍 Tracking serve trajectory & calculating speed..."):
                time.sleep(1.2)
            st.balloons()
            st.success("Analysis Complete!")
            col1, col2, col3 = st.columns(3)
            col1.metric("Peak Speed", "184 km/h", "+12 km/h")
            col2.metric("Impact Height", "2.78 m", "Optimal")
            col3.metric("Spin Rate", "2,450 RPM", "Topspin")

# ==========================================
# 4. Feature 2: AI Racket & Tension Calculator
# ==========================================
elif page_selection == t["nav_2"]:
    st.title(t["calc_title"])
    st.write(t["calc_desc"])
    
    st.markdown("---")
    
    col_in1, col_in2, col_in3 = st.columns(3)
    
    with col_in1:
        ntrp = st.select_slider(
            "1️⃣ Player NTRP Level (NTRP 레벨)",
            options=["2.0", "2.5", "3.0", "3.5", "4.0", "4.5", "5.0+"]
        )
    
    with col_in2:
        current_tension_opt = st.selectbox(
            "2️⃣ Current String Tension (현재 사용 텐션)",
            [
                "Unknown / Don't Know (모름 / 정보없음)",
                "Low (40 - 45 lbs)",
                "Medium (46 - 52 lbs)",
                "High (53 - 58 lbs)"
            ]
        )
    
    with col_in3:
        serve_speed = st.number_input(
            "3️⃣ Measured AI Serve Speed (AI 측정 서브 속도 km/h)",
            min_value=60,
            max_value=250,
            value=145,
            step=5
        )

    if st.button("🎯 Calculate Optimal Tension (최적 텐션 산출)"):
        base_tension = 48.0
        ntrp_val = float(ntrp.replace("+", ""))
        ntrp_adj = (ntrp_val - 3.0) * 1.5
        speed_adj = (serve_speed - 130) * 0.1
        
        tension_adj = 0.0
        if "Low" in current_tension_opt:
            tension_adj = -2.0
        elif "High" in current_tension_opt:
            tension_adj = 2.0
            
        rec_main = round(base_tension + ntrp_adj + speed_adj + tension_adj)
        rec_cross = rec_main - 2
        
        st.markdown("---")
        st.subheader("💡 AI Optimal String Tension Report (최적 텐션 산출 리포트)")
        
        res_col1, res_col2 = st.columns([1, 1])
        with res_col1:
            st.metric("Recommended Main Tension (메인 텐션)", f"{rec_main} lbs")
            st.metric("Recommended Cross Tension (크로스 텐션)", f"{rec_cross} lbs")
            
        with res_col2:
            st.info(f"""
            **Diagnostic Summary (진단요약)**:
            • **NTRP**: {ntrp}  
            • **Measured Serve Speed**: {serve_speed} km/h  
            • **Previous Tension**: {current_tension_opt.split('(')[0]}  
            
            **Recommendation Note**:
            A main tension of **{rec_main} lbs** combined with a cross tension of **{rec_cross} lbs** provides optimal control without over-stressing your elbow joint at your current serve velocity.
            """)

# ==========================================
# 5. Feature 3: Tournaments & Accommodation Subpage
# ==========================================
elif page_selection == t["nav_3"]:
    if selected_tourn in tournaments_db:
        tr = tournaments_db[selected_tourn]
        if st.button(t["back_btn_tourn"]):
            st.query_params.clear()
            st.rerun()

        title_curr = tr["title_en"] if lang == "English" else tr["title_kr"]
        loc_curr = tr["location_en"] if lang == "English" else tr["location_kr"]
        desc_curr = tr["desc_en"] if lang == "English" else tr["desc_kr"]

        st.markdown(f"## 🏆 [{tr['badge']}] {title_curr}")
        st.info(f"📅 **Date**: {tr['date']} | 📍 **Venue & Resort**: {loc_curr}")
        st.write(desc_curr)
        
        col_form, col_summary = st.columns([1, 1])
        
        with col_form:
            st.subheader("1️⃣ Player & Room Registration Form")
            p_name = st.text_input("Player Name (참가자 성명)", placeholder="John Smith")
            p_phone = st.text_input("Phone Number (연락처)", placeholder="+1 555-0192 / 010-9876-5432")
            p_email = st.text_input("Email (이메일)", value=st.session_state["logged_in_user"] or "")
            p_ntrp = st.selectbox("Your NTRP Rating (NTRP 레벨)", ["2.5", "3.0", "3.5", "4.0", "4.5", "5.0+"])
            
            p_acc = st.radio(
                "Accommodation Option (숙박 선택)",
                [
                    "Standard Room-share Twin (2인 1실 룸쉐어 매칭) [Included]",
                    "Private Single Room Upgrade (+ $120 / ₩150,000)",
                    "No Accommodation / Entry Only (- $50 / ₩60,000)"
                ]
            )

        with col_summary:
            st.subheader("2️⃣ Registration Fee & Payment Checkout")
            st.metric("Total Package Entry Fee", tr["fee_usd"])

            with st.form("tourn_checkout_form"):
                card_no = st.text_input("Credit Card Number (결제 카드번호)", placeholder="4000-0000-0000-0000")
                special_req = st.text_area("Special Request (e.g., Preferred roommate or diet)")
                submit_tourn = st.form_submit_button("💳 Pay & Complete Registration")

            if submit_tourn:
                if p_name and p_phone and card_no:
                    t_ord_id = f"TOURN-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
                    
                    st.session_state["match_orders"].append({
                        "order_id": t_ord_id,
                        "tournament": title_curr,
                        "player_name": p_name,
                        "phone": p_phone,
                        "email": p_email,
                        "ntrp": p_ntrp,
                        "accommodation": p_acc,
                        "amount": tr["fee_usd"],
                        "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                    })
                    st.balloons()
                    st.success("🎉 Registration & Resort Booking Complete! Your receipt is logged in the backend.")
                else:
                    st.error("⚠️ Please fill in all required fields (Name, Phone, Card Number).")

    else:
        st.title(t["tourn_title"])
        st.write(t["tourn_desc"])
        st.markdown("---")

        for key, tr in tournaments_db.items():
            title_curr = tr["title_en"] if lang == "English" else tr["title_kr"]
            loc_curr = tr["location_en"] if lang == "English" else tr["location_kr"]
            desc_curr = tr["desc_en"] if lang == "English" else tr["desc_kr"]

            with st.container(border=True):
                c_left, c_right = st.columns([3, 1])
                with c_left:
                    st.subheader(f"[{tr['badge']}] {title_curr}")
                    st.write(f"📅 **Date**: {tr['date']} | 📍 {loc_curr}")
                    st.write(f"💰 **Entry & Accommodation**: {tr['fee_usd']}")
                    st.caption(desc_curr)
                with c_right:
                    if st.button("📝 Register & Pay", key=f"tourn_btn_{key}"):
                        st.query_params["tourn"] = key
                        st.rerun()

# ==========================================
# 6. Feature 4: Real Estate & Tax Service Choice Subpage
# ==========================================
elif page_selection == t["nav_4"]:
    if selected_estate in real_estate_products:
        est = real_estate_products[selected_estate]
        if st.button(t["back_btn_estate"]):
            st.query_params.clear()
            st.rerun()

        title_curr = est["title_en"] if lang == "English" else est["title_kr"]
        loc_curr = est["location_en"] if lang == "English" else est["location_kr"]
        size_curr = est["size_en"] if lang == "English" else est["size_kr"]
        desc_curr = est["desc_en"] if lang == "English" else est["desc_kr"]

        st.markdown(f"## 🏢 [{est['badge']}] {title_curr}")
        st.info(f"📍 **Location**: {loc_curr} | 📐 **Size**: {size_curr}")
        st.write(desc_curr)
        
        col_info, col_pay = st.columns([1, 1])
        with col_info:
            st.subheader("1️⃣ Buyer / Investor Contact Details")
            b_name = st.text_input("Full Name (성명)", placeholder="John Doe / 홍길동")
            b_phone = st.text_input("Phone Number (연락처)", placeholder="+1 234 567 8900 / 010-1234-5678")
            b_email = st.text_input("Email (이메일)", value=st.session_state["logged_in_user"] or "")
            
            pay_option = st.radio(
                "Select Transaction Option (결제/주문 옵션 선택)",
                [
                    "Option A: Hold Deposit Only (예약 보증금 결제)",
                    "Option B: Full Acquisition / Rent Contract Booking (전액 매수/계약 주문)"
                ]
            )

            # Plus Choice: Professional Tax Service
            st.markdown("---")
            st.subheader("📑 Plus Choice Add-On (부가 서비스 선택)")
            include_tax_service = st.checkbox(
                "🏛️ Include Professional Real Estate Tax & Legal Advisory Service (+ $1,200 USD / ₩1,500,000)\n"
                "(부동산 매매/임대 계약 관련 전담 세무 자문 및 법률 검토 서비스 추가)",
                value=True
            )

        with col_pay:
            st.subheader("2️⃣ Real Estate Order & Payment Checkout")
            
            # Dynamic Price Calculation with Tax Service
            base_amt = est["price_deposit_num"] if "Option A" in pay_option else est["price_full_num"]
            tax_fee = 1200 if include_tax_service else 0
            total_amt = base_amt + tax_fee
            
            total_display_str = f"${total_amt:,} USD"
            
            st.metric("Total Order / Checkout Amount", total_display_str, delta=f"+$1,200 Tax Service" if include_tax_service else "No Tax Service")

            with st.form("estate_checkout_form"):
                card_num = st.text_input("Credit Card Number (카드번호)", placeholder="4000-1234-5678-9010")
                inq_notes = st.text_area("Inquiry Notes / Requested On-site Tour Date")
                submit_est_order = st.form_submit_button("🚀 Submit Order & Pay Reservation")

            if submit_est_order:
                if b_name and b_phone and card_num:
                    new_ord_id = f"EST-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
                    
                    st.session_state["estate_orders"].append({
                        "order_id": new_ord_id,
                        "property": title_curr,
                        "buyer_name": b_name,
                        "phone": b_phone,
                        "email": b_email,
                        "option": pay_option,
                        "tax_service": "Included (+ $1,200)" if include_tax_service else "Not Selected",
                        "amount": total_display_str,
                        "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                    })
                    st.balloons()
                    st.success("🎉 Property Order & Reservation Payment Submitted! Order recorded in Backend Management.")
                else:
                    st.error("⚠️ Please fill in all required fields (Name, Phone, Card Number).")

    else:
        st.title(t["estate_title"])
        st.write(t["estate_desc"])
        st.markdown("---")

        for key, est in real_estate_products.items():
            title_curr = est["title_en"] if lang == "English" else est["title_kr"]
            loc_curr = est["location_en"] if lang == "English" else est["location_kr"]
            size_curr = est["size_en"] if lang == "English" else est["size_kr"]
            desc_curr = est["desc_en"] if lang == "English" else est["desc_kr"]

            with st.container(border=True):
                c_left, c_right = st.columns([3, 1])
                with c_left:
                    st.subheader(f"[{est['badge']}] {title_curr}")
                    st.write(f"📍 {loc_curr} | 📐 {size_curr}")
                    st.write(f"💰 **Deposit**: {est['price_deposit_usd']} | **Full Value**: {est['price_full_usd']}")
                    st.write("🏛️ **Plus Choice Available**: Professional Real Estate Tax Advisory (+ $1,200)")
                    st.caption(desc_curr)
                with c_right:
                    if st.button("🔎 Details & Order Checkout", key=f"est_sub_{key}"):
                        st.query_params["estate"] = key
                        st.rerun()

# ==========================================
# 7. Feature 5: Support & Inquiries (Messaging System)
# ==========================================
elif page_selection == t["nav_5"]:
    st.title(t["support_title"])
    st.write(t["support_desc"])
    st.markdown("---")

    col_send, col_history = st.columns([1, 1])

    with col_send:
        st.subheader("📬 Submit a New Message / Support Ticket")
        with st.form("support_ticket_form"):
            inq_email = st.text_input("Your Email Address (이메일 주소)", value=st.session_state["logged_in_user"] or "")
            inq_category = st.selectbox(
                "Category (문의 유형)",
                [
                    "Tournament & Accommodation (대회 및 숙박)",
                    "Tennis Real Estate Investment (부동산 매매/임대)",
                    "Tax & Legal Advisory Service (세무 및 법률 자문)",
                    "AI Serve Analysis & Racket Calculator (AI 측정 및 라켓)",
                    "General & Account Support (일반 및 계정 문의)"
                ]
            )
            inq_subject = st.text_input("Subject (제목)", placeholder="e.g. Real estate acquisition tax consultation")
            inq_msg = st.text_area("Message Detail (문의 내용)", placeholder="Type your detailed message here...", height=150)
            
            submit_ticket = st.form_submit_button("📤 Submit Message")

        if submit_ticket:
            if inq_email and inq_subject and inq_msg:
                ticket_id = f"INQ-{datetime.datetime.now().strftime('%M%S')}"
                st.session_state["inquiries"].append({
                    "id": ticket_id,
                    "user_email": inq_email,
                    "subject": inq_subject,
                    "category": inq_category,
                    "message": inq_msg,
                    "status": "Pending Admin Reply",
                    "created_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "admin_reply": ""
                })
                st.success(f"✅ Message submitted successfully! Reference ID: {ticket_id}")
            else:
                st.error("⚠️ Please complete all input fields.")

    with col_history:
        st.subheader("📜 Ticket Inbox & Admin Replies")
        
        user_tickets = st.session_state["inquiries"]
        if st.session_state["logged_in_user"]:
            user_tickets = [q for q in st.session_state["inquiries"] if q["user_email"] == st.session_state["logged_in_user"]]

        if len(user_tickets) == 0:
            st.info("No tickets or messages found for your account.")
        else:
            for ticket in reversed(user_tickets):
                with st.expander(f"📌 [{ticket['status']}] {ticket['subject']} ({ticket['created_at']})"):
                    st.write(f"**Category**: {ticket['category']}")
                    st.write(f"**From**: {ticket['user_email']}")
                    st.write(f"**Message**: {ticket['message']}")
                    
                    if ticket["admin_reply"]:
                        st.success(f"💬 **Admin Reply**: {ticket['admin_reply']}")
                    else:
                        st.warning("⏳ Pending response from support backend.")

# ==========================================
# 8. Feature 6: Admin Dashboard Synchronization
# ==========================================
elif page_selection == t["nav_6"]:
    st.title("🔒 Admin / Backend Dashboard")

    if not st.session_state["admin_logged_in"]:
        st.warning("⚠️ Admin credentials required.")
        with st.form("admin_login_form"):
            admin_id = st.text_input("Admin ID", placeholder="admin")
            admin_pw = st.text_input("Password", type="password", placeholder="admin")
            if st.form_submit_button("Unlock Dashboard"):
                if admin_id == "admin" and admin_pw == "admin":
                    st.session_state["admin_logged_in"] = True
                    st.success("Authenticated!")
                    st.rerun()
                else:
                    st.error("Invalid credentials (admin/admin)")
    else:
        col_t, col_l = st.columns([4, 1])
        with col_t:
            st.success("🟢 Authenticated as Backend Administrator")
        with col_l:
            if st.button("Logout"):
                st.session_state["admin_logged_in"] = False
                st.rerun()

        st.markdown("---")
        
        tab1, tab2, tab3 = st.tabs([
            "🏢 Real Estate Purchase Orders & Tax Options",
            "🏆 Tournament & Resort Orders",
            "📩 Support Ticket Inbox & Reply Tool"
        ])

        with tab1:
            st.subheader("🏢 Real Estate Transactions Database (부동산 실시간 주문 및 세무 옵션)")
            if len(st.session_state["estate_orders"]) == 0:
                st.info("No real estate orders submitted yet.")
            else:
                st.dataframe(st.session_state["estate_orders"], use_container_width=True)

        with tab2:
            st.subheader("🏆 Tournament & Accommodation Registration Database")
            if len(st.session_state["match_orders"]) == 0:
                st.info("No tournament orders submitted yet.")
            else:
                st.dataframe(st.session_state["match_orders"], use_container_width=True)

        with tab3:
            st.subheader("📩 Support Messages & Reply Portal")
            if len(st.session_state["inquiries"]) == 0:
                st.info("No user messages in backend.")
            else:
                for idx, ticket in enumerate(st.session_state["inquiries"]):
                    with st.expander(f"✉️ Ticket {ticket['id']}: {ticket['subject']} - From {ticket['user_email']}"):
                        st.write(f"**Category**: {ticket['category']}")
                        st.write(f"**Date**: {ticket['created_at']}")
                        st.write(f"**User Message**: {ticket['message']}")
                        st.write(f"**Current Status**: `{ticket['status']}`")

                        reply_input = st.text_area(f"Reply to {ticket['user_email']}", value=ticket['admin_reply'], key=f"reply_area_{idx}")
                        if st.button("💬 Send / Update Reply", key=f"reply_btn_{idx}"):
                            st.session_state["inquiries"][idx]["admin_reply"] = reply_input
                            st.session_state["inquiries"][idx]["status"] = "Answered"
                            st.success("Reply saved! The user can now view it in their Support Inbox.")
                            st.rerun()

# Navigation Fallback
else:
    st.title(page_selection)
    st.info("Feature active.")
