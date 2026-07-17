import requests

BASE_URL = "http://127.0.0.1:8000"


def login(email, password):
    return requests.post(
        f"{BASE_URL}/auth/login",
        json={
            "email": email,
            "password": password
        }
    )


def get_me(token):
    return requests.get(
        f"{BASE_URL}/users/me",
        headers={
            "Authorization": f"Bearer {token}"}
    )


def get_projects(token):
    return requests.get(
        f"{BASE_URL}/projects/",
        headers={
            "Authorization": f"Bearer {token}"}
    )


def create_project(token, data):
    return requests.post(
        f"{BASE_URL}/projects/",
        json=data,
        headers={
            "Authorization": f"Bearer {token}"}
    )


def update_project(token, project_id, data):
    return requests.put(
        f"{BASE_URL}/projects/{project_id}",
        json=data,
        headers={
            "Authorization": f"Bearer {token}"
        }
    )


def delete_project(token, project_id):
    return requests.delete(
        f"{BASE_URL}/projects/{project_id}",
        headers={
            "Authorization": f"Bearer {token}"}
    )



def get_tickets(token):
    return requests.get(
        f"{BASE_URL}/tickets/",
        headers={
            "Authorization": f"Bearer {token}"}
    
            
        )


def create_ticket(token, data):
    return requests.post(
        f"{BASE_URL}/tickets/",
        json=data,
        headers={
            "Authorization": f"Bearer {token}"
        }
    )


def update_ticket(token, ticket_id, data):
    return requests.put(
        f"{BASE_URL}/tickets/{ticket_id}",
        json=data,
        headers={
            "Authorization": f"Bearer {token}"
        }
    )


def delete_ticket(token, ticket_id):
    return requests.delete(
        f"{BASE_URL}/tickets/{ticket_id}",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )


def get_comments(token, ticket_id):
    return requests.get(
        f"{BASE_URL}/comments/ticket/{ticket_id}",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )


def create_comment(token, data):
    return requests.post(
        f"{BASE_URL}/comments/",
        json=data,
        headers={
            "Authorization": f"Bearer {token}"
        }
    )


def update_comment(token, comment_id, data):
    return requests.put(
        f"{BASE_URL}/comments/{comment_id}",
        json=data,
        headers={
            "Authorization": f"Bearer {token}"
        }
    )


def delete_comment(token, comment_id):
    return requests.delete(
        f"{BASE_URL}/comments/{comment_id}",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )


def get_labels(token):
    return requests.get(
        f"{BASE_URL}/labels/",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )


def create_label(token, data):
    return requests.post(
        f"{BASE_URL}/labels/",
        json=data,
        headers={
            "Authorization": f"Bearer {token}"
        }
    )


def update_label(token, label_id, data):
    return requests.put(
        f"{BASE_URL}/labels/{label_id}",
        json=data,
        headers={
            "Authorization": f"Bearer {token}"
        }
    )


def delete_label(token, label_id):
    return requests.delete(
        f"{BASE_URL}/labels/{label_id}",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

def get_attachments(token):
    return requests.get(
        f"{BASE_URL}/attachments/",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )


def create_attachment(token, data):
    return requests.post(
        f"{BASE_URL}/attachments/",
        json=data,
        headers={
            "Authorization": f"Bearer {token}"
        }
    )


def update_attachment(token, attachment_id, data):
    return requests.put(
        f"{BASE_URL}/attachments/{attachment_id}",
        json=data,
        headers={
            "Authorization": f"Bearer {token}"
        }
    )


def delete_attachment(token, attachment_id):
    return requests.delete(
        f"{BASE_URL}/attachments/{attachment_id}",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

def get_project_members(token, project_id):
    return requests.get(
        f"{BASE_URL}/project-members/project/{project_id}",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )


def add_project_member(token, data):
    return requests.post(
        f"{BASE_URL}/project-members/",
        json=data,
        headers={
            "Authorization": f"Bearer {token}"
        }
    )


def delete_project_member(token, member_id):
    return requests.delete(
        f"{BASE_URL}/project-members/{member_id}",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )


def get_users(token):
    return requests.get(
        f"{BASE_URL}/users/",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

def get_dashboard(token):
    return requests.get(
        f"{BASE_URL}/dashboard/",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

def signup(user_data):

    return requests.post(
        f"{BASE_URL}/users/signup",
        json=user_data
    )