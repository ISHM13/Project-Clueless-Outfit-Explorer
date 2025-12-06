import logging
import streamlit as st
from modules.nav import SideBarLinks
import requests
from datetime import datetime

logger = logging.getLogger(__name__)

st.set_page_config(layout='wide')
SideBarLinks()

API_BASE_URL = "http://web-api:4000"

# =============================================================================
# Session State
# =============================================================================

if 'notif_view' not in st.session_state:
    st.session_state.notif_view = 'landing'  # 'landing', 'view', 'detail'

if 'selected_notif' not in st.session_state:
    st.session_state.selected_notif = None

if 'notifications' not in st.session_state:
    st.session_state.notifications = [
        {
            'id': 1,
            'type': 'System notifications',
            'message': 'API sync failed with Zara.',
            'full_message': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. The API connection to Zara inventory system failed at 3:42 PM. Please check the server logs for more details.',
            'read': False,
            'timestamp': datetime.now()
        },
        {
            'id': 2,
            'type': 'User alert',
            'message': '5 new flagged uploads.',
            'full_message': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Five user uploads have been flagged for review. Items include potentially inappropriate content or copyright violations. Please review these items in the moderation queue.',
            'read': False,
            'timestamp': datetime.now()
        },
        {
            'id': 3,
            'type': 'User comments',
            'message': 'I cannot upload new clothes...',
            'full_message': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. User reported: "I cannot upload new clothes to my closet. Every time I try, the app crashes. I have tried reinstalling but the issue persists. Please help!"',
            'read': False,
            'timestamp': datetime.now()
        },
        {
            'id': 4,
            'type': 'User comments',
            'message': 'I cannot sign into the app...',
            'full_message': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. User reported: "I cannot sign into the app since the last update. It keeps saying invalid credentials even though I am using the correct password. I have reset my password twice already."',
            'read': False,
            'timestamp': datetime.now()
        }
    ]

# =============================================================================
# Helper Functions
# =============================================================================

def count_by_type(notif_type):
    return sum(1 for n in st.session_state.notifications if n['type'] == notif_type and not n['read'])

def mark_all_read():
    for n in st.session_state.notifications:
        n['read'] = True

def back_button(target='landing'):
    if st.button("← Back"):
        st.session_state.notif_view = target
        st.session_state.selected_notif = None
        st.rerun()

# =============================================================================
# Page UI
# =============================================================================

# =============================================================================
# LANDING VIEW
# =============================================================================
if st.session_state.notif_view == 'landing':
    st.title('Notifications & Alerts Page')
    
    st.markdown("### Alerts ⚠️")
    
    for notif_type in ['System notifications', 'User alert', 'User comments']:
        col1, col2 = st.columns([4, 1])
        with col1:
            st.write(f"{notif_type}:")
        with col2:
            count = count_by_type(notif_type)
            if count > 0:
                st.markdown(f"<span style='background-color:#EF4444;color:white;padding:2px 10px;border-radius:50%;font-size:14px;'>{count}</span>", unsafe_allow_html=True)
    
    st.write("")
    
    if st.button("🔔 View Notifications & Alerts →", use_container_width=True):
        st.session_state.notif_view = 'view'
        st.rerun()
    
    st.divider()
    
    st.subheader('Issue Notifications')
    
    st.write("**Receiver**")
    receiver = st.text_input("Receiver", placeholder="Please enter receiver's name", label_visibility="collapsed")
    
    st.write("")
    message = st.text_area("Message", placeholder="Type here...", max_chars=200, label_visibility="collapsed", height=150)
    st.caption(f"{len(message)}/200 characters")
    
    st.write("")
    
    if st.button("Send", use_container_width=True, type="primary", disabled=not receiver or not message):
        st.session_state.notifications.append({
            'id': len(st.session_state.notifications) + 1,
            'type': 'System notifications',
            'message': f"Sent to {receiver}: {message[:30]}...",
            'full_message': f"Message sent to {receiver}: {message}",
            'read': False,
            'timestamp': datetime.now()
        })
        st.success(f"Notification sent to {receiver}!")
        st.rerun()

# =============================================================================
# VIEW PAGE - List of Notifications
# =============================================================================
elif st.session_state.notif_view == 'view':
    back_button('landing')
    st.title('View Notifications & Alerts')
    
    unread = [n for n in st.session_state.notifications if not n['read']]
    read = [n for n in st.session_state.notifications if n['read']]
    
    # Unread Section
    st.subheader(f"🔴 Unread ({len(unread)})")
    
    if unread:
        for notif in unread:
            with st.container(border=True):
                col1, col2, col3 = st.columns([0.5, 1, 8])
                with col1:
                    st.markdown("🔴")
                with col2:
                    st.markdown("✉️")
                with col3:
                    st.markdown(f"**{notif['type']}**")
                    st.write(notif['message'])
                
                if st.button("View Details →", key=f"view_{notif['id']}", use_container_width=True):
                    st.session_state.selected_notif = notif
                    st.session_state.notif_view = 'detail'
                    st.rerun()
    else:
        st.info("No unread notifications")
    
    st.divider()
    
    # Read Section
    st.subheader(f"✅ Read ({len(read)})")
    
    if read:
        for notif in read:
            with st.container(border=True):
                col1, col2, col3 = st.columns([0.5, 1, 8])
                with col1:
                    st.markdown("⚪")
                with col2:
                    st.markdown("✉️")
                with col3:
                    st.markdown(f"**{notif['type']}**")
                    st.write(notif['message'])
                
                if st.button("View Details →", key=f"view_read_{notif['id']}", use_container_width=True):
                    st.session_state.selected_notif = notif
                    st.session_state.notif_view = 'detail'
                    st.rerun()
    else:
        st.info("No read notifications")

# =============================================================================
# DETAIL VIEW - Single Notification
# =============================================================================
elif st.session_state.notif_view == 'detail':
    back_button('view')
    
    notif = st.session_state.selected_notif
    
    if notif:
        st.title(notif['type'])
        
        st.markdown(f"**Subject:** {notif['message']}")
        st.caption(f"Received: {notif['timestamp'].strftime('%B %d, %Y at %I:%M %p')}")
        
        st.divider()
        
        st.write(notif.get('full_message', notif['message']))
        
        st.divider()
        
        col1, col2 = st.columns(2)
        with col1:
            if notif['read']:
                if st.button("🔴 Mark as Unread", use_container_width=True, type="primary"):
                    for n in st.session_state.notifications:
                        if n['id'] == notif['id']:
                            n['read'] = False
                    st.success("Marked as unread!")
                    st.session_state.notif_view = 'view'
                    st.rerun()
            else:
                if st.button("✅ Mark as Read", use_container_width=True, type="primary"):
                    for n in st.session_state.notifications:
                        if n['id'] == notif['id']:
                            n['read'] = True
                    st.success("Marked as read!")
                    st.session_state.notif_view = 'view'
                    st.rerun()
        with col2:
            if st.button("🗑️ Delete", use_container_width=True):
                st.session_state.notifications = [n for n in st.session_state.notifications if n['id'] != notif['id']]
                st.success("Notification deleted!")
                st.session_state.notif_view = 'view'
                st.rerun()
    else:
        st.error("Notification not found")
        st.session_state.notif_view = 'view'
        st.rerun()