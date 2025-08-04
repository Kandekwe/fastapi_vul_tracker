from cachetools import TTLCache
import requests

osv_cache = TTLCache(maxsize=1000, ttl=3600)

# function to call osv to fetch vulnerabilities associated to our projects


def osv_fetch(package, version):
    cache_key = f"{package}=={version}"
    if cache_key in osv_cache:
        return osv_cache[cache_key]

    response = requests.post("https://api.osv.dev/v1/query", json={
        "package": {"name": package, "ecosystem": "PyPI"},
        "version": version
    })
    data = response.json()
    vulnerabilities_ids = [vul["id"]
                           for vul in data.get("vulnerabilities", [])]
    osv_cache[cache_key] = vulnerabilities_ids
    return vulnerabilities_ids
