import streamlit as st
import datetime
import time

# ==========================================
# 1. Page Configuration
# ==========================================
st.set_page_config(
    page_title="ServeAI - 테니스 AI 속도 분석 & 대회 포털",
    page_icon="🎾",
    layout="wide"
)

# Initialize Session State
if "users" not in st.session_state:
    st.session_state["users"] = {"admin@serveai.com": "password123"}  # Pre-registered sample user
if "logged_in_user" not in st.session_state:
    st.session_state["logged_in_user"] = None
if "inquiries" not in st.session_state:
    st.session_state["inquiries"] = []
if "match_orders" not in st.session_state:
    st.session_state["match_orders"] = []

# ==========================================
# 2. Tournament Database (For Sub-Page)
# ==========================================
tournament_products = {
    "match1": {
        "season": "제 1 회 (1st Event)",
        "title": "2026 서울 아마추어 테니스 오픈 · 참가 및 룸셰어 패키지",
        "date": "2026년 8월 15일 ~ 8월 16일",
        "location": "서울 올림픽공원 테니스장",
        "desc": "대회 참가 자격, 현장 AI 서브 속도 측정 및 선수촌/호텔 룸셰어 매칭 서비스가 포함된 패키지입니다.",
        "price_single_krw": 50000,
        "price_single_usd": 40.0,
        "price_pkg_krw": 180000,
        "price_pkg_usd": 140.0,
        "badge": "🟢 접수중 (Open)"
    },
    "match2": {
        "season": "제 2 회 (2nd Event)",
        "title": "2026 제주도 테니스 투어 · 참가 및 숙박 통합 패키지",
        "date": "2026년 9월 12일 ~ 9월 13일",
        "location": "제주 서귀포 테니스장",
        "desc": "제주 원정 테니스 대회! 참가비, 오션뷰 호텔 2인 룸셰어 숙박 및 ServeAI 진단 서비스 포함.",
        "price_single_krw": 60000,
        "price_single_usd": 48.0,
        "price_pkg_krw": 250000,
        "price_pkg_usd": 195.0,
        "badge": "🟢 접수중 (Open)"
    },
    "match3": {
        "season": "제 3 회 (3rd Event)",
        "title": "2026 부산 해운대 가을 마스터스 · 참가 신청",
        "date": "2026년 10월 17일 ~ 10월 18일",
        "location": "부산 스포원파크 테니스장",
        "desc": "부산 최대 규모 아마추어 대회 (NTRP 2.5 ~ 4.0+ 전 부문 모집).",
        "price_single_krw": 55000,
        "price_single_usd": 43.0,
        "price_pkg_krw": 210000,
        "price_pkg_usd": 165.0,
        "badge": "🟡 얼리버드 예약"
    }
}

# Navigation URL Routing
query_params = st.query_params
selected_item_key = query_params.get("item", None)

# ==========================================
# 3. Sidebar: User Auth & Main Navigation
# ==========================================
st.sidebar.title("🎾 ServeAI Portal")

# User Account System (Login / Register)
st.sidebar.markdown("---")
if st.session_state["logged_in_user"] is None:
    st.sidebar.subheader("👤 회원 로그인 및 가입")
    auth_mode = st.sidebar.radio("메뉴 선택", ["로그인", "회원가입"], horizontal=True)
    
    if auth_mode == "로그인":
        email_in = st.sidebar.text_input("이메일 주소")
        pw_in = st.sidebar.text_input("비밀번호", type="password")
        if st.sidebar.button("로그인"):
            if email_in in st.session_state["users"] and st.session_state["users"][email_in] == pw_in:
                st.session_state["logged_in_user"] = email_in
                st.sidebar.success(f"환영합니다, {email_in}님!")
                st.rerun()
            else:
                st.sidebar.error("이메일 또는 비밀번호가 일치하지 않습니다.")
    else: # 회원가입
        reg_email = st.sidebar.text_input("신규 이메일")
        reg_pw = st.sidebar.text_input("신규 비밀번호", type="password")
        if st.sidebar.button("가입하기"):
            if reg_email and reg_pw:
                st.session_state["users"][reg_email] = reg_pw
                st.sidebar.success("회원가입 완료! 로그인해 주세요.")
            else:
                st.sidebar.warning("모든 항목을 입력해 주세요.")
else:
    st.sidebar.success(f"🟢 **{st.session_state['logged_in_user']}** 님 로그인 중")
    if st.sidebar.button("로그아웃"):
        st.session_state["logged_in_user"] = None
        st.rerun()

st.sidebar.markdown("---")

# Main Navigation
page_selection = st.sidebar.radio(
    "📌 주요 기능 메뉴 선택",
    ["⚡ AI 서브 속도 분석 (Speed Vision)", "🎾 AI 테니스 용구 추천", "🏆 테니스 대회 & 룸셰어 (Sub-Page)", "💬 고객 문의 & Q&A"]
)

# ==========================================
# 4. Feature 1: AI Speed Analysis (Original)
# ==========================================
if page_selection == "⚡ AI 서브 속도 분석 (Speed Vision)":
    st.title("⚡ ServeAI 컴퓨터 비전 서브 속도 분석")
    st.write("테니스 서브 동영상을 업로드하면 AI가 서브 궤적과 최고 속도(km/h)를 정밀 분석합니다.")
    
    uploaded_file = st.file_uploader("서브 분석용 영상 업로드 (MP4, MOV)", type=["mp4", "mov", "avi"])
    
    if uploaded_file is not None:
        st.video(uploaded_file)
        if st.button("🚀 AI 속도 분석 시작"):
            with st.spinner("🔍 CV 프레임 궤적 추적 및 최고 속도 계산 중..."):
                time.sleep(2.0)
            
            st.balloons()
            st.success("분석 완료!")
            
            col1, col2, col3 = st.columns(3)
            col1.metric("최고 서브 속도", "184 km/h", "+12 km/h 대비 상승")
            col2.metric("임팩트 타점 높이", "2.78 m", "정상 범위")
            col3.metric("볼 회전수 (Spin Rate)", "2,450 RPM", "Topspin Good")

            st.markdown("### 📊 Dynamic Velocity Profile")
            st.line_chart([20, 60, 110, 155, 184, 160, 120, 40])

# ==========================================
# 5. Feature 2: Equipment Recommender (Original)
# ==========================================
elif page_selection == "🎾 AI 테니스 용구 추천":
    st.title("🎾 AI 맞춤형 테니스 라켓 & 스트링 추천")
    st.write("플레이 스타일과 서브 데이터를 기반으로 최적의 장비와 스트링 텐션을 추천해 드립니다.")
    
    col1, col2 = st.columns(2)
    with col1:
        play_style = st.selectbox("주요 플레이 스타일", ["공격형 베이스라이너", "서브 앤 발리어", "올라운더", "수비형 플레이어"])
        ntrp_level = st.select_slider("NTRP 레벨", options=["2.0", "2.5", "3.0", "3.5", "4.0", "4.5+"])
    with col2:
        arm_concern = st.radio("엘보우/팔 통증 여부", ["없음", "약간 있음", "심함 (부드러운 라켓 필요)"])
        preferred_brand = st.multiselect("선호 브랜드", ["Babolat", "Wilson", "Head", "Yonex", "Technifibre"])

    if st.button("🎯 맞춤 장비 추천받기"):
        st.markdown("---")
        st.subheader("💡 ServeAI 추천 장비 리포트")
        
        c1, c2 = st.columns(2)
        with c1:
            st.image("https://images.unsplash.com/photo-1617083934555-ac7d4fed8814?w=500", caption="추천 라켓", width=300)
            st.write("**추천 라켓**: Babolat Pure Aero 2026")
            st.write("**스펙**: 300g | 100 sq.in | 16x19 Pattern")
        with c2:
            st.write("### ⚙️ 추천 스트링 및 텐션 셋팅")
            st.info("""
            • **추천 스트링**: Luxilon ALU Power 1.25mm  
            • **권장 텐션**: **메인 51 lbs / 크로스 49 lbs**  
            • **추천 이유**: 강한 서브 스핀과 탑스핀 궤적에 최적화된 파워형 조합입니다.
            """)

# ==========================================
# 6. Feature 3: Tournament & Room-Share (Sub-Page)
# ==========================================
elif page_selection == "🏆 테니스 대회 & 룸셰어 (Sub-Page)":
    
    # Sub-Page Logic for direct URL params or main list view
    if selected_item_key in tournament_products:
        item = tournament_products[selected_item_key]
        if st.button("⬅️ 전체 대회 Schedule 목록으로 돌아가기"):
            st.query_params.clear()
            st.rerun()

        st.markdown(f"## 🏆 {item['season']}: {item['title']}")
        st.info(f"📅 **대회 일정**: {item['date']} | 📍 **대회 장소**: {item['location']}")
        st.write(item["desc"])
        
        col_info, col_pay = st.columns([1, 1])
        with col_info:
            st.subheader("1️⃣ 참가 정보 입력")
            p_name = st.text_input("선수 성명", placeholder="홍길동")
            p_phone = st.text_input("연락처", placeholder="010-1234-5678")
            pkg_option = st.radio("신청 상품 선택", ["대회 참가권 단품", "대회 참가권 + 룸셰어 숙박 패키지"])

        with col_pay:
            st.subheader("2️⃣ 온라인 결제")
            currency = st.radio("결제 화폐", ["KRW (₩)", "USD ($)"], horizontal=True)
            amount_str = f"₩{item['price_single_krw']:,}" if "단품" in pkg_option else f"₩{item['price_pkg_krw']:,}"
            st.metric("최종 결제 금액", amount_str)

            with st.form("subpage_pay_form"):
                card_num = st.text_input("신용카드 번호", placeholder="4000 1234 5678 9010")
                submit_pay = st.form_submit_button("🚀 즉시 결제하기")

            if submit_pay:
                if p_name and p_phone and card_num:
                    st.balloons()
                    st.success("🎉 결제 및 참가 신청이 완료되었습니다!")
                else:
                    st.error("⚠️ 모든 필수 항목을 입력해 주세요.")
    else:
        st.title("🏆 ServeAI 테니스 대회 & 룸셰어 서브페이지")
        st.write("전국 대회 일정 확인, 참가 신청 및 동호인 룸셰어 결제를 위한 전용 페이지입니다.")
        st.markdown("---")

        for key, item in tournament_products.items():
            with st.container(border=True):
                c_left, c_right = st.columns([3, 1])
                with c_left:
                    st.subheader(f"{item['season']}: {item['title']}")
                    st.write(f"📅 일정: {item['date']} | 📍 장소: {item['location']}")
                    st.caption(item["desc"])
                with c_right:
                    if st.button(f"👉 {item['season']} 신청하기", key=f"sub_btn_{key}"):
                        st.query_params["item"] = key
                        st.rerun()

# ==========================================
# 7. Feature 4: Customer Communication / Q&A
# ==========================================
elif page_selection == "💬 고객 문의 & Q&A":
    st.title("💬 고객 센터 & 1:1 커뮤니케이션")
    st.write("ServeAI 서비스, AI 분석 결과, 대회 참가 및 룸셰어 문의사항을 남겨주시면 빠르게 답변해 드립니다.")
    
    with st.form("inquiry_form"):
        st.subheader("📝 1:1 문의 작성")
        inq_title = st.text_input("문의 제목")
        inq_type = st.selectbox("문의 유형", ["AI 속도 분석 관련", "대회 및 룸셰어 결제", "계정 및 기타"])
        inq_content = st.text_area("문의 내용")
        
        user_email_display = st.session_state["logged_in_user"] if st.session_state["logged_in_user"] else "비회원"
        st.caption(f"작성자: {user_email_display}")
        
        submit_inq = st.form_submit_button("📩 문의 제출하기")

    if submit_inq:
        if inq_title and inq_content:
            st.session_state["inquiries"].append({
                "title": inq_title,
                "type": inq_type,
                "content": inq_content,
                "user": user_email_display,
                "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            })
            st.success("✅ 문의가 정상적으로 접수되었습니다!")
        else:
            st.error("⚠️ 제목과 내용을 모두 입력해 주세요.")

    # Display Submitted Inquiries
    if len(st.session_state["inquiries"]) > 0:
        st.markdown("---")
        st.subheader("📋 접수된 문의 내역")
        for idx, inq in enumerate(reversed(st.session_state["inquiries"])):
            with st.expander(f"[{inq['type']}] {inq['title']} - (작성자: {inq['user']} | {inq['time']})"):
                st.write(inq["content"])
                st.info("💬 **ServeAI 답변**: 접수해 주셔서 감사합니다. 담당자가 확인 후 답변드릴 예정입니다.")
