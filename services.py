from models import Project, Dependency
from storage import projects, dependencies
from fetch_osv import osv_fetch

# parsing requirements before creating a project


def parse_requirements(requirements: str) -> list[tuple[str, str | None]]:
    depends = []
    for line in requirements.strip().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        for sep in ["==", ">=", "<=", "~=", ">", "<"]:
            if sep in line:
                name, version = line.split(sep, 1)
                depends.append((name.strip(), version.strip()))
                break
        else:
            depends.append((line, None))
    return depends

# project creation


def create_project(name, description, requirements):
    depends = parse_requirements(requirements)
    depends_objects = []

    for pkg_name, version in depends:
        vulns = osv_fetch(pkg_name, version)
        depends = Dependency(
            name=pkg_name, version=version, vulnerabilities=vulns)
        depends_objects.append(depends)
        dependencies.setdefault(pkg_name, []).append(name)

    project = Project(name=name, description=description,
                      dependencies=depends_objects)
    projects[name] = project
    return project

# get all projects


def get_all_projects():
    return list(projects.values())

# get a project by name


def get_project(name):
    return projects.get(name)

# get all dependencies


def get_all_dependencies():
    result = []
    for pkg, projects_list in dependencies.items():
        result.append({"package": pkg, "used_in": projects_list})
    return result

# get each dependencies with its details and where it is used in a project


def get_dependency_details(pkg_name):
    used_in = dependencies.get(pkg_name, [])
    vulnerability_versions = []
    for proj in used_in:
        for depend in projects[proj].dependencies:
            if depend.name == pkg_name:
                vulnerability_versions.append({
                    "version": depend.version,
                    "vulnerabilities": depend.vulnerabilities
                })
    return {"package": pkg_name, "used_in": used_in, "details": vulnerability_versions}
