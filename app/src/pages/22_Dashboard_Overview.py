import logging
import streamlit as st
from modules.nav import SideBarLinks
import requests
import pandas as pd
import altair as alt

logger = logging.getLogger(__name__)

st.set_page_config(layout='wide')
SideBarLinks()

API_BASE_URL = "http://web-api:4000"

# =============================================================================
# API Functions
# =============================================================================

def get_admin_users():
    try:
        response = requests.get(f"{API_BASE_URL}/g/admin/users", timeout=10)
        if response.status_code == 200:
            return True, response.json()
        return False, f"HTTP {response.status_code}"
    except requests.exceptions.RequestException as e:
        return False, str(e)

def get_admin_logs():
    try:
        response = requests.get(f"{API_BASE_URL}/g/admin/logs", timeout=10)
        if response.status_code == 200:
            return True, response.json()
        return False, f"HTTP {response.status_code}"
    except requests.exceptions.RequestException as e:
        return False, str(e)

def get_trends():
    try:
        response = requests.get(f"{API_BASE_URL}/a/analytics/trend", timeout=10)
        if response.status_code == 200:
            return True, response.json()
        return False, f"HTTP {response.status_code}"
    except requests.exceptions.RequestException as e:
        return False, str(e)

def get_demand():
    try:
        response = requests.get(f"{API_BASE_URL}/a/analytics/demand", timeout=10)
        if response.status_code == 200:
            return True, response.json()
        return False, f"HTTP {response.status_code}"
    except requests.exceptions.RequestException as e:
        return False, str(e)

# =============================================================================
# Load Data
# =============================================================================

success_users, users_data = get_admin_users()
success_logs, logs_data = get_admin_logs()

# =============================================================================
# Page UI - Matching Wireframe
# =============================================================================

st.title('Dashboard & Overview Page')

# -----------------------------------------------------------------------------
# Top KPIs Section (matches wireframe)
# -----------------------------------------------------------------------------
st.subheader('Top KPIs')

col1, col2, col3 = st.columns(3)

with col1:
    # Large metric - Total Users
    total_users = len(users_data) if success_users else 0
    st.metric(label="Total Users", value=f"{total_users:,}")

with col2:
    # Total Business Clients
    st.metric(label="Total Business Clients", value="96")

with col3:
    # Pending Approvals
    pending = len(logs_data.get('business_logs', [])) if success_logs else 0
    st.metric(label="Pending Approvals", value=pending, help="Users / Retailers")

st.divider()

# -----------------------------------------------------------------------------
# Weekly New Signups Section
# -----------------------------------------------------------------------------
st.subheader('Weekly New Signups')
st.caption("Users / Businesses / Daily Outfits Uploads / Wishlist Conversions")

# Button to view graphs/charts
if st.button("📊 Graphs / Charts ↓", use_container_width=True):
    st.session_state['show_charts'] = not st.session_state.get('show_charts', False)

if st.session_state.get('show_charts', False):
    # Sample data for charts (would come from analytics in real app)
    days = ["Su", "M", "T", "W", "Th", "F", "S"]
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Users Chart
        st.write("**Users**")
        users_df = pd.DataFrame({
            "Day": days,
            "Count": [550, 625, 475, 600, 350, 750, 675]
        })
        chart = alt.Chart(users_df).mark_bar(color="#A78BFA").encode(
            x=alt.X("Day:N", sort=days),
            y=alt.Y("Count:Q", scale=alt.Scale(domain=[0, 800]))
        ).properties(height=200)
        st.altair_chart(chart, use_container_width=True)
        
        # Daily Outfit Uploads Chart
        st.write("**Daily Outfit Uploads**")
        uploads_df = pd.DataFrame({
            "Day": days,
            "Count": [220, 150, 190, 160, 80, 200, 325]
        })
        chart = alt.Chart(uploads_df).mark_bar(color="#A78BFA").encode(
            x=alt.X("Day:N", sort=days),
            y=alt.Y("Count:Q", scale=alt.Scale(domain=[0, 700]))
        ).properties(height=200)
        st.altair_chart(chart, use_container_width=True)
    
    with col2:
        # Businesses Chart
        st.write("**Businesses**")
        biz_df = pd.DataFrame({
            "Day": days,
            "Count": [300, 450, 400, 500, 250, 600, 550]
        })
        chart = alt.Chart(biz_df).mark_bar(color="#A78BFA").encode(
            x=alt.X("Day:N", sort=days),
            y=alt.Y("Count:Q", scale=alt.Scale(domain=[0, 800]))
        ).properties(height=200)
        st.altair_chart(chart, use_container_width=True)
        
        # Wishlist Conversions Chart
        st.write("**Wishlist Conversions**")
        wishlist_df = pd.DataFrame({
            "Day": days,
            "Count": [400, 250, 335, 420, 550, 600, 750]
        })
        chart = alt.Chart(wishlist_df).mark_bar(color="#A78BFA").encode(
            x=alt.X("Day:N", sort=days),
            y=alt.Y("Count:Q", scale=alt.Scale(domain=[0, 800]))
        ).properties(height=200)
        st.altair_chart(chart, use_container_width=True)

st.divider()

# -----------------------------------------------------------------------------
# Navigation Buttons (matches wireframe)
# -----------------------------------------------------------------------------
if st.button("🏢 Business Client Management →", use_container_width=True):
    st.switch_page('pages/23_Business_Client_Mgmt.py')

if st.button("📢 Announcement →", use_container_width=True):
    st.switch_page('pages/25_Notif_Alert.py')