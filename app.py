import streamlit as st
import time

# 페이지 기본 설정
st.set_page_config(
    page_title="ServeAI - AI 테니스 서브 분석 플랫폼",
    page_icon="🎾",
    layout="centered"
)

# 커스텀 CSS 스타일링
st.markdown("""
    <style>
    .main-header {
        font-size: 2.2rem;
        color: #2E7D32;
        text-align: center;
        font-weight: bold;
        margin-bottom: 5px;
    }
    .sub-header {
        font-size: 1.0rem;
        color: #666666;
        text-align: center;
        margin-bottom: 25px;
    }
    .metric-card {
        background-color: #F0F4F8;
        padding: 20px;
        border-radius: 12px;
        border-left: 5px solid #2E7D32;
        margin-bottom: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# 메인 타이틀 영역
st.markdown('<div class="main-header">🎾 ServeAI (AI 테니스 분석 MVP)</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Computer Vision 기반 타구 시속 분석 & 맞춤형 텐션 리포트</div>', unsafe_allow_html=True)

st.divider()

# 사이드바: 사용자 프로필 입력
st.sidebar.header("⚙️ 사용자 프로필 설정")
player_level = st.sidebar.selectbox("구력/실력 (NTPR)", ["NTPR 2.0 - 2.5 (초급)", "NTPR 3.0 - 3.5 (중급)", "NTPR 4.0 이상 (상급)"])
racket_model = st.sidebar.text_input("사용 중인 라켓 모델", value="Babolat Pure Drive 300g")
current_tension = st.sidebar.number_input("현재 라켓 텐션 (lbs)", min_value=35, max_value=65, value=52)

# 메인 화면: 비디오 업로드 및 분석
st.subheader("1. 서브 영상 업로드")
uploaded_file = st.file_uploader("분석할 테니스 서브 영상(MP4, MOV)을 업로드하세요", type=["mp4", "mov", "avi"])

if uploaded_file is not None:
    # 업로드 비디오 재생
    st.video(uploaded_file)
    
    st.markdown("---")
    st.subheader("2. AI 데이터 분석")
    
    # AI 분석 실행 버튼
    if st.button("🚀 AI 서브 분석 시작", type="primary"):
        with st.spinner("AI가 영상을 프레임 단위로 분석 중입니다 (임팩트 지점 및 프레임 레이트 계산 중)..."):
            time.sleep(2)  # 시뮬레이션 대기 시간
        
        st.success("✅ 분석이 성공적으로 완료되었습니다!")
        
        # 핵심 측정 지표 출력
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(label="서브 추정 시속", value="118.5 km/h", delta="+5.2 km/h (평균 대비)")
        with col2:
            st.metric(label="임팩트 높이", value="2.42 m", delta="양호")
        with col3:
            st.metric(label="볼 회전수 (추정)", value="1,850 RPM", delta="Top-Spin")

        st.markdown("---")
        st.subheader("3. 맞춤형 라켓 & 텐션 추천 리포트")
        
        # 진단 및 추천 리포트
        st.markdown(f"""
        <div class="metric-card">
            <h4>💡 AI 맞춤 진단 결과</h4>
            <ul>
                <li><b>현재 라켓:</b> {racket_model}</li>
                <li><b>측정 시속(118.5 km/h) 기반 추천 텐션:</b> <span style="color:#D32F2F; font-weight:bold;">49 - 51 lbs</span> (폴리에스터 스트링 기준)</li>
                <li><b>분석 제언:</b> 현재 설정된 {current_tension}lbs 텐션은 측정된 서브 시속 대비 다소 높게 설정되어 있습니다. 텐션을 2lbs 낮추면 비거리가 향상되며, 관절 부담 완화 및 컨트롤 유지에 도움이 됩니다.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        # 데이터 시각화 (그래프)
        st.caption("📊 프레임별 속도 변화 추이")
        chart_data = {
            "프레임 (Frame)": [1, 2, 3, 4, 5, 6, 7],
            "볼 속도 (km/h)": [0, 45, 118.5, 112, 105, 98, 85]
        }
        st.line_chart(chart_data, x="프레임 (Frame)", y="볼 속도 (km/h)")

else:
    st.info("👆 위 영역에 서브 영상 파일을 업로드하면 AI 시속 분석과 텐션 추천 리포트가 생성됩니다.")

st.markdown("---")
st.caption("© 2026 ServeAI Tech. OASIS-5 창업비자 MVP 검증용 웹 애플리케이션")
