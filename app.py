import streamlit as st
import pandas as pd
import datetime
import time

# ==========================================
# 1. PAGE CONFIG (MUST BE THE FIRST STREAMLIT CALL)
# ==========================================
st.set_page_config(
    page_title="Global Tennis Platform & AI Suite",
    page_icon="🎾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# 2. TRANSLATION DICTIONARY & HELPER
# ==========================================
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
    lang_code = "KR" if lang == "한국어" else "EN"
    return TEXTS.get(lang_code, TEXTS["EN"]).get(key, key)


# ==========================================
# 3. LUXURY SAND THEME STYLING
# ==========================================
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
# 4. STATE INITIALIZATION & AUTH SYSTEM
# ==========================================
if "language" not in st.session_state:
    st.session_state["language"] = "English"

if "registered_users" not in st.session_state:
    st.session_state["registered_users"] = {
        "alex@tennis.org": {"password": "password123", "name": "Alex Mercer", "tier": "PRO Pass", "ntrp": 4.5},
        "sarah@tennis.org": {"password": "password123", "name": "Sarah Kim", "tier": "VIP Gold", "ntrp": 5.0}
    }

if "is_logged_in" not in st.session_state:
    st.session_state["is_logged_in"] = False

if "current_user" not in st.session_state:
    st.session_state["current_user"] = None

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
        {"Coach": "Coach Rob", "Level": "USPTR Certified Master", "City": "Seoul", "Hourly": "$80/hr", "Specialty": "Serve Biomechanics", "Contact": "rob@tennis.org"},
        {"Coach": "Coach Sarah", "Level": "Ex-WTA Tour Player", "City": "Incheon", "Hourly": "$120/hr", "Specialty": "Match Strategy", "Contact": "sarah.c@tennis.org"},
        {"Coach": "Coach Min-ho", "Level": "KTA High Performance", "City": "Busan", "Hourly": "$95/hr", "Specialty": "Junior Development", "Contact": "minho@tennis.kr"}
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
# 5. SIDEBAR AUTH & NAVIGATION PANEL
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
# 6. TOP NAVIGATION HEADER
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
# 7. MODULE FUNCTIONS
# ==========================================

# --- MODULE 1: AI SERVE VELOCITY ---
def render_module_1():
    st.subheader("⚡ AI Serve Velocity & Biomechanics Analyzer")
    st.write("Upload high-speed footage to run computer-vision motion vector tracking, shoulder axis analysis, and kinetic chain evaluation.")

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
            time.sleep(1.5)
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

# --- MODULE 2: AI RACKET & STRING TENSION ---
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
            st.markdown(f"""
            **☀️ Seasonal & Altitude Tension Adjustments:**
            * **Hot Summer Weather (>28°C)**: Increase string tension by **+2 lbs** (e.g., 54 lbs) as ball felt softens and expands.
            * **Cold Winter Weather (<10°C)**: Decrease string tension by **-2 lbs** (e.g., 50 lbs) to maintain arm comfort and depth.
            * **Restring Frequency Recommendation**: Restring your racket every **{max(1, int(12 / matches_per_week))} months** based on your playing frequency.
            """)

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
            st.image("https://images.unsplash.com/photo-1595435934249-5df7ed86e1c0?w=800&q=80", caption="Center Court Facility", use_container_width=True)
        with c2:
            st.image("https://images.unsplash.com/photo-1566073771259-6a8506099945?w=800&q=80", caption="Athlete Residence Lounge", use_container_width=True)

    elif subpage == "👥 Group Buying & Voting Hub":
        st.dataframe(pd.DataFrame(st.session_state["academy_group_votes"]))

    elif subpage == "👤 Individual Enrollment":
        with st.form("indiv_academy"):
            full_name = st.text_input("Full Name *", value=st.session_state["current_user"]["name"] if st.session_state["is_logged_in"] else "")
            card = st.text_input("Credit Card *", type="password")
            if st.form_submit_button("Enroll ($890)"):
                st.success("🎉 Enrollment Confirmed!")

# --- MODULE 6: MATCHMAKING & COACH DIRECTORY ---
def render_module_5():
    st.subheader("🤝 Player Matchmaking & Coach Directory")
    st.write("Connect with local hitting partners or book certified tour coaches. Direct messaging requires an active **PRO Pass** or **VIP Gold** membership.")

    is_logged = st.session_state.get("is_logged_in", False)
    user_tier = st.session_state.get("current_user", {}).get("tier", "Free Tier") if is_logged else "Guest"
    
    has_chat_access = is_logged and user_tier in ["PRO Pass", "VIP Gold"]

    if not has_chat_access:
        st.warning(
            f"🔒 **Membership Required:** You are currently on `{user_tier}`. "
            "Direct messaging with players and coaches is exclusive to **PRO Pass** and **VIP Gold** members."
        )

    st.markdown("---")
    t1, t2 = st.tabs(["🎾 Find Partners", "👨‍🏫 Certified Coaches"])

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

    with t2:
        st.markdown("#### 👨‍🏫 Certified Tour Coaches")
        
        for idx, coach in enumerate(st.session_state["coaches_db"]):
            with st.expander(f"🏆 {coach['Coach']} — {coach['Level']} ({coach['City']})", expanded=True):
                col_info, col_action = st.columns([3, 1])
                
                with col_info:
                    st.write(f"**Specialty:** {coach['Specialty']}")
                    st.write(f"**Hourly Rate:** {coach['Hourly']}")
                    st.write(f"**Contact:** `{coach['Contact'] if has_chat_access else '••••••••@••••.org'}`")
                
                with col_action:
                    if has_chat_access:
                        if st.button("📅 Book Session", key=f"book_coach_{idx}"):
                            st.success(f"Booking request sent to {coach['Coach']}!")
                    else:
                        st.button("🔒 Locked (Upgrade)", key=f"lock_coach_{idx}", disabled=True)

# --- MODULE 7: SUPPORT & RECEIPTS ---
def render_module_6():
    lang = st.session_state.get("language", "English")
    st.subheader(get_text("title", lang))
    st.write(get_text("subtitle", lang))
    st.markdown("---")

    tab1, tab2, tab3 = st.tabs([
        get_text("tab_tickets", lang),
        get_text("tab_receipts", lang),
        get_text("tab_new_ticket", lang)
    ])

    with tab1:
        st.markdown(f"#### {get_text('active_tickets', lang)}")
        if not st.session_state["is_logged_in"]:
            st.info(get_text("login_info", lang))
        st.table(pd.DataFrame(st.session_state["inquiries"]))

    with tab2:
        st.markdown(f"#### {get_text('billing_history', lang)}")
        if st.session_state["chat_orders"]:
            df_orders = pd.DataFrame(st.session_state["chat_orders"])
            st.dataframe(df_orders, use_container_width=True)
            
            st.markdown("---")
            st.markdown(f"#### {get_text('generate_receipt', lang)}")
            selected_order_id = st.selectbox(get_text("select_order", lang), df_orders["Order ID"].tolist())
            
            if st.button("Generate Tax Invoice PDF"):
                order_detail = df_orders[df_orders["Order ID"] == selected_order_id].iloc[0]
                st.success(f"Generated official invoice for **{order_detail['Order ID']}** ({order_detail['Item']} - {order_detail['Amount']})")
        else:
            st.write(get_text("no_orders", lang))

    with tab3:
        st.markdown(f"#### {get_text('submit_ticket_hdr', lang)}")
        with st.form("support_ticket_form"):
            cat = st.selectbox(get_text("category", lang), ["Billing & Subscriptions", "Racket & Equipment Service", "Tournament Lodging", "General Inquiry"])
            subj = st.text_input(get_text("subject", lang))
            det = st.text_area(get_text("details", lang))
            
            if st.form_submit_button(get_text("submit_btn", lang)):
                if subj and det:
                    new_id = f"TK-{len(st.session_state['inquiries'])+1002}"
                    st.session_state["inquiries"].append({
                        "Ticket ID": new_id,
                        "Subject": subj,
                        "Status": "Open",
                        "Date": str(datetime.date.today())
                    })
                    msg = get_text("success_msg", lang).format(id=new_id)
                    st.success(msg)
                else:
                    st.error("Please complete all required fields.")

# --- MODULE 8: ADMIN CONTROL PANEL ---
def render_module_admin():
    st.subheader("🔒 Platform Administration Panel")
    
    if not st.session_state["is_logged_in"] or st.session_state["current_user"]["tier"] != "VIP Gold":
        st.error("⛔ Access Restricted: Admin credentials or VIP Gold management status required.")
        return

    st.success("Authorized Administrator Access Level 1")
    
    st.markdown("#### 👥 Registered User Management")
    st.json(st.session_state["registered_users"])
    
    st.markdown("#### 🧾 Global Transaction Logs")
    st.dataframe(pd.DataFrame(st.session_state["chat_orders"]))

# --- MODULE 9: CONTACT US ---
def render_module_contact():
    st.subheader("📞 Contact Global Tennis Platform")
    st.write("Have questions? Reach out directly to our operations team or headquarters.")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        **📍 Headquarters:**
        Global Tennis Center, Olympic Park
        Seoul, South Korea

        **📧 Email Direct:**
        support@globaltennis.org

        **📞 Phone:**
        +82 (02) 555-8921
        """)
    
    with col2:
        with st.form("contact_direct_form"):
            st.text_input("Your Name")
            st.text_input("Your Email")
            st.text_area("Message")
            if st.form_submit_button("Send Direct Message"):
                st.success("Message sent! Our team will get back to you shortly.")

# ==========================================
# 8. MAIN ROUTER
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
    render_module_admin()
elif menu == "📞 9. Contact Us":
    render_module_contact()
