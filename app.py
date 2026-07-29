import streamlit as st
import numpy as np

# ==========================================
# 1. Page Configuration (페이지 설정)
# ==========================================
st.set_page_config(
    page_title="ServeAI - AI Tennis Serve Analysis",
    page_icon="🎾",
    layout="wide"
)

# ==========================================
# 2. Recommendation Logic (추천 알고리즘 엔진)
# ==========================================
def calculate_recommended_tension(ntpr_str, current_tension_option, calculated_speed_kmh):
    """
    [KR] NTPR, 현재 텐션(모름 포함) 및 AI 측정 속도를 기반으로 최적 텐션(lbs)을 계산합니다.
    [EN] Calculates recommended tension based on NTPR, current tension, and AI speed.
    """
    # 1. NTPR 수치 추출 (Extract numerical value)
    try:
        ntpr_val = float(ntpr_str.split(" ")[1])
    except:
        ntpr_val = 2.5

    # 2. NTPR별 평균 기준 데이터 (Standard Baselines)
    standard_baseline_map = {2.0: 48, 2.5: 50, 3.0: 51, 3.5: 52, 4.0: 53, 4.5: 54, 5.0: 55}
    expected_speed_map = {2.0: 80.0, 2.5: 95.0, 3.0: 110.0, 3.5: 125.0, 4.0: 140.0, 4.5: 155.0, 5.0: 170.0}

    base_tension = standard_baseline_map.get(ntpr_val, 50)
    expected_speed = expected_speed_map.get(ntpr_val, 100.0)
    speed_diff = calculated_speed_kmh - expected_speed

    # 3. 사용자가 현재 텐션을 모르는 경우 (User does NOT know current tension)
    if current_tension_option is None or current_tension_option == 0:
        if speed_diff >= 10:
            rec_tension = base_tension + 2
            reason = f"NTPR({ntpr_val}) 대비 서브 속도가 빠르므로, 볼 제어력(Control) 확보를 위해 **{rec_tension} lbs**를 추천합니다. (Faster serve than average NTPR. Recommended {rec_tension} lbs for better control.)"
        elif speed_diff <= -10:
            rec_tension = base_tension - 2
            reason = f"타구 파워 보완과 엘보 보호를 위해 부드러운 **{rec_tension} lbs**로 시작하는 것을 추천합니다. (Recommended {rec_tension} lbs to enhance trampoline power and reduce arm strain.)"
        else:
            rec_tension = base_tension
            reason = f"측정된 속도 기반, NTPR({ntpr_val}) 표준 추천 텐션인 **{rec_tension} lbs**가 가장 적합합니다. (Optimal baseline tension for your NTPR level: {rec_tension} lbs.)"
        
        return rec_tension, reason, "Standard Guide"

    # 4. 사용자가 현재 텐션을 아는 경우 (User knows current tension)
    else:
        current_tension = int(current_tension_option)
        if speed_diff >= 15:
            rec_tension = current_tension + 3
            reason = "서브 속도가 매우 빠릅니다! 스핀과 볼 제어력을 위해 텐션을 +3 lbs 올려보세요. (High serve speed detected. Recommend +3 lbs for spin and control.)"
        elif 5 <= speed_diff < 15:
            rec_tension = current_tension + 2
            reason = "우수한 타구 파워를 보유하고 있습니다. 라인 아웃 방지를 위해 +2 lbs를 추천합니다. (Strong power. Recommend +2 lbs to prevent long balls.)"
        elif -5 <= speed_diff < 5:
            rec_tension = current_tension
            reason = "현재 텐션(lbs)이 사용자의 서브 속도 및 NTPR 레벨과 완벽하게 매칭됩니다! (Current tension is perfectly optimized for your serve speed!)"
        elif -15 <= speed_diff < -5:
            rec_tension = current_tension - 2
            reason = "비거리 확보를 위해 텐션을 -2 lbs 낮춰 트램펄린 효과를 활용해보세요. (Recommend -2 lbs to increase trampoline depth.)"
        else:
            rec_tension = current_tension - 3
            reason = "관절 부담을 줄이고 적은 힘으로 파워를 늘리기 위해 -3 lbs를 추천합니다. (Recommend -3 lbs to reduce elbow strain and increase depth.)"
        
        delta_val = rec_tension - current_tension
        delta_str = f"{delta_val:+d} lbs" if delta_val != 0 else "Optimal"
        return rec_tension, reason, delta_str


# ==========================================
# 3. Sidebar Setup (사이드바 사용자 프로필 입력)
# ==========================================
st.sidebar.header("⚙️ 사용자 프로필 설정 (User Profile)")

ntpr_input = st.sidebar.selectbox(
    "구력/실력 (NTPR Level)",
    ["NTPR 2.0 - 2.5", "NTPR 3.0 - 3.5", "NTPR 4.0 - 4.5", "NTPR 5.0+"]
)

racket_model = st.sidebar.text_input(
    "사용 중인 라켓 모델 (Racket Model)",
    value="Babolat Pure Drive 300g"
)

dont_know_tension = st.sidebar.checkbox("현재 텐션을 모름 (Don't know current tension)")

if dont_know_tension:
    current_tension_input = None
else:
    current_tension_input = st.sidebar.number_input(
        "현재 라켓 텐션 (Current Tension in lbs)",
        min_value=30, max_value=70, value=52
    )

st.sidebar.markdown("---")
st.sidebar.info("💡 **ServeAI MVP v1.0**\nSingle Camera Computer Vision & Intelligent Tension Recommender")


# ==========================================
# 4. Main UI Content (메인 화면 구성을 위한 UI)
# ==========================================
st.title("🎾 ServeAI: AI 기반 서브 분석 & 맞춤형 텐션 추천")
st.write("단일 발사 영상만으로 서브 속도를 측정하고, 사용자의 NTPR과 타구 속도를 분석하여 최적의 라켓 텐션(lbs)을 추천합니다.")

st.markdown("---")

# Video Upload Section
uploaded_file = st.file_uploader("🎥 서브 분석 비디오 업로드 (Upload Serve Video)", type=["mp4", "mov", "avi"])

if uploaded_file is not None:
    st.video(uploaded_file)
    
    if st.button("🚀 AI 분석 실행 (Analyze Serve Video)"):
        with st.spinner("AI가 영상을 분석 중입니다... (Processing Computer Vision Engine...)"):
            # Mock Processing Simulation
            import time
            time.sleep(2)
            
            # Simulated CV Speed Result (가상의 AI 측정 구속: 118.5 km/h)
            ai_measured_speed = 118.5
            
            # Run Recommendation Engine
            rec_lbs, rec_msg, delta_status = calculate_recommended_tension(
                ntpr_str=ntpr_input,
                current_tension_option=current_tension_input,
                calculated_speed_kmh=ai_measured_speed
            )
            
            st.success("✅ 분석이 완료되었습니다! (Analysis Complete)")
            st.markdown("### 📊 AI 분석 리포트 (Analysis Report)")
            
            # Metric Display Cards
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric(
                    label="측정된 서브 속도 (Measured Serve Speed)", 
                    value=f"{ai_measured_speed} km/h"
                )
            with col2:
                st.metric(
                    label="추천 라켓 텐션 (Recommended Tension)", 
                    value=f"{rec_lbs} lbs", 
                    delta=delta_status
                )
            with col3:
                st.metric(
                    label="타깃 라켓 (Target Racket)", 
                    value=racket_model if racket_model else "Standard"
                )
            
            # Recommendation Box
            st.info(f"💡 **AI 피드백 및 조정 제안 (AI Feedback)**:\n\n{rec_msg}")

else:
    st.info("👆 위 영역에 서브 분석을 위한 영상(MP4, MOV)을 업로드해주세요.")
