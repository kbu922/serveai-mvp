import streamlit as st
import datetime

# ==========================================
# 1. 페이지 기본 설정 (Page Config)
# ==========================================
st.set_page_config(
    page_title="ServeAI 테니스 대회 및 패키지 신청 포털",
    page_icon="🎾",
    layout="wide"
)

# 세션 스토리지 (결제 및 참가 신청 데이터 저장)
if "match_orders" not in st.session_state:
    st.session_state["match_orders"] = []

# ==========================================
# 2. 테니스 대회 및 상품 Schedule 데이터베이스
# ==========================================
tournament_products = {
    "match1": {
        "season": "제 1 회 (1st Event)",
        "title": "2026 서울 아마추어 테니스 오픈 · 참가 및 룸셰어 패키지",
        "date": "2026년 8월 15일 ~ 8월 16일 (토/일)",
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
        "date": "2026년 9월 12일 ~ 9월 13일 (토/일)",
        "location": "제주 서귀포 테니스장",
        "desc": "제주 원정 테니스 대회! 참가비, 오션뷰 호텔 2인 룸셰어 숙박 및 ServeAI 진단 서비스가 포함되어 있습니다.",
        "price_single_krw": 60000,
        "price_single_usd": 48.0,
        "price_pkg_krw": 250000,
        "price_pkg_usd": 195.0,
        "badge": "🟢 접수중 (Open)"
    },
    "match3": {
        "season": "제 3 회 (3rd Event)",
        "title": "2026 부산 해운대 가을 마스터스 · 참가 신청",
        "date": "2026년 10월 17일 ~ 10월 18일 (토/일)",
        "location": "부산 스포원파크 테니스장",
        "desc": "부산 최대 규모 아마추어 대회로, 초급부(NTRP 2.5-3.0) 및 고급부(NTRP 3.5+) 부문으로 진행됩니다.",
        "price_single_krw": 55000,
        "price_single_usd": 43.0,
        "price_pkg_krw": 210000,
        "price_pkg_usd": 165.0,
        "badge": "🟡 얼리버드 예약"
    },
    "match4": {
        "season": "제 4 회 (4th Event)",
        "title": "2026 인천 국제 동호인 테니스 교류전",
        "date": "2026년 11월 14일 ~ 11월 15일 (토/일)",
        "location": "인천 열우물테니스경기장",
        "desc": "국제 아마추어 테니스 교류전으로, 국내외 카드를 위한 VISA/Mastercard 간편 결제를 지원합니다.",
        "price_single_krw": 50000,
        "price_single_usd": 40.0,
        "price_pkg_krw": 190000,
        "price_pkg_usd": 150.0,
        "badge": "⚪ 오픈 예정"
    }
}

# ==========================================
# 3. 개별 URL 라우팅 (예: ?item=match1)
# ==========================================
query_params = st.query_params
selected_item_key = query_params.get("item", None)

# ==========================================
# 4. 사이드바: 대회 Schedule 및 개별 링크 생성
# ==========================================
st.sidebar.title("🎾 ServeAI 대회 일정")
st.sidebar.caption("아래 회차를 선택하면 해당 대회의 독립 신청/결제 페이지로 이동합니다:")

nav_choice = st.sidebar.radio(
    "대회 회차 선택:",
    options=["📅 전체 대회 Schedule 목록"] + [f"{item['season']} - {item['title']}" for item in tournament_products.values()]
)

st.sidebar.markdown("---")
st.sidebar.subheader("🔗 독립 상품 링크 파라미터")
for key, item in tournament_products.items():
    st.sidebar.markdown(f"**[{item['season']}]** `?item={key}`")

# ==========================================
# 5. 뷰 A: 개별 대회 신청 및 신용카드 결제 페이지
# ==========================================
def render_item_checkout(item_key):
    item = tournament_products[item_key]
    
    # 상단 목록 돌아가기 버튼
    if st.button("⬅️ 대회 Schedule 목록으로 돌아가기"):
        st.query_params.clear()
        st.rerun()

    st.markdown(f"## 🏆 {item['season']}: {item['title']}")
    st.info(f"📅 **대회 일정**: {item['date']} | 📍 **대회 장소**: {item['location']}")
    st.write(item["desc"])
    
    st.markdown("---")
    
    col_info, col_pay = st.columns([1, 1])

    # 좌측: 참가자 정보 입력 및 패키지 선택
    with col_info:
        st.subheader("1️⃣ 참가 선수 정보 입력")
        p_name = st.text_input("선수 성명 (Full Name)", placeholder="홍길동")
        p_phone = st.text_input("연락처 (Phone Number)", placeholder="010-1234-5678")
        p_passport = st.text_input("생년월일 또는 여권번호 (ID/Passport No.)", placeholder="900101 또는 M12345678")
        p_category = st.selectbox("참가 종목", ["남자 단식 (Men's Singles)", "여자 단식 (Women's Singles)", "남자 복식 (Men's Doubles)", "혼합 복식 (Mixed Doubles)"])
        
        st.markdown("---")
        st.subheader("📦 신청 상품 및 패키지 선택")
        pkg_option = st.radio(
            "상품 선택:",
            ["대회 참가권 단품 (Single Entry Fee)", "대회 참가권 + 룸셰어 숙박 패키지 (Entry + Room-Share Package)"],
            help="룸셰어 패키지 선택 시 동일 권역 참가자와 자동으로 호텔 숙박 매칭이 진행됩니다."
        )

    # 우측: 신용카드 결제
    with col_pay:
        st.subheader("2️⃣ 온라인 수강/참가비 결제")
        
        currency = st.radio("결제 화폐 (Currency)", ["KRW (₩)", "USD ($)"], horizontal=True)
        
        # 동적 금액 계산
        if "대회 참가권 단품" in pkg_option:
            amount_krw = item["price_single_krw"]
            amount_usd = item["price_single_usd"]
            pkg_title = "대회 참가권 단품"
        else:
            amount_krw = item["price_pkg_krw"]
            amount_usd = item["price_pkg_usd"]
            pkg_title = "대회 참가권 + 룸셰어 숙박 패키지"

        if currency == "KRW (₩)":
            pay_str = f"₩{amount_krw:,} KRW"
        else:
            pay_str = f"${amount_usd:.2f} USD"

        st.metric(label=f"최종 결제 금액 ({pkg_title})", value=pay_str)
        st.caption("🔒 256-bit SSL 보안 결제 (국내 모든 신용카드 및 해외 VISA / Mastercard 지원)")

        with st.form(key=f"pay_form_{item_key}"):
            card_name = st.text_input("카드 명의자 성명", placeholder="HONG GILDONG")
            card_num = st.text_input("카드 번호", placeholder="4000 1234 5678 9010", max_chars=19)
            
            c1, c2 = st.columns(2)
            with c1:
                card_exp = st.text_input("유효기간 (MM/YY)", placeholder="12/28", max_chars=5)
            with c2:
                card_cvc = st.text_input("CVC/CVV 번호", placeholder="123", type="password", max_chars=4)

            submit_btn = st.form_submit_button(f"🚀 {pay_str} 결제하기")

        if submit_btn:
            if not p_name or not p_phone or not p_passport:
                st.error("⚠️ 선수 성명, 연락처, 생년월일/여권번호를 모두 입력해 주세요.")
            elif not card_name or not card_num or not card_exp or not card_cvc:
                st.error("⚠️ 결제 카드 정보를 정확히 입력해 주세요.")
            else:
                with st.spinner("💳 결제 승인 및 참가 확정 처리 중..."):
                    import time
                    time.sleep(1.2)

                order_id = f"SERVEAI-{item_key.upper()}-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
                st.session_state["match_orders"].append({
                    "order_id": order_id,
                    "season": item["season"],
                    "match": item["title"],
                    "player": p_name,
                    "phone": p_phone,
                    "passport": p_passport,
                    "package": pkg_title,
                    "amount": pay_str,
                    "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })

                st.balloons()
                st.success("🎉 대회 신청 및 결제가 성공적으로 완료되었습니다! 확정 안내가 문자로 발송됩니다.")

                st.markdown("### 🧾 대회 참가 및 결제 확인서 (Receipt)")
                st.info(f"""
                • **주문 번호**: {order_id}
                • **신청 회차**: {item['season']} - {item['title']}
                • **대회 일정**: {item['date']}
                • **선수 성명**: {p_name}
                • **연락처**: {p_phone}
                • **선택 상품**: {pkg_title}
                • **결제 금액**: **{pay_str}**
                """)

# ==========================================
# 6. 뷰 B: 전체 대회 Schedule 목록 (Main Portal)
# ==========================================
def render_schedule_portal():
    st.title("🎾 ServeAI 테니스 대회 & 패키지 Schedule")
    st.write("원하시는 회차의 대회 상품을 선택하시면 개별 참가 신청 및 온라인 결제 페이지로 이동합니다.")
    st.markdown("---")

    for key, item in tournament_products.items():
        with st.container(border=True):
            col_left, col_right = st.columns([3, 1])
            with col_left:
                st.subheader(f"🏆 {item['season']}: {item['title']}")
                st.write(f"📅 **일정**: `{item['date']}` | 📍 **장소**: {item['location']}")
                st.write(f"🏷️ **상태**: {item['badge']} | **참가비**: ₩{item['price_single_krw']:,} (${item['price_single_usd']})")
                st.caption(item["desc"])
            
            with col_right:
                st.write("")
                st.write("")
                if st.button(f"👉 {item['season']} 신청하기", key=f"btn_nav_{key}"):
                    st.query_params["item"] = key
                    st.rerun()

    if len(st.session_state["match_orders"]) > 0:
        st.markdown("---")
        st.subheader("📊 실시간 참가 신청 및 결제 관리 내역 (관리자용)")
        st.dataframe(st.session_state["match_orders"])

# ==========================================
# 7. 메인 라우터 제어
# ==========================================
if selected_item_key in tournament_products:
    render_item_checkout(selected_item_key)
elif nav_choice != "📅 전체 대회 Schedule 목록":
    for k, v in tournament_products.items():
        if f"{v['season']} - {v['title']}" == nav_choice:
            render_item_checkout(k)
            break
else:
    render_schedule_portal()
