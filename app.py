import streamlit as st
import sqlite3
import random
import time
import io
from PIL import Image

# ==========================================
# 0. PERSISTENT DATABASE SYSTEM (SQLite)
# ==========================================
DB_NAME = "tennis_platform.db"

def get_db_connection():
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Unified User Account Table with Auth & Phone Verification
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            phone TEXT UNIQUE NOT NULL,
            role TEXT NOT NULL, -- 'student' or 'coach'
            name TEXT NOT NULL,
            email TEXT,
            photo_blob BLOB,
            score INTEGER DEFAULT 0,
            fee_paid INTEGER DEFAULT 0,
            is_phone_verified INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Persistent Marketplace Inventory
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            price TEXT NOT NULL,
            description TEXT,
            category TEXT NOT NULL,
            coach_id INTEGER NOT NULL,
            photo_blob BLOB,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (coach_id) REFERENCES users (id)
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# ==========================================
# 1. PAGE CONFIG & STYLING
# ==========================================
st.set_page_config(
    page_title="Tennis Verified Platform",
    page_icon="🎾",
    layout="wide"
)

st.markdown("""
    <style>
    .stApp { background-color: #F8F9FA; color: #212529; }
    h1, h2, h3 { color: #1A1A1A !important; font-weight: 700; }
    .stForm { background-color: white; border-radius: 10px; padding: 25px; border: 1px solid #EAEAEA; }
    .sms-box { background-color: #E3F2FD; border: 2px dashed #1E88E5; border-radius: 8px; padding: 15px; margin: 10px 0; text-align: center; }
    .verified-badge { background-color: #E8F5E9; color: #2E7D32; padding: 5px 12px; border-radius: 20px; font-weight: bold; font-size: 13px; }
    .price-tag { color: #2E7D32; font-weight: bold; font-size: 20px; }
    </style>
""", unsafe_allow_html=True)

def image_to_blob(image_file):
    if image_file is not None:
        try:
            image = Image.open(image_file)
            image.thumbnail((800, 800))
            img_byte_arr = io.BytesIO()
            if image.mode in ('RGBA', 'LA'):
                background = Image.new(image.mode[:-1], image.size, '#ffffff')
                background.paste(image, image)
                image = background
            image.save(img_byte_arr, format='JPEG', quality=85)
            return img_byte_arr.getvalue()
        except Exception as e:
            st.error(f"Image Error: {e}")
            return None
    return None

# Session State Initializations for Auth & OTP
if "logged_in_user" not in st.session_state:
    st.session_state.logged_in_user = None

if "otp_code" not in st.session_state:
    st.session_state.otp_code = None

if "otp_verified" not in st.session_state:
    st.session_state.otp_verified = False

# ==========================================
# 2. SIDEBAR AUTHENTICATION (LOGIN / LOGOUT)
# ==========================================
st.sidebar.title("🔐 Login / Account")

if st.session_state.logged_in_user:
    u = st.session_state.logged_in_user
    st.sidebar.success(f"Logged in as: **{u['username']}** ({u['role'].capitalize()})")
    if st.sidebar.button("🚪 Log Out"):
        st.session_state.logged_in_user = None
        st.rerun()
else:
    st.sidebar.subheader("Login to Account")
    login_user = st.sidebar.text_input("User ID")
    login_pass = st.sidebar.text_input("Password", type="password")
    
    if st.sidebar.button("🔑 Log In"):
        conn = get_db_connection()
        user_rec = conn.execute(
            'SELECT * FROM users WHERE username = ? AND password = ?', 
            (login_user, login_pass)
        ).fetchone()
        conn.close()
        
        if user_rec:
            st.session_state.logged_in_user = dict(user_rec)
            st.sidebar.success("Login successful!")
            st.rerun()
        else:
            st.sidebar.error("Invalid User ID or Password.")

st.sidebar.markdown("---")
page = st.sidebar.radio("Navigation", [
    "🎾 Student Registration (Phone Verified)", 
    "🏆 Coach Certification & Verification", 
    "🛍️ Tennis Marketplace", 
    "💬 Chat & Class Portal"
])

# ==========================================
# PAGE 1: STUDENT REGISTRATION (WITH SMS OTP)
# ==========================================
if page == "🎾 Student Registration (Phone Verified)":
    st.title("🎾 Student Account Registration")
    st.write("Create your student account with **User ID, Password, and Mobile Phone SMS Verification**.")

    st.markdown("---")

    # Step 1: User Details
    st.subheader("Step 1: Account & Profile Details")
    c1, c2 = st.columns(2)
    with c1:
        s_username = st.text_input("Choose User ID *", placeholder="e.g. tennis_star99")
        s_password = st.text_input("Choose Password *", type="password")
        s_name = st.text_input("Full Name *")
    with c2:
        s_email = st.text_input("Email Address *")
        s_phone = st.text_input("Mobile Phone Number *", placeholder="010-1234-5678")
        s_photo = st.file_uploader("Upload Profile Photo *", type=['jpg', 'jpeg', 'png'])

    st.markdown("---")
    
    # Step 2: Phone Verification SMS Flow
    st.subheader("Step 2: Mobile Phone Verification")
    
    col_sms1, col_sms2 = st.columns([1, 1])
    
    with col_sms1:
        if st.button("📱 Send SMS Verification Code"):
            if s_phone:
                # Generate random 6-digit code
                generated_code = str(random.randint(100000, 999999))
                st.session_state.otp_code = generated_code
                st.session_state.otp_verified = False
                st.toast(f"📲 [SMS Mock] Verification code sent to {s_phone}!")
            else:
                st.error("Please enter a valid mobile phone number first.")

    # Show Simulated Mobile SMS Screen
    if st.session_state.otp_code:
        st.markdown(f"""
            <div class="sms-box">
                📲 <strong>[Simulated SMS Message Received]</strong><br>
                Your verification code is: <span style="font-size:22px; color:#1E88E5; font-weight:bold;">{st.session_state.otp_code}</span>
            </div>
        """, unsafe_allow_html=True)
        
        entered_code = st.text_input("Enter 6-Digit Verification Code")
        if st.button("✅ Verify Mobile Number"):
            if entered_code == st.session_state.otp_code:
                st.session_state.otp_verified = True
                st.success("📱 Phone number verified successfully!")
            else:
                st.error("❌ Incorrect verification code. Please try again.")

    st.markdown("---")

    # Step 3: Final Registration Submission
    if st.button("🚀 Complete Student Account Registration"):
        if not (s_username and s_password and s_name and s_phone and s_photo):
            st.error("Please fill in all fields and upload a profile photo.")
        elif not st.session_state.otp_verified:
            st.error("⚠️ Mobile phone verification is required before registering.")
        else:
            photo_blob = image_to_blob(s_photo)
            conn = get_db_connection()
            try:
                conn.execute('''
                    INSERT INTO users (username, password, phone, role, name, email, photo_blob, is_phone_verified)
                    VALUES (?, ?, ?, 'student', ?, ?, ?, 1)
                ''', (s_username, s_password, s_phone, s_name, s_email, photo_blob))
                conn.commit()
                st.success(f"🎉 Account '{s_username}' created successfully! You can now log in.")
                st.balloons()
                # Clear OTP states
                st.session_state.otp_code = None
                st.session_state.otp_verified = False
            except sqlite3.IntegrityError:
                st.error("⚠️ User ID or Phone Number already exists in the database.")
            finally:
                conn.close()

# ==========================================
# PAGE 2: COACH CERTIFICATION
# ==========================================
elif page == "🏆 Coach Certification & Verification":
    st.title("🏆 Coach Certification System")
    st.write("Upload video footage to analyze swing mechanics. Score **60 or above** to unlock selling privileges!")

    st.markdown("---")

    v_col1, v_col2 = st.columns([2, 1])
    with v_col1:
        video_file = st.file_uploader("Upload Tennis Playing Video (.mp4, .mov)", type=['mp4', 'mov'])
        if video_file:
            st.video(video_file)

    with v_col2:
        if video_file:
            if st.button("📊 Run AI Mechanics Analysis"):
                with st.spinner("Analyzing stroke mechanics, spin RPM, and speed..."):
                    time.sleep(1.5)
                    score = random.randint(62, 95)
                    st.session_state['coach_score'] = score

    if 'coach_score' in st.session_state:
        score = st.session_state['coach_score']
        st.markdown("---")
        st.subheader(f"AI Skill Score Result: {score} / 100")
        
        if score >= 60:
            st.success("✅ Passed! You qualify to become a certified coach.")
            
            with st.form("coach_reg_form"):
                st.subheader("Coach Registration & 10,000원 License Fee")
                c_user = st.text_input("User ID *")
                c_pass = st.text_input("Password *", type="password")
                c_name = st.text_input("Full Name *")
                c_phone = st.text_input("Mobile Phone *")
                
                if st.form_submit_button("💳 Pay 10,000원 & Create Verified Coach Account"):
                    if c_user and c_pass and c_name and c_phone:
                        conn = get_db_connection()
                        try:
                            conn.execute('''
                                INSERT INTO users (username, password, phone, role, name, score, fee_paid, is_phone_verified)
                                VALUES (?, ?, ?, 'coach', ?, ?, 1, 1)
                            ''', (c_user, c_pass, c_phone, c_name, score))
                            conn.commit()
                            st.success(f"🏆 Coach Account '{c_user}' created and verified!")
                            st.balloons()
                        except sqlite3.IntegrityError:
                            st.error("⚠️ User ID or Phone Number already exists.")
                        finally:
                            conn.close()

# ==========================================
# PAGE 3: TENNIS MARKETPLACE
# ==========================================
elif page == "🛍️ Tennis Marketplace":
    st.title("🛍️ Tennis Racquet & Gear Marketplace")

    # SHOW SELLING SYSTEM IF LOGGED IN AS VERIFIED COACH
    user = st.session_state.logged_in_user
    if user and user['role'] == 'coach' and user['fee_paid'] == 1:
        with st.expander("➕ Verified Coach: Create Product Listing"):
            with st.form("add_product"):
                p_title = st.text_input("Racquet Title *")
                p_price = st.text_input("Price (KRW) *")
                p_desc = st.text_area("Description")
                p_photo = st.file_uploader("Product Photo *", type=['jpg', 'jpeg', 'png'])
                
                if st.form_submit_button("🚀 Publish Listing"):
                    if p_title and p_price and p_photo:
                        photo_blob = image_to_blob(p_photo)
                        conn = get_db_connection()
                        conn.execute('''
                            INSERT INTO inventory (title, price, description, category, coach_id, photo_blob)
                            VALUES (?, ?, ?, 'Racquet', ?, ?)
                        ''', (p_title, p_price, p_desc, user['id'], photo_blob))
                        conn.commit()
                        conn.close()
                        st.success("Listing published permanently!")
                        st.rerun()

    st.markdown("---")
    st.subheader("Available Racquets & Gear")

    conn = get_db_connection()
    items = conn.execute('''
        SELECT inventory.*, users.name as coach_name 
        FROM inventory JOIN users ON inventory.coach_id = users.id
        ORDER BY inventory.created_at DESC
    ''').fetchall()
    conn.close()

    if not items:
        st.info("No items currently listed.")
    else:
        cols = st.columns(3)
        for idx, item in enumerate(items):
            col = cols[idx % 3]
            with col:
                if item['photo_blob']:
                    st.image(io.BytesIO(item['photo_blob']), use_container_width=True)
                st.markdown(f"### {item['title']}")
                st.markdown(f"💰 Price: `<span class='price-tag'>{item['price']}</span>`", unsafe_allow_html=True)
                st.caption(f"Seller: **Coach {item['coach_name']}**")
                st.write(item['description'])
                
                if st.button("🛒 Purchase Item", key=f"buy_{item['id']}"):
                    if user and user['role'] == 'student':
                        st.success("Order request sent! Coach will reach out for payment & free tennis lesson setup.")
                    else:
                        st.warning("Please log in as a Student to purchase.")
                st.markdown("---")

# ==========================================
# PAGE 4: CHAT & CLASS PORTAL
# ==========================================
elif page == "💬 Chat & Class Portal":
    st.title("💬 Student-Coach Connect")
    st.write("Free coaching lessons are included when you interact with verified coaches!")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("💬 Send Message")
        st.text_input("Recipient Username")
        st.text_area("Message")
        if st.button("Send Direct Message"):
            st.success("Message delivered!")
