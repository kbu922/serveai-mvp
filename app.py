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

# Custom CSS for Luxury Sand Theme
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
    
    .badge-membership {
        background-color: #E2DCD0;
        color: #211F1D;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 700;
    }

    /* Footer Styling */
    .footer-container {
        background-color: #FAF8F5;
        border-top: 2px solid #E5E0D8;
        padding: 30px;
        border-radius: 12px;
        margin-top: 40px;
    }
    .social-btn {
        display: inline-block;
        background-color: #211F1D;
        color: #FAF8F5 !important;
        padding: 8px 16px;
        border-radius: 6px;
        text-decoration: none;
        font-weight: 600;
        font-size: 13px;
        margin-right: 8px;
        margin-top: 6px;
    }
    .social-btn:hover {
        background-color: #383430;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. STATE INITIALIZATION & AUTH SYSTEM
# ==========================================

# User Authentication Database & Active Session
if "registered_users" not in st.session_state:
    st.session_state["registered_users"] = {
        "alex@tennis.org": {"password": "password123", "name": "Alex Mercer", "tier": "PRO Pass", "ntrp": 4.5},
        "sarah@tennis.org": {"password": "password123", "name": "Sarah Kim", "tier": "VIP Gold", "ntrp": 5.0}
    }

if "is_logged_in" not in st.session_state:
    st.session_state["is_logged_in"] = False

if "current_user" not in st.session_state:
    st.session_state["current_user"] = None

if "language" not in st.session_state:
    st.session_state["language"] = "English"

# Databases
if "players_db" not in st.session_state:
    st.session_state["players_db"] = [
        {"Name": "Marcus Vance", "NTRP": 4.5, "City": "Seoul", "Style": "Aggressive Baseline", "Contact": "m.vance@tennis.org"},
        {"Name": "Elena Rostova", "NTRP": 5.0, "City": "Busan", "Style": "Serve & Volley", "Contact": "elena.r@tennis.org"},
        {"Name": "Jin-woo Park", "NTRP": 4.0, "City": "Seoul", "Style": "Counter-Puncher", "Contact": "jw.park@tennis.kr"},
        {"Name": "Sarah Jenkins", "NTRP": 3.5, "City": "Incheon", "Style": "All-Court", "Contact": "s.jenkins@tennis.org"}
    ]

if "coaches_db" not in st.session_state:
    st.session_state["coaches_db"] = [
        {"Coach": "Coach Rob", "Level": "USPTR Certified Master", "City": "Seoul", "Hourly": "$80/hr", "Specialty": "Serve Biomechanics"},
        {"Coach": "Coach Sarah", "Level": "Ex-WTA Tour Player", "City": "Incheon", "Hourly": "$120/hr", "Specialty": "Match Strategy"},
        {"Coach": "Coach Min-ho", "Level": "KTA High Performance", "City": "Busan", "Hourly": "$95/hr", "Specialty": "Junior Development"}
    ]

if "tournament_group_votes" not in st.session_state:
    st.session_state["tournament_group_votes"] = [
        {"Name": "Chris P.", "Tournament": "US Open Tennis Championships", "Status": "Discount Unlocked ($85)"},
        {"Name": "Min-ji K.", "Tournament": "Seoul Open Masters", "Status": "Discount Unlocked ($85)"},
        {"Name": "Kenji S.", "Tournament": "Seoul Open Masters", "Status": "Discount Unlocked ($85)"}
    ]

if "academy_group_votes" not in st.session_state:
    st.session_state["academy_group_votes"] = [
        {"name": "Alex M.", "program": "1-Week Intensive Boot Camp", "discount_tier": "15% Off"},
        {"name": "Sarah K.", "program": "1-Week Intensive Boot Camp", "discount_tier": "15% Off"},
        {"name": "David L.", "program": "1-Month Pro Residency", "discount_tier": "20% Off"}
    ]

if "inquiries" not in st.session_state:
    st.session_state["inquiries"] = [
        {"Ticket ID": "TK-1001", "Subject": "Racket Stringing Order", "Status": "Resolved", "Date": "2026-07-15"}
    ]

if "chat_orders" not in st.session_state:
    st.session_state["chat_orders"] = [
        {"Order ID": "ORD-9921", "Item": "PRO Pass Monthly", "Amount": "$19.99", "Status": "Paid"}
    ]

# ==========================================
# 3. SIDEBAR AUTH & MEMBERSHIP PANEL
# ==========================================
st.sidebar.image("https://images.unsplash.com/photo-1595435934249-5df7ed86e1c0?w=400&q=80", caption="Global Tennis Hub")

# Account Authenticator Box
st.sidebar.markdown("### 🔐 User Portal")

if not st.session_state["is_logged_in"]:
    auth_tab1, auth_tab2 = st.sidebar.tabs(["🔑 Login", "📝 Register"])
    
    with auth_tab1:
        login_email = st.text_input("Email", key="login_email")
        login_pass = st.text_input("Password", type="password", key="login_pass")
        if st.button("Log In", key="btn_login"):
            if login_email in st.session_state["registered_users"] and st.session_state["registered_users"][login_email]["password"] == login_pass:
                st.session_state["is_logged_in"] = True
                st.session_state["current_user"] = st.session_state["registered_users"][login_email]
                st.session_state["current_user"]["email"] = login_email
                st.sidebar.success(f"Welcome back, {st.session_state['current_user']['name']}!")
                st.rerun()
            else:
                st.sidebar.error("Invalid Email or Password.")

    with auth_tab2:
        reg_name = st.text_input("Full Name", key="reg_name")
        reg_email = st.text_input("Email", key="reg_email")
        reg_pass = st.text_input("Password", type="password", key="reg_pass")
        reg_ntrp = st.slider("NTRP Skill", 1.0, 7.0, 3.5, 0.5, key="reg_ntrp")
        if st.button("Create Account", key="btn_reg"):
            if reg_email and reg_pass and reg_name:
                st.session_state["registered_users"][reg_email] = {
                    "password": reg_pass,
                    "name": reg_name,
                    "tier": "Free Tier",
                    "ntrp": reg_ntrp
                }
                st.session_state["is_logged_in"] = True
                st.session_state["current_user"] = st.session_state["registered_users"][reg_email]
                st.session_state["current_user"]["email"] = reg_email
                st.sidebar.success("Account created successfully!")
                st.rerun()
            else:
                st.sidebar.error("Please fill in all fields.")
else:
    u = st.session_state["current_user"]
    st.sidebar.markdown(f"**Logged in as:** `{u['name']}`")
    st.sidebar.markdown(f"**Membership:** <span class='badge-membership'>{u['tier']}</span>", unsafe_allow_html=True)
    st.sidebar.markdown(f"**NTRP Rating:** `{u['ntrp']}`")
    
    if st.sidebar.button("Log Out", key="btn_logout"):
        st.session_state["is_logged_in"] = False
        st.session_state["current_user"] = None
        st.rerun()

st.sidebar.markdown("---")

menu = st.sidebar.radio(
    "Select Module:",
    [
        "💳 Membership & Subscriptions",
        "1. AI Serve Velocity & Motion Analysis",
        "2. AI Racket & String Calculator",
        "3. Tournaments & Lodging (US Open / Korea)",
        "4. Residency & Academy Programs",
        "5. Matchmaking & Coach Directory",
        "6. Support & Ticket Receipts",
        "7. Admin Control Panel",
        "📞 Contact HQ & Social Links"
    ]
)

# Sidebar Quick Contact Card
st.sidebar.markdown("---")
st.sidebar.markdown("### 🏢 Global HQ Contact")
st.sidebar.caption("📍 Songpa-gu, Seoul, Korea")
st.sidebar.caption("📞 +82 2-555-1004")
st.sidebar.caption("✉️ support@globaltennis.org")

# ==========================================
# 4. TOP NAVIGATION HEADER
# ==========================================
col_h1, col_h2, col_h3 = st.columns([4, 2, 2])

with col_h1:
    st.markdown("### 🎾 Global Tennis Platform & AI Suite")
    st.caption("Live Stats: **12,400+ Serves Analyzed** | 4,200+ Active Members Globally")

with col_h2:
    lang = st.selectbox("🌐 Language / 언어", ["English", "한국어"], index=0 if st.session_state["language"] == "English" else 1)
    st.session_state["language"] = lang

with col_h3:
    current_tier = st.session_state["current_user"]["tier"] if st.session_state["is_logged_in"] else "Guest / Free"
    st.markdown(f"**Status:** `{current_tier}`")

st.markdown("---")

# ==========================================
# 5. MODULE FUNCTIONS
# ==========================================

# --- MODULE: MEMBERSHIP & SUBSCRIPTION PAYMENT GATE ---
def render_module_membership():
    st.subheader("💳 Platform Membership & Subscription Plans")
    st.write("Unlock elite AI biomechanics features, coach messaging, and group discount thresholds.")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div style="background-color:#FAF8F5; border:1px solid #E5E0D8; border-radius:12px; padding:20px; text-align:center;">
            <h3>🆓 Free Athlete</h3>
            <h2>$0 <span style="font-size:14px;">/ forever</span></h2>
            <hr>
            <p>✓ Basic AI Serve Analysis (3/mo)</p>
            <p>✓ Access Player Directory</p>
            <p>✓ View Campus Facilities</p>
            <p>✗ Coach Direct Messaging</p>
            <p>✗ Group Buying Discounts</p>
        </div>
        """, unsafe_allow_html=True)
        st.write("")
        if st.button("Current Base Plan", disabled=True, key="plan_free"):
            pass

    with col2:
        st.markdown("""
        <div style="background-color:#FAF8F5; border:2px solid #211F1D; border-radius:12px; padding:20px; text-align:center;">
            <h3>⚡ PRO Pass</h3>
            <h2>$19.99 <span style="font-size:14px;">/ month</span></h2>
            <hr>
            <p>✓ Unlimited AI Serve Velocity Analysis</p>
            <p>✓ AI Racket & Tension Optimizer</p>
            <p>✓ Matchmaking & Coach Messaging</p>
            <p>✓ Group Tournament Discounts</p>
            <p>✓ Priority Support Tickets</p>
        </div>
        """, unsafe_allow_html=True)
        st.write("")
        if st.button("Subscribe PRO ($19.99/mo)", key="plan_pro"):
            st.session_state["selected_plan"] = ("PRO Pass", "$19.99/mo")

    with col3:
        st.markdown("""
        <div style="background-color:#FAF8F5; border:1px solid #E5E0D8; border-radius:12px; padding:20px; text-align:center;">
            <h3>🏆 VIP Gold Residency</h3>
            <h2>$149.00 <span style="font-size:14px;">/ year</span></h2>
            <hr>
            <p>✓ All PRO Features Included</p>
            <p>✓ 25% Off Academy Residency Camps</p>
            <p>✓ Quarterly Video Review with Pro Coach</p>
            <p>✓ Guaranteed Hotel Discount Locking</p>
            <p>✓ VIP Lounge Access</p>
        </div>
        """, unsafe_allow_html=True)
        st.write("")
        if st.button("Subscribe VIP Gold ($149/yr)", key="plan_vip"):
            st.session_state["selected_plan"] = ("VIP Gold", "$149.00/yr")

    # Payment Checkout Box
    if "selected_plan" in st.session_state:
        plan_name, plan_price = st.session_state["selected_plan"]
        st.markdown("---")
        st.markdown(f"### 🔒 Secure Checkout: **{plan_name} ({plan_price})**")
        
        with st.form("checkout_payment_form"):
            c_a, c_b = st.columns(2)
            with c_a:
                card_name = st.text_input("Cardholder Full Name *")
                card_num = st.text_input("Credit Card Number *", type="password", placeholder="•••• •••• •••• ••••")
            with c_b:
                card_exp = st.text_input("Expiration Date (MM/YY) *", placeholder="08/28")
                card_cvv = st.text_input("CVV Security Code *", type="password", placeholder="123")

            pay_submitted = st.form_submit_button("Confirm Payment & Activate Subscription", use_container_width=True)
            
            if pay_submitted:
                if card_name and card_num and card_exp and card_cvv:
                    if st.session_state["is_logged_in"]:
                        st.session_state["current_user"]["tier"] = plan_name
                        user_email = st.session_state["current_user"]["email"]
                        st.session_state["registered_users"][user_email]["tier"] = plan_name
                    
                    st.session_state["chat_orders"].append({
                        "Order ID": f"ORD-{len(st.session_state['chat_orders'])+9922}",
                        "Item": f"Subscription: {plan_name}",
                        "Amount": plan_price,
                        "Status": "Paid"
                    })
                    st.success(f"🎉 Payment successful! You are now upgraded to **{plan_name}**.")
                    del st.session_state["selected_plan"]
                    st.rerun()
                else:
                    st.error("Please fill in all credit card payment details.")

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
                time.sleep(2)
                st.success("Analysis Complete!")
                
                m1, m2, m3 = st.columns(3)
                m1.metric("Peak Serve Speed", "118 mph", delta="+4 mph from last average")
                m2.metric("Spin Rate", "2,840 RPM", delta="Topspin / Kick")
                m3.metric("Impact Height", "2.85 meters", delta="Optimal Apex")
                
                st.markdown("#### 📐 Biomechanics Analysis Breakdown")
                st.write("* **Trophy Position**: Shoulder tilt angle measured at **28°** (Optimal range: 25°-32°).")
                st.write("* **Leg Drive & Kneebend**: Knee flexion reached **115°** prior to vertical launch.")
                st.write("* **Pronation Speed**: Wrist angular acceleration calculated at **1,420°/sec**.")

    with col2:
        st.info("💡 **Pro Tip**: Use 120 FPS or higher camera modes to eliminate shutter blur on the impact frame.")

# --- MODULE 2: AI RACKET CALCULATOR ---
def render_module_2():
    st.subheader("🎯 AI Racket & String Tension Recommendation Engine")
    
    c1, c2 = st.columns(2)
    with c1:
        ntrp = st.slider("Your NTRP Skill Rating", 1.5, 7.0, 3.5, 0.5)
        serve_speed = st.number_input("Average Serve Speed (mph)", 40, 140, 85)
        playstyle = st.selectbox("Primary Playstyle", ["Baseline Aggressor", "All-Court Counterpuncher", "Touch & Net Specialist", "Power Serve & Volley"])
    
    with c2:
        elbow_issue = st.checkbox("Suffer from Tennis Elbow / Wrist Strain?")
        spin_pref = st.select_slider("Performance Priority", options=["Max Control & Precision", "Balanced All-Around", "Max Spin & Power"])

    if st.button("Calculate Optimal Setup"):
        st.markdown("---")
        st.markdown("### 🛠️ Recommended Equipment Specification")
        
        res_col1, res_col2, res_col3 = st.columns(3)
        with res_col1:
            st.metric("Head Size", "98 - 100 sq in")
        with res_col2:
            tension = "46 - 50 lbs" if elbow_issue else "52 - 55 lbs"
            st.metric("String Tension", tension)
        with res_col3:
            string_type = "Soft Multifilament" if elbow_issue else "Co-Poly / Hybrid"
            st.metric("String Material", string_type)

# --- MODULE 3: TOURNAMENTS & LODGING ---
def render_module_3():
    st.markdown("""
        <div style="background-color:#FAF8F5; padding:20px; border-radius:12px; border:1px solid #E5E0D8; margin-bottom:20px;">
            <h2 style="color:#211F1D; margin-top:0;">🏆 Global Tournaments, Lodging & Group Buying</h2>
            <p style="color:#5C544D; font-size:14px;">
                Book hotel accommodations and player tickets for major championships including the US Open, Seoul Open Masters, and Busan Clay Court Cup.
            </p>
        </div>
    """, unsafe_allow_html=True)

    selected_event = st.selectbox(
        "📍 Select Target Competition:",
        ["🇺🇸 US Open Championships (Flushing Meadows, NY)", "🇰🇷 Seoul Open Masters (Olympic Park, Korea)", "🇰🇷 Busan Clay Court Cup (Sajik Complex, Korea)"]
    )

    subpage = st.radio(
        "Select Booking Pathway:",
        ["🖼️ Competition Infrastructure & Residence Gallery", "👥 Member Group Buying ($85 Discount)", "👤 Individual Registration & Checkout"],
        horizontal=True,
        key="tourn_subpage_nav"
    )

    st.markdown("---")

    if subpage == "🖼️ Competition Infrastructure & Residence Gallery":
        st.subheader(f"🏟️ Facility & Accommodation Tour: {selected_event.split('(')[0]}")
        st.write("Explore official tournament arenas, player lounges, and preferred partner hotels offering athlete amenities.")

        col_img1, col_img2 = st.columns(2)

        if "US Open" in selected_event:
            with col_img1:
                st.image(
                    "https://images.unsplash.com/photo-1595435934249-5df7ed86e1c0?w=800&q=80",
                    caption="🏟️ Arthur Ashe Stadium & Grandstand Courts (Flushing, NY)",
                    use_container_width=True
                )
                st.markdown("""
                **US Open Competition Ground Highlights:**
                * World's largest tennis stadium with retractable roof technology.
                * Hard court Laykold surface optimized for fast baseline rallies.
                * Dedicated warm-up courts and high-speed video tracking arrays.
                """)

            with col_img2:
                st.image(
                    "https://images.unsplash.com/photo-1566073771259-6a8506099945?w=800&q=80",
                    caption="🏨 Queens & Manhattan Athlete Residence Partner Suite",
                    use_container_width=True
                )
                st.markdown("""
                **Official Athlete Lodging:**
                * Luxury 4-star suite options within 15 minutes of Flushing Meadows.
                * Shuttle buses running every 20 minutes to competition grounds.
                * On-site gym, sports massage rooms, and high-protein player buffets.
                """)

        elif "Seoul Open" in selected_event:
            with col_img1:
                st.image(
                    "https://encrypted-tbn2.gstatic.com/licensed-image?q=tbn:ANd9GcTlJfjs63KI6QzSpQms4d1rLMcTNoDkcJphyH_y34zqGSvvZbGEs3TmtsDCJLVbWFcYD83uzV10B2lwUR0",
                    caption="🏟️ Seoul Olympic Park Tennis Center Main Arena",
                    use_container_width=True
                )
                st.markdown("""
                **Seoul Open Competition Grounds:**
                * Historic 10,000-seat center court built for high-stakes championship play.
                * 18 outdoor hard courts with night lighting and umpire cameras.
                * Directly connected to Olympic Park subway and athlete village.
                """)

            with col_img2:
                st.image(
                    "https://encrypted-tbn0.gstatic.com/licensed-image?q=tbn:ANd9GcRI-UXJPpwhWDcFekaYdcs5vb7ShKqOtbpAL6DUhV9W4HTMwQsFOzX3pKb9oNNCgU3VDScBATPtPN4KN5I",
                    caption="🏨 Olympic Village Hotel & Athlete Suites (Seoul)",
                    use_container_width=True
                )
                st.markdown("""
                **Partner Lodging Details:**
                * Premium athlete accommodations with king beds and ergonomic recovery spaces.
                * Daily breakfast buffet designed for high-performance endurance.
                """)

        else: # Busan
            with col_img1:
                st.image(
                    "https://images.unsplash.com/photo-1595435934249-5df7ed86e1c0?w=800&q=80",
                    caption="🏟️ Busan Sajik Clay Court Complex",
                    use_container_width=True
                )
                st.markdown("""
                **Busan Clay Court Arena:**
                * Premium imported European Red Clay courts for maximum spin and traction.
                * Ocean breeze climate with covered spectator stands.
                """)

            with col_img2:
                st.image(
                    "https://images.unsplash.com/photo-1566073771259-6a8506099945?w=800&q=80",
                    caption="🏨 Haeundae Oceanfront Athlete Resort",
                    use_container_width=True
                )
                st.markdown("""
                **Partner Lodging Details:**
                * Oceanfront suites with private hydrotherapy spa tubs.
                * Express shuttles direct to Sajik Tennis Complex.
                """)

    elif subpage == "👥 Member Group Buying ($85 Discount)":
        st.subheader(f"👥 Group Buying Campaign: {selected_event.split('(')[0]}")
        st.info("💡 **Group Buying Advantage**: Join forces with 5+ fellow athletes to unlock an instant $85/person bulk discount on combined hotel and tournament pass packages!")

        votes = len(st.session_state["tournament_group_votes"])
        target = 5
        st.progress(min(votes / target, 1.0))
        st.caption(f"Current Committed Members: **{votes}/{target} Athletes Joined**")

        st.markdown("#### 📋 Current Campaign Participants")
        st.table(pd.DataFrame(st.session_state["tournament_group_votes"]))

        st.markdown("#### 💳 Commit & Join Group Payment Tier")
        with st.form("join_tournament_group_form"):
            c_g1, c_g2 = st.columns(2)
            with c_g1:
                g_user_name = st.text_input("Athlete Full Name *", value=st.session_state["current_user"]["name"] if st.session_state["is_logged_in"] else "")
                g_email = st.text_input("Contact Email *", value=st.session_state["current_user"]["email"] if st.session_state["is_logged_in"] else "")
            with c_g2:
                g_card = st.text_input("Credit Card Number ($85 Discounted Deposit) *", type="password")
                g_expiry = st.text_input("Expiration (MM/YY) *", placeholder="12/28")

            submit_group = st.form_submit_button("Pay & Commit to Group Package ($215 / Person)", use_container_width=True)
            
            if submit_group:
                if g_user_name and g_email and g_card:
                    st.session_state["tournament_group_votes"].append({
                        "Name": g_user_name,
                        "Tournament": selected_event.split('(')[0].strip(),
                        "Status": "Discount Unlocked ($85 Off)"
                    })
                    st.session_state["chat_orders"].append({
                        "Order ID": f"ORD-{len(st.session_state['chat_orders'])+9922}",
                        "Item": f"Group Tourn Deposit: {selected_event.split('(')[0]}",
                        "Amount": "$215.00",
                        "Status": "Paid (Group Tier)"
                    })
                    st.success(f"🎉 Successfully joined group campaign for **{selected_event.split('(')[0]}**! Your $85 discount is locked.")
                    st.rerun()
                else:
                    st.error("Please complete all payment fields.")

    elif subpage == "👤 Individual Registration & Checkout":
        st.subheader(f"👤 Individual Player Booking: {selected_event.split('(')[0]}")
        st.write("Book standard individual hotel stay and tournament pass without group constraints.")

        with st.form("indiv_tourn_form"):
            c1, c2 = st.columns(2)
            with c1:
                p_name = st.text_input("Player Full Name *", value=st.session_state["current_user"]["name"] if st.session_state["is_logged_in"] else "")
                p_passport = st.text_input("Passport / Gov ID *")
                p_event = st.selectbox("Event Category", ["Singles Championship", "Doubles Division", "VIP Spectator Pass"])
            with c2:
                check_in = st.date_input("Hotel Check-in Date", datetime.date(2026, 9, 10))
                check_out = st.date_input("Hotel Check-out Date", datetime.date(2026, 9, 15))
                card = st.text_input("Credit Card Number ($300 Standard Rate) *", type="password")

            if st.form_submit_button("Pay & Confirm Individual Booking ($300.00)", use_container_width=True):
                if p_name and p_passport and card:
                    st.session_state["chat_orders"].append({
                        "Order ID": f"ORD-{len(st.session_state['chat_orders'])+9922}",
                        "Item": f"Individual Tourn Pass: {selected_event.split('(')[0]}",
                        "Amount": "$300.00",
                        "Status": "Paid (Individual)"
                    })
                    st.success(f"🎉 Individual tournament entry and hotel package confirmed for **{p_name}**!")
                else:
                    st.error("Please fill in all required fields.")

# --- MODULE 4: ACADEMY & RESIDENCY ---
def render_module_4():
    st.markdown("""
        <div style="background-color:#FAF8F5; padding:20px; border-radius:12px; border:1px solid #E5E0D8; margin-bottom:20px;">
            <h2 style="color:#211F1D; margin-top:0;">🏛️ Global Tennis Academy, Residency & Campus Infrastructure</h2>
            <p style="color:#5C544D; font-size:14px;">
                Accelerate your game with world-class ATP/WTA certified coaching, high-performance training grounds, and luxury athlete residences.
            </p>
        </div>
    """, unsafe_allow_html=True)

    subpage = st.radio(
        "Select Section:",
        ["🏟️ Campus Infrastructure & Facility Tour", "👥 Group Buying & Voting Hub", "👤 Individual Enrollment"],
        horizontal=True,
        key="academy_subpage_nav"
    )

    st.markdown("---")

    if subpage == "🏟️ Campus Infrastructure & Facility Tour":
        st.subheader("🏟️ World-Class Campus Infrastructure & Athletic Complex")
        st.write("Designed in partnership with top tour biomechanists, our 40-acre campus combines Grand Slam-grade playing surfaces with luxury residential suites.")

        f_col1, f_col2, f_col3, f_col4 = st.columns(4)
        f_col1.metric("Courts Total", "24 Courts", "12 Hard / 8 Clay / 4 Grass")
        f_col2.metric("Biomechanics Labs", "2 High-Speed Labs", "240 FPS Camera Arrays")
        f_col3.metric("Recovery Spa", "Olympic Hydrotherapy", "Cryo & Ice Baths")
        f_col4.metric("Dormitory Capacity", "120 Luxury Suites", "24/7 Security & Nutrition")

        st.markdown("---")

        st.markdown("### 📸 Campus Visual Gallery")
        img_col1, img_col2 = st.columns(2)
        with img_col1:
            st.image(
                "https://encrypted-tbn2.gstatic.com/licensed-image?q=tbn:ANd9GcTlJfjs63KI6QzSpQms4d1rLMcTNoDkcJphyH_y34zqGSvvZbGEs3TmtsDCJLVbWFcYD83uzV10B2lwUR0",
                caption="🏟️ Center Court & Covered Indoor High-Performance Facility",
                use_container_width=True
            )
            st.markdown("""
            **High-Performance Court Complex:**
            * Custom 9-layer cushioned Plexicushion hard courts (identical to Australian Open).
            * Red Clay courts imported from Europe with subterranean hydration.
            * Smart LED stadium lighting for night match play training.
            """)

        with img_col2:
            st.image(
                "https://encrypted-tbn0.gstatic.com/licensed-image?q=tbn:ANd9GcRI-UXJPpwhWDcFekaYdcs5vb7ShKqOtbpAL6DUhV9W4HTMwQsFOzX3pKb9oNNCgU3VDScBATPtPN4KN5I",
                caption="🛏️ Luxury Athlete Residence Suites & Lounge",
                use_container_width=True
            )
            st.markdown("""
            **Athlete Residence & Living Quarters:**
            * Private and twin luxury suites with ergonomic memory foam mattresses.
            * Executive study lounges, high-speed fiber internet, and video review suites.
            * On-site organic performance dining hall managed by sports nutritionists.
            """)

    elif subpage == "👥 Group Buying & Voting Hub":
        st.subheader("👥 Group Campaign & Voting Hub")
        st.info("💡 **How Group Buying Works**: Form or join a group with club teammates or friends. Once the headcount milestone is reached, the tiered discount automatically applies for all participants at checkout!")

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

            with st.form("group_academy_join_form"):
                member_name = st.text_input("Your Name / Club Name *", value=st.session_state["current_user"]["name"] if st.session_state["is_logged_in"] else "")
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

        with c_right:
            st.markdown("#### 📋 Current Group Roster")
            if st.session_state["academy_group_votes"]:
                for idx, item in enumerate(st.session_state["academy_group_votes"], start=1):
                    st.markdown(f"**{idx}. {item['name']}** — *{item['program']}* (`{item['discount_tier']}`)")

    elif subpage == "👤 Individual Enrollment":
        st.subheader("Individual Program Booking")
        program = st.selectbox("Select Training Program:", ["1-Week Intensive Boot Camp ($890)", "1-Month Pro Residency ($2,950)"])

        with st.form("individual_residency_form"):
            col1, col2 = st.columns(2)
            with col1:
                full_name = st.text_input("Full Name *", value=st.session_state["current_user"]["name"] if st.session_state["is_logged_in"] else "")
                passport = st.text_input("Passport / ID Number *")
                start_date = st.date_input("Preferred Start Date")
            with col2:
                ntrp = st.slider("Current NTRP Rating", 1.0, 7.0, 3.5, 0.5)
                card_num = st.text_input("Credit Card Number *", type="password")

            submitted = st.form_submit_button("Complete Individual Registration", use_container_width=True)
            if submitted:
                if full_name and passport and card_num:
                    st.success(f"🎉 Individual enrollment confirmed for **{full_name}** under the **{program}**!")

# --- MODULE 5: MATCHMAKING & COACHES ---
def render_module_5():
    st.subheader("🤝 Local Player Matchmaking & Certified Coach Directory")
    
    t1, t2 = st.tabs(["🎾 Find Hitting Partners", "👨‍🏫 Certified Coaches"])
    with t1:
        st.dataframe(pd.DataFrame(st.session_state["players_db"]), use_container_width=True)
    with t2:
        st.dataframe(pd.DataFrame(st.session_state["coaches_db"]), use_container_width=True)

# --- MODULE 6: SUPPORT & TICKETS ---
def render_module_6():
    st.subheader("🎧 Support Center & Transaction Receipts")
    
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("#### Submit Support Ticket")
        with st.form("support_ticket_form"):
            subject = st.text_input("Issue Subject *")
            details = st.text_area("Inquiry Details *")
            if st.form_submit_button("Submit Ticket"):
                if subject and details:
                    st.session_state["inquiries"].append({"Ticket ID": f"TK-{len(st.session_state['inquiries'])+1002}", "Subject": subject, "Status": "Open", "Date": str(datetime.date.today())})
                    st.success("Support ticket logged successfully!")

    with col2:
        st.markdown("#### Your Tickets")
        st.dataframe(pd.DataFrame(st.session_state["inquiries"]), use_container_width=True)
        st.markdown("#### Transaction Receipts")
        st.dataframe(pd.DataFrame(st.session_state["chat_orders"]), use_container_width=True)

# --- MODULE 7: ADMIN CONTROL PANEL ---
def render_module_7():
    st.subheader("🔒 Platform Admin Control Panel")
    password = st.text_input("Enter Admin Passcode", type="password")
    
    if password == "admin":
        st.success("Admin Authentication Successful")
        st.json({
            "Registered System Users": len(st.session_state["registered_users"]),
            "Active Orders": len(st.session_state["chat_orders"]),
            "Open Tickets": len(st.session_state["inquiries"])
        })
        st.markdown("#### Registered Users List")
        st.dataframe(pd.DataFrame.from_dict(st.session_state["registered_users"], orient='index'))

# --- MODULE 8: CONTACT HQ & SOCIAL LINKS (DEDICATED MODULE & FOOTER) ---
def render_module_contact():
    st.markdown("""
        <div style="background-color:#FAF8F5; padding:24px; border-radius:12px; border:1px solid #E5E0D8;">
            <h2 style="margin-top:0;">🏢 Global Headquarters & Corporate Office</h2>
            <p style="color:#5C544D;">Visit our administrative offices, reach out to our player admissions team, or follow us on our social media platforms.</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.write("")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 📍 Office Address & Details")
        st.markdown("""
        * **Company Name**: Global Tennis Academy & Tech Platform Inc.
        * **Global HQ Address**: 124 Olympic-ro, Songpa-gu, Seoul, 05540, South Korea *(Adjacent to Seoul Olympic Park Tennis Complex)*
        * **US Branch Office**: 120 Flushing Meadows Way, Queens, NY 11368, USA
        * **Main Office Phone**: +82 2-555-1004 / +1 (800) 555-TENNIS
        * **Support Email**: `support@globaltennis.org`
        * **Admissions Email**: `admissions@globaltennis.org`
        * **Business Hours**: Mon – Fri: 09:00 – 18:00 KST / EST
        """)

    with col2:
        st.markdown("### 🌐 Official Media Channels")
        st.markdown("Connect with our global community, watch AI biomechanics breakdowns, and stay updated on upcoming academy camps:")
        st.markdown("""
        <a href="https://youtube.com" target="_blank" class="social-btn">📺 YouTube Channel</a>
        <a href="https://instagram.com" target="_blank" class="social-btn">📸 Instagram (@GlobalTennisAI)</a>
        <a href="https://twitter.com" target="_blank" class="social-btn">🐦 X / Twitter</a>
        <a href="https://linkedin.com" target="_blank" class="social-btn">💼 LinkedIn Official</a>
        """, unsafe_allow_html=True)

# ==========================================
# 6. MAIN ROUTER & FOOTER INJECTION
# ==========================================
if menu == "💳 Membership & Subscriptions":
    render_module_membership()
elif menu == "1. AI Serve Velocity & Motion Analysis":
    render_module_1()
elif menu == "2. AI Racket & String Calculator":
    render_module_2()
elif menu == "3. Tournaments & Lodging (US Open / Korea)":
    render_module_3()
elif menu == "4. Residency & Academy Programs":
    render_module_4()
elif menu == "5. Matchmaking & Coach Directory":
    render_module_5()
elif menu == "6. Support & Ticket Receipts":
    render_module_6()
elif menu == "7. Admin Control Panel":
    render_module_7()
elif menu == "📞 Contact HQ & Social Links":
    render_module_contact()

# ==========================================
# 7. GLOBAL FOOTER (Rendered Everywhere)
# ==========================================
st.markdown("""
    <div class="footer-container">
        <div style="display:flex; justify-content:space-between; flex-wrap:wrap; gap:20px;">
            <div>
                <h4>🎾 Global Tennis Academy & Platform Inc.</h4>
                <p style="font-size:13px; color:#5C544D;">
                    📍 HQ Address: 124 Olympic-ro, Songpa-gu, Seoul, South Korea<br>
                    📞 Phone: +82 2-555-1004 | ✉️ Support: support@globaltennis.org
                </p>
            </div>
            <div>
                <h4>📱 Stay Connected</h4>
                <a href="https://youtube.com" target="_blank" class="social-btn">YouTube</a>
                <a href="https://instagram.com" target="_blank" class="social-btn">Instagram</a>
                <a href="https://twitter.com" target="_blank" class="social-btn">X / Twitter</a>
                <a href="https://linkedin.com" target="_blank" class="social-btn">LinkedIn</a>
            </div>
        </div>
        <hr style="border-color:#E5E0D8; margin-top:20px; margin-bottom:15px;">
        <p style="text-align:center; font-size:12px; color:#8C827A; margin:0;">
            © 2026 Global Tennis Platform & AI Suite. All rights reserved. Built for High-Performance Athletes Worldwide.
        </p>
    </div>
""", unsafe_allow_html=True)
