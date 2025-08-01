from cachetools import TTLCache
import requests

osv_cache = TTLCache(maxsize=1000, ttl=3600)


def query_osv(package, version):
    cache_key = f"{package}=={version}"
    if cache_key in osv_cache:
        return osv_cache[cache_key]

    response = requests.post("https://api.osv.dev/v1/query", json={
        "package": {"name": package, "ecosystem": "PyPI"},
        "version": version
    })
    data = response.json()
    vuln_ids = [v["id"] for v in data.get("vulns", [])]
    osv_cache[cache_key] = vuln_ids
    return vuln_ids
