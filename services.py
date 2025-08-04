from models import Project, Dependency
from storage import projects, dependencies
from fetch_osv import query_osv


def parse_requirements(requirements: str) -> list[tuple[str, str | None]]:
    deps = []
    for line in requirements.strip().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        for sep in ["==", ">=", "<=", "~=", ">", "<"]:
            if sep in line:
                name, version = line.split(sep, 1)
                deps.append((name.strip(), version.strip()))
                break
        else:
            deps.append((line, None))  # No version specified
    return deps


def create_project(name, description, requirements):
    deps = parse_requirements(requirements)  # now a list of (name, version)
    dep_objs = []

    for pkg_name, version in deps:
        vulns = query_osv(pkg_name, version)  # ✅ fixed
        dep = Dependency(name=pkg_name, version=version, vulnerabilities=vulns)
        dep_objs.append(dep)
        dependencies.setdefault(pkg_name, []).append(name)

    project = Project(name=name, description=description,
                      dependencies=dep_objs)
    projects[name] = project
    return project


def get_all_projects():
    return list(projects.values())


def get_project(name):
    return projects.get(name)


def get_all_dependencies():
    result = []
    for pkg, proj_list in dependencies.items():
        result.append({"package": pkg, "used_in": proj_list})
    return result


def get_dependency_details(pkg_name):
    used_in = dependencies.get(pkg_name, [])
    vuln_versions = []
    for proj in used_in:
        for dep in projects[proj].dependencies:
            if dep.name == pkg_name:
                vuln_versions.append({
                    "version": dep.version,
                    "vulnerabilities": dep.vulnerabilities
                })
    return {"package": pkg_name, "used_in": used_in, "details": vuln_versions}
