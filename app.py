import random
import time
import urllib.parse
import streamlit as st

# ==========================================
# 0. PAGE CONFIG & THEME STYLING
# ==========================================
st.set_page_config(
    page_title="Tennis AI Gear & Studio Lookbook Generator",
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

# Helper function with HIGH-ELEGANCE / BEAUTIFUL MODEL photo parameters
def get_beautiful_ai_image(prompt_details: str, seed: int = None) -> str:
    if seed is None:
        seed = random.randint(1000, 99999)
    
    # Enhanced quality modifiers for flawless, beautiful, editorial aesthetics
    quality_modifiers = (
        ", breathtakingly beautiful gorgeous athletic female model, perfect face features, "
        "fashion editorial photography, shot on 85mm lens, f1.4 bokeh background, golden hour natural light, "
        "high fashion magazine cover quality, elegant pose on luxury tennis court, ultra clear focus, 8k resolution"
    )
    full_prompt = prompt_details + quality_modifiers
    encoded_prompt = urllib.parse.quote(full_prompt)
    return f"https://image.pollinations.ai/prompt/{encoded_prompt}?seed={seed}&width=600&height=800&nologo=true"

# Initialize Session State Seed
if "img_seed" not in st.session_state:
    st.session_state.img_seed = random.randint(1000, 9999)

# ==========================================
# 1. HEADER SECTION
# ==========================================
st.title("🎾 AI Tennis Gear & High-Fashion Lookbook Generator")
st.caption("Upload your performance video for swing analytics, top-selling racquet matching, and luxury studio-grade AI apparel rendering.")

st.markdown("---")

# ==========================================
# 2. SIDEBAR CONFIGURATION
# ==========================================
st.sidebar.header("⚙️ Style & Aesthetic Profile")
gender = st.sidebar.selectbox("Apparel Line", ["Women's Performance Line", "Men's / Unisex Activewear"])
design_vibe = st.sidebar.selectbox("Preferred Style Concept", [
    "High-Fashion Luxury Heritage", 
    "Sleek Ultra-Modern Minimalist", 
    "Chic Court Couture"
])
dress_color = st.sidebar.selectbox("Primary Palette", ["Crisp Pure White", "Pastel Soft Mint", "Midnight Navy", "Champagne Gold", "Ruby Red"])

if st.sidebar.button("✨ Generate Stunning New AI Photos"):
    st.session_state.img_seed = random.randint(10000, 99999)
    st.toast("✨ Synthesizing new high-fashion photo renders...")

st.sidebar.markdown("---")
st.sidebar.info("📸 **Studio Rendering Engine**: Generates 85mm portrait-grade editorial shots with natural studio lighting.")

# ==========================================
# 3. VIDEO UPLOAD & ANALYZER SECTION
# ==========================================
col_up, col_prev = st.columns([1, 1])

with col_up:
    st.subheader("📹 1. Upload Performance Footage")
    uploaded_video = st.file_uploader("Upload video file (.mp4, .mov)", type=["mp4", "mov"])
    analyze_btn = st.button("🚀 Analyze Motion & Render High-Fashion Lookbook")

with col_prev:
    st.subheader("👁️ Video Analysis Preview")
    if uploaded_video:
        st.video(uploaded_video)
    else:
        st.info("Upload a video to trigger motion diagnostics and AI fashion photography.")

# ==========================================
# 4. ANALYSIS & RECOMMENDATION ENGINE
# ==========================================
if uploaded_video or analyze_btn:
    with st.spinner("Rendering high-fashion AI photography and running motion diagnostics..."):
        time.sleep(1.0)
        
        st.markdown("---")
        st.subheader("📊 AI Calculated Diagnostics")

        # Metric Banner
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Est. Swing Speed", "88 mph", "+5 mph vs avg")
        m2.metric("Court Mobility", "14.2 m/sec", "High Agility")
        m3.metric("Movement Profile", "Aggressive Baseline", "Full Motion Scope")
        m4.metric("Recommended Tension", "52 lbs", "Hybrid Setup")

        st.write("")
        st.markdown("### 🎾 Top 3 Selling Racquets & Instant Buy Options")
        st.caption("Matched based on calculated acceleration and frame feedback")

        # Top 3 Racquet Options
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
        st.subheader("👗 High-Fashion Editorial Lookbook: 3 Luxury Dress Designs")
        st.caption("Studio-rendered visuals of elegant tennis couture tailored for optimal movement and style.")

        d_col1, d_col2, d_col3 = st.columns(3)
        base_seed = st.session_state.img_seed

        # PROMPT 1: Luxury Pleated Heritage
        prompt_1 = f"photorealistic fashion editorial photo of stunning gorgeous female tennis model wearing a luxury {dress_color} designer pleated tennis dress with subtle golden trim"
        url_1 = get_beautiful_ai_image(prompt_1, seed=base_seed)

        # PROMPT 2: Sleek Contour Couture
        prompt_2 = f"photorealistic Vogue magazine portrait of beautiful elegant female tennis player wearing a sleek fitted {dress_color} modern high neck tennis dress, graceful holding tennis racket"
        url_2 = get_beautiful_ai_image(prompt_2, seed=base_seed + 15)

        # PROMPT 3: Graceful Active Performance
        prompt_3 = f"full length photorealistic action portrait of an attractive female tennis athlete wearing a beautiful {dress_color} racerback luxury tennis dress, sun flare, serene tennis club court background"
        url_3 = get_beautiful_ai_image(prompt_3, seed=base_seed + 30)

        # DESIGN 1
        with d_col1:
            st.image(url_1, use_container_width=True, caption="Studio Lookbook: Heritage Pleated Luxury")
            st.markdown("""
            <div class="dress-card-container">
                <div class="dress-card-content">
                    <span class="badge-design">Design 1 • Heritage Couture</span>
                    <h4 style="margin-top:10px;">The Royal Court Pleated Dress</h4>
                    <p style="font-size:13px; color:#555;">Graceful knife-pleated flare silhouette inspired by classic Grand Slam elegance and refined craftsmanship.</p>
                    <hr>
                    <p style="font-size:13px; margin-bottom:4px;"><strong>Silhouette:</strong> Pleated A-Line Cut</p>
                    <p style="font-size:13px; margin-bottom:0;"><strong>Fabric Tech:</strong> AeroDry Breathable Silk-Knit</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            d1_btn1, d1_btn2 = st.columns(2)
            with d1_btn1:
                if st.button("🛒 Buy Style 1 ($145)", key="buy_d1"):
                    st.toast("🛒 Added Heritage Pleated Dress to cart!")
            with d1_btn2:
                if st.button("⚡ New Photo", key="regen_d1"):
                    st.session_state.img_seed += 1
                    st.rerun()

        # DESIGN 2
        with d_col2:
            st.image(url_2, use_container_width=True, caption="Studio Lookbook: Sleek Contour Minimalist")
            st.markdown("""
            <div class="dress-card-container">
                <div class="dress-card-content">
                    <span class="badge-design">Design 2 • Modern Minimalist</span>
                    <h4 style="margin-top:10px;">The Riviera Contour Dress</h4>
                    <p style="font-size:13px; color:#555;">An ultra-sleek, zero-friction sculpt design offering soft compression and high motion agility on serves.</p>
                    <hr>
                    <p style="font-size:13px; margin-bottom:4px;"><strong>Silhouette:</strong> Sculpted Bodycon</p>
                    <p style="font-size:13px; margin-bottom:0;"><strong>Fabric Tech:</strong> 4-Way Luxe Compression</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            d2_btn1, d2_btn2 = st.columns(2)
            with d2_btn1:
                if st.button("🛒 Buy Style 2 ($155)", key="buy_d2"):
                    st.toast("🛒 Added Modern Minimalist Dress to cart!")
            with d2_btn2:
                if st.button("⚡ New Photo", key="regen_d2"):
                    st.session_state.img_seed += 2
                    st.rerun()

        # DESIGN 3
        with d_col3:
            st.image(url_3, use_container_width=True, caption="Studio Lookbook: High-Tech Racerback Pro")
            st.markdown("""
            <div class="dress-card-container">
                <div class="dress-card-content">
                    <span class="badge-design">Design 3 • High-Tech Racerback</span>
                    <h4 style="margin-top:10px;">The Monaco Pro Racerback</h4>
                    <p style="font-size:13px; color:#555;">High-ventilation keyhole back design engineered for maximum mobility, cooling, and competitive flare.</p>
                    <hr>
                    <p style="font-size:13px; margin-bottom:4px;"><strong>Silhouette:</strong> Ergonomic Cutout Back</p>
                    <p style="font-size:13px; margin-bottom:0;"><strong>Fabric Tech:</strong> HyperVent Micro-Grid</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            d3_btn1, d3_btn2 = st.columns(2)
            with d3_btn1:
                if st.button("🛒 Buy Style 3 ($135)", key="buy_d3"):
                    st.toast("🛒 Added Racerback Pro Dress to cart!")
            with d3_btn2:
                if st.button("⚡ New Photo", key="regen_d3"):
                    st.session_state.img_seed += 3
                    st.rerun()

        st.markdown("---")
        st.success("✨ **Editorial Quality Active**: Click **'⚡ New Photo'** on any item to re-render fresh model shots in real time.")
