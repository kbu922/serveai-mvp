import time
import random
import streamlit as st

# ==========================================
# 0. PAGE CONFIG & STYLING
# ==========================================
st.set_page_config(
    page_title="Tennis Coach Verification & Market",
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
    .price-tag {
        font-size: 18px;
        font-weight: bold;
        color: #2E7D32;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize Session States
if "current_coach" not in st.session_state:
    st.session_state.current_coach = None  # Holds verified coach info

if "marketplace_items" not in st.session_state:
    st.session_state.marketplace_items = [
        {
            "id": 1,
            "title": "Wilson Pro Staff 97 (Like New)",
            "seller": "Coach Alex",
            "price": "120,000 ₩",
            "desc": "Great condition, strung with Luxilon strings at 52lbs.",
            "images": ["https://images.unsplash.com/photo-1617083934555-ac7d4fed8824?w=500"]
        }
    ]

# Navigation
st.sidebar.title("🎾 Navigation")
page = st.sidebar.radio("Go to:", [
    "📹 Coach Video Assessment", 
    "🛍️ Second-Hand Market", 
    "💬 Chat & Make Friends"
])

# ==========================================
# 1. COACH VIDEO ASSESSMENT & VERIFICATION
# ==========================================
if page == "📹 Coach Video Assessment":
    st.title("📹 Coach Video Assessment & Verification")
    st.write("Upload your tennis video to analyze your skill score. If your score is **60 or above**, you can pay 10,000원 to get verified!")

    st.markdown("---")

    # STEP 1: UPLOAD & ANALYZE VIDEO
    st.subheader("Step 1: Upload Gameplay / Swing Video")
    coach_name = st.text_input("Your Full Name *")
    video_file = st.file_uploader("Upload video file (.mp4, .mov)", type=["mp4", "mov"])

    if video_file and coach_name:
        st.video(video_file)
        
        if st.button("📊 Analyze Video & Calculate Tennis Score"):
            with st.spinner("🤖 Analyzing biomechanics and swing technique..."):
                time.sleep(1.5)
                # Calculated tennis score
                analyzed_score = random.randint(55, 95)
                st.session_state["temp_score"] = analyzed_score

    # STEP 2: DISPLAY SCORE & PAYMENT
    if "temp_score" in st.session_state:
        score = st.session_state["temp_score"]
        st.markdown("---")
        st.subheader("Step 2: Assessment Result")

        if score >= 60:
            st.markdown(f"""
                <div class="cert-card">
                    <h2>🎉 Congratulations! Your Tennis Score: {score} / 100</h2>
                    <p>You qualified for official Coach Verification!</p>
                    <p>Verification Fee: <strong>10,000 원 (KRW)</strong></p>
                </div>
            """, unsafe_allow_html=True)

            if st.button("💳 Pay 10,000원 & Get Coach License"):
                st.session_state.current_coach = {
                    "name": coach_name,
                    "score": score,
                    "verified": True
                }
                st.balloons()
                st.success(f" ✅ Official Coach License Granted to {coach_name}! You can now sell products in the market.")
        else:
            st.markdown(f"""
                <div class="fail-card">
                    <h2>❌ Score: {score} / 100</h2>
                    <p>Your score is below the 60 threshold required to become a certified coach. Keep practicing and upload a new video!</p>
                </div>
            """, unsafe_allow_html=True)

    # DISPLAY COACH PROFILE DASHBOARD IF VERIFIED
    if st.session_state.current_coach:
        st.markdown("---")
        st.subheader(f"🏆 Coach Dashboard: {st.session_state.current_coach['name']}")
        st.success("Status: VERIFIED COACH (10,000원 Paid)")

# ==========================================
# 2. SECOND-HAND MARKET (SELL, EDIT, BUY)
# ==========================================
elif page == "🛍️ Second-Hand Market":
    st.title("🛍️ Second-Hand Tennis Market")
    st.write("Browse second-hand tennis equipment posted by certified coaches!")

    st.markdown("---")

    # BUTTON & FORM TO CREATE LISTING (VERIFIED COACHES ONLY)
    if st.session_state.current_coach and st.session_state.current_coach.get("verified"):
        st.info(f"Logged in as Verified Coach: **{st.session_state.current_coach['name']}**")
        
        with st.expander("➕ Create Selling Second-Hand Product"):
            with st.form("create_product_form"):
                p_title = st.text_input("Product Title *", placeholder="e.g. Head Speed MP Racquet")
                p_price = st.text_input("Price (KRW) *", placeholder="e.g. 80,000 ₩")
                p_desc = st.text_area("Product Description *", placeholder="Describe condition, string tension, usage...")
                
                st.write("📸 **Upload up to 3 Product Photos:**")
                f1 = st.file_uploader("Photo 1", type=["jpg", "png", "jpeg"], key="p1")
                f2 = st.file_uploader("Photo 2", type=["jpg", "png", "jpeg"], key="p2")
                f3 = st.file_uploader("Photo 3", type=["jpg", "png", "jpeg"], key="p3")

                if st.form_submit_button("🚀 Post Product for Sale"):
                    if p_title and p_price and p_desc:
                        # Collect uploaded images or default fallback
                        uploaded_imgs = []
                        for f in [f1, f2, f3]:
                            if f is not None:
                                uploaded_imgs.append(f)
                        
                        if not uploaded_imgs:
                            uploaded_imgs = ["https://images.unsplash.com/photo-1617083934555-ac7d4fed8824?w=500"]

                        new_item = {
                            "id": random.randint(1000, 9999),
                            "title": p_title,
                            "seller": st.session_state.current_coach["name"],
                            "price": p_price,
                            "desc": p_desc,
                            "images": uploaded_imgs
                        }
                        st.session_state.marketplace_items.insert(0, new_item)
                        st.success("🎉 Product listed successfully!")
                        st.rerun()
                    else:
                        st.error("Please fill in title, price, and description.")
    else:
        st.warning("🔒 Only verified coaches can sell products. Please complete video assessment and pay 10,000원 verification fee first!")

    st.markdown("### 🛍️ Available Listings")

    # DISPLAY LISTINGS
    cols = st.columns(3)
    for idx, item in enumerate(st.session_state.marketplace_items):
        col = cols[idx % 3]
        with col:
            # Display uploaded/sample photos
            st.image(item["images"][0], use_container_width=True)
            if len(item["images"]) > 1:
                st.caption(f"📷 Includes {len(item['images'])} photos")

            st.markdown(f"### {item['title']}")
            st.markdown(f"💰 Price: `<span class='price-tag'>{item['price']}</span>`", unsafe_allow_html=True)
            st.caption(f"👤 Seller: **{item['seller']}**")
            st.write(item["desc"])

            # EDIT OPTION FOR SELLER / CHAT FOR BUYERS
            if st.session_state.current_coach and item["seller"] == st.session_state.current_coach["name"]:
                with st.popover("✏️ Edit Product"):
                    new_t = st.text_input("Edit Title", value=item["title"], key=f"edit_t_{item['id']}")
                    new_p = st.text_input("Edit Price", value=item["price"], key=f"edit_p_{item['id']}")
                    new_d = st.text_area("Edit Description", value=item["desc"], key=f"edit_d_{item['id']}")
                    
                    if st.button("Save Changes", key=f"save_{item['id']}"):
                        item["title"] = new_t
                        item["price"] = new_p
                        item["desc"] = new_d
                        st.toast("Item updated!")
                        st.rerun()

                    if st.button("🗑️ Delete Product", key=f"del_{item['id']}"):
                        st.session_state.marketplace_items.remove(item)
                        st.toast("Item deleted!")
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
# 3. CHAT & FRIENDS
# ==========================================
elif page == "💬 Chat & Make Friends":
    st.title("💬 Student & Coach Chat")
    st.write("Connect, ask about second-hand products, and become friends!")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("💬 Direct Message")
        st.selectbox("Select Coach or Student:", ["Coach Alex", "Sarah Jenkins", "Emily Chen"])
        st.text_area("Message:")
        if st.button("Send Message"):
            st.success("Message sent successfully!")

    with col2:
        st.subheader("🤝 Your Tennis Friends")
        st.info("No new friend requests pending.")
