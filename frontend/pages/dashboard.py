import streamlit as st

from utils.api import (
    get_dashboard,
    get_tickets,
    get_projects,
    get_comments
)


# ----------------------------------------
# Page Configuration
# ----------------------------------------

st.set_page_config(
    page_title="TaskFlow Dashboard",
    page_icon="📊",
    layout="wide"
)



# ----------------------------------------
# Authentication
# ----------------------------------------

if "token" not in st.session_state:

    st.warning(
        "Please login first."
    )

    st.stop()


token = st.session_state["token"]



# ----------------------------------------
# Dashboard Heading
# Same size as other page headings
# ----------------------------------------

st.markdown(
    """
    <div style="
        font-size: 40px;
        font-weight: 700;
        margin-bottom: 15px;
    ">
        📊 TaskFlow Dashboard
    </div>
    """,
    unsafe_allow_html=True
)



# ----------------------------------------
# Load Dashboard Data
# ----------------------------------------

dashboard_response = get_dashboard(token)


if dashboard_response.status_code != 200:

    st.error(
        "Unable to load dashboard."
    )

    st.stop()



data = dashboard_response.json()



# ----------------------------------------
# Load Tickets
# ----------------------------------------

tickets_response = get_tickets(token)


if tickets_response.status_code == 200:

    tickets = tickets_response.json()

else:

    tickets = []



# ----------------------------------------
# Load Projects
# ----------------------------------------

projects_response = get_projects(token)


if projects_response.status_code == 200:

    projects = projects_response.json()

else:

    projects = []



# ----------------------------------------
# Load Comments
# ----------------------------------------

comments = []


for ticket in tickets:


    comment_response = get_comments(
        token,
        ticket["id"]
    )


    if comment_response.status_code == 200:

        comments.extend(
            comment_response.json()
        )



# ========================================
# OVERVIEW
# ========================================

st.write("## Overview")



col1, col2, col3 = st.columns(3)



with col1:

    st.metric(
        "📁 Projects",
        data["total_projects"]
    )



with col2:

    st.metric(
        "🎫 Tickets",
        data["total_tickets"]
    )



with col3:

    st.metric(
        "👥 Users",
        data["total_users"]
    )



# ========================================
# TICKET STATUS
# ========================================

st.write("## 🎫 Ticket Status")



col1, col2, col3 = st.columns(3)



with col1:

    st.metric(
        "🔵 To Do",
        data["todo_tickets"]
    )



with col2:

    st.metric(
        "🟡 In Progress",
        data["progress_tickets"]
    )



with col3:

    st.metric(
        "🟢 Completed",
        data["completed_tickets"]
    )



st.divider()



# ========================================
# MY PROJECTS
# ========================================

st.write("## 📁 My Projects")



if len(projects) == 0:

    st.info(
        "No projects available."
    )


else:


    recent_projects = sorted(
        projects,
        key=lambda x:x["id"],
        reverse=True
    )



    for project in recent_projects:


        with st.expander(
            f"📁 {project['name']}"
        ):


            st.write(
                project.get(
                    "description",
                    "No description available."
                )
            )


            st.caption(
                f"Project ID: {project['id']}"
            )


            project_tickets = [

                ticket

                for ticket in tickets

                if ticket.get("project_id") == project["id"]

            ]



            st.write(
                f"🎫 Total Tickets: {len(project_tickets)}"
            )



            if project_tickets:


                st.write(
                    "Recent Tickets:"
                )


                for ticket in project_tickets[:3]:


                    st.write(

                        f"""
                        • {ticket.get('title')}

                        Status:
                        {ticket.get('status')}

                        """

                    )


            else:

                st.caption(
                    "No tickets in this project."
                )



st.divider()



