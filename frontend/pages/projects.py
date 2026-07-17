import streamlit as st

from utils.api import (
    get_projects,
    create_project,
    update_project,
    delete_project,
    get_tickets,
    get_project_members,
    add_project_member,
    delete_project_member,
    get_users,
    get_me
)


st.title("📁 Project Management")


# ----------------------------------------
# Authentication
# ----------------------------------------

if "token" not in st.session_state:

    st.warning("Please login first.")
    st.stop()


token = st.session_state["token"]



# ----------------------------------------
# Current User
# ----------------------------------------

user_response = get_me(token)


if user_response.status_code == 200:

    current_user = user_response.json()

else:

    current_user = None



current_user_role = "Member"


if current_user:

    current_user_role = current_user.get(
        "role",
        "Member"
    )



# ----------------------------------------
# Create Project
# ----------------------------------------

st.subheader("➕ Create New Project")


project_name = st.text_input(
    "Project Name"
)


project_description = st.text_area(
    "Project Description"
)



if st.button("Create Project"):


    if project_name.strip() == "":

        st.warning(
            "Please enter project name."
        )


    else:

        response = create_project(
            token,
            {
                "name": project_name,
                "description": project_description
            }
        )


        if response.status_code in [200,201]:

            st.success(
                "Project created successfully."
            )

            st.rerun()


        else:

            st.error(
                response.text
            )



st.divider()



# ----------------------------------------
# Load Projects
# ----------------------------------------

st.subheader("📂 All Projects")


projects_response = get_projects(token)


if projects_response.status_code != 200:

    st.error(
        "Unable to load projects."
    )

    st.stop()



projects = projects_response.json()



if not projects:

    st.info(
        "No projects available."
    )

    st.stop()



# ----------------------------------------
# Load Tickets
# ----------------------------------------

tickets_response = get_tickets(token)


if tickets_response.status_code == 200:

    tickets = tickets_response.json()

else:

    tickets = []



# ----------------------------------------
# Load Users
# ----------------------------------------

users_response = get_users(token)


if users_response.status_code == 200:

    users = users_response.json()

else:

    users = []



user_lookup = {}


for user in users:

    user_lookup[user["id"]] = user



# ----------------------------------------
# Project List
# ----------------------------------------

for project in projects:


    with st.expander(
        f"📁 {project['name']}"
    ):


        st.subheader(
            "📝 Project Information"
        )


        st.write(
            project.get(
                "description",
                "No description available."
            )
        )


        st.write(
            "🆔 Project ID:",
            project["id"]
        )


        st.divider()



        # --------------------------------
        # Tickets
        # --------------------------------

        st.subheader(
            "🎫 Tickets"
        )


        project_tickets = [

            ticket

            for ticket in tickets

            if ticket.get("project_id") == project["id"]

        ]



        if project_tickets:


            for ticket in project_tickets:

                st.write(
                    f"""
                    🎫 **{ticket.get('title','No Title')}**

                    Status:
                    {ticket.get('status','N/A')}

                    Priority:
                    {ticket.get('priority','N/A')}
                    """
                )


        else:

            st.info(
                "No tickets available."
            )



        st.divider()



        # --------------------------------
        # Members
        # --------------------------------

        st.subheader(
            "👥 Members"
        )


        members_response = get_project_members(
            token,
            project["id"]
        )



        if members_response.status_code == 200:

            members = members_response.json()

        else:

            members = []



        if members:


            for member in members:


                member_user = user_lookup.get(
                    member["user_id"]
                )


                if member_user:


                    col1, col2 = st.columns(2)



                    with col1:

                        st.write(
                            f"""
                            👤 Name:
                            {member_user.get('name')}

                            📧 Email:
                            {member_user.get('email')}

                            🎯 Role:
                            {member.get('role','Member')}
                            """
                        )



                    with col2:


                        if current_user_role == "Manager":


                            if st.button(
                                "🗑 Remove Member",
                                key=f"remove_{member['id']}"
                            ):


                                response = delete_project_member(
                                    token,
                                    member["id"]
                                )


                                if response.status_code in [200,204]:

                                    st.success(
                                        "Member removed."
                                    )

                                    st.rerun()


        else:

            st.info(
                "No members added."
            )



        st.divider()



        # --------------------------------
        # Add Member
        # --------------------------------

        if current_user_role == "Manager":


            st.subheader(
                "➕ Add Member"
            )


            user_id = st.number_input(

                "User ID",

                min_value=1,

                step=1,

                key=f"user_{project['id']}"

            )


            role = st.selectbox(

                "Role",

                [
                    "Member",
                    "Developer",
                    "Manager",
                    "Tester"
                ],

                key=f"role_{project['id']}"

            )



            if st.button(

                "Add Member",

                key=f"add_member_{project['id']}"

            ):


                response = add_project_member(

                    token,

                    {
                        "project_id": project["id"],
                        "user_id": user_id,
                        "role": role
                    }

                )



                if response.status_code in [200,201]:

                    st.success(
                        "Member added."
                    )

                    st.rerun()


                else:

                    st.error(
                        response.text
                    )



        st.divider()



        # --------------------------------
        # Update Project
        # --------------------------------

        st.subheader(
            "✏️ Update Project"
        )


        new_name = st.text_input(

            "Project Name",

            value=project["name"],

            key=f"name_{project['id']}"

        )


        new_description = st.text_area(

            "Description",

            value=project.get(
                "description",
                ""
            ),

            key=f"description_{project['id']}"

        )



        if st.button(

            "💾 Save Changes",

            key=f"update_{project['id']}"

        ):


            response = update_project(

                token,

                project["id"],

                {
                    "name": new_name,
                    "description": new_description
                }

            )



            if response.status_code == 200:

                st.success(
                    "Project updated."
                )

                st.rerun()


            else:

                st.error(
                    response.text
                )



        # --------------------------------
        # Delete Project
        # --------------------------------

        if st.button(

            "🗑 Delete Project",

            key=f"delete_{project['id']}"

        ):


            response = delete_project(

                token,

                project["id"]

            )


            if response.status_code in [200,204]:

                st.success(
                    "Project deleted."
                )

                st.rerun()


            else:

                st.error(
                    response.text
                )