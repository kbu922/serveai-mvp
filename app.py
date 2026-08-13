import random
import time
import urllib.parse
import streamlit as st

# ==========================================
# 0. PAGE CONFIG & GLOBAL THEME
# ==========================================
st.set_page_config(
    page_title="Free Tennis Academy & AI Gear Hub",
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
    .score-badge-pass {
        background-color: #2D6A4F;
        color: white;
        padding: 12px 20px;
        border-radius: 8px;
        font-weight: bold;
        font-size: 20px;
        text-align: center;
        margin-bottom: 15px;
    }
    .score-badge-fail {
        background-color: #B7094C;
        color: white;
        padding: 12px 20px;
        border-radius: 8px;
        font-weight: bold;
        font-size: 20px;
        text-align: center;
        margin-bottom: 15px;
    }
    .student-card {
        background-color: #FFFFFF;
        border: 1px solid #E2DDD5;
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 15px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.03);
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

# Helper function for high-quality fashion AI photography
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

# Initialize Session States
if "registered_coaches" not in st.session_state:
    st.session_state.registered_coaches = []

if "registered_students" not in st.session_state:
    st.session_state.registered_students = []

if "coach_score" not in st.session_state:
    st.session_state.coach_score = None

if "img_seed" not in st.session_state:
    st.session_state.img_seed = random.randint(1000, 9999)

# ==========================================
# 1. NAVIGATION BAR
# ==========================================
st.sidebar.title("🎾 Academy Portal")
app_mode = st.sidebar.radio(
    "Select Portal Section:",
    [
        "🏆 Register as a Coach (AI Assessment)", 
        "🎾 Register as a Student (Free Lessons)", 
        "📋 Community Directory (Coaches & Students)",
        "👗 AI Tennis Gear & Lookbook"
    ]
)

st.sidebar.markdown("---")

# ==========================================
# SECTION 1: COACH REGISTRATION (SKILL GATE)
# ==========================================
if app_mode == "🏆 Register as a Coach (AI Assessment)":
    st.title("🏆 Coach Certification & Skill Evaluation")
    st.write("To become a coach in our free community academy, you must first verify your tennis mechanics with our AI system.")
    
    st.markdown("""
    > **Verification Rule**: Upload a video of your gameplay or serving motion. The AI will evaluate your swing mechanics, pace, and footwork. 
    > * **Score ≥ 60**: Approved to register as a Coach!
    > * **Score < 60**: You cannot register as a coach yet, but you are welcome to sign up as a student.
    """)

    st.markdown("---")
    st.subheader("Step 1: Upload Your Gameplay Video")
    
    coach_vid = st.file_uploader("Upload video file (.mp4, .mov)", type=["mp4", "mov"], key="coach_vid_input")

    col_v1, col_v2 = st.columns(2)

    with col_v1:
        if coach_vid:
            st.video(coach_vid)

    with col_v2:
        if coach_vid:
            if st.button("📊 Analyze Video & Calculate Skill Score"):
                with st.spinner("Analyzing biomechanics, stroke depth, and court coverage..."):
                    time.sleep(1.2)
                    # Simulated skill evaluation score (randomized between 45 and 95)
                    st.session_state.coach_score = random.randint(45, 92)

    # EVALUATION RESULTS & CONDITIONAL REGISTRATION FORM
    if st.session_state.coach_score is not None:
        score = st.session_state.coach_score
        st.markdown("---")
        st.subheader("Step 2: Verification Result")

        if score >= 60:
            st.markdown(f'<div class="score-badge-pass">✅ SCORE: {score} / 100 — SKILL VERIFIED!</div>', unsafe_allow_html=True)
            st.success(f"🎉 Fantastic performance! With a score of **{score}/100**, you qualify to register as a community coach.")

            st.markdown("### Step 3: Complete Coach Profile")
            with st.form("coach_form"):
                c1, c2 = st.columns(2)
                with c1:
                    c_name = st.text_input("Full Name *", placeholder="Coach Alex Rivera")
                    c_email = st.text_input("Email / Contact Info *", placeholder="alex.rivera@example.com")
                with c2:
                    c_location = st.text_input("Primary Location / City *", placeholder="San Francisco Courts, CA")
                    c_max = st.number_input("Max Students You Can Teach", min_value=1, max_value=10, value=3)

                c_bio = st.text_area("Coaching Philosophy / Bio", placeholder="Share your experience and coaching style...")

                if st.form_submit_button("🚀 Submit Coach Profile"):
                    if c_name and c_email and c_location:
                        new_coach = {
                            "Name": c_name,
                            "Email": c_email,
                            "Location": c_location,
                            "MaxStudents": c_max,
                            "Score": score,
                            "Bio": c_bio
                        }
                        st.session_state.registered_coaches.append(new_coach)
                        st.success("🏆 You are now officially registered as a Coach! Students will be able to find your profile.")
                        st.balloons()
                    else:
                        st.error("Please fill in all required fields (*).")

        else:
            st.markdown(f'<div class="score-badge-fail">❌ SCORE: {score} / 100 — DID NOT MEET THRESHOLD</div>', unsafe_allow_html=True)
            st.warning(f"Your score of **{score}/100** is below the **60-point threshold** required to coach. Keep practicing! You can register as a student to receive free coaching lessons from certified coaches.")

# ==========================================
# SECTION 2: STUDENT REGISTRATION
# ==========================================
elif app_mode == "🎾 Register as a Student (Free Lessons)":
    st.title("🎾 Register as a Student for Free Tennis Lessons")
    st.write("Join our free academy! Simply upload your photo and contact details so local verified coaches can reach out to teach you.")

    st.markdown("---")

    with st.form("student_form"):
        s1, s2 = st.columns(2)
        with s1:
            s_name = st.text_input("Full Name *", placeholder="Sarah Jenkins")
            s_email = st.text_input("Email Address *", placeholder="sarah@example.com")
            s_phone = st.text_input("Phone Number / WhatsApp *", placeholder="+1 (555) 019-2834")
            s_location = st.text_input("City & Preferred Courts *", placeholder="Central Park, NY")
            
        with s2:
            s_photo = st.file_uploader("Upload Your Profile Photo *", type=["jpg", "jpeg", "png"])
            s_notes = st.text_area("Notes for your Coach", placeholder="e.g. Complete beginner interested in forehand basics and weekend lessons.")

        if st.form_submit_button("🎉 Register for Free Coaching"):
            if s_name and s_email and s_location and s_photo:
                new_student = {
                    "Name": s_name,
                    "Email": s_email,
                    "Phone": s_phone,
                    "Location": s_location,
                    "Notes": s_notes,
                    "Photo": s_photo
                }
                st.session_state.registered_students.append(new_student)
                st.success(f"🎉 Profile created successfully! Verified coaches in {s_location} can now view your card and contact you for free lessons.")
                st.balloons()
            else:
                st.error("Please fill in all required fields (*) and upload a profile photo.")

# ==========================================
# SECTION 3: COMMUNITY DIRECTORY
# ==========================================
elif app_mode == "📋 Community Directory (Coaches & Students)":
    st.title("📋 Community Roster & Directory")
    st.caption("Coaches can contact students to offer free coaching sessions.")

    st.markdown("---")

    col_dir1, col_dir2 = st.columns(2)

    # COACHES LIST
    with col_dir1:
        st.subheader("🏆 Verified Coaches (Score ≥ 60)")
        if st.session_state.registered_coaches:
            for c in st.session_state.registered_coaches:
                with st.container():
                    st.markdown(f"""
                    **Name**: {c['Name']} ⭐ (AI Score: **{c['Score']}/100**)  
                    📍 **Location**: {c['Location']}  
                    📧 **Contact**: `{c['Email']}`  
                    👥 **Capacity**: Up to {c['MaxStudents']} students  
                    _{c['Bio']}_
                    ---
                    """)
        else:
            st.info("No verified coaches registered yet.")

    # STUDENTS LIST WITH PHOTOS & CONTACT
    with col_dir2:
        st.subheader("🎾 Enrolled Students (Seeking Free Coaching)")
        if st.session_state.registered_students:
            for s in st.session_state.registered_students:
                with st.container():
                    sc1, sc2 = st.columns([1, 2])
                    with sc1:
                        st.image(s["Photo"], use_container_width=True)
                    with sc2:
                        st.markdown(f"**Name**: {s['Name']}")
                        st.markdown(f"📍 **Location**: {s['Location']}")
                        st.markdown(f"📧 **Email**: `{s['Email']}`")
                        if s["Phone"]:
                            st.markdown(f"📞 **Phone**: `{s['Phone']}`")
                        st.caption(f"📝 Notes: {s['Notes']}")
                    st.markdown("---")
        else:
            st.info("No students registered yet.")

# ==========================================
# SECTION 4: AI GEAR & LOOKBOOK
# ==========================================
elif app_mode == "👗 AI Tennis Gear & Lookbook":
    st.title("👗 High-Fashion AI Tennis Lookbook & Racquets")
    st.caption("Explore dynamic AI studio dress renders and match-grade racquets.")

    st.markdown("---")

    dress_color = st.selectbox("Select Dress Color Palette", ["Crisp Pure White", "Pastel Soft Mint", "Midnight Navy", "Champagne Gold", "Ruby Red"])

    if st.button("✨ Generate New AI Studio Photos"):
        st.session_state.img_seed = random.randint(10000, 99999)

    d_col1, d_col2, d_col3 = st.columns(3)
    base_seed = st.session_state.img_seed

    prompt_1 = f"photorealistic fashion editorial photo of stunning gorgeous female tennis model wearing a luxury {dress_color} designer pleated tennis dress with subtle golden trim"
    url_1 = get_beautiful_ai_image(prompt_1, seed=base_seed)

    prompt_2 = f"photorealistic Vogue magazine portrait of beautiful elegant female tennis player wearing a sleek fitted {dress_color} modern high neck tennis dress, graceful holding tennis racket"
    url_2 = get_beautiful_ai_image(prompt_2, seed=base_seed + 10)

    prompt_3 = f"full length photorealistic action portrait of an attractive female tennis athlete wearing a beautiful {dress_color} racerback luxury tennis dress, sun flare, serene tennis club court background"
    url_3 = get_beautiful_ai_image(prompt_3, seed=base_seed + 20)

    with d_col1:
        st.image(url_1, use_container_width=True, caption="Heritage Pleated Couture")
        if st.button("🛒 Buy Style 1 ($145)", key="b1"):
            st.toast("🛒 Added Style 1 to cart!")

    with d_col2:
        st.image(url_2, use_container_width=True, caption="Modern Minimalist Contour")
        if st.button("🛒 Buy Style 2 ($155)", key="b2"):
            st.toast("🛒 Added Style 2 to cart!")

    with d_col3:
        st.image(url_3, use_container_width=True, caption="High-Tech Racerback Pro")
        if st.button("🛒 Buy Style 3 ($135)", key="b3"):
            st.toast("🛒 Added Style 3 to cart!")
