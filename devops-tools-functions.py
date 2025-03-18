import requests

SONAR_API_URL = "https://sonarqube.yourcompany.com/api/measures/component"
SONAR_TOKEN = "your_sonarqube_api_token"

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