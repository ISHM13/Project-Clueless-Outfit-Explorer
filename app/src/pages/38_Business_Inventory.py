import logging
logger = logging.getLogger(__name__)

import streamlit as st
import pandas as pd
from modules.nav import SideBarLinks
import requests
from pages._36_Business_Home import load_inventory_df

st.set_page_config(layout='wide')

API_BASE = "http://web-api:4000"

SideBarLinks()

# Defaults for Rebecca
if 'first_name' not in st.session_state:
    st.session_state['first_name'] = 'Rebecca'

if 'business_name' not in st.session_state:
    st.session_state['business_name'] = "Rebecca's Vintage Closet"

st.title("📦 Full Inventory")
st.caption(f"All items for {st.session_state['business_name']}")

st.write("---")

business_id = st.session_state.get('business_id', 1)
inv_df = load_inventory_df(business_id)

# Optional: little filters at top
with st.expander("Filter inventory"):
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        category_filter = st.multiselect(
            "Category",
            sorted(inv_df["Category"].unique()),
            default=None
        )
    with col_f2:
        ethical_filter = st.multiselect(
            "Ethically Sourced",
            ["Yes", "No"],
            default=None
        )

filtered = inv_df.copy()

if category_filter:
    filtered = filtered[filtered["Category"].isin(category_filter)]

if ethical_filter:
    filtered = filtered[filtered["Ethically Sourced"].isin(ethical_filter)]

st.dataframe(
    filtered,
    use_container_width=True,
    hide_index=True
)