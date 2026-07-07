import requests
from functools import lru_cache
from django.conf import settings


def fetch_gist_file(url):
    response = requests.get(url, timeout=5)
    response.raise_for_status()
    return response.json()

portfolio_cache = None
model_list= None    

@lru_cache(maxsize=1)
def pp_gist_data():
    
    global portfolio_cache
    global model_list

    if portfolio_cache is not None:
        print("Using cached portfolio data")  # Debugging line to check cache usage
        return portfolio_cache, model_list
        
    personal_data = fetch_gist_file(settings.ENV_PERSONAL_DATA)
    print("portfolio_data fetched ")
    # print("portfolio_data : ", personal_data)
    experience_data = fetch_gist_file(settings.ENV_EXPERIENCE_DATA)
    print("experience_data fetched")
    # print("experience_data : ", experience_data)
    project_data = fetch_gist_file(settings.ENV_PROJECT_DATA)
    print("project_data fetched")
    # print("project_data : ", project_data)
    skills_data = fetch_gist_file(settings.ENV_SKILLS_DATA)
    print("skills_data fetched")
    # print("skills_data : ", skills_data)
    education_certificate_data = fetch_gist_file(settings.ENV_EDU_CERT_DATA)
    print("education_certificate_data fetched")
    # print("education_certificate_data : ", education_certificate_data)
    model_data = fetch_gist_file(settings.ENV_MODEL_LIST)
    model_list = model_data["model"]
    print("Model_name fetched", model_list)

    
    # personal_data = {
    #     'personalInfo': {
    #         'name': 'Aniket Panchal',
    #         'title': 'Full-Stack Developer',
    #         'title2': 'AI Application & Agent Developer',
    #         'location': 'Mumbai, India',
    #         'email': 'aniketvilaspanchal@gmail.com',
    #         'linkedin': 'https://linkedin.com/in/aniket-vilas-panchal',
    #         'github': 'https://github.com/babanigit',
    #         'portfolio': 'https://pixelify-porfolio-ts-git-main-aniket-panchals-projects.vercel.app'
    #     },
    #     'summary': 'Software developer with experience building scalable web applications and a growing focus on artificial intelligence. Passionate about developing intelligent systems, AI-powered applications, and continuously learning new technologies to solve real-world problems.'
    # }

    # experience_data = [
    #     {
    #         'role': 'Software Developer',
    #         'company': 'HealthIndia Insurance TPA Services Pvt. Ltd.',
    #         'location': 'Mumbai, India',
    #         'duration': '2025-06 - Present',
    #         'company_link': 'https://www.healthindiatpa.com/',
    #         'tech_stack': ['Angular', 'TypeScript', 'ASP.NET Core', 'SQL Server', '.NET Framework', 'REST API', 'Git', 'Tortoise SVN', 'Postman'],
    #         'highlights': [
    #             'Develop and maintain enterprise web applications using Angular and TypeScript.',
    #             'Design and implement scalable backend services with ASP.NET Core and C#.',
    #             'Build and optimize SQL Server database schemas and queries for performance.',
    #             'Develop and integrate RESTful APIs across internal systems.',
    #             'Perform API testing and debugging using Postman.',
    #             'Collaborate with cross-functional teams to deliver production-ready features.',
    #             'Contribute to version control and code management using Git and SVN.'
    #         ],
    #         'image': 'healthindia.png'
    #     },
    #     {
    #         'role': 'Angular Developer Intern',
    #         'company': 'Markets Mojo',
    #         'location': 'Mumbai, India',
    #         'duration': '2024-07 - 2024-09',
    #         'company_link': 'https://www.marketsmojo.com/',
    #         'github': 'https://github.com/babanigit/markets_mojo_v16',
    #         'tech_stack': ['Angular', 'TypeScript', 'Highcharts', 'Chrome DevTools'],
    #         'highlights': [
    #             'Migrated legacy Angular pages to Angular 16 with TypeScript, improving performance and maintainability.',
    #             'Integrated Highcharts for financial data visualization, enhancing analytical insights.',
    #             'Optimized debugging and performance profiling using Chrome DevTools.'
    #         ],
    #         'image': 'marketsmojo.png'
    #     }
    # ]

    # project_data = [
    #     {
    #         'title': 'Finshark',
    #         'tech_stack': 'ASP.NET Core, React.js, TypeScript, TailwindCSS, PostgreSQL, Docker',
    #         'description': [
    #             'Developed a real-time stock tracking platform with secure JWT-based authentication.',
    #             'Integrated the Financial Modeling Prep (FMP) API to fetch live company and stock market data.',
    #             'Implemented interactive commenting features to increase community engagement.',
    #             'Optimized API performance using DTOs, interfaces, and query parameters, improving response time by 30%.'
    #         ],
    #         'project_link': 'https://github.com/babanigit/Finshark',
    #         'live_link': 'https://finshark-production.up.railway.app/',
    #         'status': 'Completed',
    #         'tags': ['ASP.NET', 'React.js', 'TypeScript', 'TailwindCSS', 'PostgreSQL', 'Docker', 'JWT'],
    #         'highlight': 'Full-stack financial research platform with real-time stock data',
    #         'date_created': '2025-05-11'
    #     },
    #     {
    #         'title': 'Multiplayer Tic-Tac-Toe',
    #         'tech_stack': 'TypeScript, Node.js, Express.js, MongoDB, React.js, TailwindCSS',
    #         'description': [
    #             'Built a real-time multiplayer game supporting 100+ concurrent users.',
    #             'Integrated Stream Chat for live messaging between players.',
    #             'Implemented secure authentication using JWT and Bcrypt.',
    #             'Designed a responsive UI for smooth gameplay across devices.'
    #         ],
    #         'project_link': 'https://github.com/babanigit/Tic-Tac-Toe-Game',
    #         'status': 'Completed',
    #         'tags': ['Node.js', 'Express.js', 'MongoDB', 'TypeScript', 'React.js', 'JWT', 'Real-time'],
    #         'highlight': 'Real-time multiplayer gaming platform with live chat',
    #         'date_created': '2024-02-10'
    #     },
    #     # ... add remaining projects the same way
    # ]

    # skills_data = {
    #     'Languages': [
    #         {'name': 'JavaScript', 'level': 'Advanced', 'is_active': 1},
    #         {'name': 'TypeScript', 'level': 'Advanced', 'is_active': 1},
    #         {'name': 'Python', 'level': 'Advanced', 'is_active': 1},
    #         {'name': 'C', 'level': 'Intermediate', 'is_active': 1},
    #         {'name': 'C++', 'level': 'Intermediate', 'is_active': 1},
    #         {'name': 'C#', 'level': 'Intermediate', 'is_active': 1},
    #         {'name': 'SQL', 'level': 'Intermediate', 'is_active': 1},
    #         {'name': 'HTML', 'level': 'Advanced', 'is_active': 1},
    #         {'name': 'CSS', 'level': 'Advanced', 'is_active': 1},
    #     ],
    #     'Frameworks': [
    #         {'name': 'Angular', 'level': 'Advanced', 'is_active': 1},
    #         {'name': 'Next.js', 'level': 'Advanced', 'is_active': 1},
    #         {'name': 'React', 'level': 'Advanced', 'is_active': 1},
    #         {'name': 'Django', 'level': 'Advanced', 'is_active': 1},
    #         {'name': 'Node.js', 'level': 'Advanced', 'is_active': 1},
    #         {'name': 'Express.js', 'level': 'Advanced', 'is_active': 1},
    #         {'name': 'ASP.NET', 'level': 'Intermediate', 'is_active': 1},
    #         {'name': 'React Native', 'level': 'Beginner', 'is_active': 0},
    #     ],
    #     # ... add Libraries, Databases, Tools, Concepts the same way
    # }

    # education_certificate_data = {
    #     'Educations': [
    #         {
    #             'title': 'Tilak Maharashtra Vidyapeeth',
    #             'year': '2021 - 2024',
    #             'subtitle': 'Bachelor in Computer Application',
    #             'details': [
    #                 'Studied core subjects like Data Structures, DBMS, Networking, Security, OOPs, Web Development, etc.',
    #                 'Implemented several projects based on learned concepts.'
    #             ],
    #             'grade': 'CGPA - 7.01'
    #         },
    #         {
    #             'title': 'Chetna College',
    #             'year': '2018 - 2020',
    #             'subtitle': 'Higher Secondary School Certificate',
    #             'details': ['Commerce with Mathematics'],
    #             'grade': '60%'
    #         }
    #     ],
    #     'Certificates': [
    #         {
    #             'title': 'Google Data Analysis',
    #             'issued_by': 'Google',
    #             'issue_date': '2024-03-15',
    #             'skills': ['Data Analysis', 'R Programming', 'Problem Solving']
    #         },
    #         {
    #             'title': 'Introduction to Cybersecurity Fundamentals',
    #             'issued_by': 'Google',
    #             'issue_date': '2023-11-20',
    #             'skills': ['Cybersecurity', 'Threat Analysis', 'Security Awareness']
    #         }
    #     ]
    # }
    
    # print("Fetched new portfolio data")  # Debugging line to confirm data fetching
    
    portfolio_cache = {
        "personal": personal_data,
        "experience": experience_data,
        "projects": project_data,
        "skills": skills_data,
        "education": education_certificate_data
    }

    return portfolio_cache, model_list
