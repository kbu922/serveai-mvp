import streamlit as st

# ==========================================
# 0. PAGE CONFIG & STYLING
# ==========================================
st.set_page_config(
    page_title="Tennis Coach & Book Exchange",
    page_icon="🎾",
    layout="wide"
)

st.markdown("""
    <style>
    .stApp {
        background-color: #F8F9FA;
        color: #212529;
    }
    .cert-box {
        background-color: #E8F5E9;
        border: 2px solid #2E7D32;
        border-radius: 10px;
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

# Initialize Session State
if "coaches" not in st.session_state:
    st.session_state.coaches = []

if "marketplace_items" not in st.session_state:
    st.session_state.marketplace_items = [
        {
            "title": "Essential Tennis Tactics Book (책)",
            "seller": "Coach Alex",
            "price": "15,000 ₩",
            "desc": "Great book for beginners wanting to master court positioning.",
            "image": "https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=500"
        }
    ]

if "friends" not in st.session_state:
    st.session_state.friends = []

# ==========================================
# SIDEBAR NAVIGATION
# ==========================================
st.sidebar.title("🎾 Navigation")
page = st.sidebar.radio("Go to:", [
    "🏆 Coach Certification (10,000₩)", 
    "📚 Marketplace (Books & Gear)", 
    "💬 Chat & Make Friends"
])

# ==========================================
# 1. COACH CERTIFICATION (SCORE >= 60)
# ==========================================
if page == "🏆 Coach Certification (10,000₩)":
    st.title("🏆 Register as a Tennis Coach")
    st.write("If your tennis score is **60 or above**, you are eligible to get a Coach Certificate for 10,000₩ and list items on our market!")

    st.markdown("---")

    with st.form("coach_reg_form"):
        name = st.text_input("Your Name *")
        email = st.text_input("Email *")
        score = st.number_input("Enter Your Tennis Score (0 - 100) *", min_value=0, max_value=100, value=65)
        bio = st.text_area("Short Bio")
        
        submitted = st.form_submit_button("Submit Score & Verify")

    if submitted:
        if score >= 60:
            st.success(f"🎉 Congratulations {name}! Your score of {score} qualifies you to become a Coach.")
            
            # 10,000 KRW Certification Fee Payment Block
            st.markdown("""
                <div class="cert-box">
                    <h3>📜 Official Coach Certificate License</h3>
                    <p>License Fee: <strong>10,000 원 (KRW)</strong></p>
                    <p>Unlocks: Selling rights for Tennis Books (책) & direct student messaging.</p>
                </div>
            """, unsafe_allow_html=True)

            if st.button("💳 Pay 10,000원 & Receive Coach License"):
                new_coach = {"name": name, "email": email, "score": score, "bio": bio, "certified": True}
                st.session_state.coaches.append(new_coach)
                st.balloons()
                st.success(" ✅ License Issued! You are now a Certified Coach and can start posting items for sale.")
        else:
            st.error(f"❌ Your score ({score}) is below 60. Practice more to reach 60+ and unlock coach registration!")

# ==========================================
# 2. MARKETPLACE (BOOKS & GEAR)
# ==========================================
elif page == "📚 Marketplace (Books & Gear)":
    st.title("📚 Coach Book & Gear Marketplace")
    st.write("Browse tennis books (책) and gear listed by our certified coaches.")

    st.markdown("---")

    # EXPANDER: COACH-ONLY LISTING CREATION
    if st.session_state.coaches:
        coach_names = [c["name"] for c in st.session_state.coaches]
        
        with st.expander("➕ Certified Coaches Only: Post an Item (Book / Gear)"):
            with st.form("add_item_form"):
                seller = st.selectbox("Select Your Certified Coach Account *", coach_names)
                title = st.text_input("Item Title (e.g. Tennis Strategy Book / 책) *")
                price = st.text_input("Price (e.g. 12,000 ₩) *")
                desc = st.text_area("Item Description *")
                photo = st.file_uploader("Upload Item Photo", type=["jpg", "png", "jpeg"])

                if st.form_submit_button("🚀 Upload Item"):
                    if title and price and desc:
                        img_url = "https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=500"
                        if photo:
                            img_url = photo

                        new_item = {
                            "title": title,
                            "seller": seller,
                            "price": price,
                            "desc": desc,
                            "image": img_url
                        }
                        st.session_state.marketplace_items.insert(0, new_item)
                        st.success("🎉 Your item has been listed successfully!")
                        st.rerun()
                    else:
                        st.error("Please fill in all required fields.")
    else:
        st.info("💡 Only certified coaches can post items. Complete certification first!")

    st.markdown("### 🛍️ Available Listings")

    # SHOW LISTINGS IN 3-COLUMN GRID
    cols = st.columns(3)
    for idx, item in enumerate(st.session_state.marketplace_items):
        col = cols[idx % 3]
        with col:
            st.image(item["image"], use_container_width=True)
            st.markdown(f"### {item['title']}")
            st.markdown(f"💰 Price: `<span class='price-tag'>{item['price']}</span>`", unsafe_allow_html=True)
            st.caption(f"👤 Seller: **{item['seller']}**")
            st.write(item["desc"])
            
            # CHAT & FRIEND ACTION BUTTONS
            b1, b2 = st.columns(2)
            with b1:
                if st.button(f"💬 Chat", key=f"chat_{idx}"):
                    st.toast(f"Opening chat with {item['seller']}...")
            with b2:
                if st.button(f"🤝 Add Friend", key=f"friend_{idx}"):
                    if item["seller"] not in st.session_state.friends:
                        st.session_state.friends.append(item["seller"])
                        st.toast(f"🎉 You are now friends with {item['seller']}!")
                    else:
                        st.toast(f"You are already friends with {item['seller']}!")
            st.markdown("---")

# ==========================================
# 3. CHAT & FRIENDS
# ==========================================
elif page == "💬 Chat & Make Friends":
    st.title("💬 Student-Coach Connect & Friends")
    st.write("Chat with coaches, ask about their books/lessons, and grow your tennis circle!")

    st.markdown("---")

    col_c1, col_c2 = st.columns([1, 1])

    with col_c1:
        st.subheader("🤝 Your Tennis Friends")
        if st.session_state.friends:
            for friend in st.session_state.friends:
                st.success(f"🎾 **{friend}** (Coach Friend)")
        else:
            st.info("You haven't added any coach friends yet. Visit the Marketplace to send friend requests!")

    with col_c2:
        st.subheader("💬 Direct Message")
        if st.session_state.coaches:
            target_coach = st.selectbox("Select Coach to Message:", [c["name"] for c in st.session_state.coaches])
            msg = st.text_area("Your Message:")
            if st.button("📤 Send Message"):
                if msg:
                    st.toast(f"Message sent to {target_coach}!")
                    st.success("Message delivered!")
        else:
            st.write("No coaches registered yet.")
