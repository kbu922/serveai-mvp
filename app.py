import streamlit as st
import pandas as pd
import datetime
import time

# ==========================================
# 1. PAGE CONFIG & LUXURY SAND THEME
# ==========================================
st.set_page_config(
    page_title="Global Tennis Platform & AI Suite",
    page_icon="🎾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Luxury Sand Theme & Complete Visual Layout
st.markdown("""
    <style>
    /* Main Background & Base Styling */
    .stApp {
        background-color: #F5F2EB;
        color: #211F1D;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Headers & Typography */
    h1, h2, h3, h4, h5 {
        color: #211F1D !important;
        font-weight: 600;
        letter-spacing: -0.02em;
    }
    
    /* Cards & Containers */
    .stCard, div[data-testid="stExpander"], div[data-testid="stForm"] {
        background-color: #FAF8F5;
        border: 1px solid #E5E0D8;
        border-radius: 12px;
        padding: 24px;
        box-shadow: 0 4px 12px rgba(33, 31, 29, 0.03);
    }
    
    /* Buttons */
    .stButton > button, div[data-testid="stForm"] button {
        background-color: #211F1D !important;
        color: #FAF8F5 !important;
        border-radius: 8px !important;
        border: none !important;
        font-weight: 600 !important;
        padding: 12px 24px !important;
        transition: all 0.2s ease;
        width: 100%;
    }
    .stButton > button:hover {
        background-color: #383430 !important;
        box-shadow: 0 4px 8px rgba(0,0,0,0.12);
    }
    
    /* Metrics & Badges */
    div[data-testid="stMetricValue"] {
        color: #211F1D !important;
        font-weight: 700;
    }
    
    /* Input Fields */
    .stTextInput>div>div>input, .stSelectbox>div>div>div, .stTextArea>div>div>textarea, .stNumberInput>div>div>input {
        background-color: #FFFFFF !important;
        border: 1px solid #D6D0C4 !important;
        border-radius: 8px !important;
        color: #211F1D !important;
    }
    
    /* Tabs Customization */
    button[data-baseweb="tab"] {
        font-weight: 600 !important;
        color: #5C544D !important;
    }
    button[aria-selected="true"] {
        color: #211F1D !important;
        border-bottom-color: #211F1D !important;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. STATE INITIALIZATION (100% PRESERVED)
# ==========================================
if "user" not in st.session_state:
    st.session_state["user"] = "Guest Athlete"
if "language" not in st.session_state:
    st.session_state["language"] = "English"
if "vip_pass" not in st.session_state:
    st.session_state["vip_pass"] = False

# Players Database
if "players_db" not in st.session_state:
    st.session_state["players_db"] = [
        {"Name": "Marcus Vance", "NTRP": 4.5, "City": "Seoul", "Style": "Aggressive Baseline", "Contact": "m.vance@tennis.org"},
        {"Name": "Elena Rostova", "NTRP": 5.0, "City": "Busan", "Style": "Serve & Volley", "Contact": "elena.r@tennis.org"},
        {"Name": "Jin-woo Park", "NTRP": 4.0, "City": "Seoul", "Style": "Counter-Puncher", "Contact": "jw.park@tennis.kr"},
        {"Name": "Sarah Jenkins", "NTRP": 3.5, "City": "Incheon", "Style": "All-Court", "Contact": "s.jenkins@tennis.org"}
    ]

# Coaches Database
if "coaches_db" not in st.session_state:
    st.session_state["coaches_db"] = [
        {"Coach": "Coach Rob", "Level": "USPTR Certified Master", "City": "Seoul", "Hourly": "$80/hr", "Specialty": "Serve Biomechanics"},
        {"Coach": "Coach Sarah", "Level": "Ex-WTA Tour Player", "City": "Incheon", "Hourly": "$120/hr", "Specialty": "Match Strategy"},
        {"Coach": "Coach Min-ho", "Level": "KTA High Performance", "City": "Busan", "Hourly": "$95/hr", "Specialty": "Junior Development"}
    ]

# Group Voting States
if "tournament_group_votes" not in st.session_state:
    st.session_state["tournament_group_votes"] = [
        {"Name": "Chris P.", "Tournament": "Seoul Open Masters", "Status": "Discount Unlocked ($85)"},
        {"Name": "Min-ji K.", "Tournament": "Seoul Open Masters", "Status": "Discount Unlocked ($85)"},
        {"Name": "Kenji S.", "Tournament": "Seoul Open Masters", "Status": "Discount Unlocked ($85)"}
    ]

if "academy_group_votes" not in st.session_state:
    st.session_state["academy_group_votes"] = [
        {"name": "Alex M.", "program": "1-Week Intensive Boot Camp", "discount_tier": "15% Off"},
        {"name": "Sarah K.", "program": "1-Week Intensive Boot Camp", "discount_tier": "15% Off"},
        {"name": "David L.", "program": "1-Month Pro Residency", "discount_tier": "20% Off"}
    ]

# Support & Order History
if "inquiries" not in st.session_state:
    st.session_state["inquiries"] = [
        {"Ticket ID": "TK-1001", "Subject": "Racket Stringing Order", "Status": "Resolved", "Date": "2026-07-15"}
    ]

if "chat_orders" not in st.session_state:
    st.session_state["chat_orders"] = [
        {"Order ID": "ORD-9921", "Item": "VIP Annual Pass", "Amount": "$4.99", "Status": "Paid"}
    ]

# ==========================================
# 3. TOP NAVIGATION & HEADER
# ==========================================
col_h1, col_h2, col_h3 = st.columns([4, 2, 2])

with col_h1:
    st.markdown("### 🎾 Global Tennis Platform & AI Suite")
    st.caption("Live Stats: **12,400+ Serves Analyzed** | 4,200+ Active Members Globally")

with col_h2:
    lang = st.selectbox("🌐 Language / 언어", ["English", "한국어"], index=0 if st.session_state["language"] == "English" else 1)
    st.session_state["language"] = lang

with col_h3:
    status_label = "⭐ VIP Member" if st.session_state["vip_pass"] else "👤 Guest / Free"
    st.markdown(f"**Status:** `{status_label}`")
    if not st.session_state["vip_pass"]:
        if st.button("Upgrade VIP ($4.99/mo)"):
            st.session_state["vip_pass"] = True
            st.session_state["chat_orders"].append({
                "Order ID": f"ORD-{len(st.session_state['chat_orders'])+9922}",
                "Item": "VIP Pass Subscription",
                "Amount": "$4.99",
                "Status": "Paid"
            })
            st.success("VIP Unlocked! Access to Coach Direct Messaging and Priority Analysis Enabled.")
            st.rerun()

st.markdown("---")

# ==========================================
# 4. SIDEBAR NAVIGATION
# ==========================================
st.sidebar.image("https://images.unsplash.com/photo-1595435934249-5df7ed86e1c0?w=400&q=80", caption="Global Tennis Hub")
menu = st.sidebar.radio(
    "Select Module:",
    [
        "1. AI Serve Velocity & Motion Analysis",
        "2. AI Racket & String Calculator",
        "3. Tournaments & Lodging (Group Buy)",
        "4. Residency & Academy Programs",
        "5. Matchmaking & Coach Directory",
        "6. Support & Ticket Receipts",
        "7. Admin Control Panel"
    ]
)

# ==========================================
# 5. MODULE FUNCTIONS
# ==========================================

# --- MODULE 1: AI SERVE VELOCITY ---
def render_module_1():
    st.subheader("⚡ AI Serve Velocity & Biomechanics Analyzer")
    st.write("Upload your serve footage (MP4/MOV) to analyze motion frames, kinetic transfer, shoulder angle, and peak speed.")

    col1, col2 = st.columns([3, 2])
    with col1:
        video_file = st.file_uploader("Upload Serve Video (MP4/MOV)", type=["mp4", "mov"])
        angle = st.selectbox("Camera Angle", ["Behind Court (Baseline)", "Side View (Court Level)", "45-Degree Angle"])
        fps = st.slider("Video Capture FPS", 30, 240, 60, help="Higher FPS increases calculation accuracy at impact frame.")

        if video_file and st.button("Run AI Speed & Motion Analysis"):
            with st.spinner("Processing video frames and calculating ball trajectory..."):
                time.sleep(2.5)
                st.success("Analysis Complete!")
                
                m1, m2, m3 = st.columns(3)
                m1.metric("Peak Serve Speed", "118 mph", delta="+4 mph from last average")
                m2.metric("Spin Rate", "2,840 RPM", delta="Topspin / Kick")
                m3.metric("Impact Height", "2.85 meters", delta="Optimal Apex")
                
                st.markdown("#### 📐 Biomechanics Analysis Breakdown")
                st.write("* **Trophy Position**: Shoulder tilt angle measured at **28°** (Optimal range: 25°-32°).")
                st.write("* **Leg Drive & Kneebend**: Knee flexion reached **115°** prior to vertical launch.")
                st.write("* **Pronation Speed**: Wrist angular acceleration calculated at **1,420°/sec**.")
                st.write("* **Recommended Adjustment**: Toss placement is 4 inches too far right for maximum kick trajectory.")

    with col2:
        st.info("""
        💡 **Recording Tips for Best AI Precision**:
        1. Place camera at waist-height 5 feet behind the baseline.
        2. Ensure high shutter speed to eliminate ball motion blur.
        3. Keep both the toss release point and impact frame in clear view.
        """)

# --- MODULE 2: AI RACKET CALCULATOR ---
def render_module_2():
    st.subheader("🎯 AI Racket & String Tension Recommendation Engine")
    st.write("Input your physical attributes and playstyle parameters to compute your ideal racket setup and string tension.")

    c1, c2 = st.columns(2)
    with c1:
        ntrp = st.slider("Your NTRP Skill Rating", 1.5, 7.0, 3.5, 0.5)
        serve_speed = st.number_input("Average Serve Speed (mph)", 40, 140, 85)
        playstyle = st.selectbox("Primary Playstyle", ["Baseline Aggressor", "All-Court Counterpuncher", "Touch & Net Specialist", "Power Serve & Volley"])
        swing_speed = st.select_slider("Swing Speed", options=["Slow & Compact", "Medium / Moderate", "Fast & Full Loop"])

    with c2:
        elbow_issue = st.checkbox("Suffer from Tennis Elbow / Wrist Strain?")
        spin_pref = st.select_slider("Performance Priority", options=["Max Control & Precision", "Balanced All-Around", "Max Spin & Power"])
        racket_weight = st.selectbox("Preferred Racket Unstrung Weight", ["Light (< 295g)", "Medium (300g - 305g)", "Tour Weight (310g+)"])

    if st.button("Calculate Optimal Setup"):
        st.markdown("---")
        st.markdown("### 🛠️ Recommended Equipment Specification")
        
        res_col1, res_col2, res_col3, res_col4 = st.columns(4)
        with res_col1:
            st.metric("Head Size", "98 - 100 sq in")
        with res_col2:
            tension = "46 - 50 lbs" if elbow_issue else ("52 - 56 lbs" if spin_pref == "Max Control & Precision" else "50 - 53 lbs")
            st.metric("String Tension", tension)
        with res_col3:
            string_type = "Soft Multifilament / Gut" if elbow_issue else "Co-Poly 1.25mm / Hybrid"
            st.metric("String Material", string_type)
        with res_col4:
            balance = "Head Light (315mm)" if "Tour" in racket_weight else "Even Balance (325mm)"
            st.metric("Frame Balance", balance)

        st.success("Setup calculation stored to profile! Take these specs to your local stringer.")

# --- MODULE 3: TOURNAMENTS & LODGING ---
def render_module_3():
    st.subheader("🏆 Tournaments, Hotel Lodging & Member Group Buying")
    
    tab1, tab2 = st.tabs(["👥 Group Buying & Voting Hub", "👤 Individual Registration"])
    
    with tab1:
        st.markdown("#### Member Group Buying & Discount Campaign")
        st.write("Join active member group bookings to unlock bulk rates ($85 discount per athlete) for official tournament hotel stays.")
        
        votes = len(st.session_state["tournament_group_votes"])
        target = 5
        st.progress(min(votes / target, 1.0))
        
        if votes >= target:
            st.success(f"🎉 **Group Discount Unlocked!** ({votes}/{target} Athletes Joined)")
        else:
            st.caption(f"Current Commitment: **{votes}/{target} Athletes Joined** — Need {target - votes} more to unlock discount.")

        st.markdown("##### Current Group Roster")
        st.table(pd.DataFrame(st.session_state["tournament_group_votes"]))

        with st.form("join_tournament_group_form"):
            user_name = st.text_input("Athlete Name *", value=st.session_state["user"])
            tourn_choice = st.selectbox("Tournament", ["Seoul Open Masters", "Busan Clay Championship", "Incheon National Cup"])
            submit_group = st.form_submit_button("Commit & Join Group Campaign")
            
            if submit_group:
                if user_name:
                    st.session_state["tournament_group_votes"].append({
                        "Name": user_name,
                        "Tournament": tourn_choice,
                        "Status": "Discount Unlocked ($85)" if votes + 1 >= target else "Pending Threshold"
                    })
                    st.success("Successfully joined tournament group campaign!")
                    st.rerun()

    with tab2:
        st.markdown("#### Individual Registration & Hotel Booking")
        with st.form("indiv_tourn_form"):
            c1, c2 = st.columns(2)
            with c1:
                p_name = st.text_input("Player Full Name *")
                p_passport = st.text_input("Passport / Gov ID *")
                p_event = st.selectbox("Event Category", ["Men's Open Singles", "Women's Open Singles", "Mixed Doubles (NTRP 4.0)"])
            with c2:
                check_in = st.date_input("Hotel Check-in Date", datetime.date(2026, 9, 10))
                check_out = st.date_input("Hotel Check-out Date", datetime.date(2026, 9, 15))
                card = st.text_input("Payment Card Number *", type="password")

            if st.form_submit_button("Complete Individual Booking"):
                if p_name and p_passport and card:
                    st.success("Individual tournament entry & hotel stay reserved successfully!")
                else:
                    st.error("Please fill in all mandatory fields.")

# --- MODULE 4: ACADEMY & RESIDENCY (UPDATED WITH GROUP HUB + GALLERY) ---
def render_module_4():
    st.markdown("""
        <div style="background-color:#FAF8F5; padding:20px; border-radius:12px; border:1px solid #E5E0D8; margin-bottom:20px;">
            <h2 style="color:#211F1D; margin-top:0;">🏛️ Global Tennis Academy & Residency Programs</h2>
            <p style="color:#5C544D; font-size:14px;">
                Accelerate your game with world-class ATP/WTA certified coaching, high-performance training grounds, and luxury athlete residences.
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Subpage Switcher
    subpage = st.radio(
        "Select Enrollment Pathway:",
        ["👤 Individual Enrollment", "👥 Group Buying & Voting Hub"],
        horizontal=True,
        key="academy_subpage_nav"
    )

    st.markdown("---")

    # SUBPAGE 1: INDIVIDUAL ENROLLMENT
    if subpage == "👤 Individual Enrollment":
        st.subheader("Individual Program Booking")
        
        program = st.selectbox(
            "Select Training Program:",
            ["1-Week Intensive Boot Camp ($890)", "1-Month Pro Residency ($2,950)"]
        )

        with st.form("individual_residency_form"):
            col1, col2 = st.columns(2)
            with col1:
                full_name = st.text_input("Full Name *")
                passport = st.text_input("Passport / ID Number *")
                phone = st.text_input("Contact Phone / WhatsApp *")
                start_date = st.date_input("Preferred Start Date")
            with col2:
                ntrp = st.slider("Current NTRP Rating", 1.0, 7.0, 3.5, 0.5)
                health_notes = st.text_area("Medical / Dietary Requirements", placeholder="e.g., Allergies, physical therapy needs...")
                card_num = st.text_input("Credit Card Number *", type="password")

            submitted = st.form_submit_button("Complete Individual Registration", use_container_width=True)
            if submitted:
                if full_name and passport and card_num:
                    st.success(f"🎉 Individual enrollment confirmed for **{full_name}** under the **{program}**!")
                    st.session_state["chat_orders"].append({
                        "Order ID": f"ORD-{len(st.session_state['chat_orders'])+9922}",
                        "Item": f"Academy: {program}",
                        "Amount": "$890" if "1-Week" in program else "$2,950",
                        "Status": "Confirmed"
                    })
                else:
                    st.error("Please fill in all required fields marked with *.")

    # SUBPAGE 2: GROUP BUYING & VOTING HUB
    elif subpage == "👥 Group Buying & Voting Hub":
        st.subheader("👥 Group Campaign & Voting Hub")
        st.info("💡 **How Group Buying Works**: Form or join a group with club teammates or friends. Once the headcount milestone is reached, the tiered discount automatically applies for all participants at checkout!")

        # Facility & Campus Gallery Showcase
        st.markdown("### 📸 Campus & Residence Virtual Tour")
        col_img1, col_img2 = st.columns(2)
        with col_img1:
            st.image(
                "https://encrypted-tbn2.gstatic.com/licensed-image?q=tbn:ANd9GcTlJfjs63KI6QzSpQms4d1rLMcTNoDkcJphyH_y34zqGSvvZbGEs3TmtsDCJLVbWFcYD83uzV10B2lwUR0", 
                caption="High-Performance Training Courts & Indoor Facility", 
                use_container_width=True
            )
        with col_img2:
            st.image(
                "https://encrypted-tbn0.gstatic.com/licensed-image?q=tbn:ANd9GcRI-UXJPpwhWDcFekaYdcs5vb7ShKqOtbpAL6DUhV9W4HTMwQsFOzX3pKb9oNNCgU3VDScBATPtPN4KN5I", 
                caption="Luxury Athlete Residence Suites & Lounge", 
                use_container_width=True
            )

        st.markdown("---")

        # Live Campaign Progress & Voting
        c_left, c_right = st.columns([3, 2])

        with c_left:
            st.markdown("#### 🎯 Active Group Discount Thresholds")
            total_joined = len(st.session_state["academy_group_votes"])
            target_tier_2 = 10

            progress_val = min(total_joined / target_tier_2, 1.0)
            st.progress(progress_val)
            
            st.caption(f"Current Members Committed: **{total_joined} Athletes**")
            
            t1_status = "✅ UNLOCKED" if total_joined >= 5 else f"Need {5 - total_joined} more"
            t2_status = "✅ UNLOCKED" if total_joined >= 10 else f"Need {10 - total_joined} more"

            st.markdown(f"""
            * **Tier 1 (5+ Athletes)**: 15% Group Discount — status: `{t1_status}`
            * **Tier 2 (10+ Athletes)**: 25% Group Discount + Free Video Analysis — status: `{t2_status}`
            """)

            st.markdown("#### 💬 Group Vote & Join Campaign")
            with st.form("group_academy_join_form"):
                member_name = st.text_input("Your Name / Club Name *")
                selected_program = st.selectbox("Group Program Choice", ["1-Week Intensive Boot Camp", "1-Month Pro Residency"])
                vote_btn = st.form_submit_button("Commit & Vote for Group Rate", use_container_width=True)

                if vote_btn:
                    if member_name:
                        st.session_state["academy_group_votes"].append({
                            "name": member_name,
                            "program": selected_program,
                            "discount_tier": "15% Off (Tier 1)" if total_joined + 1 >= 5 else "Pending Threshold"
                        })
                        st.success(f"Welcome aboard, {member_name}! You joined the Group Academy Campaign.")
                        st.rerun()
                    else:
                        st.warning("Please enter your name to join the vote.")

        with c_right:
            st.markdown("#### 📋 Current Group Roster")
            if st.session_state["academy_group_votes"]:
                for idx, item in enumerate(st.session_state["academy_group_votes"], start=1):
                    st.markdown(f"**{idx}. {item['name']}** — *{item['program']}* (`{item['discount_tier']}`)")
            else:
                st.caption("No group members joined yet. Be the first!")

# --- MODULE 5: MATCHMAKING & COACHES ---
def render_module_5():
    st.subheader("🤝 Local Player Matchmaking & Certified Coach Directory")
    
    t1, t2 = st.tabs(["🎾 Find Hitting Partners", "👨‍🏫 Certified Coaches"])
    
    with t1:
        st.markdown("#### Available Local Hitting Partners")
        filter_city = st.selectbox("Filter by City", ["All", "Seoul", "Busan", "Incheon"])
        
        df_players = pd.DataFrame(st.session_state["players_db"])
        if filter_city != "All":
            df_players = df_players[df_players["City"] == filter_city]
            
        st.dataframe(df_players, use_container_width=True)
        
        st.markdown("##### Connect with Partner")
        with st.form("connect_partner_form"):
            partner_name = st.selectbox("Select Partner", df_players["Name"].tolist() if not df_players.empty else ["None"])
            msg = st.text_area("Message / Court Proposal")
            if st.form_submit_button("Send Challenge / Connection Request"):
                if st.session_state["vip_pass"]:
                    st.success(f"Message sent to {partner_name}!")
                else:
                    st.warning("🔒 Free tier users can send 1 request/day. Upgrade to VIP for unlimited direct messaging.")

    with t2:
        st.markdown("#### Certified Coach Directory")
        st.dataframe(pd.DataFrame(st.session_state["coaches_db"]), use_container_width=True)

# --- MODULE 6: SUPPORT & TICKETS ---
def render_module_6():
    st.subheader("🎧 Support Center & Transaction Receipts")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("#### Submit Support Inquiry")
        with st.form("support_ticket_form"):
            subject = st.text_input("Issue / Inquiry Subject *")
            category = st.selectbox("Category", ["Billing & VIP", "Tournament Package", "Academy Residency", "Technical / Video Analysis"])
            details = st.text_area("Inquiry Details *")
            if st.form_submit_button("Submit Support Ticket"):
                if subject and details:
                    st.session_state["inquiries"].append({
                        "Ticket ID": f"TK-{len(st.session_state['inquiries'])+1002}",
                        "Subject": subject,
                        "Status": "Open",
                        "Date": str(datetime.date.today())
                    })
                    st.success("Support ticket logged successfully!")
                else:
                    st.error("Please fill in subject and details.")

    with col2:
        st.markdown("#### Your Active Support Tickets")
        if st.session_state["inquiries"]:
            st.dataframe(pd.DataFrame(st.session_state["inquiries"]), use_container_width=True)
        else:
            st.caption("No open support tickets.")
            
        st.markdown("#### Transaction & Booking Receipts")
        if st.session_state["chat_orders"]:
            st.dataframe(pd.DataFrame(st.session_state["chat_orders"]), use_container_width=True)

# --- MODULE 7: ADMIN CONTROL PANEL ---
def render_module_7():
    st.subheader("🔒 Platform Admin Control Panel")
    password = st.text_input("Enter Admin Passcode", type="password")
    
    if password == "admin":
        st.success("Admin Authentication Successful")
        
        st.markdown("#### Platform Operational Snapshot")
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Total Players Registered", len(st.session_state["players_db"]))
        m2.metric("Certified Coaches", len(st.session_state["coaches_db"]))
        m3.metric("Academy Group Votes", len(st.session_state["academy_group_votes"]))
        m4.metric("Active Support Tickets", len(st.session_state["inquiries"]))

        st.markdown("#### Manage Inquiries")
        st.dataframe(pd.DataFrame(st.session_state["inquiries"]), use_container_width=True)
        
        st.markdown("#### Complete System Transaction Log")
        st.dataframe(pd.DataFrame(st.session_state["chat_orders"]), use_container_width=True)

    elif password:
        st.error("Access Denied: Incorrect Passcode")

# ==========================================
# 6. MAIN ROUTER
# ==========================================
if menu == "1. AI Serve Velocity & Motion Analysis":
    render_module_1()
elif menu == "2. AI Racket & String Calculator":
    render_module_2()
elif menu == "3. Tournaments & Lodging (Group Buy)":
    render_module_3()
elif menu == "4. Residency & Academy Programs":
    render_module_4()
elif menu == "5. Matchmaking & Coach Directory":
    render_module_5()
elif menu == "6. Support & Ticket Receipts":
    render_module_6()
elif menu == "7. Admin Control Panel":
    render_module_7()
