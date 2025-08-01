from pydantic import BaseModel
from typing import List, Optional


class ProjectCreate(BaseModel):
    name: str
    description: str
    requirements: List[str]


class Project(BaseModel):
    id: int
    name: str
    description: str
    dependencies: List[str]


class Dependency(BaseModel):
    name: str
    projects: List[int]
    vulnerabilities: List[dict]
