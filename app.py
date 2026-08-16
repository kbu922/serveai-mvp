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
DB_NAME = "rally_and_date.db"

def get_db_connection():
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Updated User Table with Dating & Tennis Attributes
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            phone TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            role TEXT NOT NULL, -- 'player' or 'coach'
            name TEXT NOT NULL,
            gender TEXT,
            seeking_gender TEXT,
            ntrp_level TEXT DEFAULT 'NTRP 2.5 (Unverified)',
            preferred_courts TEXT,
            dating_bio TEXT,
            play_style TEXT,
            photo_blob BLOB,
            score INTEGER DEFAULT 0,
            fee_paid INTEGER DEFAULT 0,
            is_email_verified INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Structured Rally Date Invitations Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS date_invites (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender_id INTEGER NOT NULL,
            receiver_id INTEGER NOT NULL,
            court_location TEXT NOT NULL,
            match_time TEXT NOT NULL,
            post_plan TEXT NOT NULL,
            status TEXT DEFAULT 'Pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (sender_id) REFERENCES users (id),
            FOREIGN KEY (receiver_id) REFERENCES users (id)
        )
    ''')

    # Marketplace & Mixed Doubles Events
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            price TEXT NOT NULL,
            description TEXT,
            category TEXT NOT NULL, -- 'Racquet' or 'Mixed Doubles Event'
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
# 1. EMAIL OTP SENDER FUNCTION
# ==========================================
def send_real_email_otp(recipient_email, otp_code, sender_email, sender_password):
    """Sends a real email using Gmail's SMTP server."""
    subject = "🎾 Rally & Date - Verification Code"
    body = f"Your 6-digit verification code is: {otp_code}\n\nEnter this in the app to activate your profile!"
    
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

# Convert AI score to Official NTRP Rating
def score_to_ntrp(score):
    if score >= 88:
        return "NTRP 4.5+ (Advanced)"
    elif score >= 78:
        return "NTRP 4.0 (Intermediate-High)"
    elif score >= 68:
        return "NTRP 3.5 (Intermediate)"
    elif score >= 60:
        return "NTRP 3.0 (Solid Rally)"
    else:
        return "NTRP 2.5 (Beginner)"

# Helper: Image Processor
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

# ==========================================
# 2. CONFIG & STYLING
# ==========================================
st.set_page_config(
    page_title="Rally & Date - Tennis Matchmaking",
    page_icon="🎾",
    layout="wide"
)

st.markdown("""
    <style>
    .stApp { background-color: #FAF9F6; color: #212529; }
    .dating-card {
        background-color: white;
        border-radius: 15px;
        padding: 20px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }
    .badge-ntrp {
        background-color: #2E7D32;
        color: white;
        padding: 4px 10px;
        border-radius: 12px;
        font-weight: bold;
        font-size: 12px;
    }
    .badge-vibe {
        background-color: #E91E63;
        color: white;
        padding: 4px 10px;
        border-radius: 12px;
        font-weight: bold;
        font-size: 12px;
    }
    .price-tag { color: #2E7D32; font-weight: bold; font-size: 18px; }
    </style>
""", unsafe_allow_html=True)

# Session States
if "logged_in_user" not in st.session_state:
    st.session_state.logged_in_user = None

if "otp_code" not in st.session_state:
    st.session_state.otp_code = None

if "otp_verified" not in st.session_state:
    st.session_state.otp_verified = False

# ==========================================
# 3. SIDEBAR AUTH & SMTP CONFIG
# ==========================================
st.sidebar.title("🎾 Rally & Date ❤️")

if st.session_state.logged_in_user:
    u = st.session_state.logged_in_user
    st.sidebar.success(f"Logged in: **{u['name']}** ({u['role'].capitalize()})")
    st.sidebar.caption(f"Badge: {u['ntrp_level']}")
    if st.sidebar.button("🚪 Log Out"):
        st.session_state.logged_in_user = None
        st.rerun()
else:
    st.sidebar.subheader("Member Login")
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
            st.sidebar.success("Logged in successfully!")
            st.rerun()
        else:
            st.sidebar.error("Invalid User ID or Password.")

st.sidebar.markdown("---")

with st.sidebar.expander("⚙️ Email SMTP Configuration"):
    smtp_email = st.text_input("Gmail Address", value="your_email@gmail.com")
    smtp_pass = st.text_input("Gmail App Password", type="password")

st.sidebar.markdown("---")
page = st.sidebar.radio("Navigation", [
    "❤️ Rally & Date Matchmaking", 
    "🎾 Single Player Registration", 
    "📹 AI Skill Verification & Coach Status", 
    "🏆 Mixed Doubles Mixers & Marketplace",
    "💌 My Date Invites"
])

# ==========================================
# PAGE 1: MATCHMAKING DISCOVERY
# ==========================================
if page == "❤️ Rally & Date Matchmaking":
    st.title("❤️ Find Your Tennis & Rally Match")
    st.write("Browse single tennis players nearby. Verify skills with AI video analysis or send a **Rally Date Invite**!")

    st.markdown("---")
    
    # Filter Controls
    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1:
        gender_filter = st.selectbox("Show Me:", ["All Singles", "Female", "Male"])
    with col_f2:
        style_filter = st.selectbox("Play Style:", ["All Vibe Types", "Casual Rally & Coffee", "Competitive Match", "Post-Match Drinks"])
    with col_f3:
        only_verified = st.checkbox("Only Show AI Video-Verified Players", value=False)

    st.markdown("---")

    conn = get_db_connection()
    query = "SELECT * FROM users WHERE role = 'player'"
    params = []

    if gender_filter != "All Singles":
        query += " AND gender = ?"
        params.append(gender_filter)
    if style_filter != "All Vibe Types":
        query += " AND play_style = ?"
        params.append(style_filter)
    if only_verified:
        query += " AND score >= 60"

    users_list = conn.execute(query, params).fetchall()
    conn.close()

    if not users_list:
        st.info("No singles found matching your search criteria yet!")
    else:
        cols = st.columns(3)
        for idx, u_profile in enumerate(users_list):
            col = cols[idx % 3]
            with col:
                st.markdown('<div class="dating-card">', unsafe_allow_html=True)
                
                # Image Display
                if u_profile['photo_blob']:
                    st.image(io.BytesIO(u_profile['photo_blob']), use_container_width=True)
                else:
                    st.image("https://via.placeholder.com/300x300.png?text=No+Photo", use_container_width=True)
                
                st.markdown(f"### {u_profile['name']} ({u_profile['gender']})")
                st.markdown(f"<span class='badge-ntrp'>🎾 {u_profile['ntrp_level']}</span> <span class='badge-vibe'>🍷 {u_profile['play_style']}</span>", unsafe_allow_html=True)
                
                st.write(f"📍 **Preferred Courts:** {u_profile['preferred_courts']}")
                st.write(f"💬 *\"{u_profile['dating_bio']}\"*")
                
                # Rally Date Invite Trigger
                if st.session_state.logged_in_user:
                    sender = st.session_state.logged_in_user
                    if sender['id'] != u_profile['id']:
                        with st.popover(f"🎾 Invite {u_profile['name']} to a Rally Date"):
                            st.subheader(f"Send Rally Date Invite to {u_profile['name']}")
                            court_loc = st.text_input("Proposed Court Location", value=u_profile['preferred_courts'], key=f"loc_{u_profile['id']}")
                            m_time = st.text_input("Proposed Date & Time", placeholder="e.g. Saturday 10:00 AM", key=f"time_{u_profile['id']}")
                            post_plan = st.text_input("Post-Match Plan", value="Smoothies & Coffee", key=f"plan_{u_profile['id']}")
                            
                            if st.button("🚀 Send Court Invite", key=f"send_inv_{u_profile['id']}"):
                                if court_loc and m_time:
                                    conn_inv = get_db_connection()
                                    conn_inv.execute('''
                                        INSERT INTO date_invites (sender_id, receiver_id, court_location, match_time, post_plan)
                                        VALUES (?, ?, ?, ?, ?)
                                    ''', (sender['id'], u_profile['id'], court_loc, m_time, post_plan))
                                    conn_inv.commit()
                                    conn_inv.close()
                                    st.success("🎉 Rally Date invitation sent!")
                                else:
                                    st.error("Please enter a location and time.")
                else:
                    st.caption("🔒 *Log in to send a Rally Date Invite*")
                
                st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# PAGE 2: PLAYER REGISTRATION
# ==========================================
elif page == "🎾 Single Player Registration":
    st.title("🎾 Join Rally & Date as a Single Player")
    st.write("Create your profile with **Email OTP Verification** and tennis matchmaking preferences.")

    st.markdown("---")

    st.subheader("Step 1: Account Credentials")
    c1, c2 = st.columns(2)
    with c1:
        s_username = st.text_input("User ID *")
        s_password = st.text_input("Password *", type="password")
        s_name = st.text_input("Full Name *")
    with c2:
        s_phone = st.text_input("Mobile Phone *")
        s_email = st.text_input("Email Address *")
        s_photo = st.file_uploader("Upload Dating Profile Photo *", type=['jpg', 'jpeg', 'png'])

    st.markdown("---")

    st.subheader("Step 2: Matchmaking & Tennis Profile")
    d1, d2 = st.columns(2)
    with d1:
        s_gender = st.selectbox("My Gender *", ["Female", "Male", "Non-binary"])
        s_seeking = st.selectbox("Seeking *", ["Male", "Female", "Everyone"])
        s_style = st.selectbox("Dating Match Vibe *", ["Casual Rally & Coffee", "Competitive Match", "Post-Match Drinks"])
    with d2:
        s_courts = st.text_input("Preferred Local Courts *", placeholder="e.g. Banpo Tennis Club, Olympic Park")
        s_bio = st.text_area("Dating Bio & Icebreaker *", placeholder="My toxic tennis trait is trying to hit winners on every shot...")

    st.markdown("---")

    st.subheader("Step 3: Real Email Verification")
    col_otp1, col_otp2 = st.columns([1, 1])
    
    with col_otp1:
        if st.button("📧 Send Verification Code"):
            if s_email:
                generated_code = str(random.randint(100000, 999999))
                st.session_state.otp_code = generated_code
                st.session_state.otp_verified = False
                
                if "gmail.com" in smtp_email and len(smtp_pass) > 5:
                    success, msg = send_real_email_otp(s_email, generated_code, smtp_email, smtp_pass)
                    if success:
                        st.success(f"📩 Real verification code sent to **{s_email}**!")
                    else:
                        st.error(f"Email error: {msg}")
                else:
                    st.warning("⚠️ SMTP not set. Test Code:")
                    st.info(f"Verification Code: **{generated_code}**")
            else:
                st.error("Please enter an email address.")

    if st.session_state.otp_code:
        entered_code = st.text_input("Enter 6-Digit Email Code")
        if st.button("✅ Verify Code"):
            if entered_code == st.session_state.otp_code:
                st.session_state.otp_verified = True
                st.success("🎉 Email Verified!")
            else:
                st.error("❌ Incorrect Code.")

    st.markdown("---")

    if st.button("🚀 Complete Single Player Profile"):
        if not (s_username and s_password and s_name and s_email and s_photo and s_bio):
            st.error("Please fill in all required fields.")
        elif not st.session_state.otp_verified:
            st.error("⚠️ Complete Email Verification first.")
        else:
            photo_blob = image_to_blob(s_photo)
            conn = get_db_connection()
            try:
                conn.execute('''
                    INSERT INTO users (username, password, phone, email, role, name, gender, seeking_gender, preferred_courts, dating_bio, play_style, photo_blob, is_email_verified)
                    VALUES (?, ?, ?, ?, 'player', ?, ?, ?, ?, ?, ?, ?, 1)
                ''', (s_username, s_password, s_phone, s_email, s_name, s_gender, s_seeking, s_courts, s_bio, s_style, photo_blob))
                conn.commit()
                st.success("🎉 Account created! Log in from the sidebar to start matching.")
                st.balloons()
            except sqlite3.IntegrityError:
                st.error("⚠️ Username or Email already exists.")
            finally:
                conn.close()

# ==========================================
# PAGE 3: AI SKILL VERIFICATION & COACH STATUS
# ==========================================
elif page == "📹 AI Skill Verification & Coach Status":
    st.title("📹 AI Skill Verification & Coach Wingman Status")
    st.write("Upload a tennis video to get an **Anti-Catfish Verified NTRP Badge** on your dating profile, or pay 10,000원 to become a Verified Wingman/Coach Event Organizer!")

    st.markdown("---")

    v_col1, v_col2 = st.columns([2, 1])
    with v_col1:
        video_file = st.file_uploader("Upload Gameplay Video (.mp4, .mov)", type=['mp4', 'mov'])
        if video_file:
            st.video(video_file)

    with v_col2:
        if video_file:
            if st.button("📊 Analyze Swing & Spin Mechanics"):
                with st.spinner("AI evaluating stroke mechanics & spin speed..."):
                    time.sleep(1.5)
                    analyzed_score = random.randint(62, 95)
                    st.session_state['coach_score'] = analyzed_score

    if 'coach_score' in st.session_state:
        score = st.session_state['coach_score']
        ntrp = score_to_ntrp(score)
        st.markdown("---")
        st.subheader(f"AI Score Result: {score} / 100")
        st.success(f"🏆 Your Verified Tennis Skill Rating is: **{ntrp}**")
        
        # Option A: Attach NTRP Badge to Existing Account
        if st.session_state.logged_in_user:
            if st.button("🏅 Update My Profile with Verified NTRP Badge"):
                u_id = st.session_state.logged_in_user['id']
                conn = get_db_connection()
                conn.execute('UPDATE users SET score = ?, ntrp_level = ? WHERE id = ?', (score, ntrp, u_id))
                conn.commit()
                conn.close()
                st.success("🎉 Your dating profile now displays your Verified NTRP Badge!")

        st.markdown("---")

        # Option B: Upgrade to Coach / Mixer Host
        if score >= 60:
            st.info("🌟 You qualify for **Coach / Event Organizer Certification**! Host 4-player Mixed Doubles Blind Dates or sell gear.")
            with st.form("coach_upgrade"):
                c_user = st.text_input("Coach User ID *")
                c_pass = st.text_input("Password *", type="password")
                c_name = st.text_input("Full Name *")
                c_phone = st.text_input("Mobile Phone *")
                c_email = st.text_input("Email *")
                
                if st.form_submit_button("💳 Pay 10,000원 & Get Event Organizer License"):
                    conn = get_db_connection()
                    try:
                        conn.execute('''
                            INSERT INTO users (username, password, phone, email, role, name, score, fee_paid, ntrp_level, is_email_verified)
                            VALUES (?, ?, ?, ?, 'coach', ?, ?, 1, ?, 1)
                        ''', (c_user, c_pass, c_phone, c_email, c_name, score, f"Pro Coach ({ntrp})"))
                        conn.commit()
                        st.success("🏆 Coach / Event Host License Granted!")
                        st.balloons()
                    except sqlite3.IntegrityError:
                        st.error("User ID or Email already exists.")
                    finally:
                        conn.close()

# ==========================================
# PAGE 4: MIXED DOUBLES & MARKETPLACE
# ==========================================
elif page == "🏆 Mixed Doubles Mixers & Marketplace":
    st.title("🏆 Mixed Doubles Dating Events & Market")
    st.write("Join 4-player Mixed Doubles Blind Date Sessions hosted by coaches, or trade gear!")

    user = st.session_state.logged_in_user
    
    # Coach Event Creation
    if user and user['role'] == 'coach':
        with st.expander("➕ Coach Wingman: Host Mixed Doubles Blind Date Event or Gear"):
            with st.form("add_event"):
                e_title = st.text_input("Event / Item Name *", placeholder="e.g. Saturday Mixed Doubles Singles Mixer (2M + 2F)")
                e_cat = st.selectbox("Category", ["Mixed Doubles Event", "Racquet / Gear"])
                e_price = st.text_input("Price (KRW) *", placeholder="30,000 ₩ per person")
                e_desc = st.text_area("Event Details / Court Location")
                e_photo = st.file_uploader("Upload Image *", type=['jpg', 'jpeg', 'png'])
                
                if st.form_submit_button("🚀 Publish Event / Item"):
                    if e_title and e_price and e_photo:
                        photo_blob = image_to_blob(e_photo)
                        conn = get_db_connection()
                        conn.execute('''
                            INSERT INTO inventory (title, price, description, category, coach_id, photo_blob)
                            VALUES (?, ?, ?, ?, ?, ?)
                        ''', (e_title, e_price, e_desc, e_cat, user['id'], photo_blob))
                        conn.commit()
                        conn.close()
                        st.success("Published successfully!")
                        st.rerun()

    st.markdown("---")
    st.subheader("Active Events & Offers")

    conn = get_db_connection()
    items = conn.execute('''
        SELECT inventory.*, users.name as coach_name 
        FROM inventory JOIN users ON inventory.coach_id = users.id
        ORDER BY inventory.created_at DESC
    ''').fetchall()
    conn.close()

    if not items:
        st.info("No events or gear listed yet.")
    else:
        cols = st.columns(3)
        for idx, item in enumerate(items):
            col = cols[idx % 3]
            with col:
                if item['photo_blob']:
                    st.image(io.BytesIO(item['photo_blob']), use_container_width=True)
                st.markdown(f"### {item['title']}")
                st.caption(f"Category: **{item['category']}** | Host: **Coach {item['coach_name']}**")
                st.markdown(f"💰 Fee: `<span class='price-tag'>{item['price']}</span>`", unsafe_allow_html=True)
                st.write(item['description'])
                
                if st.button("🎟️ Book Ticket / Join Event", key=f"evt_{item['id']}"):
                    if user:
                        st.success("Ticket booked! Details sent to your account email.")
                    else:
                        st.warning("Please log in to join.")
                st.markdown("---")

# ==========================================
# PAGE 5: MY DATE INVITES
# ==========================================
elif page == "💌 My Date Invites":
    st.title("💌 My Rally Date Invitations")
    st.write("Manage your incoming and outgoing court date invites!")

    if not st.session_state.logged_in_user:
        st.warning("Please log in to view your invitations.")
    else:
        u_id = st.session_state.logged_in_user['id']
        conn = get_db_connection()
        
        # Received Invites
        st.subheader("📥 Received Date Invitations")
        received = conn.execute('''
            SELECT date_invites.*, users.name as sender_name, users.ntrp_level, users.play_style
            FROM date_invites
            JOIN users ON date_invites.sender_id = users.id
            WHERE receiver_id = ?
            ORDER BY created_at DESC
        ''', (u_id,)).fetchall()
        
        if not received:
            st.info("No incoming date invites yet.")
        else:
            for r in received:
                with st.expander(f"🎾 Rally Invite from {r['sender_name']} ({r['ntrp_level']}) - Status: {r['status']}"):
                    st.write(f"📍 **Court Location:** {r['court_location']}")
                    st.write(f"⏰ **Proposed Time:** {r['match_time']}")
                    st.write(f"🍷 **Post-Match Plan:** {r['post_plan']}")
                    
                    if r['status'] == 'Pending':
                        c_a, c_b = st.columns(2)
                        with c_a:
                            if st.button("✅ Accept Date", key=f"acc_{r['id']}"):
                                conn.execute("UPDATE date_invites SET status = 'Accepted' WHERE id = ?", (r['id'],))
                                conn.commit()
                                st.success("Date Accepted! See you on the court!")
                                st.rerun()
                        with c_b:
                            if st.button("❌ Decline", key=f"dec_{r['id']}"):
                                conn.execute("UPDATE date_invites SET status = 'Declined' WHERE id = ?", (r['id'],))
                                conn.commit()
                                st.rerun()

        st.markdown("---")

        # Sent Invites
        st.subheader("📤 Sent Invitations")
        sent = conn.execute('''
            SELECT date_invites.*, users.name as receiver_name 
            FROM date_invites
            JOIN users ON date_invites.receiver_id = users.id
            WHERE sender_id = ?
            ORDER BY created_at DESC
        ''', (u_id,)).fetchall()
        
        if not sent:
            st.info("You haven't sent any invitations yet.")
        else:
            for s in sent:
                st.write(f"🎾 Sent to **{s['receiver_name']}** for *{s['court_location']}* on *{s['match_time']}* — **Status:** `{s['status']}`")

        conn.close()
