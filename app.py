import random
import time
import urllib.parse
import streamlit as st

# ==========================================
# 0. PAGE CONFIG & GLOBAL STYLING
# ==========================================
st.set_page_config(
    page_title="Tennis AI Hub & Academy",
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
    .score-badge-pass {
        background-color: #2D6A4F;
        color: white;
        padding: 10px 18px;
        border-radius: 8px;
        font-weight: bold;
        font-size: 18px;
        display: inline-block;
    }
    .score-badge-fail {
        background-color: #B7094C;
        color: white;
        padding: 10px 18px;
        border-radius: 8px;
        font-weight: bold;
        font-size: 18px;
        display: inline-block;
    }
    </style>
""", unsafe_allow_html=True)

# Helper function with HIGH-ELEGANCE / BEAUTIFUL MODEL photo parameters
def get_beautiful_ai_image(prompt_details: str, seed: int = None) -> str:
    if seed is None:
        seed = random.randint(1000, 99999)
    
    quality_modifiers = (
        ", breathtakingly beautiful gorgeous athletic female model, perfect face features, "
        "fashion editorial photography, shot on 85mm lens, f1.4 bokeh background, golden hour natural light, "
        "high fashion magazine cover quality, elegant pose on luxury tennis court, ultra clear focus, 8k resolution"
    )
    full_prompt = prompt_details + quality_modifiers
    encoded_prompt = urllib.parse.quote(full_prompt)
    return f"https://image.pollinations.ai/prompt/{encoded_prompt}?seed={seed}&width=600&height=800&nologo=true"

# Initialize Session State
if "img_seed" not in st.session_state:
    st.session_state.img_seed = random.randint(1000, 9999)

if "registered_coaches" not in st.session_state:
    st.session_state.registered_coaches = []

if "registered_students" not in st.session_state:
    st.session_state.registered_students = []

if "coach_score" not in st.session_state:
    st.session_state.coach_score = None

# ==========================================
# 1. NAVIGATION SUBPAGE SELECTOR
# ==========================================
st.sidebar.title("📍 Navigation")
page_selection = st.sidebar.radio(
    "Go to Subpage:",
    ["🎾 Gear & Lookbook AI", "🎓 Free Tennis Academy Registration"]
)

st.sidebar.markdown("---")

# ==========================================
# SUBPAGE 1: GEAR & LOOKBOOK AI
# ==========================================
if page_selection == "🎾 Gear & Lookbook AI":
    st.title("🎾 AI Tennis Gear & High-Fashion Lookbook Generator")
    st.caption("Upload your performance video for swing analytics, top-selling racquet matching, and luxury studio-grade AI apparel rendering.")

    st.markdown("---")

    # SIDEBAR CONFIGURATION FOR GEAR
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

    # VIDEO UPLOAD & ANALYZER
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

    # ANALYSIS & RECOMMENDATION ENGINE
    if uploaded_video or analyze_btn:
        with st.spinner("Rendering high-fashion AI photography and running motion diagnostics..."):
            time.sleep(0.8)
            
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

            prompt_1 = f"photorealistic fashion editorial photo of stunning gorgeous female tennis model wearing a luxury {dress_color} designer pleated tennis dress with subtle golden trim"
            url_1 = get_beautiful_ai_image(prompt_1, seed=base_seed)

            prompt_2 = f"photorealistic Vogue magazine portrait of beautiful elegant female tennis player wearing a sleek fitted {dress_color} modern high neck tennis dress, graceful holding tennis racket"
            url_2 = get_beautiful_ai_image(prompt_2, seed=base_seed + 15)

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

# ==========================================
# SUBPAGE 2: FREE TENNIS ACADEMY REGISTRATION
# ==========================================
elif page_selection == "🎓 Free Tennis Academy Registration":
    st.title("🎓 Free Community Tennis Academy")
    st.caption("Connect with verified tennis coaches or sign up as a student to learn tennis completely free of charge.")

    st.markdown("---")

    reg_tab1, reg_tab2, tab3_roster = st.tabs([
        "🎾 Register as a Free Student", 
        "🏆 Register as a Coach (AI Skill Check)", 
        "📋 Active Community Roster"
    ])

    # ------------------------------------
    # TAB 1: STUDENT REGISTRATION FORM
    # ------------------------------------
    with reg_tab1:
        st.subheader("🎾 Join as a Student (100% Free Lessons)")
        st.write("Fill out your details to match with local volunteer coaches and receive free coaching sessions.")

        with st.form("student_reg_form"):
            s_col1, s_col2 = st.columns(2)
            with s_col1:
                student_name = st.text_input("Full Name *", placeholder="e.g. Sarah Jenkins")
                student_email = st.text_input("Email Address *", placeholder="sarah@example.com")
                student_location = st.text_input("City / Preferred Court Location *", placeholder="e.g. Central Park Tennis Center, NY")
            with s_col2:
                student_level = st.selectbox("Current Tennis Skill Level", [
                    "Complete Beginner (NTRP 1.0 - 2.0)", 
                    "Advanced Beginner (NTRP 2.5)", 
                    "Intermediate (NTRP 3.0 - 3.5)"
                ])
                student_goals = st.multiselect("Learning Goals", [
                    "Forehand & Backhand Fundamentals", 
                    "Serve Technique & Motion", 
                    "Match Play & Strategy", 
                    "Fitness & Cardio Tennis"
                ], default=["Forehand & Backhand Fundamentals"])
                student_availability = st.selectbox("Preferred Training Days", [
                    "Weekend Mornings", "Weekday Evenings", "Flexible Schedule"
                ])

            submit_student = st.form_submit_button("🎉 Submit Free Student Application")

            if submit_student:
                if student_name and student_email and student_location:
                    new_student = {
                        "Name": student_name,
                        "Email": student_email,
                        "Location": student_location,
                        "Level": student_level,
                        "Availability": student_availability,
                        "Role": "Student"
                    }
                    st.session_state.registered_students.append(new_student)
                    st.success(f"🎉 Welcome aboard, {student_name}! You have successfully registered for free tennis lessons. A coach in {student_location} will be in touch soon.")
                    st.balloons()
                else:
                    st.error("⚠️ Please complete all required fields (*).")

    # ------------------------------------
    # TAB 2: COACH REGISTRATION WITH AI SCORE GATE
    # ------------------------------------
    with reg_tab2:
        st.subheader("🏆 Coach Verification & AI Skill Evaluation")
        st.info("📌 **Coach Threshold**: To maintain high teaching standards, coaches must upload a video to be analyzed. You need an **AI Performance Score of 60 or higher** to register as a coach.")

        st.markdown("### Step 1: Upload Footage for Skill Analysis")
        coach_video = st.file_uploader("Upload your tennis rally or serve video (.mp4, .mov)", type=["mp4", "mov"], key="coach_vid_up")

        col_v1, col_v2 = st.columns([1, 1])
        with col_v1:
            if coach_video:
                st.video(coach_video)

        with col_v2:
            if coach_video:
                if st.button("📊 Analyze Video & Calculate Coach Skill Score"):
                    with st.spinner("Analyzing biomechanics, stroke mechanics, and consistency..."):
                        time.sleep(1.2)
                        # Simulating realistic evaluation score (range 65 - 95 for demo)
                        score = random.randint(62, 92)
                        st.session_state.coach_score = score

        # Display Evaluation Score Results & Conditional Form
        if st.session_state.coach_score is not None:
            score = st.session_state.coach_score
            st.markdown("---")
            st.markdown("### Step 2: Verification Result")

            if score >= 60:
                st.markdown(f"""
                <div class="score-badge-pass">
                    ✅ PASSED: AI Performance Score = {score} / 100
                </div>
                """, unsafe_allow_html=True)
                st.success(f"Congratulations! Your tennis mechanics score of **{score}/100** qualifies you to register as an official community coach.")

                st.markdown("---")
                st.markdown("### Step 3: Complete Coach Registration")
                with st.form("coach_reg_form"):
                    c_col1, c_col2 = st.columns(2)
                    with c_col1:
                        coach_name = st.text_input("Coach Full Name *", placeholder="e.g. Coach Alex Rivera")
                        coach_email = st.text_input("Email Address *", placeholder="alex.rivera@example.com")
                        coach_location = st.text_input("Primary Court / City *", placeholder="e.g. San Francisco Public Courts, CA")
                    with c_col2:
                        coach_exp = st.selectbox("Coaching Experience", [
                            "Certified Tennis Pro (USPTR / USPTA)", 
                            "Former Collegiate Player", 
                            "Experienced Club Player (4.0+ NTRP)"
                        ])
                        coach_max_students = st.number_input("Max Free Students You Can Accept", min_value=1, max_value=20, value=3)
                        coach_bio = st.text_area("Brief Coaching Philosophy / Bio", placeholder="Share your enthusiasm for teaching tennis...")

                    submit_coach = st.form_submit_button("🚀 Finalize Coach Registration")

                    if submit_coach:
                        if coach_name and coach_email and coach_location:
                            new_coach = {
                                "Name": coach_name,
                                "Email": coach_email,
                                "Location": coach_location,
                                "Experience": coach_exp,
                                "Capacity": coach_max_students,
                                "Score": score,
                                "Role": "Coach"
                            }
                            st.session_state.registered_coaches.append(new_coach)
                            st.success(f"🏆 Thank you, {coach_name}! Your profile as a verified volunteer coach is active.")
                            st.balloons()
                        else:
                            st.error("⚠️ Please complete all required fields (*).")
            else:
                st.markdown(f"""
                <div class="score-badge-fail">
                    ❌ SCORE: {score} / 100 (Below 60 Passing Threshold)
                </div>
                """, unsafe_allow_html=True)
                st.warning("Your calculated skill score is below the 60-point threshold required to teach. We invite you to join our academy as a student to hone your skills for free!")

    # ------------------------------------
    # TAB 3: COMMUNITY ROSTER DISPLAY
    # ------------------------------------
    with tab3_roster:
        st.subheader("📋 Active Community Members")
        st.caption("Browse registered verified volunteer coaches and students seeking lessons.")

        col_c_list, col_s_list = st.columns(2)

        with col_c_list:
            st.markdown("#### 🏆 Verified Volunteer Coaches")
            if st.session_state.registered_coaches:
                for idx, c in enumerate(st.session_state.registered_coaches, 1):
                    st.markdown(f"""
                    **{idx}. {c['Name']}** ⭐ (AI Score: **{c.get('Score', 85)}/100**)  
                    🏅 *{c['Experience']}* | 📍 *{c['Location']}*  
                    👥 Max Capacity: **{c['Capacity']} Students**  
                    ---
                    """)
            else:
                st.info("No verified coaches registered yet. Upload your video above to qualify!")

        with col_s_list:
            st.markdown("#### 🎾 Enrolled Students")
            if st.session_state.registered_students:
                for idx, s in enumerate(st.session_state.registered_students, 1):
                    st.markdown(f"""
                    **{idx}. {s['Name']}** ({s['Level']})  
                    📍 *{s['Location']}* | ⏰ Availability: **{s['Availability']}**  
                    ---
                    """)
            else:
                st.info("No students enrolled yet. Sign up today for free coaching!")
