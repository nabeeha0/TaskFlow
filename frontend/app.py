import streamlit as st

st.set_page_config(
    page_title="TaskFlow",
    page_icon="📋",
    layout="wide"
)

pg = st.navigation(
    [
        
        st.Page("pages/login.py", title="Login", icon="🔐"),
        st.Page("pages/dashboard.py",title="Dashboard",icon="📊"),
        st.Page("pages/tickets.py", title="Tickets", icon="🎫"),
        st.Page("pages/board.py",title="Board",icon="📋"),
        st.Page("pages/projects.py", title="Projects", icon="📁"),
        st.Page("pages/project_members.py", title="Project Members", icon="👥"),
        st.Page("pages/signup.py", title="Signup", icon="📝"),
    ]
)

pg.run()