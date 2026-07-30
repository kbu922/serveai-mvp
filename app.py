import streamlit as st
import pandas as pd
import datetime
import time


# -------------------------------------------------------------
# 1. TRANSLATION DICTIONARY & HELPER (PURE PYTHON - SAFE BEFORE SET_PAGE_CONFIG)
# -------------------------------------------------------------
TEXTS = {
    "EN": {
        "title": "🎧 Support Center & Billing Receipts",
        "subtitle": "Manage your support inquiries, request equipment service updates, and access official tax invoices/receipts.",
        "tab_tickets": "📋 My Support Tickets",
        "tab_receipts": "🧾 Transaction Receipts & Invoices",
        "tab_new_ticket": "📩 Submit New Inquiry",
        "active_tickets": "🎫 Active & Past Support Requests",
        "login_info": "💡 Please log in to view your personalized support history.",
        "billing_history": "💳 Billing History & Official Receipts",
        "generate_receipt": "📄 Generate Detailed Digital Receipt",
        "select_order": "Select Order ID to View Receipt:",
        "submit_ticket_hdr": "📩 Create a Support Ticket",
        "category": "Inquiry Category:",
        "subject": "Subject / Title *",
        "details": "Provide details about your inquiry *",
        "submit_btn": "Submit Support Ticket",
        "success_msg": "🎉 Ticket **{id}** submitted successfully! Our team will respond within 24 hours.",
        "no_orders": "No transaction records found."
    },
    "KR": {
        "title": "🎧 고객 지원 센터 및 결제 영수증",
        "subtitle": "문의 내역 관리, 장비 서비스 업데이트 요청 및 공식 세금 계산서/영수증을 확인하세요.",
        "tab_tickets": "📋 내 지원 티켓",
        "tab_receipts": "🧾 거래 내역 및 영수증",
        "tab_new_ticket": "📩 새 문의 제출하기",
        "active_tickets": "🎫 진행 중 및 지난 문의 내역",
        "login_info": "💡 개인 맞춤 지원 내역을 확인하려면 로그인해 주세요.",
        "billing_history": "💳 결제 내역 및 공식 영수증",
        "generate_receipt": "📄 상세 디지털 영수증 발급",
        "select_order": "영수증을 조회할 주문 ID를 선택하세요:",
        "submit_ticket_hdr": "📩 지원 티켓 작성",
        "category": "문의 유형:",
        "subject": "제목 *",
        "details": "문의 내용을 자세히 작성해 주세요 *",
        "submit_btn": "지원 티켓 제출",
        "success_msg": "🎉 티켓 **{id}**이(가) 성공적으로 접수되었습니다! 24시간 이내에 답변해 드리겠습니다.",
        "no_orders": "거래 내역이 없습니다."
    }
}

def get_text(key, lang="EN"):
    """Helper function to safely retrieve localized strings."""
    return TEXTS.get(lang, TEXTS["EN"]).get(key, key)


# -------------------------------------------------------------
# 2. FIRST STREAMLIT COMMAND (MUST BE FIRST STREAMLIT CALL)
# -------------------------------------------------------------
st.set_page_config(
    page_title="Global Tennis Academy",
    page_icon="🎾",
    layout="wide"
)

# -------------------------------------------------------------
# 3. INITIALIZE SESSION STATE AFTER PAGE CONFIG
# -------------------------------------------------------------
if "language" not in st.session_state:
    st.session_state["language"] = "KR"  # Default to Korean or English
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

    .social-btn {
        display: inline-block;
        background-color: #211F1D;
        color: #FAF8F5 !important;
        padding: 10px 20px;
        border-radius: 8px;
        text-decoration: none;
        font-weight: 600;
        font-size: 14px;
        margin-right: 10px;
        margin-top: 10px;
    }
    .social-btn:hover {
        background-color: #383430;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. STATE INITIALIZATION & AUTH SYSTEM
# ==========================================

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
# 3. SIDEBAR AUTH & NAVIGATION PANEL
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
        "⚡ 1. AI Serve Velocity & Biomechanics Analyzer",
        "🎯 2. AI Racket & String Tension Recommendation Engine",
        "💳 3. Membership & Subscriptions",
        "🏆 4. Tournaments & Lodging (US Open / Korea)",
        "🏛️ 5. Residency & Academy Programs",
        "🤝 6. Matchmaking & Coach Directory",
        "🎧 7. Support & Ticket Receipts",
        "🔒 8. Admin Control Panel",
        "📞 9. Contact Us"
    ]
)

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
# 5. ENHANCED MODULE FUNCTIONS
# ==========================================

# --- MODULE 1: AI SERVE VELOCITY (GRAPHIC & DETAILED) ---
def render_module_1():
    st.subheader("⚡ AI Serve Velocity & Biomechanics Analyzer")
    st.write("Upload high-speed footage to run computer-vision motion vector tracking, shoulder axis analysis, and kinetic kinetic chain evaluation.")

    col1, col2 = st.columns([3, 2])
    with col1:
        video_file = st.file_uploader("Upload Serve Video Footage (MP4/MOV)", type=["mp4", "mov"])
        c_a, c_b = st.columns(2)
        with c_a:
            angle = st.selectbox("Camera Angle", ["Behind Court (Baseline)", "Side View (Court Level)", "45-Degree Angle"])
        with c_b:
            fps = st.slider("Frame Rate (FPS)", 30, 240, 120, help="Higher FPS provides pinpoint accuracy at ball contact frame.")

        run_analysis = st.button("Run Deep AI Velocity & Motion Analysis")

    with col2:
        st.markdown("""
        <div style="background-color:#FAF8F5; border:1px solid #E5E0D8; border-radius:12px; padding:16px;">
            <h4 style="margin-top:0;">📊 AI Motion Vector Benchmarks</h4>
            <p style="font-size:13px; color:#5C544D; margin-bottom:8px;"><strong>Trophy Angle Target:</strong> 25° - 35°</p>
            <p style="font-size:13px; color:#5C544D; margin-bottom:8px;"><strong>Pronation Speed Target:</strong> >1,300°/sec</p>
            <p style="font-size:13px; color:#5C544D; margin-bottom:0;"><strong>Kinetic Efficiency Target:</strong> >85%</p>
        </div>
        """, unsafe_allow_html=True)

    if video_file or run_analysis:
        with st.spinner("Analyzing high-speed frames, calculating kinetic launch metrics, and plotting biomechanical vectors..."):
            time.sleep(2)
            st.markdown("---")
            st.markdown("### 📈 Biomechanical Diagnostic Report")
            
            # Primary Metrics Row
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Peak Serve Speed", "118.4 mph", delta="+4.2 mph vs past avg")
            m2.metric("Spin Rate", "2,840 RPM", delta="Topspin-Kick Profile")
            m3.metric("Impact Height", "2.88 meters", delta="Optimal Apex Point")
            m4.metric("Kinetic Transfer", "88.2%", delta="Optimal Leg Drive")

            st.write("")
            
            # Interactive Biomechanics Data Charts
            t_col1, t_col2 = st.columns(2)
            
            with t_col1:
                st.markdown("#### 📐 Velocity & Angular Acceleration Curve")
                chart_data = pd.DataFrame({
                    "Serve Phase": ["Trophy Position", "Racket Drop", "Acceleration", "Ball Impact", "Follow Through"],
                    "Racket Speed (mph)": [12, 38, 92, 118, 45],
                    "Wrist Angular Speed (°/s)": [180, 420, 1100, 1450, 320]
                })
                st.line_chart(chart_data.set_index("Serve Phase"))

            with t_col2:
                st.markdown("#### 🎯 Impact Spot Radar & Accuracy Distribution")
                impact_data = pd.DataFrame({
                    "Court Zone": ["T-Point (Center)", "Body Serve", "Wide Angle"],
                    "Consistency %": [68, 84, 52],
                    "Avg Speed (mph)": [118, 112, 108]
                })
                st.bar_chart(impact_data.set_index("Court Zone"))

            st.markdown("#### 🔍 4-Phase Biomechanical Breakdown")
            
            tab_p1, tab_p2, tab_p3, tab_p4 = st.tabs(["Phase 1: Trophy Position", "Phase 2: Kinetic Chain", "Phase 3: Impact & Extension", "Phase 4: Pronation & Landing"])
            
            with tab_p1:
                st.markdown("""
                * **Shoulder Tilt Angle**: Measured at **28°** (Target Range: 25°-32°). Excellent shoulder alignment.
                * **Knee Flexion**: Flexion reached **115°** prior to vertical thrust. Great power storage.
                * **Toss Height & Position**: Ball toss apex is **0.15m inside baseline**, allowing optimal forward momentum transfer.
                """)
            with tab_p2:
                st.markdown("""
                * **Hip-to-Shoulder Separation**: Rotation gap measured at **34°** (High core torque creation).
                * **Racket Head Drop**: Maximum depth reached smoothly without hitch or pausing.
                """)
            with tab_p3:
                st.markdown("""
                * **Arm Extension at Contact**: **172°** arm-to-shoulder angle at impact frame (Maximum reaching power).
                * **Net Clearance Axis**: Ball path clears the net cord by **0.68m**, ensuring high margin for error.
                """)
            with tab_p4:
                st.markdown("""
                * **Internal Shoulder Rotation**: Forearm pronation rate measured at **1,450°/sec**.
                * **Non-Dominant Arm Re-coil**: Left arm tucks into abdomen cleanly to decelerate upper body rotation smoothly.
                """)

# --- MODULE 2: AI RACKET & STRING TENSION (GRAPHIC & SUGGESTION MATRIX) ---
def render_module_2():
    st.subheader("🎯 AI Racket & String Tension Recommendation Engine")
    st.write("Input your playstyle profile, injury history, and performance requirements to generate customized frame specs and string tension matrixes.")

    col1, col2 = st.columns(2)
    with col1:
        ntrp = st.slider("Your NTRP Skill Rating", 1.5, 7.0, 4.0, 0.5)
        serve_speed = st.number_input("Average First Serve Speed (mph)", 40, 140, 95)
        playstyle = st.selectbox("Primary Playstyle", ["Baseline Aggressor (Heavy Spin)", "All-Court Counterpuncher", "Touch & Net Specialist", "Power Serve & Volley"])
        matches_per_week = st.slider("Playing Frequency (Sessions / Week)", 1, 7, 3)

    with col2:
        elbow_issue = st.checkbox("Suffer from Tennis Elbow / Wrist Strain?")
        string_durability = st.select_slider("Main Priority", options=["Maximum Arm Comfort", "Balanced Feel & Control", "Maximum Spin & Durability"])
        racket_weight_pref = st.radio("Frame Weight Preference", ["Light & Maneuverable (<300g)", "Standard Tour Weight (300g-315g)", "Heavy Tour Weight (>315g)"])

    if st.button("Generate Detailed Setup & Tension Recommendations"):
        st.markdown("---")
        st.markdown("### 🛠️ Customized Equipment & Tension Specification")

        # Top Level Spec Summary Cards
        r1, r2, r3, r4 = st.columns(4)
        r1.metric("Recommended Head Size", "98 - 100 sq in")
        r2.metric("Target Frame Weight", "305 grams (Unstrung)")
        r3.metric("String Tension (Mains / Crosses)", "50 / 48 lbs" if elbow_issue else "54 / 52 lbs")
        r4.metric("String Material", "Multifilament / Gut" if elbow_issue else "Co-Poly Hybrid")

        st.write("")
        st.markdown("#### 📊 Tension & String Performance Dynamic Analysis")

        # Graphic Tension Matrix Simulation Chart
        tension_chart = pd.DataFrame({
            "Tension (Lbs)": [44, 48, 52, 56, 60],
            "Control & Precision Score": [55, 68, 82, 94, 98],
            "Trampoline Power & Depth": [96, 88, 74, 60, 48],
            "Dwell Time / Arm Comfort": [92, 85, 72, 58, 42]
        })
        st.line_chart(tension_chart.set_index("Tension (Lbs)"))

        st.markdown("#### 📝 Diagnostic Tension Suggestions & Tuning Guidelines")
        
        c_s1, c_s2 = st.columns(2)
        with c_s1:
            st.markdown("""
            **🧵 String Material & Main/Cross Differential:**
            * **Mains (Vertical Strings)**: String with **Co-Polymer (1.25mm / 16L Gauge)** for snapback and topspin generation.
            * **Crosses (Horizontal Strings)**: String with **Soft Multifilament** at **2 lbs lower** than the mains to widen the sweet spot and reduce arm shock.
            * **Recommended Tension Differential**: Maintaining a 2 lb drop on cross strings increases dwell time and sweet spot width by up to **14%**.
            """)
        with c_s2:
            st.markdown("""
            **☀️ Seasonal & Altitude Tension Adjustments:**
            * **Hot Summer Weather (>28°C)**: Increase string tension by **+2 lbs** (e.g., 54 lbs) as ball felt softens and expands.
            * **Cold Winter Weather (<10°C)**: Decrease string tension by **-2 lbs** (e.g., 50 lbs) to maintain arm comfort and depth.
            * **Restring Frequency Recommendation**: Restring your racket every **{0} months** based on your playing frequency.
            """.format(max(1, int(12 / matches_per_week))))

# --- MODULE 3: MEMBERSHIP & SUBSCRIPTIONS ---
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
        st.button("Current Base Plan", disabled=True, key="plan_free")

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

# --- MODULE 4: TOURNAMENTS & LODGING ---
def render_module_3():
    st.subheader("🏆 Global Tournaments, Lodging & Group Buying")

    selected_event = st.selectbox(
        "📍 Select Target Competition:",
        ["🇺🇸 US Open Championships (Flushing Meadows, NY)", "🇰🇷 Seoul Open Masters (Olympic Park, Korea)", "🇰🇷 Busan Clay Court Cup (Sajik Complex, Korea)"]
    )

    subpage = st.radio(
        "Select Pathway:",
        ["🖼️ Competition Infrastructure & Residence Gallery", "👥 Member Group Buying ($85 Discount)", "👤 Individual Registration & Checkout"],
        horizontal=True
    )

    st.markdown("---")

    if subpage == "🖼️ Competition Infrastructure & Residence Gallery":
        col_img1, col_img2 = st.columns(2)
        with col_img1:
            st.image("https://images.unsplash.com/photo-1595435934249-5df7ed86e1c0?w=800&q=80", caption="🏟️ Tournament Main Arena & Hard Courts", use_container_width=True)
        with col_img2:
            st.image("https://images.unsplash.com/photo-1566073771259-6a8506099945?w=800&q=80", caption="🏨 Official Partner Athlete Residence Suites", use_container_width=True)

    elif subpage == "👥 Member Group Buying ($85 Discount)":
        st.info("💡 Join 5+ athletes to unlock an instant $85/person discount on hotel and tournament packages!")
        votes = len(st.session_state["tournament_group_votes"])
        st.progress(min(votes / 5, 1.0))
        st.caption(f"Current Committed Members: **{votes}/5 Athletes Joined**")
        st.table(pd.DataFrame(st.session_state["tournament_group_votes"]))

    elif subpage == "👤 Individual Registration & Checkout":
        with st.form("indiv_tourn_form"):
            p_name = st.text_input("Player Full Name *", value=st.session_state["current_user"]["name"] if st.session_state["is_logged_in"] else "")
            p_passport = st.text_input("Passport / Gov ID *")
            card = st.text_input("Credit Card Number ($300 Standard Rate) *", type="password")
            if st.form_submit_button("Pay & Confirm Individual Booking ($300.00)"):
                if p_name and card:
                    st.success("🎉 Individual tournament entry and hotel package confirmed!")

# --- MODULE 5: ACADEMY & RESIDENCY ---
def render_module_4():
    st.subheader("🏛️ Global Tennis Academy & Residency Programs")
    
    subpage = st.radio("Select Section:", ["🏟️ Campus Gallery", "👥 Group Buying & Voting Hub", "👤 Individual Enrollment"], horizontal=True)
    st.markdown("---")

    if subpage == "🏟️ Campus Gallery":
        c1, c2 = st.columns(2)
        with c1:
            st.image("https://encrypted-tbn2.gstatic.com/licensed-image?q=tbn:ANd9GcTlJfjs63KI6QzSpQms4d1rLMcTNoDkcJphyH_y34zqGSvvZbGEs3TmtsDCJLVbWFcYD83uzV10B2lwUR0", caption="Center Court Facility", use_container_width=True)
        with c2:
            st.image("https://encrypted-tbn0.gstatic.com/licensed-image?q=tbn:ANd9GcRI-UXJPpwhWDcFekaYdcs5vb7ShKqOtbpAL6DUhV9W4HTMwQsFOzX3pKb9oNNCgU3VDScBATPtPN4KN5I", caption="Athlete Residence Lounge", use_container_width=True)

    elif subpage == "👥 Group Buying & Voting Hub":
        st.dataframe(pd.DataFrame(st.session_state["academy_group_votes"]))

    elif subpage == "👤 Individual Enrollment":
        with st.form("indiv_academy"):
            full_name = st.text_input("Full Name *", value=st.session_state["current_user"]["name"] if st.session_state["is_logged_in"] else "")
            card = st.text_input("Credit Card *", type="password")
            if st.form_submit_button("Enroll ($890)"):
                st.success("🎉 Enrollment Confirmed!")

# --- MODULE 6: MATCHMAKING & COACH DIRECTORY (WITH MEMBERSHIP VERIFICATION) ---
def render_module_5():
    st.subheader("🤝 Player Matchmaking & Coach Directory")
    st.write("Connect with local hitting partners or book certified tour coaches. Direct messaging requires an active **PRO Pass** or **VIP Gold** membership.")

    # -------------------------------------------------------------
    # 1. MEMBERSHIP VERIFICATION LOGIC
    # -------------------------------------------------------------
    is_logged = st.session_state.get("is_logged_in", False)
    user_tier = st.session_state.get("current_user", {}).get("tier", "Free Tier") if is_logged else "Guest"
    
    # Paid tiers authorized to chat
    has_chat_access = is_logged and user_tier in ["PRO Pass", "VIP Gold"]

    # Visual banner alerting unpaid/guest users
    if not has_chat_access:
        st.warning(
            f"🔒 **Membership Required:** You are currently on `{user_tier}`. "
            "Direct messaging with players and coaches is exclusive to **PRO Pass** and **VIP Gold** members."
        )

    st.markdown("---")
    t1, t2 = st.tabs(["🎾 Find Partners", "👨‍🏫 Certified Coaches"])

    # -------------------------------------------------------------
    # TAB 1: PLAYER MATCHMAKING
    # -------------------------------------------------------------
    with t1:
        st.markdown("#### 👥 Available Hitting Partners")
        
        for idx, player in enumerate(st.session_state["players_db"]):
            with st.expander(f"🎾 {player['Name']} — NTRP {player['NTRP']} ({player['City']})", expanded=True):
                col_info, col_action = st.columns([3, 1])
                
                with col_info:
                    st.write(f"**Style:** {player['Style']}")
                    st.write(f"**City:** {player['City']}")
                    st.write(f"**Contact:** `{player['Contact'] if has_chat_access else '••••••••@••••.org'}`")
                
                with col_action:
                    if has_chat_access:
                        if st.button("💬 Chat Now", key=f"chat_player_{idx}"):
                            st.success(f"Opening secure chat room with {player['Name']}...")
                    else:
                        st.button("🔒 Locked (Upgrade)", key=f"lock_player_{idx}", disabled=True)

    # -------------------------------------------------------------
    # TAB 2: COACH DIRECTORY
    # -------------------------------------------------------------
    with t2:
        st.markdown("#### 👨‍🏫 Certified Tour Coaches")
        
        for idx, coach in enumerate(st.session_state["coaches_db"]):
            with st.expander(f"🏆 {coach['Coach']} — {coach['Level']} ({coach['City']})", expanded=True):
                col_info, col_action = st.columns([3, 1])
                
                with col_info:
                    st.write(f"**Specialty:** {coach['Specialty']}")
                    st.write(f"**Rate:** {coach['Hourly']}")
                    st.write(f"**Location:** {coach['City']}")
                
                with col_action:
                    if has_chat_access:
                        if st.button("💬 Book & Chat", key=f"chat_coach_{idx}"):
                            st.success(f"Initiating private consultation with {coach['Coach']}...")
                    else:
                        st.button("🔒 Locked (Upgrade)", key=f"lock_coach_{idx}", disabled=True)

# --- MODULE 7: SUPPORT CENTER & TRANSACTION RECEIPTS (MULTILINGUAL) ---
def render_module_6():
    # Detect language (Defaults to EN if not set)
    lang = st.session_state.get("language", "EN")
    t = TEXTS.get(lang, TEXTS["EN"])

    st.subheader(t["title"])
    st.write(t["subtitle"])

    is_logged = st.session_state.get("is_logged_in", False)
    current_user = st.session_state.get("current_user") or {}

    tab_tickets, tab_receipts, tab_new_ticket = st.tabs([
        t["tab_tickets"], 
        t["tab_receipts"], 
        t["tab_new_ticket"]
    ])

    # -------------------------------------------------------------
    # TAB 1: SUPPORT TICKETS LIST
    # -------------------------------------------------------------
    with tab_tickets:
        st.markdown(f"#### {t['active_tickets']}")
        
        if not is_logged:
            st.info(t["login_info"])
        
        inquiries_df = pd.DataFrame(st.session_state.get("inquiries", []))
        st.dataframe(inquiries_df, width="stretch")

    # -------------------------------------------------------------
    # TAB 2: TRANSACTION RECEIPTS & INVOICE GENERATOR
    # -------------------------------------------------------------
    with tab_receipts:
        st.markdown(f"#### {t['billing_history']}")
        
        chat_orders = st.session_state.get("chat_orders", [])
        orders_df = pd.DataFrame(chat_orders)
        st.dataframe(orders_df, width="stretch")
        
        st.markdown("---")
        st.markdown(f"##### {t['generate_receipt']}")
        
        if chat_orders:
            order_ids = [order["Order ID"] for order in chat_orders]
            selected_order_id = st.selectbox(t["select_order"], order_ids)

            selected_order = next((item for item in chat_orders if item["Order ID"] == selected_order_id), None)

            if selected_order:
                with st.expander(f"🧾 Digital Invoice — {selected_order['Order ID']}", expanded=True):
                    c_a, c_b = st.columns(2)
                    with c_a:
                        st.markdown("**Global Tennis Academy & Tech Platform Inc.**")
                        st.caption("124 Olympic-ro, Songpa-gu, Seoul, South Korea")
                        st.write(f"**Billed To / 청구 대상:** {current_user.get('name', 'Guest Athlete')}")
                        st.write(f"**Email / 이메일:** {current_user.get('email', 'N/A')}")
                    
                    with c_b:
                        st.write(f"**Invoice No:** `{selected_order['Order ID']}`")
                        st.write(f"**Status:** `{selected_order['Status']}`")
                        st.write(f"**Payment Method:** Visa ending in •••• 4242")
                    
                    st.markdown("---")
                    st.markdown(f"""
                    | Item Description | Qty | Amount |
                    | :--- | :---: | :---: |
                    | **{selected_order['Item']}** | 1 | {selected_order['Amount']} |
                    | **VAT / Sales Tax (Included)** | - | $0.00 |
                    | **Total Paid** | | **{selected_order['Amount']}** |
                    """)

                    st.download_button(
                        label="📥 Download Receipt (TXT)",
                        data=f"INVOICE: {selected_order['Order ID']}\nItem: {selected_order['Item']}\nAmount: {selected_order['Amount']}\nStatus: {selected_order['Status']}",
                        file_name=f"Receipt_{selected_order['Order ID']}.txt",
                        mime="text/plain"
                    )
        else:
            st.info(t["no_orders"])

    # -------------------------------------------------------------
    # TAB 3: SUBMIT NEW INQUIRY
    # -------------------------------------------------------------
    with tab_new_ticket:
        st.markdown(f"#### {t['submit_ticket_hdr']}")
        
        with st.form("create_ticket_form"):
            t_category = st.selectbox(t["category"], [
                "Racket Stringing / Customization Order (라켓 스트링/커스텀)",
                "Academy Residency & Accommodations (아카데미 숙소/입소)",
                "AI Biomechanics / Video Analysis Help (AI 분석 문의)",
                "Membership & Billing Inquiry (멤버십 및 결제)",
                "Tournament Registration Issue (대회 참가 등록)"
            ])
            t_subject = st.text_input(t["subject"])
            t_details = st.text_area(t["details"])
            
            submit_ticket = st.form_submit_button(t["submit_btn"])

            if submit_ticket:
                if t_subject and t_details:
                    inquiries = st.session_state.setdefault("inquiries", [])
                    new_id = f"TK-{len(inquiries) + 1002}"
                    today_date = datetime.date.today().strftime("%Y-%m-%d")
                    
                    inquiries.append({
                        "Ticket ID": new_id,
                        "Subject": f"[{t_category}] {t_subject}",
                        "Status": "Open (In Review)" if lang == "EN" else "검토 중",
                        "Date": today_date
                    })
                    st.success(t["success_msg"].format(id=new_id))
                else:
                    st.error("Please fill out all required fields. / 모든 필수 항목을 작성해 주세요.")

# --- MODULE 8: ADMIN CONTROL PANEL ---
def render_module_7():
    st.subheader("🔒 Platform Admin Control Panel")
    if st.text_input("Passcode", type="password") == "admin":
        st.success("Access Granted")
        st.dataframe(pd.DataFrame.from_dict(st.session_state["registered_users"], orient='index'))

# --- MODULE 9: SINGLE DEDICATED CONTACT PAGE ---
def render_module_contact():
    st.markdown("""
        <div style="background-color:#FAF8F5; padding:28px; border-radius:12px; border:1px solid #E5E0D8; margin-bottom:24px;">
            <h2 style="margin-top:0;">📞 Contact Headquarters & Official Channels</h2>
            <p style="color:#5C544D; margin-bottom:0;">Have questions regarding academy admissions, tournament packages, or AI analysis services? Get in touch with our team directly.</p>
        </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🏢 Global Corporate Office")
        st.markdown("""
        * **Company Name**: Global Tennis Academy & Tech Platform Inc.
        * **HQ Address**: 124 Olympic-ro, Songpa-gu, Seoul, 05540, South Korea
        * **US Branch Office**: 120 Flushing Meadows Way, Queens, NY 11368, USA
        * **Telephone**: +82 2-555-1004 / +1 (800) 555-TENNIS
        * **Support Email**: `support@globaltennis.org`
        * **Admissions Email**: `admissions@globaltennis.org`
        * **Office Hours**: Monday – Friday: 09:00 – 18:00 KST / EST
        """)

    with col2:
        st.markdown("### 🌐 Connect On Social Media")
        st.markdown("Follow our official channels for tournament updates, student highlights, and AI biomechanics tips:")
        st.markdown("""
        <a href="https://youtube.com" target="_blank" class="social-btn">📺 YouTube Channel</a>
        <a href="https://instagram.com" target="_blank" class="social-btn">📸 Instagram (@GlobalTennisAI)</a>
        <a href="https://twitter.com" target="_blank" class="social-btn">🐦 X / Twitter</a>
        <a href="https://linkedin.com" target="_blank" class="social-btn">💼 LinkedIn Official</a>
        """, unsafe_allow_html=True)

# ==========================================
# 6. ROUTER LOGIC
# ==========================================
if menu == "⚡ 1. AI Serve Velocity & Biomechanics Analyzer":
    render_module_1()
elif menu == "🎯 2. AI Racket & String Tension Recommendation Engine":
    render_module_2()
elif menu == "💳 3. Membership & Subscriptions":
    render_module_membership()
elif menu == "🏆 4. Tournaments & Lodging (US Open / Korea)":
    render_module_3()
elif menu == "🏛️ 5. Residency & Academy Programs":
    render_module_4()
elif menu == "🤝 6. Matchmaking & Coach Directory":
    render_module_5()
elif menu == "🎧 7. Support & Ticket Receipts":
    render_module_6()
elif menu == "🔒 8. Admin Control Panel":
    render_module_7()
elif menu == "📞 9. Contact Us":
    render_module_contact()
