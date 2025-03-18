import os
import requests

# SONAR_API_URL = "https://sonarcloud.io/projects/api/measures/component"
SONAR_API_URL = "https://sonarcloud.io/api/measures/component"
SONAR_TOKEN = os.environ.get('SONAR_TOKEN')

def get_sonar_data(repo_name):
    """Fetches code coverage, code smells, and security hotspots from SonarQube."""
    params = {
        "component": repo_name,  # SonarQube project key
        "metricKeys": "coverage,code_smells,security_hotspots"
    }
    headers = {
        "Authorization": f"Bearer {SONAR_TOKEN}"
    }
    response = requests.get(SONAR_API_URL, params=params, headers=headers)

    if response.status_code == 200:
        data = response.json()
        measures = {m["metric"]: m["value"] for m in data["component"]["measures"]}

        return {
            "code_coverage": measures.get("coverage", "N/A"),
            "code_smells": measures.get("code_smells", "N/A"),
            "security_hotspots": measures.get("security_hotspots", "N/A"),
        }

    print(f"Failed to fetch SonarQube data for {repo_name}: {response.status_code}")
    return {"code_coverage": "N/A", "code_smells": "N/A", "security_hotspots": "N/A"}

SNYK_API_URL = "https://snyk.io/api/v1/orgs/YOUR_ORG_ID/projects"
SNYK_TOKEN = "your_snyk_api_token"

def get_snyk_data(repo_name):
    """Fetches critical and high vulnerabilities from Snyk for a given repository."""
    headers = {"Authorization": f"token {SNYK_TOKEN}"}
    response = requests.get(SNYK_API_URL, headers=headers)

    if response.status_code == 200:
        projects = response.json().get("projects", [])
        for project in projects:
            if repo_name.lower() in project["name"].lower():
                return {
                    "critical_vulns": project["issueCountsBySeverity"].get("critical", "N/A"),
                    "high_vulns": project["issueCountsBySeverity"].get("high", "N/A"),
                }

    print(f"Failed to fetch Snyk data for {repo_name}: {response.status_code}")
    return {"critical_vulns": "N/A", "high_vulns": "N/A"}

CHECKMARX_API_URL = "https://checkmarx.yourcompany.com/api/v1/scans"
CHECKMARX_TOKEN = "your_checkmarx_api_token"

def get_checkmarx_data(repo_name):
    """Fetches security vulnerabilities from Checkmarx for a given repository."""
    headers = {"Authorization": f"Bearer {CHECKMARX_TOKEN}"}
    response = requests.get(CHECKMARX_API_URL, headers=headers)

    if response.status_code == 200:
        scans = response.json().get("scans", [])
        for scan in scans:
            if repo_name.lower() in scan["project"]["name"].lower():
                return {
                    "checkmarx_critical": scan["highSeverity"],
                    "checkmarx_high": scan["mediumSeverity"]
                }

    print(f"Failed to fetch Checkmarx data for {repo_name}: {response.status_code}")
    return {"checkmarx_critical": "N/A", "checkmarx_high": "N/A"}