import random
import time
import urllib.parse
import streamlit as st

# ==========================================
# 0. PAGE CONFIG & GLOBAL THEME
# ==========================================
st.set_page_config(
    page_title="Free Tennis Academy & Second-Hand Market",
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
        padding: 14px 20px;
        border-radius: 8px;
        font-weight: bold;
        font-size: 22px;
        text-align: center;
        margin-bottom: 15px;
    }
    .score-badge-fail {
        background-color: #B7094C;
        color: white;
        padding: 14px 20px;
        border-radius: 8px;
        font-weight: bold;
        font-size: 22px;
        text-align: center;
        margin-bottom: 15px;
    }
    .leaderboard-box {
        background-color: #FFFFFF;
        border: 2px solid #FFD700;
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 20px;
        box-shadow: 0 4px 12px rgba(255, 215, 0, 0.15);
    }
    .ball-badge {
        background-color: #CCFF00;
        color: #1A1918;
        font-weight: bold;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 14px;
        border: 1px solid #A2CC00;
    }
    .location-badge {
        background-color: #2D6A4F;
        color: white;
        padding: 3px 10px;
        border-radius: 6px;
        font-weight: bold;
        font-size: 12px;
    }
    .gift-badge {
        background-color: #D90429;
        color: white;
        padding: 3px 10px;
        border-radius: 6px;
        font-weight: bold;
        font-size: 12px;
    }
    </style>
""", unsafe_allow_html=True)

# Helper function for high-quality item photography
def get_marketplace_image(prompt_details: str, seed: int = None) -> str:
    if seed is None:
        seed = random.randint(1000, 99999)
    quality_modifiers = ", realistic second hand marketplace photo, clear clean focus, high quality product photography, 8k"
    full_prompt = prompt_details + quality_modifiers
    encoded_prompt = urllib.parse.quote(full_prompt)
    return f"https://image.pollinations.ai/prompt/{encoded_prompt}?seed={seed}&width=500&height=500&nologo=true"

# Initialize Session States with Pre-populated Data
if "registered_coaches" not in st.session_state:
    st.session_state.registered_coaches = [
        {"Name": "Coach Alex Rivera", "Email": "alex@tennis.com", "Location": "Gangnam-gu, Seoul", "MaxStudents": 5, "Score": 88, "Bio": "USPTR Certified Pro focused on youth development."},
        {"Name": "Coach Marcus Vance", "Email": "marcus@tennis.com", "Location": "Seocho-gu, Seoul", "MaxStudents": 3, "Score": 92, "Bio": "Former ATP player specializing in advanced stroke bio-mechanics."}
    ]

if "registered_students" not in st.session_state:
    st.session_state.registered_students = [
        {"Name": "Sarah Jenkins", "Email": "sarah@example.com", "Phone": "+1 555-0192", "Location": "Mapo-gu, Seoul", "Notes": "Super eager beginner looking to master the forehand!", "Balls": 15, "Photo": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=400"},
        {"Name": "Emily Chen", "Email": "emily@example.com", "Phone": "+1 555-0183", "Location": "Seocho-gu, Seoul", "Notes": "Practicing serve techniques and backhand slice.", "Balls": 8, "Photo": "https://images.unsplash.com/photo-1517841905240-472988babdf9?w=400"}
    ]

if "marketplace_items" not in st.session_state:
    st.session_state.marketplace_items = [
        {
            "title": "Wilson Pro Staff 97 v13 (Near New)",
            "category": "Racquet",
            "price": "140,000 ₩",
            "is_gift": False,
            "condition": "Like New (9.5/10)",
            "location": "Gangnam-gu, Seoul",
            "seller": "Coach Alex Rivera",
            "desc": "Used only 3 times. Strung with Luxilon ALU Power at 52 lbs.",
            "image": "https://images.unsplash.com/photo-1617083934555-ac7d4fed8824?w=500"
        },
        {
            "title": "Babolat Pure Drive 2021 (Gift for Dedicated Student)",
            "category": "Racquet",
            "price": "FREE GIFT 🎁",
            "is_gift": True,
            "target_student": "Sarah Jenkins",
            "condition": "Good (8/10)",
            "location": "Seocho-gu, Seoul",
            "seller": "Coach Marcus Vance",
            "desc": "Donating this racquet to Sarah to help her practice her forehand rallies!",
            "image": "https://images.unsplash.com/photo-1595435934249-5df7ed86e1c0?w=500"
        }
    ]

if "coach_eval_data" not in st.session_state:
    st.session_state.coach_eval_data = None

# ==========================================
# 1. NAVIGATION BAR
# ==========================================
st.sidebar.title("🎾 Academy Portal")
app_mode = st.sidebar.radio(
    "Select Portal Section:",
    [
        "🏆 Register as a Coach (AI Assessment)", 
        "🎾 Register as a Student (Free Lessons)", 
        "📋 Community Directory & Ball Leaderboard",
        "🛍️ Coach Second-Hand & Donation Market"
    ]
)

st.sidebar.markdown("---")

# ==========================================
# SECTION 1: COACH REGISTRATION
# ==========================================
if app_mode == "🏆 Register as a Coach (AI Assessment)":
    st.title("🏆 Coach Certification & AI Motion Breakdown")
    st.write("Upload your footage to analyze your biomechanics and calculate your official Coach Evaluation Score.")
    
    st.markdown("---")
    st.subheader("Step 1: Upload Your Gameplay / Rally Video")
    
    coach_vid = st.file_uploader("Upload video file (.mp4, .mov)", type=["mp4", "mov"], key="coach_vid_input")

    col_v1, col_v2 = st.columns([1, 1])

    with col_v1:
        if coach_vid:
            st.video(coach_vid)

    with col_v2:
        if coach_vid:
            if st.button("📊 Analyze Video & Breakdown Mechanics"):
                with st.spinner("🔍 Running computer vision biomechanics analysis..."):
                    time.sleep(1.2)
                    stroke_tech = random.randint(50, 98)
                    footwork = random.randint(45, 95)
                    consistency = random.randint(50, 96)
                    speed_power = random.randint(48, 94)
                    
                    overall = int((stroke_tech * 0.35) + (footwork * 0.25) + (consistency * 0.25) + (speed_power * 0.15))
                    
                    st.session_state.coach_eval_data = {
                        "overall": overall, "stroke": stroke_tech,
                        "footwork": footwork, "consistency": consistency, "speed": speed_power
                    }

    if st.session_state.coach_eval_data is not None:
        eval_d = st.session_state.coach_eval_data
        overall_score = eval_d["overall"]

        st.markdown("---")
        st.subheader("Step 2: AI Video Analysis Breakdown")

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Stroke Mechanics", f"{eval_d['stroke']}/100")
        m2.metric("Footwork Agility", f"{eval_d['footwork']}/100")
        m3.metric("Precision", f"{eval_d['consistency']}/100")
        m4.metric("Racquet Speed", f"{eval_d['speed']}/100")

        if overall_score >= 60:
            st.markdown(f'<div class="score-badge-pass">✅ OVERALL SCORE: {overall_score} / 100 — SKILL VERIFIED!</div>', unsafe_allow_html=True)
            
            st.markdown("### Step 3: Complete Coach Profile")
            with st.form("coach_form"):
                c1, c2 = st.columns(2)
                with c1:
                    c_name = st.text_input("Full Name *", placeholder="Coach Alex Rivera")
                    c_email = st.text_input("Email *", placeholder="alex.rivera@example.com")
                with c2:
                    c_location = st.text_input("Neighborhood / City *", placeholder="Gangnam-gu, Seoul")
                    c_max = st.number_input("Max Students You Can Teach", min_value=1, max_value=10, value=3)

                c_bio = st.text_area("Coaching Philosophy / Bio")

                if st.form_submit_button("🚀 Submit Verified Coach Profile"):
                    if c_name and c_email and c_location:
                        new_coach = {
                            "Name": c_name, "Email": c_email, "Location": c_location, 
                            "MaxStudents": c_max, "Score": overall_score, "Bio": c_bio
                        }
                        st.session_state.registered_coaches.append(new_coach)
                        st.success("🏆 You are now officially registered as a Coach!")
                        st.balloons()
        else:
            st.markdown(f'<div class="score-badge-fail">❌ OVERALL SCORE: {overall_score} / 100 — DID NOT MEET THRESHOLD</div>', unsafe_allow_html=True)
            st.warning("Score below 60 threshold. Join as a student to improve your skills!")

# ==========================================
# SECTION 2: STUDENT REGISTRATION
# ==========================================
elif app_mode == "🎾 Register as a Student (Free Lessons)":
    st.title("🎾 Register as a Student for Free Tennis Lessons")
    st.write("Join our free academy! Upload your photo and details so coaches can connect with you and support your progress.")

    st.markdown("---")

    with st.form("student_form"):
        s1, s2 = st.columns(2)
        with s1:
            s_name = st.text_input("Full Name *", placeholder="Sarah Jenkins")
            s_email = st.text_input("Email Address *", placeholder="sarah@example.com")
            s_phone = st.text_input("Phone Number *", placeholder="+1 (555) 019-2834")
            s_location = st.text_input("Neighborhood & Preferred Courts *", placeholder="Mapo-gu, Seoul")
            
        with s2:
            s_photo = st.file_uploader("Upload Profile Photo *", type=["jpg", "jpeg", "png"])
            s_notes = st.text_area("Notes for your Coach", placeholder="Goals and schedule preferences...")

        if st.form_submit_button("🎉 Register Profile"):
            if s_name and s_email and s_location and s_photo:
                new_student = {
                    "Name": s_name, "Email": s_email, "Phone": s_phone, 
                    "Location": s_location, "Notes": s_notes, "Photo": s_photo, "Balls": 0
                }
                st.session_state.registered_students.append(new_student)
                st.success("🎉 Profile created! Coaches can now find you, donate tennis balls, or gift you gear!")
                st.balloons()

# ==========================================
# SECTION 3: DIRECTORY & LEADERBOARD
# ==========================================
elif app_mode == "📋 Community Directory & Ball Leaderboard":
    st.title("📋 Community Directory & Ball Popularity Contest")
    st.caption("Coaches can purchase tennis balls and donate them to their favorite students! The student with the most balls wins the Popularity Prize.")

    st.markdown("---")

    # LEADERBOARD HEADER
    st.subheader("👑 Most Popular Student Leaderboard")
    
    if st.session_state.registered_students:
        sorted_students = sorted(st.session_state.registered_students, key=lambda x: x.get("Balls", 0), reverse=True)
        top_student = sorted_students[0]

        st.markdown(f"""
        <div class="leaderboard-box">
            <h3>🥇 Current #1 Popular Student: <strong>{top_student['Name']}</strong> 🎉</h3>
            <p><strong>Total Donated Tennis Balls:</strong> <span class="ball-badge">🎾 {top_student.get('Balls', 0)} Balls</span></p>
            <p style="color:#555; margin-bottom:0;"><em>Prize: Free Pro Racquet & VIP Training Session!</em></p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    col_dir1, col_dir2 = st.columns([1, 1.2])

    with col_dir1:
        st.subheader("🏆 Verified Coaches")
        if st.session_state.registered_coaches:
            for c in st.session_state.registered_coaches:
                st.markdown(f"""
                **{c['Name']}** ⭐ (AI Score: **{c['Score']}/100**)  
                📍 *{c['Location']}* | 📧 `{c['Email']}`  
                👥 Max Capacity: **{c['MaxStudents']} students**  
                ---
                """)

    with col_dir2:
        st.subheader("🎾 Enrolled Students & Ball Donations")
        if st.session_state.registered_students:
            for idx, s in enumerate(st.session_state.registered_students):
                with st.container():
                    sc1, sc2 = st.columns([1, 1.8])
                    with sc1:
                        st.image(s["Photo"], use_container_width=True)
                    with sc2:
                        st.markdown(f"### {s['Name']}")
                        st.markdown(f"🎾 **Tennis Balls Received**: <span class='ball-badge'>{s.get('Balls', 0)} Balls</span>", unsafe_allow_html=True)
                        st.markdown(f"📍 **Location**: {s['Location']}")
                        st.markdown(f"📧 **Email**: `{s['Email']}`")
                        
                        st.markdown("**🎾 Buy & Donate Tennis Balls:**")
                        don_col1, don_col2 = st.columns([1, 1])
                        with don_col1:
                            ball_pack = st.selectbox("Select Pack", ["3 Balls ($5)", "12 Can ($18)", "50 Bucket ($60)"], key=f"pack_{idx}")
                        with don_col2:
                            if st.button(f"🎁 Donate to {s['Name'].split()[0]}", key=f"don_btn_{idx}"):
                                count_map = {"3 Balls ($5)": 3, "12 Can ($18)": 12, "50 Bucket ($60)": 50}
                                added_balls = count_map[ball_pack]
                                s["Balls"] = s.get("Balls", 0) + added_balls
                                st.toast(f"🎉 Successfully donated {added_balls} tennis balls to {s['Name']}!")
                                time.sleep(0.5)
                                st.rerun()

                    st.markdown("---")

# ==========================================
# SECTION 4: 🛍️ COACH-ONLY MARKETPLACE & GIFT DONATIONS
# ==========================================
elif app_mode == "🛍️ Coach Second-Hand & Donation Market":
    st.title("🛍️ Neighborhood Second-Hand & Gear Donation Market")
    st.caption("Only verified coaches can list tennis gear for sale or donate equipment as free gifts to students!")

    st.markdown("---")

    # EXPANDER TO POST A NEW ITEM (COACHES ONLY)
    if st.session_state.registered_coaches:
        coach_names = [c["Name"] for c in st.session_state.registered_coaches]
        
        with st.expander("➕ Coaches Only: Sell or Donate Gear (Create Listing)"):
            with st.form("coach_sell_form"):
                p1, p2 = st.columns(2)
                with p1:
                    selected_coach = st.selectbox("Posting as Coach *", coach_names)
                    item_title = st.text_input("Item Title *", placeholder="e.g. Head Speed MP 2023")
                    item_cat = st.selectbox("Category *", ["Racquet", "Shoes", "Dress/Outfit", "Bags/Accessories"])
                    item_cond = st.selectbox("Condition *", ["Brand New", "Like New (9/10)", "Good (8/10)", "Fair (6/10)"])

                with p2:
                    is_donation = st.checkbox("🎁 Donate as a FREE GIFT to a Student", value=False)
                    item_price = st.text_input("Price (KRW / USD)", placeholder="e.g. 80,000 ₩", disabled=is_donation)
                    
                    student_options = ["Anyone / Any Student"] + [s["Name"] for s in st.session_state.registered_students]
                    target_student = st.selectbox("Gift Destination Student", student_options, disabled=not is_donation)
                    
                    item_photo = st.file_uploader("Upload Photo of Gear", type=["jpg", "png", "jpeg"])
                    item_desc = st.text_area("Item Description", placeholder="Mention strings, condition, or why you are gifting this...")

                if st.form_submit_button("🚀 Publish Listing"):
                    if item_title:
                        img_url = "https://images.unsplash.com/photo-1617083934555-ac7d4fed8824?w=500"
                        if item_photo:
                            img_url = item_photo

                        # Find coach location
                        coach_obj = next((c for c in st.session_state.registered_coaches if c["Name"] == selected_coach), None)
                        loc = coach_obj["Location"] if coach_obj else "Seoul"

                        final_price = "FREE GIFT 🎁" if is_donation else (item_price if item_price else "Contact for Price")

                        new_item = {
                            "title": item_title,
                            "category": item_cat,
                            "price": final_price,
                            "is_gift": is_donation,
                            "target_student": target_student if is_donation else None,
                            "condition": item_cond,
                            "location": loc,
                            "seller": selected_coach,
                            "desc": item_desc,
                            "image": img_url
                        }
                        st.session_state.marketplace_items.insert(0, new_item)
                        st.success(f"🎉 Listing published by {selected_coach}!")
                        st.rerun()
                    else:
                        st.error("Please fill in the Item Title.")
    else:
        st.warning("🔒 Only verified coaches can list items. Please register as a coach first!")

    st.markdown("### 🛍️ Available Gear & Free Student Gifts")

    # CATEGORY FILTER
    cat_filter = st.radio("Filter Category:", ["All Gear", "Racquet", "Shoes", "Dress/Outfit", "Bags/Accessories"], horizontal=True)

    filtered_items = st.session_state.marketplace_items
    if cat_filter != "All Gear":
        filtered_items = [i for i in filtered_items if i["category"] == cat_filter]

    st.markdown("<br>", unsafe_allow_html=True)

    # MARKETPLACE GRID (3 COLUMNS)
    m_cols = st.columns(3)

    for idx, item in enumerate(filtered_items):
        col = m_cols[idx % 3]
        with col:
            with st.container():
                st.image(item["image"], use_container_width=True)
                
                # Badge rendering (Location vs Gift)
                if item.get("is_gift"):
                    st.markdown(f"<span class='gift-badge'>🎁 DONATION GIFT</span> <span class='location-badge'>📍 {item['location']}</span>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<span class='location-badge'>📍 {item['location']}</span>", unsafe_allow_html=True)
                
                st.markdown(f"#### {item['title']}")
                st.markdown(f"💰 **Price**: `{item['price']}`")
                
                if item.get("is_gift") and item.get("target_student"):
                    st.caption(f"🎁 Reserved for: **{item['target_student']}**")
                
                st.caption(f"✨ Condition: **{item['condition']}** | Coach Seller: **{item['seller']}**")
                st.write(item["desc"])

                if item.get("is_gift"):
                    if st.button(f"🎁 Claim Free Gift from {item['seller'].split()[0]}", key=f"gift_{idx}"):
                        st.toast(f"🎉 Gift request sent to {item['seller']}!")
                else:
                    if st.button(f"💬 Chat with {item['seller'].split()[0]}", key=f"chat_{idx}"):
                        st.toast(f"💬 Direct chat opened with {item['seller']}!")
                st.markdown("---")
