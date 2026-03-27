from fastapi import FastAPI
from .routers import citizens, employers, vacancies, applications, skills

app = FastAPI(title="Employment Center API")

app.include_router(citizens.router)
app.include_router(employers.router)
app.include_router(vacancies.router)
app.include_router(applications.router)
app.include_router(skills.router)
