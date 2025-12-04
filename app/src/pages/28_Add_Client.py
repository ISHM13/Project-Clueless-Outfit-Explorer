import streamlit as st
import requests
from streamlit_extras.app_logo import add_logo
from modules.nav import SideBarLinks

# Initialize sidebar
SideBarLinks()

st.title("Add New Client")

# Initialize session state for modal
if "show_success_modal" not in st.session_state:
    st.session_state.show_success_modal = False
if "success_client_name" not in st.session_state:
    st.session_state.success_client_name = ""
if "reset_form" not in st.session_state:
    st.session_state.reset_form = False
if "form_key_counter" not in st.session_state:
    st.session_state.form_key_counter = 0

# Define the success dialog function
@st.dialog("Success")
def show_success_dialog(client_name):
    st.markdown(f"### {client_name} has been successfully added to the system!")
    
    # Create two buttons side by side
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Return to Client Directory", use_container_width=True):
            st.session_state.show_success_modal = False
            st.session_state.success_client_name = ""
            st.switch_page("pages/27_Client_Prof.py")
    
    with col2:
        if st.button("Add Another Client", use_container_width=True):
            st.session_state.show_success_modal = False
            st.session_state.success_client_name = ""
            st.session_state.reset_form = True
            st.rerun()

# Handle form reset
if st.session_state.reset_form:
    st.session_state.form_key_counter += 1
    st.session_state.reset_form = False

# API endpoint
API_URL = "http://web-api:4000/ngo/ngos"

# Create a form for NGO details with dynamic key to force reset
with st.form(f"add_ngo_form_{st.session_state.form_key_counter}"):
    st.subheader("Client Information")

    # Required fields
    name = st.text_input("Company Name *")
    company_id = st.number_input("Company ID *", min_value=100000, max_value=999999, value=160206)
    business_type = st.text_input("Business Type *")
    contact_name = st.text_input("Contact Name *")
    street = st.text_input("Address - Street *")
    city = st.text_input("Address - City *")
    state = st.text_input("Address - State *")
    country = st.text_input("Address - Country *")
    zip_code = st.text_input("Address - Zip *")
    

    # Form submission button
    submitted = st.form_submit_button("Add Client")

    if submitted:
        # Validate required fields
        if not all([name, company_id, business_type, contact_name, street, city, state, country, zip_code]):
            st.error("Please fill in all required fields marked with *")
        else:
            # Prepare the data for API
            ngo_data = {
                "Company Name": name,
                "Company ID":  company_id,
                "Business Type": business_type,
                "Contact Name": contact_name,
                "Street": street,
                "City": city,
                "State": state,
                "Country": country,
                "Zip": zip_code
            }

            try:
                # Send POST request to API
                response = requests.post(API_URL, json=ngo_data)

                if response.status_code == 201:
                    # Store NGO name and show modal
                    st.session_state.show_success_modal = True
                    st.session_state.success_client_name = name
                    st.rerun()
                else:
                    st.error(
                        f"Failed to add Client: {response.json().get('error', 'Unknown error')}"
                    )

            except requests.exceptions.RequestException as e:
                st.error(f"Error connecting to the API: {str(e)}")
                st.info("Please ensure the API server is running")

# Show success modal if NGO was added successfully
if st.session_state.show_success_modal:
    show_success_dialog(st.session_state.success_client_name)

# Add a button to return to the NGO Directory
if st.button("Return to Client Directory"):
    st.switch_page("pages/27_Client_Prof.py")
