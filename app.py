import streamlit as st
import datetime
import time

# ==========================================
# 1. Page Configuration
# ==========================================
st.set_page_config(
    page_title="ServeAI - AI 테니스 분석, 대회 & 투자 포털",
    page_icon="🎾",
    layout="wide"
)

# Initialize Session State
if "users" not in st.session_state:
    st.session_state["users"] = {"admin@serveai.com": "password123"}
if "logged_in_user" not in st.session_state:
    st.session_state["logged_in_user"] = None

# Databases
if "inquiries" not in st.session_state:
    st.session_state["inquiries"] = [
        {
            "title": "대회 룸셰어 매칭 질문입니다",
            "type": "대회 및 룸셰어 결제",
            "content": "2인 1실 배정 시 성별이 동일한 인원끼리 매칭되나요?",
            "user": "user01@gmail.com",
            "time": "2026-07-28 14:20",
            "reply": "네, 맞습니다! 동일 성별 및 비슷한 NTRP 레벨 배정이 기본 원칙입니다."
        }
    ]

if "match_orders" not in st.session_state:
    st.session_state["match_orders"] = [
        {
            "order_id": "ORD-20260729-01",
            "event": "2026 서울 아마추어 테니스 오픈",
            "name": "김철수",
            "phone": "010-9876-5432",
            "package": "대회 참가권 + 룸셰어 숙박 패키지",
            "amount": "₩180,000",
            "card": "4000-****-****-1234",
            "time": "2026-07-29 10:15"
        }
    ]

if "investment_inquiries" not in st.session_state:
    st.session_state["investment_inquiries"] = []

# ==========================================
# 2. Tournament Database
# ==========================================
tournament_products = {
    "match1": {
        "season": "제 1 회 (1st Event)",
        "title": "2026 서울 아마추어 테니스 오픈 · 참가 및 룸셰어 패키지",
        "date": "2026년 8월 15일 ~ 8월 16일",
        "location": "서울 올림픽공원 테니스장",
        "desc": "대회 참가 자격, 현장 AI 서브 속도 측정 및 선수촌/호텔 룸셰어 매칭 서비스가 포함된 패키지입니다.",
        "price_single_krw": 50000,
        "price_pkg_krw": 180000,
        "badge": "🟢 접수중 (Open)"
    },
    "match2": {
        "season": "제 2 회 (2nd Event)",
        "title": "2026 제주도 테니스 투어 · 참가 및 숙박 통합 패키지",
        "date": "2026년 9월 12일 ~ 9월 13일",
        "location": "제주 서귀포 테니스장",
        "desc": "제주 원정 테니스 대회! 참가비, 오션뷰 호텔 2인 룸셰어 숙박 및 ServeAI 진단 서비스 포함.",
        "price_single_krw": 60000,
        "price_pkg_krw": 250000,
        "badge": "🟢 접수중 (Open)"
    },
    "match3": {
        "season": "제 3 회 (3rd Event)",
        "title": "2026 부산 해운대 가을 마스터스 · 참가 신청",
        "date": "2026년 10월 17일 ~ 10월 18일",
        "location": "부산 스포원파크 테니스장",
        "desc": "부산 최대 규모 아마추어 대회 (NTRP 2.5 ~ 4.0+ 전 부문 모집).",
        "price_single_krw": 55000,
        "price_pkg_krw": 210000,
        "badge": "🟡 얼리버드 예약"
    }
}

# Real Estate & Investment Database
real_estate_products = {
    "estate1": {
        "category": "매매 (Sell)",
        "title": "강남 테헤란로 실내 테니스 아카데미 매매",
        "location": "서울 강남구 역삼동",
        "size": "전용 220평 (코트 3면 + 풀옵션 샤워실)",
        "desc": "월 매출 4,500만원 입증 완료. AI 서브 측정 장비 및 회원 300명 양도 포함.",
        "price_sale": "보증금 2억원 / 매매가 8억 5천만원",
        "roi": "예상 연 수익률 14.5%",
        "badge": "🔥 추천 매물"
    },
    "estate2": {
        "category": "임대 (Rent)",
        "title": "분당 정자동 최신식 실내 테니스장 롱텀 임대",
        "location": "경기 성남시 분당구",
        "size": "전용 150평 (실내 2면, 높은 층고 8m)",
        "desc": "주차 50대 가능. 층간소음 방지 설계 완료. 즉시 아카데미 영업 가능.",
        "price_sale": "보증금 1억원 / 월세 950만원",
        "roi": "즉시 입주 가능",
        "badge": "🟢 임대 가능"
    },
    "estate3": {
        "category": "투자 지분 참여 (School Investment)",
        "title": "ServeAI 2호점 '인천 송도 테니스 파크' 프랜차이즈 지분 투자",
        "location": "인천 연수구 송도동",
        "size": "야외 4면 + 실내 2면 대형 클럽",
        "desc": "ServeAI 기술이 탑재된 테니스 전문 학교 설립 사업. 최소 1 구좌부터 지분 참여 가능.",
        "price_sale": "1구좌당 3,000만원",
        "roi": "연 확정 수익률 9.0% + 이익 배당",
        "badge": "💎 지분 투자"
    }
}

# Navigation URL Routing
query_params = st.query_params
selected_tournament = query_params.get("item", None)
selected_estate = query_params.get("estate", None)

# ==========================================
# 3. Sidebar: User Auth & Navigation
# ==========================================
st.sidebar.title("🎾 ServeAI Portal")

# User Account System
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
    else:
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

# Navigation Menu Options
nav_options = [
    "⚡ AI 서브 속도 분석 (Speed Vision)",
    "🎾 AI 테니스 용구 추천",
    "🏆 테니스 대회 & 룸셰어 (Sub-Page)",
    "🏢 테니스 시설 투자 & 부동산 (Sub-Page)",
    "💬 고객 문의 & Q&A",
    "⚙️ 백엔드 / 관리자 대시보드"
]

page_selection = st.sidebar.radio("📌 주요 기능 메뉴 선택", nav_options)

# ==========================================
# 4. Feature 1: AI Speed Analysis
# ==========================================
if page_selection == "⚡ AI 서브 속도 분석 (Speed Vision)":
    st.title("⚡ ServeAI 컴퓨터 비전 서브 속도 분석")
    st.write("테니스 서브 동영상을 업로드하면 AI가 서브 궤적과 최고 속도(km/h)를 정밀 분석합니다.")
    
    uploaded_file = st.file_uploader("서브 분석용 영상 업로드 (MP4, MOV)", type=["mp4", "mov", "avi"])
    
    if uploaded_file is not None:
        st.video(uploaded_file)
        if st.button("🚀 AI 속도 분석 시작"):
            with st.spinner("🔍 CV 프레임 궤적 추적 및 최고 속도 계산 중..."):
                time.sleep(1.5)
            
            st.balloons()
            st.success("분석 완료!")
            
            col1, col2, col3 = st.columns(3)
            col1.metric("최고 서브 속도", "184 km/h", "+12 km/h 대비 상승")
            col2.metric("임팩트 타점 높이", "2.78 m", "정상 범위")
            col3.metric("볼 회전수 (Spin Rate)", "2,450 RPM", "Topspin Good")

            st.markdown("### 📊 Dynamic Velocity Profile")
            st.line_chart([20, 60, 110, 155, 184, 160, 120, 40])

# ==========================================
# 5. Feature 2: Equipment Recommender
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
# 6. Feature 3: Tournament Sub-Page
# ==========================================
elif page_selection == "🏆 테니스 대회 & 룸셰어 (Sub-Page)":
    if selected_tournament in tournament_products:
        item = tournament_products[selected_tournament]
        if st.button("⬅️ 전체 대회 목록으로 돌아가기"):
            st.query_params.clear()
            st.rerun()

        st.markdown(f"## 🏆 {item['season']}: {item['title']}")
        st.info(f"📅 **일정**: {item['date']} | 📍 **장소**: {item['location']}")
        st.write(item["desc"])
        
        col_info, col_pay = st.columns([1, 1])
        with col_info:
            st.subheader("1️⃣ 참가자 정보 입력")
            p_name = st.text_input("선수 성명", placeholder="홍길동")
            p_phone = st.text_input("연락처", placeholder="010-1234-5678")
            pkg_option = st.radio("신청 상품 선택", ["대회 참가권 단품", "대회 참가권 + 룸셰어 숙박 패키지"])

        with col_pay:
            st.subheader("2️⃣ 온라인 결제")
            amount_val = item['price_single_krw'] if "단품" in pkg_option else item['price_pkg_krw']
            amount_str = f"₩{amount_val:,}"
            st.metric("최종 결제 금액", amount_str)

            with st.form("subpage_pay_form"):
                card_num = st.text_input("신용카드 번호", placeholder="4000-1234-5678-9010")
                submit_pay = st.form_submit_button("🚀 즉시 결제하기")

            if submit_pay:
                if p_name and p_phone and card_num:
                    new_ord_id = f"ORD-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
                    st.session_state["match_orders"].append({
                        "order_id": new_ord_id,
                        "event": item['title'],
                        "name": p_name,
                        "phone": p_phone,
                        "package": pkg_option,
                        "amount": amount_str,
                        "card": card_num,
                        "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                    })
                    st.balloons()
                    st.success("🎉 결제 및 참가 신청이 완료되었습니다! (백엔드 대시보드에 기록됨)")
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
# 7. Feature 4: Real Estate & School Investment Sub-Page
# ==========================================
elif page_selection == "🏢 테니스 시설 투자 & 부동산 (Sub-Page)":
    if selected_estate in real_estate_products:
        est = real_estate_products[selected_estate]
        if st.button("⬅️ 전체 부동산/투자 목록으로 돌아가기"):
            st.query_params.clear()
            st.rerun()

        st.markdown(f"## 🏢 [{est['category']}] {est['title']}")
        st.success(f"📍 위치: {est['location']} | 📐 규모: {est['size']}")
        st.write(est["desc"])
        
        c_left, c_right = st.columns([1, 1])
        with c_left:
            st.subheader("💡 조건 및 수익률 분석")
            st.metric("조건/가액", est["price_sale"])
            st.metric("수익률 / 특이사항", est["roi"])
            
        with c_right:
            st.subheader("📞 매매/임대 및 투자 상담 신청")
            with st.form("estate_inquiry_form"):
                inv_name = st.text_input("신청인 성명")
                inv_phone = st.text_input("연락처")
                inv_budget = st.text_input("가용 투자/매수 예산", placeholder="예: 3억원")
                inv_memo = st.text_area("문의 사항 및 희망 현장 방문일")
                submit_inv = st.form_submit_button("🚀 상담 접수하기")

            if submit_inv:
                if inv_name and inv_phone:
                    st.session_state["investment_inquiries"].append({
                        "property": est['title'],
                        "name": inv_name,
                        "phone": inv_phone,
                        "budget": inv_budget,
                        "memo": inv_memo,
                        "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                    })
                    st.balloons()
                    st.success("✅ 상담 신청이 완료되었습니다. 백엔드 담당자가 확인 후 연락드리겠습니다.")
                else:
                    st.error("⚠️ 성명과 연락처를 작성해 주세요.")
    else:
        st.title("🏢 테니스 학교/아카데미 투자 & 부동산 매매 서브페이지")
        st.write("한국 내 테니스 실내외 코트/아카데미 매매, 임대, 그리고 프랜차이즈 지분 투자 기회를 확인하세요.")
        st.markdown("---")

        for key, est in real_estate_products.items():
            with st.container(border=True):
                c_left, c_right = st.columns([3, 1])
                with c_left:
                    st.subheader(f"[{est['category']}] {est['title']}")
                    st.write(f"📍 {est['location']} | 📐 {est['size']}")
                    st.write(f"💰 **조건**: {est['price_sale']} | 📈 **수익**: {est['roi']}")
                    st.caption(est["desc"])
                with c_right:
                    st.markdown(f"### {est['badge']}")
                    if st.button("🔎 상세보기 & 신청", key=f"est_btn_{key}"):
                        st.query_params["estate"] = key
                        st.rerun()

# ==========================================
# 8. Feature 5: Customer Communication (Q&A)
# ==========================================
elif page_selection == "💬 고객 문의 & Q&A":
    st.title("💬 고객 센터 & 1:1 커뮤니케이션")
    st.write("ServeAI 서비스, AI 분석 결과, 대회 참가 및 룸셰어 문의사항을 남겨주시면 빠르게 답변해 드립니다.")
    
    with st.form("inquiry_form"):
        st.subheader("📝 1:1 문의 작성")
        inq_title = st.text_input("문의 제목")
        inq_type = st.selectbox("문의 유형", ["AI 속도 분석 관련", "대회 및 룸셰어 결제", "부동산 및 투자 문의", "기타"])
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
                "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                "reply": None
            })
            st.success("✅ 문의가 정상적으로 접수되었습니다!")
        else:
            st.error("⚠️ 제목과 내용을 모두 입력해 주세요.")

    # Display Inquiries
    if len(st.session_state["inquiries"]) > 0:
        st.markdown("---")
        st.subheader("📋 접수된 문의 내역")
        for idx, inq in enumerate(reversed(st.session_state["inquiries"])):
            with st.expander(f"[{inq['type']}] {inq['title']} - (작성자: {inq['user']} | {inq['time']})"):
                st.write(f"**문의 내용**: {inq['content']}")
                if inq.get("reply"):
                    st.success(f"💬 **ServeAI 답변**: {inq['reply']}")
                else:
                    st.info("💬 **ServeAI 답변**: 담당자가 확인 중입니다.")

# ==========================================
# 9. Feature 6: Backend / Admin Dashboard
# ==========================================
elif page_selection == "⚙️ 백엔드 / 관리자 대시보드":
    st.title("⚙️ ServeAI 백엔드 통합 관리 대시보드")
    st.write("고객 주문/결제 내역, 1:1 문의 메세지 박스, 그리고 테니스 부동산 투자 상담 현황을 실시간 관리합니다.")
    st.markdown("---")

    tab1, tab2, tab3 = st.tabs(["💳 대회 주문 및 결제 내역", "📩 메세지 박스 (Q&A 관리)", "🏢 부동산/투자 상담 리스트"])

    # Tab 1: Orders and Payment
    with tab1:
        st.subheader("💳 대회 및 룸셰어 결제 주문 수집 (Order Database)")
        if len(st.session_state["match_orders"]) == 0:
            st.info("현재 접수된 결제 내역이 없습니다.")
        else:
            st.dataframe(st.session_state["match_orders"], use_container_width=True)

    # Tab 2: Message Box (Customer Inquiry Management)
    with tab2:
        st.subheader("📩 고객 1:1 문의 메세지 박스 (Customer Support Box)")
        if len(st.session_state["inquiries"]) == 0:
            st.info("접수된 문의 메시지가 없습니다.")
        else:
            for idx, inq in enumerate(st.session_state["inquiries"]):
                with st.expander(f"[{inq['time']}] {inq['title']} - {inq['user']}"):
                    st.write(f"**분류**: {inq['type']}")
                    st.write(f"**내역**: {inq['content']}")
                    st.write(f"**현재 답변**: {inq.get('reply', '답변 대기중')}")
                    
                    with st.form(key=f"reply_form_{idx}"):
                        reply_text = st.text_input("답변 작성/수정", value=inq.get("reply", "") or "")
                        submit_reply = st.form_submit_button("✉️ 답변 저장 및 고객 전송")
                        if submit_reply:
                            st.session_state["inquiries"][idx]["reply"] = reply_text
                            st.success("답변이 성공적으로 업데이트되었습니다!")
                            st.rerun()

    # Tab 3: Real Estate / School Investment Inquiries
    with tab3:
        st.subheader("🏢 테니스 학교 투자 및 부동산 매수 상담 내역")
        if len(st.session_state["investment_inquiries"]) == 0:
            st.info("접수된 투자/매수 상담 내역이 없습니다.")
        else:
            st.dataframe(st.session_state["investment_inquiries"], use_container_width=True)
