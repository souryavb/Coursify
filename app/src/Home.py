##################################################
# This is the main/entry-point file for the 
# sample application for your project
##################################################

# Set up basic logging infrastructure
import logging
logging.basicConfig(format='%(filename)s:%(lineno)s:%(levelname)s -- %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# import the main streamlit library as well
# as SideBarLinks function from src/modules folder
import streamlit as st
from modules.nav import SideBarLinks

# streamlit supports reguarl and wide layout (how the controls
# are organized/displayed on the screen).
st.set_page_config(layout = 'wide')

# If a user is at this page, we assume they are not 
# authenticated.  So we change the 'authenticated' value
# in the streamlit session_state to false. 
st.session_state['authenticated'] = False

# Use the SideBarLinks function from src/modules/nav.py to control
# the links displayed on the left-side panel. 
# IMPORTANT: ensure src/.streamlit/config.toml sets
# showSidebarNavigation = false in the [client] section
SideBarLinks(show_home=True)

# ***************************************************
#    The major content of this page
# ***************************************************

# set the title of the page and provide a simple prompt. 
logger.info("Loading the Home page of the app")

st.title('Coursify')
st.write('\n\n')
st.write('### Welcome! Choose your role to continue:')
st.write('')

# Create two rows of two columns for a clean grid layout
col1, col2 = st.columns(2)

# For each of the user personas for which we are implementing
# functionality, we put a button on the screen that the user 
# can click to MIMIC logging in as that mock user. 

with col1:
    with st.container(border=True):
        st.write('#### 👨‍🎓 Student - Andrea')
        st.write('Plan courses and track your degree progress')
        st.write('')
        if st.button('Act as Andrea, a Student',
                     type='primary',
                     use_container_width=True,
                     key='student'):
            st.session_state['authenticated'] = True
            st.session_state['role'] = 'student'
            st.session_state['first_name'] = 'Andrea'
            st.session_state['user_id'] = 1001
            logger.info("Logging in as Student Persona")
            st.switch_page('pages/11_Student_Home.py')

with col2:
    with st.container(border=True):
        st.write('#### 👨‍🏫 Professor - Amelia')
        st.write('Manage courses and view student planning data')
        st.write('')
        if st.button('Act as Amelia, a Professor', 
                    type='primary', 
                    use_container_width=True,
                    key='professor'):
            st.session_state['authenticated'] = True
            st.session_state['role'] = 'professor'
            st.session_state['first_name'] = 'Amelia'
            st.switch_page('pages/20_Professor_Home.py')

st.write('')

col3, col4 = st.columns(2)

with col3:
    with st.container(border=True):
        st.write('#### 🔧 System Admin - Jordan')
        st.write('Manage system resources and configurations')
        st.write('')
        if st.button('Act as System Administrator', 
                    type='primary', 
                    use_container_width=True,
                    key='admin'):
            st.session_state['authenticated'] = True
            st.session_state['role'] = 'administrator'
            st.session_state['first_name'] = 'SysAdmin'
            st.switch_page('pages/20_Admin_Home.py')

with col4:
    with st.container(border=True):
        st.write('#### 📊 Data Analyst - Joe')
        st.write('Access insights and analytics on course planning')
        st.write('')
        if st.button('Act as Data Analyst', 
                    type='primary', 
                    use_container_width=True,
                    key='analyst'):
            st.session_state['authenticated'] = True
            st.session_state['role'] = 'Data_analyst'
            st.session_state['first_name'] = 'Joe'
            st.switch_page('pages/40_data_A_Home.py')