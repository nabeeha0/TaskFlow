from fastapi import FastAPI
from sqlalchemy import text

from app.database.database import engine 
import app.database.base

from app.routes.user import router as user_router
from app.routes.auth import router as auth_router
from app.routes.project import router as project_router
from app.routes.ticket import router as ticket_router
from app.routes.comment import router as comment_router
from app.routes.project_member import router as project_member_router
from app.routes.label import router as label_router
from app.routes.attachment import router as attachment_router
from app.routes.dashboard import router as dashboard_router


app = FastAPI(title="TaskFlow API")

app.include_router(user_router)
app.include_router(auth_router)
app.include_router(project_router)
app.include_router(ticket_router)
app.include_router(comment_router)
app.include_router(project_member_router)
app.include_router(label_router)
app.include_router(attachment_router)
app.include_router(dashboard_router)

@app.get("/")
def root():
    return {"message": "TaskFlow API is running!"}


@app.get("/db-test")
def db_test():
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            return {
                "message": "Database connected successfully!",
                "result": result.scalar()
            }
    except Exception as e:
        return {"error": str(e)}