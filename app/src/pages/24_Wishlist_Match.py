import logging
logger = logging.getLogger(__name__)
import streamlit as st
from modules.nav import SideBarLinks
import requests
from datetime import datetime
import pandas as pd

st.set_page_config(layout = 'wide')

SideBarLinks()

# Initialize session state
if 'wishlist_items' not in st.session_state:
    st.session_state.wishlist_items = [
        {
            'name': 'White winter hood',
            'wishlist_count': 36,
            'business': 'Zara International',
            'sku': '14Kp569',
            'mapped': False
        },
        {
            'name': 'Black leather jacket',
            'wishlist_count': 28,
            'business': 'H&M',
            'sku': 'HM7894',
            'mapped': False
        },
        {
            'name': 'Blue denim jeans',
            'wishlist_count': 22,
            'business': 'Levi\'s',
            'sku': 'LV5012',
            'mapped': False
        }
    ]

st.title('Wishlist Matching Page')

st.write('\n\n')
st.write('## Wishlist Overview')

# Navigation buttons
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🌟 Top Wishlisted →", use_container_width=True):
        st.session_state.view = 'top_wishlisted'
with col2:
    if st.button("📦 Unmatched Items →", use_container_width=True):
        st.session_state.view = 'unmatched'
with col3:
    if st.button("🔗 Mapping Suggestions →", use_container_width=True):
        st.session_state.view = 'mapping'

st.caption("Mapping Suggestions Wishlist item to retailer SKU")

st.divider()

st.write('\n\n')
st.write('## Inventory Status')

col1, col2 = st.columns(2)
with col1:
    st.metric(label="Inventory Added", value="12")
with col2:
    st.metric(label="New Collection in Pipeline", value="8")

st.divider()

# Mapping Suggestions Section
st.write('\n\n')
st.write('## Mapping Suggestions')

# Top Wishlist Item
st.write("### Top Wishlist")

top_item = st.session_state.wishlist_items[0]

col1, col2 = st.columns([1, 10])
with col1:
    st.markdown("⭐")
with col2:
    st.markdown(f"**{top_item['name']}**")
    st.caption(f"# in Wishlist {top_item['wishlist_count']}")

st.write('\n')

# Mapping Suggestion Details
st.write("### Mapping Suggestion")

col1, col2, col3 = st.columns([1, 8, 2])
with col1:
    st.markdown("ℹ️")
with col2:
    st.markdown(f"**Business:** {top_item['business']}")
    st.markdown(f"**SKU:** {top_item['sku']}")
with col3:
    # Placeholder for product image
    st.markdown("<p style='font-size: 60px; margin: 0;'>🧥</p>", unsafe_allow_html=True)

st.write('\n\n')

# Map button
if st.button("Map", use_container_width=True, type="primary"):
    top_item['mapped'] = True
    st.success(f"Successfully mapped '{top_item['name']}' to {top_item['business']} SKU: {top_item['sku']}")
    st.rerun()

st.divider()

# Additional sections in tabs
tab1, tab2, tab3 = st.tabs(["All Wishlist Items", "Unmapped Items", "Mapping History"])

with tab1:
    st.write('\n\n')
    st.write('## All Wishlist Items')
    
    df = pd.DataFrame(st.session_state.wishlist_items)
    st.dataframe(
        df[['name', 'wishlist_count', 'business', 'sku', 'mapped']],
        use_container_width=True,
        hide_index=True
    )

with tab2:
    st.write('\n\n')
    st.write('## Unmatched Items')
    
    unmapped = [item for item in st.session_state.wishlist_items if not item['mapped']]
    
    if unmapped:
        df_unmapped = pd.DataFrame(unmapped)
        st.dataframe(
            df_unmapped[['name', 'wishlist_count']],
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("All items have been mapped!")

with tab3:
    st.write('\n\n')
    st.write('## Mapping History')
    
    mapped = [item for item in st.session_state.wishlist_items if item['mapped']]
    
    if mapped:
        df_mapped = pd.DataFrame(mapped)
        st.dataframe(
            df_mapped[['name', 'business', 'sku', 'wishlist_count']],
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No items mapped yet")
