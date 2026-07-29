import streamlit as st
import datetime
import time

# ==========================================
# 1. Page Configuration & Initial State
# ==========================================
st.set_page_config(
    page_title="ServeAI - Global Tennis & Sports-Tech Portal",
    page_icon="🎾",
    layout="wide"
)

# Session State Initialization
if "users" not in st.session_state:
    st.session_state["users"] = {"admin@serveai.com": "password123"}
if "logged_in_user" not in st.session_state:
    st.session_state["logged_in_user"] = None
if "admin_logged_in" not in st.session_state:
    st.session_state["admin_logged_in"] = False

# Membership Pass Database (Tracks 1-Month Subscriptions)
if "memberships" not in st.session_state:
    st.session_state["memberships"] = {
        "alex@globaltennis.com": {
            "status": "Active",
            "plan": "1-Month Unlimited Pass ($4.99/mo)",
            "expires": "2026-08-29"
        }
    }

# Mock Community Databases
if "players_db" not in st.session_state:
    st.session_state["players_db"] = [
        {"id": "P-101", "name": "Jessica Chen", "ntrp": 3.5, "gender": "Female", "location": "Gangnam Center, Seoul", "bio": "Looking for consistent rally partners on weekends! Topspin baseline player.", "avatar": "👩‍🎾"},
        {"id": "P-102", "name": "Min-woo Park", "ntrp": 3.5, "gender": "Male", "location": "Gangnam Center, Seoul", "bio": "Aggressive serve & volleyer. Available weekday evenings.", "avatar": "👨‍🎾"},
        {"id": "P-103", "name": "Elena Rostova", "ntrp": 4.0, "gender": "Female", "location": "Jeju Ocean Resort", "bio": "Advanced player preparing for local tournaments. Prefers singles.", "avatar": "👩‍🎾"},
        {"id": "P-104", "name": "Kenji Sato", "ntrp": 3.0, "gender": "Male", "location": "Songdo Park, Incheon", "bio": "Intermediate player working on backhand consistency. Friendly games!", "avatar": "👨‍🎾"},
        {"id": "P-105", "name": "Sophia Lee", "ntrp": 4.0, "gender": "Female", "location": "Gangnam Center, Seoul", "bio": "Ex-college club player, great rallies and match play.", "avatar": "👩‍🎾"}
    ]

if "coaches_db" not in st.session_state:
    st.session_state["coaches_db"] = [
        {"id": "C-201", "name": "Coach Daniel Kim", "cert": "USPTA Elite Certified", "exp": "8 Years Pro Coaching", "rate": "$45 / hr", "location": "Gangnam Center, Seoul", "bio": "Specializes in serve biomechanics, AI trajectory fixes, and match strategy."},
        {"id": "C-202", "name": "Coach Hannah Choi", "cert": "KTA Certified Senior Coach", "exp": "12 Years Experience", "rate": "$50 / hr", "location": "Jeju Ocean Resort", "bio": "Former national junior coach. Slice, drop shots, and tactical movement."},
        {"id": "C-203", "name": "Coach Alex Rivera", "cert": "PTR Master Professional", "exp": "10 Years Experience", "rate": "$40 / hr", "location": "Songdo Park, Incheon", "bio": "Focuses on footwork, racket head speed, and beginner-to-advanced progression."}
    ]

if "chat_orders" not in st.session_state:
    st.session_state["chat_orders"] = [
        {
            "order_id": "MSG-20260729-01",
            "sender": "alex@globaltennis.com",
            "recipient": "Jessica Chen (NTRP 3.5)",
            "message": "Hi Jessica! Want to hit at Gangnam court this Saturday at 10 AM?",
            "time": "2026-07-29 14:10"
        }
    ]

if "inquiries" not in st.session_state:
    st.session_state["inquiries"] = []

if "match_orders" not in st.session_state:
    st.session_state["match_orders"] = []

if "estate_orders" not in st.session_state:
    st.session_state["estate_orders"] = []

# ==========================================
# 2. Language Switcher & Localization
# ==========================================
st.sidebar.title("🎾 ServeAI Global")
lang = st.sidebar.selectbox("🌐 Language / 언어", ["English", "한국어"])
st.sidebar.markdown("---")

t = {
    "English": {
        "nav_title": "📌 Navigation",
        "nav_1": "⚡ AI Serve Speed Analysis",
        "nav_2": "🎾 AI Racket & Tension Calculator",
        "nav_3": "🏆 Tournaments & Accommodation Subpage",
        "nav_4": "🏫 Tennis School Service & Training Packages",
        "nav_5": "🤝 NTRP Match & VIP Chat Pass",
        "nav_6": "💬 Support & Inquiries",
        "nav_7": "🔒 Admin / Backend Dashboard",
        "login_sub": "👤 User Account",
        "login_tab": "Login",
        "reg_tab": "Register",
        "email_lbl": "Email Address",
        "pw_lbl": "Password",
        "btn_login": "Login",
        "btn_logout": "Logout",
        "welcome": "Welcome",
        "err_login": "Invalid email or password.",
        "reg_success": "Registration complete! Please log in.",
        "calc_title": "🎾 AI Tennis NTRP & Tension Calculator",
        "calc_desc": "Calculates your optimal string tension (lbs) based on your NTRP level and AI serve speed.",
        "support_title": "💬 Customer Support & Ticket Center",
        "support_desc": "Submit your questions regarding membership or app features.",
        "match_title": "🤝 Community NTRP Matching & Unlimited VIP Chat Pass",
        "match_desc": "Subscribe for $4.99/month to get unlimited free direct messaging with local coaches and NTRP hitting partners!"
    },
    "한국어": {
        "nav_title": "📌 메뉴 선택",
        "nav_1": "⚡ AI 서브 속도 분석",
        "nav_2": "🎾 AI 라켓 & 텐션 추천 계산기",
        "nav_3": "🏆 테니스 대회 & 숙박 서브페이지",
        "nav_4": "🏫 글로벌 테니스 스쿨 서비스 & 장기 레지던시",
        "nav_5": "🤝 NTRP 파트너 매칭 & VIP 무제한 채팅",
        "nav_6": "💬 고객 지원 & 문의",
        "nav_7": "🔒 백엔드 관리자 대시보드",
        "login_sub": "👤 회원 계정",
        "login_tab": "로그인",
        "reg_tab": "회원가입",
        "email_lbl": "이메일 주소",
        "pw_lbl": "비밀번호",
        "btn_login": "로그인",
        "btn_logout": "로그아웃",
        "welcome": "환영합니다",
        "err_login": "이메일 또는 비밀번호가 올바르지 않습니다.",
        "reg_success": "가입 완료! 로그인해 주세요.",
        "calc_title": "🎾 AI 테니스 NTRP / 최적 텐션 계산기",
        "calc_desc": "NTRP 레벨과 AI 측정 서브 속도를 바탕으로 최적의 텐션을 정밀 계산합니다.",
        "support_title": "💬 고객 지원 & 1:1 문의하기",
        "support_desc": "멤버십 및 서비스 관련 궁금하신 점을 문의해 주세요.",
        "match_title": "🤝 커뮤니티 NTRP 매칭 & 1개월 무제한 VIP 멤버십",
        "match_desc": "월 $4.99(약 6,500원) 멤버십 구독 시, 주변 모든 NTRP 파트너 및 검증 코치와 무제한 무료 대화가 가능합니다!"
    }
}[lang]

# Login Block
if st.session_state["logged_in_user"] is None:
    st.sidebar.subheader(t["login_sub"])
    auth_mode = st.sidebar.radio("Action", [t["login_tab"], t["reg_tab"]], horizontal=True)
    
    if auth_mode == t["login_tab"]:
        email_in = st.sidebar.text_input(t["email_lbl"])
        pw_in = st.sidebar.text_input(t["pw_lbl"], type="password")
        if st.sidebar.button(t["btn_login"]):
            if email_in in st.session_state["users"] and st.session_state["users"][email_in] == pw_in:
                st.session_state["logged_in_user"] = email_in
                st.sidebar.success(f"{t['welcome']}, {email_in}!")
                st.rerun()
            else:
                st.sidebar.error(t["err_login"])
    else:
        reg_email = st.sidebar.text_input(f"New {t['email_lbl']}")
        reg_pw = st.sidebar.text_input(f"New {t['pw_lbl']}", type="password")
        if st.sidebar.button(t["reg_tab"]):
            if reg_email and reg_pw:
                st.session_state["users"][reg_email] = reg_pw
                st.sidebar.success(t["reg_success"])
            else:
                st.sidebar.warning("Fill in all fields.")
else:
    st.sidebar.success(f"🟢 **{st.session_state['logged_in_user']}**")
    user_mem = st.session_state["memberships"].get(st.session_state["logged_in_user"], None)
    if user_mem and user_mem["status"] == "Active":
        st.sidebar.caption("⭐ **VIP Pass Active** (Unlimited Chat)")
    else:
        st.sidebar.caption("⚪ **Basic Account** (Chat Locked)")

    if st.sidebar.button(t["btn_logout"]):
        st.session_state["logged_in_user"] = None
        st.rerun()

st.sidebar.markdown("---")

nav_options = [
    t["nav_1"],
    t["nav_2"],
    t["nav_3"],
    t["nav_4"],
    t["nav_5"],
    t["nav_6"],
    t["nav_7"]
]
page_selection = st.sidebar.radio(t["nav_title"], nav_options)

# ==========================================
# 3. Feature 1 & 2: Speed & Calculator
# ==========================================
if page_selection == t["nav_1"]:
    st.title(t["nav_1"])
    st.write("Upload a tennis serve video to calculate velocity trajectory and impact point.")

elif page_selection == t["nav_2"]:
    st.title(t["calc_title"])
    st.write(t["calc_desc"])

elif page_selection == t["nav_3"]:
    st.title("🏆 Tournaments Subpage")

elif page_selection == t["nav_4"]:
    st.title("🏫 Tennis School Residency")

# ==========================================
# 4. Feature 5: NTRP Matching & 1-Month VIP Pass
# ==========================================
elif page_selection == t["nav_5"]:
    st.title(t["match_title"])
    st.write(t["match_desc"])
    
    # Membership Status Banner
    current_user = st.session_state["logged_in_user"]
    user_mem_info = st.session_state["memberships"].get(current_user, None) if current_user else None
    has_active_vip = user_mem_info and user_mem_info["status"] == "Active"

    if has_active_vip:
        st.success(f"🌟 **VIP Pass Active** | Expiration: `{user_mem_info['expires']}` | **Unlimited Free Chat Unlocked!**")
    else:
        with st.expander("💳 **Get 1-Month VIP Chat Pass ($4.99 / Month) - Click Here to Unlock All Chats**", expanded=not has_active_vip):
            st.markdown("#### Enjoy unlimited direct chats with all local tennis players & coaches for 30 days!")
            c_mem1, c_mem2 = st.columns([2, 1])
            with c_mem1:
                mem_email = st.text_input("Account Email", value=current_user or "")
                card_no = st.text_input("Card Number", placeholder="4000-0000-0000-0000")
            with c_mem2:
                st.write("**Plan**: 1-Month VIP Membership")
                st.write("**Price**: `$4.99 USD` / month")
                if st.button("🚀 Pay $4.99 & Activate Pass"):
                    if mem_email and card_no:
                        st.session_state["memberships"][mem_email] = {
                            "status": "Active",
                            "plan": "1-Month Unlimited Pass ($4.99/mo)",
                            "expires": (datetime.datetime.now() + datetime.timedelta(days=30)).strftime("%Y-%m-%d")
                        }
                        st.balloons()
                        st.success("🎉 Membership activated! You can now chat with all players and coaches for free.")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("Please enter email and card details.")

    st.markdown("---")

    sub_tab1, sub_tab2, sub_tab3 = st.tabs([
        "🎾 Find Nearby NTRP Players",
        "👨‍🏫 Connect with Verified Coaches",
        "📝 Coach Registration Portal"
    ])

    # TAB 1: PLAYER MATCHING
    with sub_tab1:
        st.subheader("🔍 Filter Nearby Players by Location & NTRP")
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            filter_loc = st.selectbox("Location", ["All Locations (전체)", "Gangnam Center, Seoul", "Jeju Ocean Resort", "Songdo Park, Incheon"])
        with col_f2:
            my_ntrp = st.slider("Your NTRP Level", min_value=2.0, max_value=5.0, value=3.5, step=0.5)

        filtered_players = []
        for p in st.session_state["players_db"]:
            match_loc = (filter_loc == "All Locations (전체)") or (p["location"] == filter_loc)
            match_ntrp = abs(p["ntrp"] - my_ntrp) <= 0.5
            if match_loc and match_ntrp:
                filtered_players.append(p)

        st.markdown("---")
        for pl in filtered_players:
            with st.container(border=True):
                p_col1, p_col2 = st.columns([3, 1])
                with p_col1:
                    st.markdown(f"### {pl['avatar']} {pl['name']} *(NTRP {pl['ntrp']})*")
                    st.write(f"📍 **Location**: {pl['location']} | **Gender**: {pl['gender']}")
                    st.caption(f"💬 \"{pl['bio']}\"")
                with p_col2:
                    if has_active_vip:
                        st.success("✅ **Free Chat (VIP Active)**")
                        if st.button("💬 Chat Now", key=f"chat_{pl['id']}"):
                            st.session_state[f"open_chat_{pl['id']}"] = True
                    else:
                        st.warning("🔒 **Requires VIP Pass**")
                        st.caption("Subscribe above for $4.99/mo")

            # VIP Active Direct Chat Box
            if st.session_state.get(f"open_chat_{pl['id']}", False) and has_active_vip:
                with st.form(key=f"form_msg_{pl['id']}"):
                    st.write(f"💬 Direct Message to **{pl['name']}**")
                    free_msg = st.text_area("Write your message", placeholder=f"Hi {pl['name']}, let's set up a time to play at {pl['location']}!")
                    if st.form_submit_button("✉️ Send Message"):
                        if free_msg:
                            st.session_state["chat_orders"].append({
                                "order_id": f"MSG-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}",
                                "sender": current_user,
                                "recipient": f"{pl['name']} (NTRP {pl['ntrp']})",
                                "message": free_msg,
                                "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                            })
                            st.success(f"Message sent to {pl['name']}!")
                            st.session_state[f"open_chat_{pl['id']}"] = False
                        else:
                            st.error("Please enter a message.")

    # TAB 2: COACH MESSAGING
    with sub_tab2:
        st.subheader("👨‍🏫 Experienced Tennis Coaches")
        for ch in st.session_state["coaches_db"]:
            with st.container(border=True):
                c_col1, c_col2 = st.columns([3, 1])
                with c_col1:
                    st.markdown(f"### 🎾 {ch['name']}")
                    st.write(f"📜 **Cert**: {ch['cert']} ({ch['exp']})")
                    st.write(f"📍 **Location**: {ch['location']} | 🏷️ **Lesson Rate**: {ch['rate']}")
                    st.caption(f"💡 {ch['bio']}")
                with c_col2:
                    if has_active_vip:
                        st.success("✅ **Free Chat (VIP Active)**")
                        if st.button("💬 Contact Coach", key=f"coach_btn_{ch['id']}"):
                            st.session_state[f"open_coach_{ch['id']}"] = True
                    else:
                        st.warning("🔒 **Requires VIP Pass**")
                        st.caption("Subscribe above for $4.99/mo")

            if st.session_state.get(f"open_coach_{ch['id']}", False) and has_active_vip:
                with st.form(key=f"form_c_msg_{ch['id']}"):
                    st.write(f"💬 Direct Message to **{ch['name']}**")
                    c_free_msg = st.text_area("Inquiry Notes", placeholder="Hi Coach, what are your available lesson times this week?")
                    if st.form_submit_button("✉️ Send Message"):
                        if c_free_msg:
                            st.session_state["chat_orders"].append({
                                "order_id": f"MSG-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}",
                                "sender": current_user,
                                "recipient": f"{ch['name']} (Coach)",
                                "message": c_free_msg,
                                "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                            })
                            st.success(f"Message delivered to {ch['name']}!")
                            st.session_state[f"open_coach_{ch['id']}"] = False
                        else:
                            st.error("Please enter a message.")

    # TAB 3: COACH REGISTRATION
    with sub_tab3:
        st.subheader("📝 Register as an Experienced Tennis Teacher")
        with st.form("coach_reg_form"):
            new_c_name = st.text_input("Full Name", placeholder="Coach Alex Mercer")
            new_c_cert = st.text_input("Certification", placeholder="USPTA Certified / 10 Yrs Exp")
            new_c_loc = st.selectbox("Primary Location", ["Gangnam Center, Seoul", "Jeju Ocean Resort", "Songdo Park, Incheon"])
            new_c_rate = st.text_input("Lesson Rate", placeholder="$50 / hr")
            new_c_bio = st.text_area("Bio & Philosophy", placeholder="Specialized in topspin mechanics and match strategy.")
            if st.form_submit_button("🚀 Submit Coach Profile"):
                if new_c_name and new_c_cert:
                    st.session_state["coaches_db"].append({
                        "id": f"C-{len(st.session_state['coaches_db'])+201}",
                        "name": new_c_name,
                        "cert": new_c_cert,
                        "exp": "Verified Teacher",
                        "rate": new_c_rate,
                        "location": new_c_loc,
                        "bio": new_c_bio
                    })
                    st.balloons()
                    st.success("Profile submitted and listed!")

# ==========================================
# 5. Feature 6 & 7: Support & Admin
# ==========================================
elif page_selection == t["nav_6"]:
    st.title(t["support_title"])

elif page_selection == t["nav_7"]:
    st.title("🔒 Admin Dashboard")
    if not st.session_state["admin_logged_in"]:
        with st.form("adm_login"):
            a_id = st.text_input("Admin ID")
            a_pw = st.text_input("Password", type="password")
            if st.form_submit_button("Login"):
                if a_id == "admin" and a_pw == "admin":
                    st.session_state["admin_logged_in"] = True
                    st.rerun()
    else:
        st.success("🟢 Admin Mode")
        st.subheader("💳 Active VIP Memberships ($4.99/mo)")
        st.json(st.session_state["memberships"])
        
        st.subheader("💬 Delivered Community Messages")
        st.dataframe(st.session_state["chat_orders"], use_container_width=True)
