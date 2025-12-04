import logging
logger = logging.getLogger(__name__)
import streamlit as st
from modules.nav import SideBarLinks
import requests
from datetime import datetime

st.set_page_config(layout = 'wide')

SideBarLinks()

st.title('Notifications & Alerts Page')

# Initialize session state
if 'notifications' not in st.session_state:
    st.session_state.notifications = [
        {
            'type': 'System notifications',
            'message': 'API sync failed with Zara.',
            'read': False,
            'timestamp': datetime.now()
        },
        {
            'type': 'User alert',
            'message': '5 new flagged uploads.',
            'read': False,
            'timestamp': datetime.now()
        },
        {
            'type': 'User comments',
            'message': 'I cannot upload new clothes...',
            'read': False,
            'timestamp': datetime.now()
        },
        {
            'type': 'User comments',
            'message': 'I cannot sign into the app...',
            'read': False,
            'timestamp': datetime.now()
        }
    ]

# Helper functions
def count_notifications_by_type(notification_type):
    return sum(1 for n in st.session_state.notifications if n['type'] == notification_type and not n['read'])

def mark_all_as_read():
    for n in st.session_state.notifications:
        n['read'] = True

st.write('\n\n')
st.write('## Alert Summary')

# Display alert counts
col1, col2, col3 = st.columns(3)
with col1:
    system_count = count_notifications_by_type('System notifications')
    st.metric(label="System Notifications", value=system_count)
with col2:
    user_alerts_count = count_notifications_by_type('User alert')
    st.metric(label="User Alerts", value=user_alerts_count)
with col3:
    user_comments_count = count_notifications_by_type('User comments')
    st.metric(label="User Comments", value=user_comments_count)

st.divider()

# Tabs for different views
tab1, tab2 = st.tabs(["View Notifications", "Issue Notification"])

with tab1:
    st.write('\n\n')
    st.write('## Active Notifications')
    
    unread_notifications = [n for n in st.session_state.notifications if not n['read']]
    
    if not unread_notifications:
        st.info("No unread notifications")
    else:
        for idx, notification in enumerate(unread_notifications):
            col1, col2 = st.columns([1, 20])
            with col1:
                st.markdown("🔴")
            with col2:
                st.markdown(f"**{notification['type']}**")
                st.write(notification['message'])
            st.divider()
    
    st.write('\n\n')
    st.write('## Actions')
    
    col1, col2 = st.columns([3, 1])
    with col1:
        action = st.selectbox("Select action", ["Mark as read", "Delete", "Archive"], label_visibility="collapsed")
    with col2:
        if st.button("Enter", use_container_width=True):
            if action == "Mark as read":
                mark_all_as_read()
                st.success("All notifications marked as read!")
                st.rerun()
            elif action == "Delete":
                st.session_state.notifications = [n for n in st.session_state.notifications if n['read']]
                st.success("Unread notifications deleted!")
                st.rerun()
            elif action == "Archive":
                mark_all_as_read()
                st.success("All notifications archived!")
                st.rerun()

with tab2:
    st.write('\n\n')
    st.write('## Issue Notifications')
    
    st.write("**Receiver**")
    receiver = st.text_input("Receiver", placeholder="Please enter receiver's name", label_visibility="collapsed")
    
    st.write('\n')
    message = st.text_area("Message", placeholder="Type here...", max_chars=200, label_visibility="collapsed", height=150)
    
    char_count = len(message)
    st.caption(f"{char_count}/200 characters")
    
    st.write('\n')
    if st.button("Send", use_container_width=True, disabled=not receiver or not message):
        st.success(f"Notification sent to {receiver}!")
        st.session_state.notifications.append({
            'type': 'System notifications',
            'message': f"New notification: {message[:30]}...",
            'read': False,
            'timestamp': datetime.now()
        })
        st.rerun()
