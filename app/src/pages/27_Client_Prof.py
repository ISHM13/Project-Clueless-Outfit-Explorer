import logging
logger = logging.getLogger(__name__)
import streamlit as st
from modules.nav import SideBarLinks
import requests

st.set_page_config(layout='wide')

SideBarLinks()

# Initialize session state
if 'clients' not in st.session_state:
    st.session_state.clients = [
        {
            'id': 1,
            'company_name': 'Zara International',
            'company_id': 160206,
            'business_type': 'Fast fashion',
            'contact_name': 'Adam Smith',
            'street': '888 Boylston Street',
            'city': 'Boston',
            'state': 'MA',
            'country': 'USA',
            'zip': '02199'
        },
        {
            'id': 2,
            'company_name': 'H&M',
            'company_id': 245789,
            'business_type': 'Retail',
            'contact_name': 'Jane Doe',
            'street': '123 Fashion Ave',
            'city': 'Boston',
            'state': 'MA',
            'country': 'USA',
            'zip': '02101'
        }
    ]

if 'selected_client' not in st.session_state:
    st.session_state.selected_client = None

if 'view_mode' not in st.session_state:
    st.session_state.view_mode = 'list'  # 'list', 'profile', 'add'

if 'show_success_modal' not in st.session_state:
    st.session_state.show_success_modal = False

if 'success_client_name' not in st.session_state:
    st.session_state.success_client_name = ""

if 'reset_form' not in st.session_state:
    st.session_state.reset_form = False

if 'form_key_counter' not in st.session_state:
    st.session_state.form_key_counter = 0

# API endpoint
API_URL = "http://web-api:4000/ngo/ngos"

# Success dialog
@st.dialog("Success")
def show_success_dialog(client_name):
    st.markdown(f"### {client_name} has been successfully added to the system!")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Return to Client Directory", use_container_width=True):
            st.session_state.show_success_modal = False
            st.session_state.success_client_name = ""
            st.session_state.view_mode = 'list'
            st.rerun()
    
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

# Show success modal if triggered
if st.session_state.show_success_modal:
    show_success_dialog(st.session_state.success_client_name)

# List View
if st.session_state.view_mode == 'list':
    st.title('Business Client Profile')
    
    st.write('\n\n')
    
    # Search and filter
    col1, col2 = st.columns([5, 1])
    with col1:
        search = st.text_input("Search", placeholder="Search", label_visibility="collapsed")
    with col2:
        st.button("🔀 Filter")
    
    # Display clients
    for client in st.session_state.clients:
        with st.container():
            st.markdown(f"**Name**")
            st.write(client['company_name'])
            
            st.markdown(f"**Company ID**")
            st.write(client['company_id'])
            
            st.markdown(f"**Business Type**")
            st.write(client['business_type'])
            
            st.markdown(f"**Contact Person**")
            st.write(f"Name: {client['contact_name']}")
            
            if st.button(f"Business Client Profile →", key=f"profile_{client['id']}", use_container_width=True):
                st.session_state.selected_client = client
                st.session_state.view_mode = 'profile'
                st.rerun()
            
            st.divider()
    
    # Action buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Edit", use_container_width=True):
            st.info("Select a client to edit")
    with col2:
        if st.button("Add", use_container_width=True):
            st.session_state.view_mode = 'add'
            st.rerun()

# Profile View
elif st.session_state.view_mode == 'profile':
    col1, col2 = st.columns([1, 10])
    with col1:
        if st.button("← Back"):
            st.session_state.view_mode = 'list'
            st.rerun()
    with col2:
        st.title('Business Client Profile')
    
    st.write('\n\n')
    
    # Search bar
    search = st.text_input("Search", placeholder="Search", label_visibility="collapsed")
    
    st.write('\n\n')
    st.write('## Profile')
    
    client = st.session_state.selected_client
    
    st.markdown("**Name**")
    st.write(client['company_name'])
    
    st.markdown("**Company ID**")
    st.write(client['company_id'])
    
    st.markdown("**Business Type**")
    st.write(client['business_type'])
    
    st.markdown("**Address**")
    full_address = f"{client['street']}, {client['city']}, {client['state']} {client['zip']}, {client['country']}"
    st.write(full_address)
    
    st.markdown("**Contact**")
    st.write(client['contact_name'])
    
    st.write('\n\n')
    
    if st.button("View uploaded document →", use_container_width=True):
        st.info("Document viewer coming soon")
    
    st.write('\n\n')
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Remove", use_container_width=True):
            st.session_state.clients = [c for c in st.session_state.clients if c['id'] != client['id']]
            st.session_state.view_mode = 'list'
            st.success(f"{client['company_name']} has been removed")
            st.rerun()
    with col2:
        if st.button("Next", use_container_width=True, type="primary"):
            st.info("Navigate to next client")

# Add Client View
elif st.session_state.view_mode == 'add':
    col1, col2 = st.columns([1, 10])
    with col1:
        if st.button("← Back"):
            st.session_state.view_mode = 'list'
            st.rerun()
    with col2:
        st.title('Add Business Client')
    
    st.write('\n\n')
    st.write('## Business Profile')
    
    with st.form(f"add_client_form_{st.session_state.form_key_counter}"):
        st.subheader("Client Information")
        
        # Required fields matching your code
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
                    "Company ID": company_id,
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
                        # Add to session state
                        new_client = {
                            'id': len(st.session_state.clients) + 1,
                            'company_name': name,
                            'company_id': company_id,
                            'business_type': business_type,
                            'contact_name': contact_name,
                            'street': street,
                            'city': city,
                            'state': state,
                            'country': country,
                            'zip': zip_code
                        }
                        
                        st.session_state.clients.append(new_client)
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
    
    # Add a button to return to the Client Directory
    if st.button("Return to Client Directory"):
        st.session_state.view_mode = 'list'
        st.rerun()
