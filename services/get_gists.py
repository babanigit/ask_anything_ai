import requests
from functools import lru_cache


def fetch_gist_file(url):
    response = requests.get(url, timeout=5)
    response.raise_for_status()
    return response.json()


portfolio_cache = None

@lru_cache(maxsize=1)
def load_portfolio_data():
    
    global portfolio_cache

    if portfolio_cache is not None:
        print("Using cached portfolio data")  # Debugging line to check cache usage
        return portfolio_cache
    
    experience_data = fetch_gist_file("https://gist.githubusercontent.com/babanigit/43103848b14f49b18387bb1c678bd599/raw/getExperience.json")
    project_data = fetch_gist_file("https://gist.githubusercontent.com/babanigit/fdf26ec31d044caccefc83d4349b5a67/raw/getProjects.json")
    skills_data = fetch_gist_file("https://gist.githubusercontent.com/babanigit/61c0739ab835b4d850e08141161752bf/raw/getSkills.json")
    education_certificate_data = fetch_gist_file("https://gist.githubusercontent.com/babanigit/6e1f45b979154bc109323ef4afafa909/raw/getEduAndCerti.json")
    
    print("Fetched new portfolio data")  # Debugging line to confirm data fetching
    portfolio_cache = {
        "experience": experience_data,
        "projects": project_data,
        "skills": skills_data,
        "education": education_certificate_data
    }

    return portfolio_cache
