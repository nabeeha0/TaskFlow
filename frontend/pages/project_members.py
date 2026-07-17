import streamlit as st

from utils.api import (
    get_projects,
    get_project_members,
    add_project_member,
    delete_project_member
)


st.title("👥 Project Members")


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
# Load Projects
# ----------------------------------------

projects_response = get_projects(token)


if projects_response.status_code != 200:

    st.error(
        "Unable to load projects."
    )

    st.stop()


projects = projects_response.json()



project_dict = {

    project["name"]: project["id"]

    for project in projects

}



# ----------------------------------------
# Add Member
# ----------------------------------------

st.subheader(
    "➕ Add Member To Project"
)



selected_project = st.selectbox(
    "Select Project",
    list(project_dict.keys())
)



user_id = st.number_input(
    "User ID",
    min_value=1,
    step=1
)



if st.button(
    "Add Member"
):

    response = add_project_member(
        token,
        {
            "project_id": project_dict[selected_project],
            "user_id": user_id
        }
    )


    if response.status_code == 200:

        st.success(
            "✅ Member Added Successfully"
        )

        st.rerun()


    else:

        st.error(
            response.text
        )



st.divider()



# ----------------------------------------
# View Members
# ----------------------------------------

st.subheader(
    "📋 Project Team Members"
)



view_project = st.selectbox(
    "View Project Members",
    list(project_dict.keys()),
    key="view_project"
)



members_response = get_project_members(
    token,
    project_dict[view_project]
)



if members_response.status_code != 200:

    st.error(
        "Unable to load members."
    )

    st.stop()



members = members_response.json()



if len(members) == 0:

    st.info(
        "No members assigned."
    )

    st.stop()



# ----------------------------------------
# Display Members
# ----------------------------------------

for member in members:


    with st.container():


        st.write(
            "👤 Member ID:",
            member["user_id"]
        )


        st.write(
            "📁 Project ID:",
            member["project_id"]
        )


        if st.button(
            "🗑 Remove Member",
            key=f"delete_member_{member['id']}"
        ):


            response = delete_project_member(
                token,
                member["id"]
            )


            if response.status_code == 200:

                st.success(
                    "Member Removed"
                )

                st.rerun()


            else:

                st.error(
                    response.text
                )


        st.divider()