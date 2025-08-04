from fastapi import FastAPI, HTTPException
from models import ProjectCreate, Project
from services import (create_project as create_project_service, get_all_projects, get_project,
                      get_all_dependencies, get_dependency_details
                      )

app = FastAPI()

# Endpoints to navigate our business logic and responses


@app.get("/")
def start_root():
    return {"message": "Welcome to the Vulnability tracker"}


@app.post("/projects", response_model=Project)
async def create_project(project: ProjectCreate):
    return create_project_service(
        name=project.name,
        description=project.description,
        requirements="\n".join(project.requirements)
    )


@app.get("/projects")
def list_projects():
    return get_all_projects()


@app.get("/projects/{name}")
def get_project_endpoint(name: str):
    proj = get_project(name)
    if not proj:
        raise HTTPException(status_code=404, detail="Project not found")
    return proj


@app.get("/dependencies")
def list_dependencies():
    return get_all_dependencies()


@app.get("/dependencies/{pkg_name}")
def get_dependency(pkg_name: str):
    return get_dependency_details(pkg_name)
