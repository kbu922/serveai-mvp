# Streamlit logic inside Module 4: Academy & Residency
st.markdown("## 🏛️ Global Tennis Academy & Residency Programs")

subpage = st.radio(
    "Select Enrollment Type:",
    ["Individual Enrollment", "👥 Group Buying & Voting Hub"],
    horizontal=True
)

if subpage == "Individual Enrollment":
    # Existing single booking workflow
    render_individual_residency_booking()

elif subpage == "👥 Group Buying & Voting Hub":
    # Group campaign & voting subpage
    st.subheader("Group Training Campaigns & Member Discounts")
    
    # Campus Preview
    col1, col2 = st.columns(2)
    with col1:
        st.image("campus_aerial.jpg", caption="Main Training Center & Courts")
    with col2:
        st.image("residence_interior.jpg", caption="Athlete Suite Living Quarters")
        
    # Group Campaign Progress
    st.write("### Active Group Campaign: 1-Week Intensive (Group Rate)")
    members_joined = len(st.session_state.get("residency_group_votes", []))
    target = 10
    
    st.progress(min(members_joined / target, 1.0))
    st.caption(f"{members_joined}/{target} Athletes Joined — **Unlock $150 Off/Person at 10 Athletes**")
    
    if st.button("Vote & Join Group Campaign"):
        st.session_state["residency_group_votes"].append(st.session_state.get("user", "Anonymous"))
        st.success("You joined the group residency campaign!")
