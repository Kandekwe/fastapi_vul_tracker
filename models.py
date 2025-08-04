from pydantic import BaseModel
from typing import List, Optional


class ProjectCreate(BaseModel):
    name: str
    description: str
    requirements: List[str]


class Dependency(BaseModel):
    name: str
    version: str
    vulnerabilities: List[dict]


class Project(BaseModel):
    id: Optional[int] = None
    name: str
    description: str
    dependencies: List[Dependency]
