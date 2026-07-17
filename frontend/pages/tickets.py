import streamlit as st
from datetime import date

from utils.api import (
    get_projects,
    get_tickets,
    create_ticket,
    update_ticket,
    delete_ticket,

    get_comments,
    create_comment,
    update_comment,
    delete_comment,

    get_attachments,
    create_attachment,
    delete_attachment,

    get_labels,
    create_label,
    delete_label
)


st.title("🎫 Ticket Management")


# ----------------------------------------
# Authentication
# ----------------------------------------

if "token" not in st.session_state:
    st.warning("Please login first.")
    st.stop()


token = st.session_state["token"]


# ----------------------------------------
# Load Projects
# ----------------------------------------

projects_response = get_projects(token)


if projects_response.status_code != 200:
    st.error("Could not load projects.")
    st.stop()


projects = projects_response.json()


project_names = {
    project["name"]: project["id"]
    for project in projects
}


# ----------------------------------------
# Create Ticket
# ----------------------------------------
# ----------------------------------------
# Ticket Information
# ----------------------------------------

st.subheader("➕ Create New Ticket")

col1, col2 = st.columns(2)

with col1:

    title = st.text_input(
        "🎫 Title"
    )

    priority = st.selectbox(
        "Priority",
        [
            "Low",
            "Medium",
            "High"
        ]
    )

    project_name = st.selectbox(
        "Project",
        list(project_names.keys())
    )

with col2:

    status = st.selectbox(
        "Status",
        [
            "To Do",
            "In Progress",
            "Done"
        ]
    )

    due_date = st.date_input(
        "Due Date"
    )

description = st.text_area(
    "📝 Description",
    height=120
)


if st.button("➕ Create Ticket"):

    if not title.strip():

        st.warning("⚠ Please enter a ticket title.")

    else:

        response = create_ticket(
            token,
            {
                "title": title,
                "description": description,
                "priority": priority,
                "status": status,
                "due_date": str(due_date),
                "project_id": project_names[project_name],
                "assignee_id": None
            }
        )

        if response.status_code == 200:

            st.success("✅ Ticket created successfully.")
            st.rerun()

        else:

            st.error(response.text)


st.divider()


# ----------------------------------------
# Display Tickets
# ----------------------------------------

st.header("📋 All Tickets")
# ----------------------------------------
# Search Ticket
# ----------------------------------------

search = st.text_input(
    "🔍 Search Ticket",
    placeholder="Search by ticket number or title..."
)
# ----------------------------------------
# Ticket Filters
# ----------------------------------------

filter_col1, filter_col2, filter_col3 = st.columns(3)

with filter_col1:

    status_filter = st.selectbox(
        "Status",
        [
            "All",
            "To Do",
            "In Progress",
            "Done"
        ]
    )

with filter_col2:

    priority_filter = st.selectbox(
        "Priority",
        [
            "All",
            "Low",
            "Medium",
            "High"
        ]
    )

with filter_col3:

    project_filter = st.selectbox(
        "Project",
        ["All"] + list(project_names.keys())
    )



# ----------------------------------------
# Load Tickets
# ----------------------------------------

response = get_tickets(token)

if response.status_code != 200:

    st.error("Unable to load tickets.")

    st.stop()

tickets = response.json()

if len(tickets) == 0:

    st.info(
        "📭 No tickets available.\n\nCreate your first ticket to start managing your project."
    )

    st.stop()

# ----------------------------------------
# Apply Search
# ----------------------------------------

if search:

    tickets = [

        ticket

        for ticket in tickets

        if search.lower() in ticket["title"].lower()

        or search in str(ticket["ticket_number"])

    ]



# ----------------------------------------
# Apply Filters
# ----------------------------------------

if status_filter != "All":

    tickets = [
        ticket
        for ticket in tickets
        if ticket["status"] == status_filter
    ]


if priority_filter != "All":

    tickets = [
        ticket
        for ticket in tickets
        if ticket["priority"] == priority_filter
    ]


if project_filter != "All":

    project_id = project_names[project_filter]

    tickets = [
        ticket
        for ticket in tickets
        if ticket["project_id"] == project_id
    ]





# ----------------------------------------
# Ticket Sorting
# ----------------------------------------

sort_by = st.selectbox(
    "↕ Sort By",
    [
        "Newest First",
        "Oldest First",
        "Priority",
        "Due Date"
    ],
    index=1
)

# ----------------------------------------
# Apply Sorting
# ----------------------------------------

if sort_by == "Newest First":

    tickets = sorted(
        tickets,
        key=lambda x: x["id"],
        reverse=True
    )


elif sort_by == "Oldest First":

    tickets = sorted(
        tickets,
        key=lambda x: x["id"]
    )


elif sort_by == "Priority":

    priority_order = {
        "High": 1,
        "Medium": 2,
        "Low": 3
    }

    tickets = sorted(
        tickets,
        key=lambda x: priority_order.get(
            x["priority"],
            99
        )
    )


elif sort_by == "Due Date":

    tickets = sorted(
        tickets,
        key=lambda x: (
            x["due_date"] is None,
            x["due_date"]
        )
    )


# ----------------------------------------
# Ticket Summary
# ----------------------------------------

all_tickets = len(tickets)

todo_tickets = len(
    [
        t
        for t in tickets
        if t["status"] == "To Do"
    ]
)

progress_tickets = len(
    [
        t
        for t in tickets
        if t["status"] == "In Progress"
    ]
)

done_tickets = len(
    [
        t
        for t in tickets
        if t["status"] == "Done"
    ]
)



# ----------------------------------------
# Ticket Overview
# ----------------------------------------

st.subheader("📊 Ticket Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "All Tickets",
        all_tickets
    )

with col2:

    st.metric(
        "To Do",
        todo_tickets
    )

with col3:

    st.metric(
        "In Progress",
        progress_tickets
    )

with col4:

    st.metric(
        "Done",
        done_tickets
    )

st.divider()




for ticket in tickets:

    with st.expander(
        f"🎫 Ticket #{ticket['ticket_number']} | {ticket['title']}",
        expanded=False
        ):


        st.markdown(
            f"""
            ## 🎫 {ticket['title']}
            """
        )


        col1, col2, col3 = st.columns(3)


        with col1:

            st.metric(
                "Ticket Number",
                f"#{ticket['ticket_number']}"
            )


        with col2:

            st.metric(
                "Status",
                ticket["status"]
            )


        with col3:

            st.metric(
                "Priority",
                ticket["priority"]
            )


        st.divider()


        new_title = st.text_input(
            "Title",
            value=ticket["title"],
            key=f"title_{ticket['id']}"
        )


        new_description = st.text_area(
            "Description",
            value=ticket["description"] or "",
            key=f"description_{ticket['id']}"
        )


        new_priority = st.selectbox(
            "Priority",
            [
                "Low",
                "Medium",
                "High"
            ],
            index=[
                "Low",
                "Medium",
                "High"
            ].index(ticket["priority"]),
            key=f"priority_{ticket['id']}"
        )


        new_status = st.selectbox(
            "Status",
            [
                "To Do",
                "In Progress",
                "Done"
            ],
            index=[
                "To Do",
                "In Progress",
                "Done"
            ].index(ticket["status"]),
            key=f"status_{ticket['id']}"
        )

                # ----------------------------------------
        # Ticket Information
        # ----------------------------------------

        st.divider()

        st.subheader("📋 Ticket Information")


        col1, col2 = st.columns(2)


        with col1:

            st.write(
                f"📁 **Project ID:** {ticket['project_id']}"
            )

            st.write(
                f"👤 **Reporter ID:** {ticket['reporter_id']}"
            )

            st.write(
                f"👤 **Assignee ID:** {ticket['assignee_id']}"
            )


        with col2:

            st.write(
                f"📅 **Due Date:** {ticket['due_date']}"
            )

            st.write(
                f"🕒 **Created:** {ticket['created_at']}"
            )

            st.write(
                f"🔄 **Updated:** {ticket['updated_at']}"
            )


        st.divider()


        # ----------------------------------------
        # Status Display
        # ----------------------------------------

        st.subheader("📌 Ticket Status")


        if ticket["status"] == "Done":

            st.success(
                "🟢 Done"
            )


        elif ticket["status"] == "In Progress":

            st.warning(
                "🟡 In Progress"
            )


        else:

            st.info(
                "🔵 To Do"
            )


        # ----------------------------------------
        # Priority Display
        # ----------------------------------------

        st.subheader("⚡ Priority")


        if ticket["priority"] == "High":

            st.error(
                "🔴 High"
            )


        elif ticket["priority"] == "Medium":

            st.warning(
                "🟡 Medium"
            )


        else:

            st.success(
                "🟢 Low"
            )


        st.divider()


        # ----------------------------------------
        # Update / Delete Ticket
        # ----------------------------------------

        action1, action2 = st.columns(2)


        with action1:

            if st.button(
                "💾 Save Changes",
                key=f"update_{ticket['id']}"
            ):

                response = update_ticket(
                    token,
                    ticket["id"],
                    {
                        "title": new_title,
                        "description": new_description,
                        "priority": new_priority,
                        "status": new_status
                    }
                )


                if response.status_code == 200:

                    st.success(
                        "✅ Ticket updated successfully."
                    )

                    st.rerun()


                else:

                    st.error(
                        response.text
                    )



        with action2:

            if st.button(
                "🗑 Delete Ticket",
                key=f"delete_{ticket['id']}"
            ):

                response = delete_ticket(
                    token,
                    ticket["id"]
                )


                if response.status_code == 200:

                    st.success(
                        "✅ Ticket deleted successfully."
                    )

                    st.rerun()


                else:

                    st.error(
                        response.text
                    )


        # ----------------------------------------
        # Comments Section
        # ----------------------------------------

        st.divider()

        with st.expander("💬 Comments", expanded=False):

            comments_response = get_comments(
                token,
                ticket["id"]
            )

            if comments_response.status_code == 200:

                comments = comments_response.json()

                if len(comments) == 0:

                    st.info(
                        "📭 No comments yet."
                    )

                else:

                    for comment in comments:

                        with st.container():

                            st.markdown(
                                f"""
                                💬 **Comment**

                                {comment['content']}
                                """
                            )

                            st.caption(
                                f"Created at: {comment['created_at']}"
                            )

                            updated_comment = st.text_area(
                                "Edit Comment",
                                value=comment["content"],
                                key=f"edit_comment_{comment['id']}"
                            )

                            col1, col2 = st.columns(2)

                            with col1:

                                if st.button(
                                    "✏️ Update Comment",
                                    key=f"update_comment_{comment['id']}"
                                ):

                                    response = update_comment(
                                        token,
                                        comment["id"],
                                        {
                                            "content": updated_comment
                                        }
                                    )

                                    if response.status_code == 200:

                                        st.success(
                                            "✅ Comment updated successfully."
                                        )

                                        st.rerun()

                                    else:

                                        st.error(response.text)

                            with col2:

                                if st.button(
                                    "🗑 Delete Comment",
                                    key=f"delete_comment_{comment['id']}"
                                ):

                                    response = delete_comment(
                                        token,
                                        comment["id"]
                                    )

                                    if response.status_code == 200:

                                        st.success(
                                            "✅ Comment deleted successfully."
                                        )

                                        st.rerun()

                                    else:

                                        st.error(response.text)

                            st.divider()

            # ----------------------------------------
            # Add Comment
            # ----------------------------------------

            st.subheader("➕ Add Comment")

            comment_text = st.text_area(
                "Write your comment",
                key=f"comment_text_{ticket['id']}"
            )

            if st.button(
                "💬 Add Comment",
                key=f"add_comment_{ticket['id']}"
            ):

                if not comment_text.strip():

                    st.warning("⚠ Please enter a comment.")

                else:

                    response = create_comment(
                        token,
                        {
                            "content": comment_text,
                            "ticket_id": ticket["id"]
                        }
                    )

                    if response.status_code == 200:

                        st.success("✅ Comment added successfully.")
                        st.rerun()

                    else:

                        st.error(response.text)
        # ----------------------------------------
        # Attachments Section
        # ----------------------------------------

        st.divider()

        with st.expander("📎 Attachments", expanded=False):

            attachments_response = get_attachments(token)

            if attachments_response.status_code == 200:

                attachments = attachments_response.json()

                ticket_attachments = [
                    attachment
                    for attachment in attachments
                    if attachment["ticket_id"] == ticket["id"]
                ]

                if len(ticket_attachments) == 0:

                    st.info("No attachments added yet.")

                else:

                    for attachment in ticket_attachments:

                        col1, col2 = st.columns(2)

                        with col1:

                            st.write(f"📎 {attachment['filename']}")
                            st.write(f"📂 Path: {attachment['filepath']}")

                        with col2:

                            if st.button(
                                "🗑 Delete Attachment",
                                key=f"delete_attachment_{attachment['id']}"
                            ):

                                response = delete_attachment(
                                    token,
                                    attachment["id"]
                                )

                                if response.status_code == 200:

                                    st.success("Attachment Deleted")
                                    st.rerun()

                                else:

                                    st.error(response.text)

                # ----------------------------------------
                # Add Attachment
                # ----------------------------------------

                st.subheader("➕ Add Attachment")

                filename = st.text_input(
                    "File Name",
                    key=f"filename_{ticket['id']}"
                )

                filepath = st.text_input(
                    "File Path",
                    key=f"filepath_{ticket['id']}"
                )

                if st.button(
                    "Upload Attachment",
                    key=f"add_attachment_{ticket['id']}"
                ):

                    response = create_attachment(
                        token,
                        {
                            "filename": filename,
                            "filepath": filepath,
                            "ticket_id": ticket["id"]
                        }
                    )

                    if response.status_code == 200:

                        st.success("✅ Attachment Added Successfully")
                        st.rerun()

                    else:

                        st.error(response.text)

                        # ----------------------------------------
        # Labels Section
        # ----------------------------------------
        st.divider()

        with st.expander("🏷 Labels", expanded=False):


            labels_response = get_labels(token)


            if labels_response.status_code == 200:

                labels = labels_response.json()


                if len(labels) == 0:

                    st.info(
                        "📭 No labels assigned to this ticket."
                    )


                else:

                    for label in labels:

                        col1, col2 = st.columns(2)


                        with col1:

                            st.write(
                                f"🏷 {label['name']}"
                            )


                        with col2:

                            if st.button(
                                "🗑 Delete Label",
                                key=f"delete_label_{label['id']}_{ticket['id']}"
                            ):

                                response = delete_label(
                                    token,
                                    label["id"]
                                )


                                if response.status_code == 200:

                                    st.success(
                                        "Label Deleted"
                                    )

                                    st.rerun()


                                else:

                                    st.error(
                                        response.text
                                    )


            st.divider()


            # ----------------------------------------
            # Add Label
            # ----------------------------------------

            

            
            st.subheader("➕ Add Label")

            label_name = st.text_input(
                "Label Name",
                key=f"label_name_{ticket['id']}"
            )


            if st.button(
                "Create Label",
                key=f"create_label_{ticket['id']}"
            ):


                if label_name.strip() == "":

                    st.warning(
                        "Enter label name."
                    )


                else:

                    response = create_label(
                        token,
                        {
                            "name": label_name
                        }
                    )


                    if response.status_code == 200:

                        st.success(
                            "✅ Label Created"
                        )

                        st.rerun()


                    else:

                        st.error(
                            response.text
                        )





        # ----------------------------------------
        # End of Ticket Card
        # ----------------------------------------

        st.caption(
            "TaskFlow Ticket Management System"
        )
# ----------------------------------------
# End of Tickets Page
# ----------------------------------------

st.sidebar.info(
    "🎫 Manage tickets, comments, and workflow from here."
)


