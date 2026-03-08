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
    
    # experience_data =  [{'role': 'Software Developer', 'duration': 'June 2025 - Present', 'company': 'HealthIndia Insurance TPA Services Pvt. Ltd.', 'location': 'Mumbai, India', 'companyLink': 'https://www.healthindiatpa.com/', 'techStack': ['Angular', 'ASP.NET Core', 'SQL', '.NET Framework', 'TypeScript', 'Postman API', 'Tortoise SVN', 'Git', 'SQL Server Management Studio', 'Visual Studio', 'HTML5', 'C#'], 'highlights': ['Develop and maintain front-end architecture using Angular and TypeScript.', 'Design and implement scalable, responsive, and cross-platform web applications.', 'Build and manage robust back-end systems using ASP.NET Core and C#.', 'Create and optimize complex database schemas with SQL Server.', 'Design RESTful APIs and ensure seamless integration across services.', 'Use Postman for API testing and debugging.', 'Manage code versioning using Git and Tortoise SVN.', 'Lead projects from concept through to deployment with focus on performance and UX.', 'Stay updated with latest trends and best practices in full-stack development.'], 'image': 'healthindia.png'}, {'role': 'Angular Developer, Internship', 'duration': 'July 2024 - September 2024', 'company': 'Markets Mojo, Stock Research Organization, Mumbai', 'location': 'Mumbai, India', 'github': 'https://github.com/babanigit/markets_mojo_v16', 'companyLink': 'https://www.marketsmojo.com/', 'techStack': ['Angular', 'TypeScript', 'Highcharts', 'Chrome DevTools'], 'highlights': ['Migrated old Angular pages to Angular 16 + TypeScript, boosting performance.', 'Integrated Highcharts for Data Visualization, improving insights by 30%.', 'Leveraged Chrome DevTools to enhance debugging and profiling efficiency.'], 'image': 'mario.png'}] 
    
    personal_data = fetch_gist_file("https://gist.githubusercontent.com/babanigit/a0e0e15cc12c23c54b0f9227750f4b10/raw/getPersonal.json")
    experience_data = fetch_gist_file("https://gist.githubusercontent.com/babanigit/43103848b14f49b18387bb1c678bd599/raw/getExperience.json")
    project_data = fetch_gist_file("https://gist.githubusercontent.com/babanigit/fdf26ec31d044caccefc83d4349b5a67/raw/getProjects.json")
    skills_data = fetch_gist_file("https://gist.githubusercontent.com/babanigit/61c0739ab835b4d850e08141161752bf/raw/getSkills.json")
    education_certificate_data = fetch_gist_file("https://gist.githubusercontent.com/babanigit/6e1f45b979154bc109323ef4afafa909/raw/getEduAndCerti.json")
    
    print("Fetched new portfolio data")  # Debugging line to confirm data fetching
    portfolio_cache = {
        "personal": personal_data,
        "experience": experience_data,
        "projects": project_data,
        "skills": skills_data,
        "education": education_certificate_data
    }

    return portfolio_cache
