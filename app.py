from flask import Flask, render_template, send_from_directory, request, jsonify
import requests

app = Flask(__name__)

# Complete structured baseline from your CV profile data
PROFILE_DATA = {
    "developer": "Thato Khonkhe",
    "role": "Aspiring Technical Analyst & Full-Stack Developer",
    "contact": {
        "email": "Siyaballack1@gmail.com",
        "linkedin": "https://linkedin.com/in/thato-siyabonga-khonkhe-b07a12226",
        "github": "https://github.com/Mabals",
        "location": "Soweto, Johannesburg"
    },
    "summary": "Ambitious and solutions-driven professional with a strong background in Computer Science and Information Technology. Proven track record in building automated, data-driven frameworks, deploying scalable web applications, and implementing predictive architectures.",
    "certifications": [
        "PCAP – Certified Associate Python Programmer",
        "AWS Certified Cloud Practitioner"
    ],
    "skills": {
        "languages": ["Python (PCAP)", "Java", "C#", "SQL", "HTML", "CSS"],
        "data_ai": ["Google GenAI SDK (Gemini API)", "Prompt Engineering", "Data Parsing", "Predictive Modeling"],
        "frameworks": ["Flask", "Django", "Matplotlib", "Pandas", "Numpy", "pyodbc"],
        "tools": ["AWS", "Power BI Desktop", "SSMS", "VS Code", "Visual Studio"]
    }
}

# Explicit mapped descriptions from your CV to cross-match with GitHub Repos
CV_PROJECT_DETAILS = {
    "Thato-Learning-Architecture-TLA--Project": {
        "title": "The Thato Learning Architecture (TLA)",
        "desc": "Engineered an enterprise-grade corporate talent development ecosystem featuring a Python data engine, a responsive Flask administrative portal, and automated AI evaluation pipelines with the Google GenAI SDK.",
        "tags": ["Python", "Flask", "Google GenAI SDK", "SQL Server", "Power BI"]
    },
    "StratumAnalytics": {
        "title": "Stratum Analytics Predictive Engine",
        "desc": "Engineered an independent full-stack predictive web platform modeling historical soccer metrics utilizing an advanced Poisson Distribution Matrix algorithm to map precise outcome vectors.",
        "tags": ["Python", "Flask", "MS SQL Server", "Poisson Distribution", "Data Analytics"]
    },
    "Sales_Dashboard": {
        "title": "Sales Performance Dashboard",
        "desc": "Built a comprehensive data visualization dashboard tracking regional performance using Pandas and Matplotlib to isolate organizational growth bottlenecks.",
        "tags": ["Python", "Pandas", "Matplotlib", "Data Visualization"]
    }
}

def fetch_live_github_repos():
    """Queries the live GitHub API and enhances repo entries dynamically"""
    url = "https://api.github.com/users/Mabals/repos"
    refined_projects = []
    
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            repos = response.json()
            for repo in repos:
                name = repo.get("name")
                # Look for matching target items matching your CV repositories
                if name in CV_PROJECT_DETAILS:
                    refined_projects.append({
                        "title": CV_PROJECT_DETAILS[name]["title"],
                        "description": CV_PROJECT_DETAILS[name]["desc"],
                        "tags": CV_PROJECT_DETAILS[name]["tags"],
                        "github_url": repo.get("html_url"),
                        "stars": repo.get("stargazers_count", 0),
                        "language": repo.get("language", "Python")
                    })
        
        # Fallback if GitHub rate limits occur or repositories are private
        if not refined_projects:
            raise ValueError("No matching repos returned.")
            
    except Exception as e:
        # Secure manual fail-safe backup array
        for name, details in CV_PROJECT_DETAILS.items():
            refined_projects.append({
                "title": details["title"],
                "description": details["desc"],
                "tags": details["tags"],
                "github_url": f"https://github.com/Mabals/{name}",
                "stars": 0,
                "language": "Python"
            })
            
    return refined_projects

@app.route('/')
def home():
    live_projects = fetch_live_github_repos()
    return render_template('index.html', profile=PROFILE_DATA, projects=live_projects)

# Dedicated download action endpoint serving your actual file
@app.route('/download-cv')
def download_cv():
    return send_from_directory(
        directory='static',
        path='Thato_Khonkhe_CV_Final.pdf',
        as_attachment=True
    )

# Form route handler proving backend interaction capabilities to recruiters
@app.route('/submit-contact', methods=['POST'])
def handle_contact():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    message = data.get('message')
    
    # In a full ecosystem, you could store this inside a database or send an automated email.
    print(f"System Message Logged from {name} ({email}): {message}")
    
    return jsonify({"status": "success", "message": "Handshake complete. Message parsed securely."})

if __name__ == '__main__':
    app.run(debug=True, port=5000)