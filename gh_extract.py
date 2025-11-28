import requests

class Release:
    def __init__(self, gh_data : dict):
        self.raw = gh_data
        self.version = gh_data["tag_name"].replace("v", "")
        self.swu_download_url = gh_data["assets"][0]["browser_download_url"]
        self.changelog = gh_data["body"][:511]
    
    def download_swu(self, dest_path: str):
        response = requests.get(self.swu_download_url)
        response.raise_for_status()
        with open(dest_path, "wb") as f:
            f.write(response.content)

    def print(self):
        print(f"Release version: {self.version}")
        print(f"SWU download URL: {self.swu_download_url}")
        print("Changelog:")
        print(self.changelog)

def fetch_latest_release(repo_owner: str, repo_name: str) -> Release:
    api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/releases/latest"
    response = requests.get(api_url)
    response.raise_for_status()
    gh_data = response.json()
    return Release(gh_data)

if __name__ == "__main__":
    release = fetch_latest_release("OpenCentauri", "cc-fw-tools")
    release.print()