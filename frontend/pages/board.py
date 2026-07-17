import streamlit as st

from utils.api import (
    get_projects,
    get_tickets,
    update_ticket
)

from streamlit_kanban import st_kanban


# =====================================================
# AUTHENTICATION
# =====================================================

if "token" not in st.session_state:

    st.warning(
        "Please login first."
    )

    st.stop()


token = st.session_state["token"]


st.markdown(
    """
    <div style="
        font-size: 40px;
        font-weight: 700;
        margin-bottom: 15px;
    ">
        📊 TaskFlow Board
    </div>
    """,
    unsafe_allow_html=True
)

st.divider()

# =====================================================
# LOAD PROJECTS
# =====================================================

response = get_projects(token)

if response.status_code != 200:

    st.error(
        "Unable to load projects."
    )

    st.stop()


projects = response.json()


if len(projects) == 0:

    st.info(
        "No projects found."
    )

    st.stop()



# =====================================================
# PROJECT SELECTOR
# =====================================================

project_lookup = {}

for project in projects:

    project_lookup[
        project["name"]
    ] = project["id"]



left, right = st.columns(
    [3, 2]
)


with left:

    selected_project = st.selectbox(

        "Project",

        list(project_lookup.keys())

    )


with right:

    search = st.text_input(

        "Search Ticket",

        placeholder="Search by title..."

    )


selected_project_id = project_lookup[
    selected_project
]


st.divider()



# =====================================================
# LOAD TICKETS
# =====================================================

response = get_tickets(token)


if response.status_code != 200:

    st.error(
        "Unable to load tickets."
    )

    st.stop()


tickets = response.json()



# =====================================================
# FILTER PROJECT
# =====================================================

tickets = [

    ticket

    for ticket in tickets

    if ticket["project_id"] == selected_project_id

]



# =====================================================
# SEARCH
# =====================================================

if search:

    tickets = [

        ticket

        for ticket in tickets

        if search.lower()

        in ticket["title"].lower()

    ]


# =====================================================
# STATUS LISTS
# =====================================================

todo = []

progress = []

review = []

done = []



for ticket in tickets:

    status = ticket["status"]


    if status == "To Do":

        todo.append(ticket)


    elif status == "In Progress":

        progress.append(ticket)


    elif status == "Review":

        review.append(ticket)


    elif status == "Done":

        done.append(ticket)



# =====================================================
# PRIORITY BADGE
# =====================================================

def priority_badge(priority):

    priority = (priority or "").lower()


    if priority == "high":

        return "🔴 High"


    elif priority == "medium":

        return "🟡 Medium"


    else:

        return "🟢 Low"
    

# =====================================================
# CREATE KANBAN DATA
# =====================================================

kanban_columns = [

    {
        "id": "To Do",
        "title": "📝 To Do",
        "cards": [

            {
                "id": str(ticket["id"]),

                "title":
                    f"#{ticket['ticket_number']} - {ticket['title']}",

                "description":
                    priority_badge(
                        ticket["priority"]
                    )
            }

            for ticket in todo
        ]
    },


    {
        "id": "In Progress",
        "title": "⚙️ In Progress",
        "cards": [

            {
                "id": str(ticket["id"]),

                "title":
                    f"#{ticket['ticket_number']} - {ticket['title']}",

                "description":
                    priority_badge(
                        ticket["priority"]
                    )
            }

            for ticket in progress
        ]
    },


    {
        "id": "Review",
        "title": "👀 Review",
        "cards": [

            {
                "id": str(ticket["id"]),

                "title":
                    f"#{ticket['ticket_number']} - {ticket['title']}",

                "description":
                    priority_badge(
                        ticket["priority"]
                    )
            }

            for ticket in review
        ]
    },


    {
        "id": "Done",
        "title": "✅ Done",
        "cards": [

            {
                "id": str(ticket["id"]),

                "title":
                    f"#{ticket['ticket_number']} - {ticket['title']}",

                "description":
                    priority_badge(
                        ticket["priority"]
                    )
            }

            for ticket in done
        ]
    }

]

st.markdown(
    """
    <style>

    .kanban {
        background-color: white !important;
    }

    .kanban-column {
        background-color: #f5f5f5 !important;
        color: black !important;
    }

    .kanban-card {
        background-color: white !important;
        color: black !important;
        border: 1px solid #ddd !important;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# =====================================================
# DRAG AND DROP BOARD
# =====================================================

updated_board = st_kanban(

    kanban_columns,

    key="taskflow_drag_board"

)



# =====================================================
# SAVE NEW STATUS
# =====================================================

if updated_board:


    for column in updated_board:


        new_status = column["id"]


        for card in column["cards"]:


            ticket_id = int(card["id"])


            old_ticket = next(

                (

                    ticket

                    for ticket in tickets

                    if ticket["id"] == ticket_id

                ),

                None

            )


            if old_ticket:


                if old_ticket["status"] != new_status:


                    update_ticket(

                        token,

                        ticket_id,

                        {
                            "status": new_status
                        }

                    )


                    st.success(

                        f"Ticket moved to {new_status}"

                    )


                    st.rerun()