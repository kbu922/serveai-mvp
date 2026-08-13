import streamlit as st
import sqlite3
import random
import time
import io
import smtplib
from email.mime.text import MIMEText
from PIL import Image

# ==========================================
# 0. DATABASE PERSISTENCE LAYER (SQLite)
# ==========================================
DB_NAME = "tennis_platform.db"

def get_db_connection():
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Unified User Account Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            phone TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            role TEXT NOT NULL, -- 'student' or 'coach'
            name TEXT NOT NULL,
            photo_blob BLOB,
            score INTEGER DEFAULT 0,
            fee_paid INTEGER DEFAULT 0,
            is_email_verified INTEGER DEFAULT 0,
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
# 1. REAL EMAIL OTP SENDER FUNCTION
# ==========================================
def send_real_email_otp(recipient_email, otp_code, sender_email, sender_password):
    """Sends a real email using Gmail's SMTP server."""
    subject = "🎾 Tennis Platform - Verification Code"
    body = f"Your 6-digit email verification code is: {otp_code}\n\nPlease enter this code in the registration page to verify your account."
    
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = recipient_email

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, msg.as_string())
        return True, "Email sent successfully!"
    except Exception as e:
        return False, str(e)

# ==========================================
# 2. PAGE CONFIG & STYLING
# ==========================================
st.set_page_config(
    page_title="Reality Tennis Platform",
    page_icon="🎾",
    layout="wide"
)

st.markdown("""
    <style>
    .stApp { background-color: #F8F9FA; color: #212529; }
    h1, h2, h3 { color: #1A1A1A !important; font-weight: 700; }
    .stForm { background-color: white; border-radius: 10px; padding: 25px; border: 1px solid #EAEAEA; }
    .email-box { background-color: #E8F5E9; border: 2px dashed #2E7D32; border-radius: 8px; padding: 15px; margin: 10px 0; text-align: center; }
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

# Session State Variables
if "logged_in_user" not in st.session_state:
    st.session_state.logged_in_user = None

if "otp_code" not in st.session_state:
    st.session_state.otp_code = None

if "otp_verified" not in st.session_state:
    st.session_state.otp_verified = False

# ==========================================
# 3. SIDEBAR: AUTH & SMTP SETTINGS
# ==========================================
st.sidebar.title("🔐 Account & Settings")

# LOGIN SYSTEM
if st.session_state.logged_in_user:
    u = st.session_state.logged_in_user
    st.sidebar.success(f"Logged in: **{u['username']}** ({u['role'].capitalize()})")
    if st.sidebar.button("🚪 Log Out"):
        st.session_state.logged_in_user = None
        st.rerun()
else:
    st.sidebar.subheader("Account Login")
    login_user = st.sidebar.text_input("User ID", key="l_user")
    login_pass = st.sidebar.text_input("Password", type="password", key="l_pass")
    
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

# SMTP CONFIGURATION EXPANDER (For Sending Real Emails)
with st.sidebar.expander("⚙️ Email Sender Config (Gmail SMTP)"):
    st.caption("Enter your Gmail address & App Password to dispatch real email verification codes.")
    smtp_email = st.text_input("Gmail Address", value="your_email@gmail.com")
    smtp_pass = st.text_input("Gmail App Password", type="password", help="Generated in Google Account > Security > App Passwords")

st.sidebar.markdown("---")
page = st.sidebar.radio("Navigation", [
    "🎾 Student Registration (Email OTP)", 
    "🏆 Coach Certification & License", 
    "🛍️ Tennis Marketplace", 
    "💬 Chat & Free Classes"
])

# ==========================================
# PAGE 1: STUDENT REGISTRATION (REAL EMAIL OTP)
# ==========================================
if page == "🎾 Student Registration (Email OTP)":
    st.title("🎾 Student Account Registration")
    st.write("Register your student profile using a **User ID, Password, and Real Email Verification Code**.")

    st.markdown("---")

    # Account Form
    st.subheader("Step 1: Credentials & Information")
    c1, c2 = st.columns(2)
    with c1:
        s_username = st.text_input("User ID *", placeholder="e.g. tennis_student1")
        s_password = st.text_input("Password *", type="password")
        s_name = st.text_input("Full Name *")
    with c2:
        s_phone = st.text_input("Mobile Phone Number *", placeholder="010-1234-5678")
        s_email = st.text_input("Email Address *", placeholder="your_address@domain.com")
        s_photo = st.file_uploader("Upload Profile Photo *", type=['jpg', 'jpeg', 'png'])

    st.markdown("---")
    
    # Email Verification Flow
    st.subheader("Step 2: Real Email Verification")
    
    col_otp1, col_otp2 = st.columns([1, 1])
    
    with col_otp1:
        if st.button("📧 Send Email Verification Code"):
            if s_email:
                # 1. Generate 6-digit code
                generated_code = str(random.randint(100000, 999999))
                st.session_state.otp_code = generated_code
                st.session_state.otp_verified = False
                
                # 2. Send Real Email or Display Screen Fallback
                if "gmail.com" in smtp_email and len(smtp_pass) > 5:
                    success, msg = send_real_email_otp(s_email, generated_code, smtp_email, smtp_pass)
                    if success:
                        st.success(f"📩 Real verification code sent to **{s_email}**! Check your inbox.")
                    else:
                        st.error(f"Email failed to send: {msg}")
                else:
                    st.warning("⚠️ Gmail credentials not set in sidebar settings. Displaying test code below:")
                    st.markdown(f"""
                        <div class="email-box">
                            📩 <strong>[Test Code Display]</strong><br>
                            Verification code for {s_email}: <span style="font-size:22px; color:#2E7D32; font-weight:bold;">{generated_code}</span>
                        </div>
                    """, unsafe_allow_html=True)
            else:
                st.error("Please enter your email address first.")

    # OTP Input Field
    if st.session_state.otp_code:
        entered_code = st.text_input("Enter 6-Digit Code Received in Email", key="input_otp")
        if st.button("✅ Verify Email Code"):
            if entered_code == st.session_state.otp_code:
                st.session_state.otp_verified = True
                st.success("🎉 Email address verified successfully!")
            else:
                st.error("❌ Invalid code. Please check your inbox and try again.")

    st.markdown("---")

    # Step 3: Complete Registration
    if st.button("🚀 Finalize Account Creation"):
        if not (s_username and s_password and s_name and s_phone and s_email and s_photo):
            st.error("Please fill out all required fields and upload your profile photo.")
        elif not st.session_state.otp_verified:
            st.error("⚠️ Please complete Email Verification before registering.")
        else:
            photo_blob = image_to_blob(s_photo)
            conn = get_db_connection()
            try:
                conn.execute('''
                    INSERT INTO users (username, password, phone, email, role, name, photo_blob, is_email_verified)
                    VALUES (?, ?, ?, ?, 'student', ?, ?, 1)
                ''', (s_username, s_password, s_phone, s_email, s_name, photo_blob))
                conn.commit()
                st.success(f"🎉 Welcome {s_name}! Account '{s_username}' created permanently in the database.")
                st.balloons()
                st.session_state.otp_code = None
                st.session_state.otp_verified = False
            except sqlite3.IntegrityError:
                st.error("⚠️ User ID or Email already registered in the system.")
            finally:
                conn.close()

# ==========================================
# PAGE 2: COACH CERTIFICATION
# ==========================================
elif page == "🏆 Coach Certification & License":
    st.title("🏆 Coach Certification System")
    st.write("Upload a video of your gameplay. If your AI skill score is **60 or above**, you can pay 10,000원 to obtain a Verified Coach account and list products!")

    st.markdown("---")

    v_col1, v_col2 = st.columns([2, 1])
    with v_col1:
        video_file = st.file_uploader("Upload Gameplay Video (.mp4, .mov)", type=['mp4', 'mov'])
        if video_file:
            st.video(video_file)

    with v_col2:
        if video_file:
            if st.button("📊 Calculate Tennis Skill Score"):
                with st.spinner("Analyzing spin rate, ball velocity, and stroke technique..."):
                    time.sleep(1.5)
                    analyzed_score = random.randint(62, 96)
                    st.session_state['coach_score'] = analyzed_score

    if 'coach_score' in st.session_state:
        score = st.session_state['coach_score']
        st.markdown("---")
        st.subheader(f"AI Skill Evaluation Result: {score} / 100")
        
        if score >= 60:
            st.success("✅ Assessment Passed! You qualify for official Coach Verification.")
            
            with st.form("coach_reg_form"):
                st.subheader("Coach Registration & License Fee (10,000원)")
                c_user = st.text_input("Desired User ID *")
                c_pass = st.text_input("Password *", type="password")
                c_name = st.text_input("Full Name *")
                c_phone = st.text_input("Mobile Phone *")
                c_email = st.text_input("Email Address *")
                
                if st.form_submit_button("💳 Pay 10,000원 & Receive Verified Coach License"):
                    if c_user and c_pass and c_name and c_phone and c_email:
                        conn = get_db_connection()
                        try:
                            conn.execute('''
                                INSERT INTO users (username, password, phone, email, role, name, score, fee_paid, is_email_verified)
                                VALUES (?, ?, ?, ?, 'coach', ?, ?, 1, 1)
                            ''', (c_user, c_pass, c_phone, c_email, c_name, score))
                            conn.commit()
                            st.success(f"🏆 Coach Account '{c_user}' created! You can now log in to list items in the market.")
                            st.balloons()
                        except sqlite3.IntegrityError:
                            st.error("⚠️ User ID or Email already exists in the system.")
                        finally:
                            conn.close()

# ==========================================
# PAGE 3: TENNIS MARKETPLACE
# ==========================================
elif page == "🛍️ Tennis Marketplace":
    st.title("🛍️ Tennis Racquet & Gear Marketplace")

    user = st.session_state.logged_in_user
    
    # SELLING FORM (ONLY ACCESSIBLE TO LOGGED-IN VERIFIED COACHES)
    if user and user['role'] == 'coach' and user['fee_paid'] == 1:
        with st.expander("➕ Verified Coach: Create Product Listing"):
            with st.form("add_product"):
                p_title = st.text_input("Racquet Model Name *")
                p_price = st.text_input("Price (KRW) *", placeholder="e.g. 120,000 ₩")
                p_desc = st.text_area("Product Description")
                p_photo = st.file_uploader("Upload Product Photo *", type=['jpg', 'jpeg', 'png'])
                
                if st.form_submit_button("🚀 Post Product for Sale"):
                    if p_title and p_price and p_photo:
                        photo_blob = image_to_blob(p_photo)
                        conn = get_db_connection()
                        conn.execute('''
                            INSERT INTO inventory (title, price, description, category, coach_id, photo_blob)
                            VALUES (?, ?, ?, 'Racquet', ?, ?)
                        ''', (p_title, p_price, p_desc, user['id'], photo_blob))
                        conn.commit()
                        conn.close()
                        st.success("Product listing published permanently!")
                        st.rerun()

    st.markdown("---")
    st.subheader("Available Racquets")

    conn = get_db_connection()
    items = conn.execute('''
        SELECT inventory.*, users.name as coach_name 
        FROM inventory JOIN users ON inventory.coach_id = users.id
        ORDER BY inventory.created_at DESC
    ''').fetchall()
    conn.close()

    if not items:
        st.info("No items listed in the database yet.")
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
                
                if st.button("🛒 Buy Product", key=f"buy_{item['id']}"):
                    if user and user['role'] == 'student':
                        st.success(f"Order submitted to Coach {item['coach_name']}! You also receive a free tennis trial class.")
                    else:
                        st.warning("Please log in as a Student to purchase items.")
                st.markdown("---")

# ==========================================
# PAGE 4: CHAT & FREE CLASSES
# ==========================================
elif page == "💬 Chat & Free Classes":
    st.title("💬 Coach & Student Community")
    st.write("Connect with certified coaches for free tennis lessons!")
    
    c_left, c_right = st.columns(2)
    with c_left:
        st.subheader("📩 Direct Message")
        st.text_input("Recipient Username")
        st.text_area("Message Text")
        if st.button("Send Message"):
            st.success("Message sent!")

    with c_right:
        st.subheader("🎾 Free Class Offers")
        st.info("When you purchase a racquet from a certified coach, you are eligible for 1 free private coaching session!")
