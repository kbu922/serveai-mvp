import time
import pandas as pd
import streamlit as st

# ==========================================
# 0. PAGE CONFIG & THEME STYLING
# ==========================================
st.set_page_config(
    page_title="Tennis AI Gear & Apparel Matcher",
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
    .badge-design {
        background-color: #1A1918;
        color: #FFFFFF;
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
st.title("🎾 AI Tennis Gear & Apparel Design Matcher")
st.caption("Upload performance video to analyze biomechanics, choose top-selling racquets, and explore AI-styled tennis dress design concepts.")

st.markdown("---")

# ==========================================
# 2. SIDEBAR CONFIGURATION
# ==========================================
st.sidebar.header("⚙️ Style & Player Profile")
gender = st.sidebar.selectbox("Apparel Line", ["Women's Performance Line", "Men's / Unisex Activewear"])
design_vibe = st.sidebar.selectbox("Preferred Aesthetic Vibe", [
    "Classic Court Heritage", 
    "Sleek Modern Minimalist", 
    "High-Tech Athletic Pro"
])
color_palette = st.sidebar.select_slider("Color Palette", options=["Monochrome", "Pastel Court", "Vibrant Accent"])

st.sidebar.markdown("---")
st.sidebar.info("💡 **AI Design Vector**: Video pose tracking matches dress swing-skirt silhouettes to your stroke movement patterns.")

# ==========================================
# 3. VIDEO UPLOAD & ANALYZER SECTION
# ==========================================
col_up, col_prev = st.columns([1, 1])

with col_up:
    st.subheader("📹 1. Upload Performance Footage")
    uploaded_video = st.file_uploader("Upload video file (.mp4, .mov)", type=["mp4", "mov"])
    analyze_btn = st.button("🚀 Analyze Motion & Match Equipment & Style Design")

with col_prev:
    st.subheader("👁️ Video Analysis Preview")
    if uploaded_video:
        st.video(uploaded_video)
    else:
        st.info("Upload a video to trigger swing telemetry and AI dress design recommendation.")

# ==========================================
# 4. ANALYSIS & RECOMMENDATION ENGINE
# ==========================================
if uploaded_video or analyze_btn:
    with st.spinner("Analyzing computer-vision swing vectors, mobility range & style recommendations..."):
        time.sleep(1.2) # Simulated processing delay
        
        st.markdown("---")
        st.subheader("📊 AI Calculated Diagnostics")

        # Metric Banner
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Est. Swing Speed", "88 mph", "+5 mph vs avg")
        m2.metric("Court Coverage Radius", "14.2 m/sec", "High Agility")
        m3.metric("Movement Style", "Aggressive Baseline", "Full Motion Scope")
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
        st.subheader("👗 3 AI Tennis Dress Design & Style Visual Recommendations")
        st.caption("AI-selected silhouette styles tailored to match court movement and aesthetics")

        d_col1, d_col2, d_col3 = st.columns(3)

        # DESIGN 1: Classic Pleated Heritage
        with d_col1:
            st.image(
                "https://images.unsplash.com/photo-1595435934249-5df7ed86e1c0?w=600&q=80",
                use_container_width=True,
                caption="AI Lookbook: Style 1 • Classic Pleated Heritage"
            )
            st.markdown("""
            <div class="dress-card-container">
                <div class="dress-card-content">
                    <span class="badge-design">Design 1 • Heritage Pleated</span>
                    <h4 style="margin-top:10px;">The Grand Slam Pleat Dress</h4>
                    <p style="font-size:13px; color:#555;">A timeless silhouette featuring knife-pleated skirts that flare dynamically during footwork, combined with a breathable polo neck.</p>
                    <hr>
                    <p style="font-size:13px; margin-bottom:4px;"><strong>Silhouette:</strong> Fitted Bodice & Box Pleats</p>
                    <p style="font-size:13px; margin-bottom:4px;"><strong>Fabric Tech:</strong> AeroDry Mesh & UV Protection</p>
                    <p style="font-size:13px; margin-bottom:0;"><strong>Vibe:</strong> Traditional Elegance / Country Club</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            d1_btn1, d1_btn2 = st.columns(2)
            with d1_btn1:
                if st.button("🛒 Buy Style 1 ($115)", key="buy_d1"):
                    st.toast("🛒 Added Classic Pleated Dress to cart!")
            with d1_btn2:
                if st.button("🎨 Custom Color", key="color_d1"):
                    st.toast("🎨 Opening Color Customizer for Design 1...")

        # DESIGN 2: Modern Seamless Minimalist
        with d_col2:
            st.image(
                "https://images.unsplash.com/photo-1566073771259-6a8506099945?w=600&q=80",
                use_container_width=True,
                caption="AI Lookbook: Style 2 • Modern Seamless Cut"
            )
            st.markdown("""
            <div class="dress-card-container">
                <div class="dress-card-content">
                    <span class="badge-design">Design 2 • Modern Minimalist</span>
                    <h4 style="margin-top:10px;">The Contour Aerodynamic Dress</h4>
                    <p style="font-size:13px; color:#555;">Ultra-sleek, clean-cut aesthetic with zero-friction bonded seams and a subtle side slit for maximum stride freedom.</p>
                    <hr>
                    <p style="font-size:13px; margin-bottom:4px;"><strong>Silhouette:</strong> Streamlined Bodycon A-Line</p>
                    <p style="font-size:13px; margin-bottom:4px;"><strong>Fabric Tech:</strong> 4-Way Stretch Compression</p>
                    <p style="font-size:13px; margin-bottom:0;"><strong>Vibe:</strong> Contemporary & High-Fashion</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            d2_btn1, d2_btn2 = st.columns(2)
            with d2_btn1:
                if st.button("🛒 Buy Style 2 ($125)", key="buy_d2"):
                    st.toast("🛒 Added Modern Seamless Dress to cart!")
            with d2_btn2:
                if st.button("🎨 Custom Color", key="color_d2"):
                    st.toast("🎨 Opening Color Customizer for Design 2...")

        # DESIGN 3: Dynamic Racerback Performance
        with d_col3:
            st.image(
                "https://images.unsplash.com/photo-1530549387789-4c1017266635?w=600&q=80",
                use_container_width=True,
                caption="AI Lookbook: Style 3 • Racerback Performance Cut"
            )
            st.markdown("""
            <div class="dress-card-container">
                <div class="dress-card-content">
                    <span class="badge-design">Design 3 • High-Tech Racerback</span>
                    <h4 style="margin-top:10px;">The Pro-Velocity Racerback</h4>
                    <p style="font-size:13px; color:#555;">Engineered for aggressive tournament play with keyhole shoulder cutouts for uninhibited overhead serve motion.</p>
                    <hr>
                    <p style="font-size:13px; margin-bottom:4px;"><strong>Silhouette:</strong> Ergonomic Cutout Racerback</p>
                    <p style="font-size:13px; margin-bottom:4px;"><strong>Fabric Tech:</strong> HyperVent Cool Touch Micro-Knit</p>
                    <p style="font-size:13px; margin-bottom:0;"><strong>Vibe:</strong> Athletic & Dynamic Performance</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            d3_btn1, d3_btn2 = st.columns(2)
            with d3_btn1:
                if st.button("🛒 Buy Style 3 ($110)", key="buy_d3"):
                    st.toast("🛒 Added Racerback Performance Dress to cart!")
            with d3_btn2:
                if st.button("🎨 Custom Color", key="color_d3"):
                    st.toast("🎨 Opening Color Customizer for Design 3...")

        st.markdown("---")
        st.success("✅ **Design Recommendations Updated**: You can choose any of the 3 dress designs or customize colors directly on the cards.")
