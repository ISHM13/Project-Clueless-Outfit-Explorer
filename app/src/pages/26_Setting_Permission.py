import logging
logger = logging.getLogger(__name__)
import streamlit as st
from modules.nav import SideBarLinks
import requests
from datetime import datetime

st.set_page_config(layout = 'wide')

SideBarLinks()

# Initialize session state
if 'admins' not in st.session_state:
    st.session_state.admins = [
        {'name': 'Lucas Fu', 'user_id': '111111111', 'role': 'Super Admin'},
        {'name': 'Alvin Wong', 'user_id': '222222222', 'role': 'Content Moderator'}
    ]

if 'usage_violations' not in st.session_state:
    st.session_state.usage_violations = [
        {
            'name': 'Minsang Lee',
            'user_id': 'MD9877',
            'reason': 'Invalid email'
        },
        {
            'name': 'Saba Khundadze',
            'user_id': 'KN2374',
            'reason': 'Password Violation'
        }
    ]

st.title('Settings & Permissions Page')

st.write('\n\n')

# Create tabs for different sections
tab1, tab2 = st.tabs(["Admin Management", "Remove Usage Access"])

with tab1:
    st.write('\n\n')
    st.write('## Add Admin')
    
    with st.form("add_admin_form"):
        st.markdown("**Name**")
        admin_name = st.text_input("Name", value="Nicolas", label_visibility="collapsed")
        
        st.markdown("**User ID**")
        admin_user_id = st.text_input("User ID", value="000000000", label_visibility="collapsed")
        
        st.markdown("**Admin Roles**")
        admin_role = st.selectbox(
            "Admin Roles",
            ["Super Admin", "Content Moderator", "Data Analyst", "Support Staff"],
            label_visibility="collapsed"
        )
        
        st.write('\n')
        
        submitted = st.form_submit_button("Add", use_container_width=True, type="primary")
        
        if submitted:
            if admin_name and admin_user_id:
                new_admin = {
                    'name': admin_name,
                    'user_id': admin_user_id,
                    'role': admin_role
                }
                st.session_state.admins.append(new_admin)
                st.success(f"Admin {admin_name} has been added successfully!")
                st.rerun()
            else:
                st.error("Please fill in all fields")
    
    st.divider()
    
    st.write('\n\n')
    st.write('## Remove Admin')
    
    search_admin = st.text_input("Search Admin", placeholder="Search", label_visibility="collapsed")
    st.caption("Search by Name or User ID")
    
    st.write('\n')
    
    # Display current admins
    if st.session_state.admins:
        st.write("**Current Admins:**")
        for admin in st.session_state.admins:
            col1, col2, col3 = st.columns([3, 2, 1])
            with col1:
                st.write(f"**{admin['name']}**")
            with col2:
                st.write(f"ID: {admin['user_id']}")
            with col3:
                if st.button("❌", key=f"remove_admin_{admin['user_id']}"):
                    st.session_state.admins = [a for a in st.session_state.admins if a['user_id'] != admin['user_id']]
                    st.success(f"Removed {admin['name']}")
                    st.rerun()
    
    st.write('\n')
    
    if st.button("Remove", use_container_width=True):
        if search_admin:
            st.info(f"Searching for: {search_admin}")
        else:
            st.warning("Please enter a name or User ID to search")

with tab2:
    st.write('\n\n')
    
    # Alerts section
    col1, col2 = st.columns([5, 1])
    with col1:
        st.markdown("## 🔺 Alerts")
    
    st.write("**Users with usage violation**")
    
    violation_count = len(st.session_state.usage_violations)
    if violation_count > 0:
        st.markdown(f"<span style='background-color:#FF4B4B;color:white;padding:5px 12px;border-radius:50%;font-weight:bold;'>{violation_count}</span>", unsafe_allow_html=True)
    
    st.write('\n\n')
    
    # Display users with violations
    for violation in st.session_state.usage_violations:
        with st.container():
            col1, col2 = st.columns([1, 10])
            with col1:
                st.markdown("🔴")
            with col2:
                col_a, col_b = st.columns([8, 2])
                with col_a:
                    st.markdown(f"**{violation['name']}**")
                    st.write(f"User ID: {violation['user_id']}")
                    st.write(f"Reason: {violation['reason']}")
                with col_b:
                    st.markdown("👤")
            
            st.divider()
    
    st.write('\n\n')
    st.write('## User search')
    
    search_user = st.text_input("Search User", placeholder="Search", label_visibility="collapsed")
    st.caption("Search by Name or User ID")
    
    st.write('\n')
    
    if st.button("Remove", use_container_width=True, key="remove_user_access"):
        if search_user:
            # Check if user is in violations list
            user_found = any(v['user_id'] == search_user or v['name'].lower() == search_user.lower() 
                           for v in st.session_state.usage_violations)
            if user_found:
                st.session_state.usage_violations = [
                    v for v in st.session_state.usage_violations 
                    if v['user_id'] != search_user and v['name'].lower() != search_user.lower()
                ]
                st.success(f"Removed user: {search_user}")
                st.rerun()
            else:
                st.warning("User not found in violations list")
        else:
            st.warning("Please enter a name or User ID to search")