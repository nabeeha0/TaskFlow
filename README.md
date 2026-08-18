# 📊 TaskFlow

TaskFlow is a full-stack task and project management application designed to organize work through a simple and intuitive ticket-based workflow.

The application provides a Jira-inspired Kanban experience where users can create, manage, track, and organize tasks across different workflow stages.

---

## ✨ Features

- User authentication
- Task/ticket management
- Create and update tickets
- Kanban-style workflow
- Drag-and-drop task organization
- Task status management
- Dashboard and project overview
- Ticket statistics
- Task categorization
- Backend REST API
- Streamlit-based frontend
- PostgreSQL database integration
- Interactive charts and visualizations

---

## 📋 Task Workflow

TaskFlow uses a simple workflow:

```text
┌──────────┐
│  To Do   │
└────┬─────┘
     │
     ▼
┌─────────────┐
│ In Progress │
└──────┬──────┘
       │
       ▼
┌──────────┐
│  Review  │
└────┬─────┘
     │
     ▼
┌──────────┐
│   Done   │
└──────────┘