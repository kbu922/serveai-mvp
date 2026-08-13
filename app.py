import time
import random
import streamlit as st

# ==========================================
# 0. PAGE CONFIG & STYLING
# ==========================================
st.set_page_config(
    page_title="Tennis Coach & Student Market",
    page_icon="🎾",
    layout="wide"
)

st.markdown("""
    <style>
    .stApp {
        background-color: #F8F9FA;
        color: #212529;
    }
    .cert-card {
        background-color: #E8F5E9;
        border: 2px solid #2E7D32;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        margin-bottom: 20px;
    }
    .fail-card {
        background-color: #FFEBEE;
        border: 2px solid #C62828;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        margin-bottom: 20px;
    }
    .claimed-badge {
        background-color: #D90429;
        color: white;
        padding: 4px 10px;
        border-radius: 6px;
        font-weight: bold;
        font-size: 13px;
    }
    .price-tag {
        font-size: 18px;
        font-weight: bold;
        color: #2E7D32;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize Session States
if "current_coach" not in st.session_state:
    st.session_state.current_coach = None

if "current_student" not in st.session_state:
    st.session_state.current_student = None

if "marketplace_items" not in st.session_state:
    st.session_state.marketplace_items = [
        {
            "id": 1,
            "title": "Wilson Pro Staff 97 (Like New)",
            "seller": "Coach Alex",
            "price": "120,000 ₩",
            "desc": "Great condition, strung with Luxilon strings at 52lbs.",
            "images": ["https://images.unsplash.com/photo-1617083934555-ac7d4fed8824?w=500"],
            "claimed_by": None
        }
    ]

# Navigation
st.sidebar.title("🎾 Navigation")

# Current User Status Badge in Sidebar
if st.session_state.current_coach:
    st.sidebar.success(f"👤 Coach: {st.session_state.current_coach['name']} (Verified)")
elif st.session_state.current_student:
    st.sidebar.info(f"🎓 Student: {st.session_state.current_student['name']}")
else:
    st.sidebar.caption("Not logged in")

page = st.sidebar.radio("Go to:", [
    "📹 Coach Video Assessment", 
    "🎾 Register as Student",
    "🛍️ Second-Hand Market", 
    "💬 Chat & Make Friends"
])

# ==========================================
# 1. COACH VIDEO ASSESSMENT & VERIFICATION
# ==========================================
if page == "📹 Coach Video Assessment":
    st.title("📹 Coach Assessment & Verification")
    st.write("Upload your video to analyze your score. Score **60 or above** unlocks Coach Verification for **10,000원**!")

    st.markdown("---")

    st.subheader("Step 1: Upload Swing / Match Video")
    coach_name = st.text_input("Coach Name *", value=st.session_state.current_coach['name'] if st.session_state.current_coach else "")
    video_file = st.file_uploader("Upload video file (.mp4, .mov)", type=["mp4", "mov"])

    if video_file and coach_name:
        st.video(video_file)
        
        if st.button("📊 Analyze Swing & Get Score"):
            with st.spinner("🤖 Analyzing biomechanics..."):
                time.sleep(1.2)
                analyzed_score = random.randint(62, 95)
                st.session_state["temp_score"] = analyzed_score

    if "temp_score" in st.session_state:
        score = st.session_state["temp_score"]
        st.markdown("---")

        if score >= 60:
            st.markdown(f"""
                <div class="cert-card">
                    <h2>🎉 Score: {score} / 100</h2>
                    <p>Verified Coach License Fee: <strong>10,000 원 (KRW)</strong></p>
                </div>
            """, unsafe_allow_html=True)

            if st.button("💳 Pay 10,000원 & Receive License"):
                st.session_state.current_coach = {
                    "name": coach_name,
                    "score": score,
                    "verified": True
                }
                # Clear student state if switching roles
                st.session_state.current_student = None
                st.balloons()
                st.success(f"✅ Official Coach License Granted to {coach_name}!")
        else:
            st.markdown(f"""
                <div class="fail-card">
                    <h2>❌ Score: {score} / 100</h2>
                    <p>Score below 60. Practice and try uploading again!</p>
                </div>
            """, unsafe_allow_html=True)

# ==========================================
# 2. STUDENT REGISTRATION
# ==========================================
elif page == "🎾 Register as Student":
    st.title("🎾 Register as a Student")
    st.write("Register to connect with coaches and claim products as free gifts!")

    st.markdown("---")

    with st.form("student_reg_form"):
        s_name = st.text_input("Full Name *")
        s_email = st.text_input("Email *")
        s_photo = st.file_uploader("Upload Profile Photo *", type=["jpg", "png", "jpeg"])
        
        if st.form_submit_button("🚀 Register Student Profile"):
            if s_name and s_email and s_photo:
                st.session_state.current_student = {
                    "name": s_name,
                    "email": s_email,
                    "photo": s_photo
                }
                # Clear coach state if switching roles
                st.session_state.current_coach = None
                st.balloons()
                st.success(f"🎉 Welcome {s_name}! You can now claim products in the marketplace as free gifts!")
            else:
                st.error("Please fill in your name, email, and upload a photo.")

    if st.session_state.current_student:
        st.markdown("---")
        st.subheader("Your Active Profile")
        col_s1, col_s2 = st.columns([1, 3])
        with col_s1:
            st.image(st.session_state.current_student["photo"], use_container_width=True)
        with col_s2:
            st.markdown(f"### {st.session_state.current_student['name']}")
            st.write(f"📧 **Email**: {st.session_state.current_student['email']}")

# ==========================================
# 3. SECOND-HAND MARKETPLACE
# ==========================================
elif page == "🛍️ Second-Hand Market":
    st.title("🛍️ Second-Hand Tennis Market")
    st.write("Coaches can list products for sale, and students can claim items as gifts!")

    st.markdown("---")

    # EXPANDER FOR VERIFIED COACHES TO LIST PRODUCTS
    if st.session_state.current_coach and st.session_state.current_coach.get("verified"):
        with st.expander("➕ Create Second-Hand Product Listing"):
            with st.form("create_product_form"):
                p_title = st.text_input("Product Title *", placeholder="e.g. Babolat Pure Drive")
                p_price = st.text_input("Price (KRW) *", placeholder="e.g. 50,000 ₩")
                p_desc = st.text_area("Description *")
                
                st.write("📸 **Upload Up to 3 Photos:**")
                f1 = st.file_uploader("Photo 1", type=["jpg", "png", "jpeg"], key="p1")
                f2 = st.file_uploader("Photo 2", type=["jpg", "png", "jpeg"], key="p2")
                f3 = st.file_uploader("Photo 3", type=["jpg", "png", "jpeg"], key="p3")

                if st.form_submit_button("🚀 Upload Product"):
                    if p_title and p_price and p_desc:
                        uploaded_imgs = [f for f in [f1, f2, f3] if f is not None]
                        if not uploaded_imgs:
                            uploaded_imgs = ["https://images.unsplash.com/photo-1617083934555-ac7d4fed8824?w=500"]

                        new_item = {
                            "id": random.randint(1000, 9999),
                            "title": p_title,
                            "seller": st.session_state.current_coach["name"],
                            "price": p_price,
                            "desc": p_desc,
                            "images": uploaded_imgs,
                            "claimed_by": None
                        }
                        st.session_state.marketplace_items.insert(0, new_item)
                        st.success("🎉 Product listed successfully!")
                        st.rerun()

    st.markdown("### 🛍️ Available Listings")

    cols = st.columns(3)
    for idx, item in enumerate(st.session_state.marketplace_items):
        col = cols[idx % 3]
        with col:
            st.image(item["images"][0], use_container_width=True)
            
            st.markdown(f"### {item['title']}")
            st.markdown(f"💰 Price: `<span class='price-tag'>{item['price']}</span>`", unsafe_allow_html=True)
            st.caption(f"👤 Coach Seller: **{item['seller']}**")
            st.write(item["desc"])

            # SHOW CLAIM STATUS
            if item.get("claimed_by"):
                st.markdown(f"<span class='claimed-badge'>🎁 Claimed by: {item['claimed_by']}</span>", unsafe_allow_html=True)
                st.write("")
            else:
                # ACTION BUTTONS BASED ON USER ROLE
                if st.session_state.current_student:
                    if st.button(f"🎁 Claim as Free Gift", key=f"claim_{item['id']}"):
                        item["claimed_by"] = st.session_state.current_student["name"]
                        st.toast(f"🎉 You claimed {item['title']} as a gift!")
                        st.rerun()

            # EDIT/DELETE OPTIONS FOR SELLER
            if st.session_state.current_coach and item["seller"] == st.session_state.current_coach["name"]:
                with st.popover("✏️ Edit / Delete"):
                    new_t = st.text_input("Title", value=item["title"], key=f"et_{item['id']}")
                    new_p = st.text_input("Price", value=item["price"], key=f"ep_{item['id']}")
                    new_d = st.text_area("Description", value=item["desc"], key=f"ed_{item['id']}")
                    
                    if st.button("Save Changes", key=f"save_{item['id']}"):
                        item["title"] = new_t
                        item["price"] = new_p
                        item["desc"] = new_d
                        st.toast("Saved!")
                        st.rerun()

                    if st.button("🗑️ Delete Listing", key=f"del_{item['id']}"):
                        st.session_state.marketplace_items.remove(item)
                        st.rerun()
            else:
                c1, c2 = st.columns(2)
                with c1:
                    if st.button("💬 Chat", key=f"chat_{item['id']}"):
                        st.toast(f"Opening chat with {item['seller']}...")
                with c2:
                    if st.button("🤝 Add Friend", key=f"friend_{item['id']}"):
                        st.toast(f"Sent friend request to {item['seller']}!")
            st.markdown("---")

# ==========================================
# 4. CHAT & FRIENDS
# ==========================================
elif page == "💬 Chat & Make Friends":
    st.title("💬 Student & Coach Chat")
    st.write("Direct message coaches or students to make friends!")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("💬 Send Message")
        st.selectbox("Recipient:", ["Coach Alex", "Sarah Jenkins"])
        st.text_area("Message Content:")
        if st.button("Send"):
            st.success("Message delivered!")

    with col2:
        st.subheader("🤝 Friends List")
        st.info("No active friend requests.")
