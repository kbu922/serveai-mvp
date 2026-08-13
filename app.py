import datetime
import time
import pandas as pd
import streamlit as st

# ==========================================
# 0. PAGE CONFIG & THEME STYLING
# ==========================================
st.set_page_config(
    page_title="Tennis AI Equipment & Apparel Matcher",
    page_icon="🎾",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    .stApp {
        background-color: #F7F5F0;
        color: #1A1918;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    h1, h2, h3, h4 {
        color: #1A1918 !important;
        font-weight: 600;
    }
    .stCard, div[data-testid="stExpander"], div[data-testid="stForm"] {
        background-color: #FFFFFF;
        border: 1px solid #E2DDD5;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03);
    }
    .stButton > button {
        background-color: #1A1918 !important;
        color: #FFFFFF !important;
        border-radius: 8px !important;
        border: none !important;
        font-weight: 600 !important;
        padding: 10px 16px !important;
        width: 100%;
    }
    .stButton > button:hover {
        background-color: #33312E !important;
    }
    .metric-box {
        background-color: #FFFFFF;
        border: 1px solid #E2DDD5;
        border-radius: 10px 10px 0 0;
        padding: 16px;
        text-align: center;
        min-height: 220px;
    }
    .dress-card-container {
        border: 1px solid #E2DDD5;
        border-radius: 12px;
        background-color: #FFFFFF;
        overflow: hidden;
        box-shadow: 0 4px 10px rgba(0,0,0,0.04);
        margin-bottom: 10px;
    }
    .dress-card-content {
        padding: 18px;
    }
    .badge-recommend {
        background-color: #1A1918;
        color: #FFFFFF;
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 0.5px;
        text-transform: uppercase;
    }
    .badge-standard {
        background-color: #E2DDD5;
        color: #1A1918;
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 0.5px;
        text-transform: uppercase;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 1. HEADER SECTION
# ==========================================
st.title("🎾 AI Tennis Gear & Visual Dress Matcher")
st.caption("Upload playing footage for motion analytics, top-selling racquet matching, and 1-click order fulfillment.")

st.markdown("---")

# ==========================================
# 2. SIDEBAR CONFIGURATION
# ==========================================
st.sidebar.header("⚙️ Athlete Body Profile")
gender = st.sidebar.selectbox("Outfit Fitting Line", ["Women's Performance Line", "Men's / Unisex Activewear"])
height_cm = st.sidebar.number_input("Height (cm)", min_value=140, max_value=210, value=168)
weight_kg = st.sidebar.number_input("Weight (kg)", min_value=40, max_value=120, value=58)
style_pref = st.sidebar.selectbox("Preferred Style Cut", [
    "Aerodynamic Slim Fit", 
    "Classic Pleated & Balanced", 
    "Relaxed Motion Cut"
])

st.sidebar.markdown("---")
st.sidebar.info("💡 **AI Sizing Vector**: Video body tracking calibrates recommended dress frame and torso proportions.")

# ==========================================
# 3. VIDEO UPLOAD & ANALYZER SECTION
# ==========================================
col_up, col_prev = st.columns([1, 1])

with col_up:
    st.subheader("📹 1. Upload Performance Footage")
    uploaded_video = st.file_uploader("Upload video file (.mp4, .mov)", type=["mp4", "mov"])
    analyze_btn = st.button("🚀 Analyze Motion & Generate AI Outfit Lookbook")

with col_prev:
    st.subheader("👁️ Video Analysis Preview")
    if uploaded_video:
        st.video(uploaded_video)
    else:
        st.info("Upload a video to initialize swing telemetry & AI outfit sizing.")

# ==========================================
# 4. ANALYSIS & RECOMMENDATION ENGINE
# ==========================================
if uploaded_video or analyze_btn:
    with st.spinner("Processing computer-vision pose estimation, swing velocity & dress size matching..."):
        time.sleep(1.2) # Simulated processing delay
        
        st.markdown("---")
        st.subheader("📊 AI Calculated Diagnostics")

        # Metric Banner
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Est. Swing Speed", "88 mph", "+5 mph vs avg")
        m2.metric("Posture Stability", "91%", "Optimal Core Balance")
        m3.metric("Measured Body Frame", f"{height_cm}cm / {weight_kg}kg", "Athletic Proportions")
        m4.metric("Recommended Tension", "52 lbs", "Hybrid Setup")

        st.write("")
        st.markdown("### 🎾 Top 3 Selling Racquets & Instant Buy Options")
        st.caption("Matched based on calculated acceleration and impact stability")

        # Top 3 Racquet Options with Buy Buttons
        r_col1, r_col2, r_col3 = st.columns(3)

        # RACQUET 1: Wilson Clash 100 v3
        with r_col1:
            st.markdown("""
            <div class="metric-box">
                <h4>1. Wilson Clash 100 v3</h4>
                <p><strong>Type:</strong> Arm Comfort & High Flex</p>
                <p><strong>Head Size:</strong> 100 sq in | <strong>Weight:</strong> 295g</p>
                <p><strong>SI3D Flex:</strong> Soft frame feedback with massive sweet spot.</p>
                <h3 style="color:#2D6A4F; margin-top:8px;">$299.00</h3>
            </div>
            """, unsafe_allow_html=True)
            
            btn_col1, btn_col2 = st.columns(2)
            with btn_col1:
                if st.button("🛒 Buy It Now", key="buy_clash"):
                    st.toast("🛒 Added Wilson Clash 100 v3 to cart!")
            with btn_col2:
                if st.button("⚙️ Custom String", key="string_clash"):
                    st.toast("⚙️ Opening custom stringing setup for Wilson Clash 100 v3...")

        # RACQUET 2: Babolat Pure Drive Gen11
        with r_col2:
            st.markdown("""
            <div class="metric-box">
                <h4>2. Babolat Pure Drive Gen11</h4>
                <p><strong>Type:</strong> Explosive Pace & Spin</p>
                <p><strong>Head Size:</strong> 100 sq in | <strong>Weight:</strong> 300g</p>
                <p><strong>Best For:</strong> Aggressive baseline power hitters.</p>
                <h3 style="color:#2D6A4F; margin-top:8px;">$279.00</h3>
            </div>
            """, unsafe_allow_html=True)
            
            btn_col1, btn_col2 = st.columns(2)
            with btn_col1:
                if st.button("🛒 Buy It Now", key="buy_babolat"):
                    st.toast("🛒 Added Babolat Pure Drive to cart!")
            with btn_col2:
                if st.button("⚙️ Custom String", key="string_babolat"):
                    st.toast("⚙️ Opening custom stringing setup for Babolat...")

        # RACQUET 3: Head Radical MP 2025
        with r_col3:
            st.markdown("""
            <div class="metric-box">
                <h4>3. Head Radical MP 2025</h4>
                <p><strong>Type:</strong> All-Court Precision</p>
                <p><strong>Head Size:</strong> 98 sq in | <strong>Weight:</strong> 300g</p>
                <p><strong>Best For:</strong> Directional placement and touch feel.</p>
                <h3 style="color:#2D6A4F; margin-top:8px;">$269.00</h3>
            </div>
            """, unsafe_allow_html=True)
            
            btn_col1, btn_col2 = st.columns(2)
            with btn_col1:
                if st.button("🛒 Buy It Now", key="buy_head"):
                    st.toast("🛒 Added Head Radical MP to cart!")
            with btn_col2:
                if st.button("⚙️ Custom String", key="string_head"):
                    st.toast("⚙️ Opening custom stringing setup for Head Radical...")

        st.markdown("---")
        st.subheader("👗 3 AI Tennis Dress Size & Style Visual Recommendations")
        st.caption(f"Visualized for profile height: **{height_cm} cm** | weight: **{weight_kg} kg**")

        d_col1, d_col2, d_col3 = st.columns(3)

        # AI Photo Dress 1
        with d_col1:
            st.image(
                "https://images.unsplash.com/photo-1595435934249-5df7ed86e1c0?w=600&q=80",
                use_container_width=True,
                caption="AI Model Preview: Size Small Fit Profile"
            )
            st.markdown("""
            <div class="dress-card-container">
                <div class="dress-card-content">
                    <span class="badge-standard">Option 1 • Size S</span>
                    <h4 style="margin-top:10px;">Pro Match Aerodynamic Cut</h4>
                    <p style="font-size:13px; color:#555;">Snug contouring for high-speed dynamic movements with minimal air resistance.</p>
                    <hr>
                    <p style="font-size:13px; margin-bottom:4px;"><strong>Bust / Chest:</strong> 82 - 87 cm</p>
                    <p style="font-size:13px; margin-bottom:4px;"><strong>Waistline:</strong> 64 - 69 cm</p>
                    <p style="font-size:13px; margin-bottom:4px;"><strong>Dress Length:</strong> 78 cm</p>
                    <p style="font-size:13px; margin-bottom:0;"><strong>Fit Type:</strong> Compression / Tight</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("🛍️ Order Size S ($110)", key="buy_dress_s"):
                st.toast("🛍️ Added Size S Dress to cart!")

        # AI Photo Dress 2 (Recommended)
        with d_col2:
            st.image(
                "https://images.unsplash.com/photo-1566073771259-6a8506099945?w=600&q=80",
                use_container_width=True,
                caption="AI Model Preview: Size Medium Recommended Fit"
            )
            st.markdown("""
            <div class="dress-card-container" style="border: 2px solid #1A1918;">
                <div class="dress-card-content">
                    <span class="badge-recommend">★ AI Match Choice • Size M</span>
                    <h4 style="margin-top:10px;">Classic Pleated Performance Dress</h4>
                    <p style="font-size:13px; color:#555;">Optimal balance of upper torso stretch and skirt flare for unrestricted overhead motion.</p>
                    <hr>
                    <p style="font-size:13px; margin-bottom:4px;"><strong>Bust / Chest:</strong> 88 - 93 cm</p>
                    <p style="font-size:13px; margin-bottom:4px;"><strong>Waistline:</strong> 70 - 75 cm</p>
                    <p style="font-size:13px; margin-bottom:4px;"><strong>Dress Length:</strong> 80 cm</p>
                    <p style="font-size:13px; margin-bottom:0;"><strong>Fit Type:</strong> Standard Athletic Fit</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("🛍️ Order Size M ($110) [Recommended]", key="buy_dress_m"):
                st.toast("🛍️ Added Recommended Size M Dress to cart!")

        # AI Photo Dress 3
        with d_col3:
            st.image(
                "https://images.unsplash.com/photo-1530549387789-4c1017266635?w=600&q=80",
                use_container_width=True,
                caption="AI Model Preview: Size Large Comfort Fit"
            )
            st.markdown("""
            <div class="dress-card-container">
                <div class="dress-card-content">
                    <span class="badge-standard">Option 3 • Size L</span>
                    <h4 style="margin-top:10px;">Breathe-Motion Relaxed Cut</h4>
                    <p style="font-size:13px; color:#555;">Generous ventilation and comfortable ease around shoulders for hot climate play.</p>
                    <hr>
                    <p style="font-size:13px; margin-bottom:4px;"><strong>Bust / Chest:</strong> 94 - 99 cm</p>
                    <p style="font-size:13px; margin-bottom:4px;"><strong>Waistline:</strong> 76 - 81 cm</p>
                    <p style="font-size:13px; margin-bottom:4px;"><strong>Dress Length:</strong> 82 cm</p>
                    <p style="font-size:13px; margin-bottom:0;"><strong>Fit Type:</strong> Comfort / Relaxed</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("🛍️ Order Size L ($110)", key="buy_dress_l"):
                st.toast("🛍️ Added Size L Dress to cart!")

        st.markdown("---")
        st.success("✅ **Interactive E-Commerce Enabled**: Clicking any button triggers cart alerts and seamless checkout handling.")
