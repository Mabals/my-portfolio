from flask import Flask, render_template, send_from_directory, request, jsonify
import requests

app = Flask(__name__)

# Profile data, sourced from the CV
PROFILE_DATA = {
    "developer": "Thato Khonkhe",
    "role": "Aspiring Technical Analyst & Full-Stack Developer",
    "contact": {
        "email": "Siyaballack1@gmail.com",
        "phone": "081 373 8241",
        "linkedin": "https://www.linkedin.com/in/thato-siyabonga-khonkheb07a12226",
        "github": "https://github.com/Mabals",
        "location": "Diepkloof, Soweto"
    },
    "summary": (
        "Ambitious and solutions-driven professional with a background in Information "
        "Technology, currently gaining structured experience as a Full-Stack Developer "
        "(Work-Integrated Learning) at Mindworx Consulting & Academy. I like turning "
        "abstract business rules into secure, working applications — and messy datasets "
        "into a clear story — and I'm always picking up new tools along the way."
    ),
    "certifications": [
        "PCAP — Certified Associate Python Programmer",
        "AWS Certified Cloud Practitioner"
    ],
    "education": [
        {"degree": "BSc Information Technology", "school": "North-West University", "dates": "2021 – 2024"},
        {"degree": "Matric NSC", "school": "Jet Nteo Secondary School", "dates": "2016 – 2020"}
    ],
    "experience": [
        {
            "role": "Full-Stack Developer (WIL)",
            "org": "Mindworx Consulting & Academy",
            "dates": "Sep 2025 – Current",
            "bullets": [
                "Leveraged technical training in AWS Cloud Computing, Python data libraries, and Machine Learning to build scalable internal applications.",
                "Owned the end-to-end development life cycle — coding, troubleshooting, and technical documentation — for internal pod delivery teams.",
                "Translated abstract project requirements into structured technical designs aligned with enterprise governance standards."
            ]
        }
    ],
    "skills": {
        "Languages": ["Python (PCAP)", "JavaScript", "TypeScript", "Java", "C#", "SQL", "HTML", "CSS"],
        "Web development": ["React", "Node.js", "Express", "Django", "Flask", "Jinja2", "Bootstrap 5", "Chart.js"],
        "AI & data engineering": ["Google GenAI SDK (Gemini API)", "Prompt engineering", "Automated data extraction", "Predictive modeling", "EDA"],
        "Data libraries": ["Pandas", "NumPy", "Matplotlib", "pyodbc"],
        "Platforms & tools": ["Git", "GitHub", "AWS", "Power BI", "SSMS", "VS Code", "PyCharm", "Excel"],
    }
}

# Explicit project copy, keyed by exact GitHub repo name, in the order they should display.
# The dict order is the display order (Match IQ featured first).
CV_PROJECT_DETAILS = {
    "mabals-matchiq": {
        "title": "Mabals Match IQ",
        "desc": "A full-stack football analytics platform that turns raw fixture data into AI-generated pre-match insight. Pulls live fixtures, form, and head-to-head stats across four European leagues via the football-data.org API, then uses the Gemini API to generate result-tendency, BTTS, and Over/Under insight strictly derived from the computed statistics. API keys stay server-side behind a responsive, tabbed React UI.",
        "tags": ["React", "TypeScript", "Node.js", "Express", "Gemini API"],
        "featured": True
    },
    "Edu-Track-Student-System": {
        "title": "EduTrack",
        "desc": "A Django school management system with full CRUD for students and teachers, a relational data model linking students to classes and teachers to departments, view-level auth, and a Chart.js analytics dashboard with Gemini-generated insight on live enrollment and staffing data.",
        "tags": ["Django", "Chart.js", "Gemini API"],
        "featured": False
    },
    "shopwave-analysis": {
        "title": "ShopWave Sales & Customer Analysis",
        "desc": "Cleaned and analyzed a two-table e-commerce dataset (~6,800 rows) with Python and Pandas — fixing inconsistent formatting, mixed date formats, and missing data — then built an interactive Power BI dashboard with slicers, KPI cards, and multi-dimensional revenue breakdowns.",
        "tags": ["Python", "Pandas", "Power BI"],
        "featured": False
    },
    "Sales_Dashboard": {
        "title": "Sales Performance Dashboard",
        "desc": "Self-directed analysis of 10,000 retail sales records to track revenue by region and flag growth opportunities — regional GroupBy breakdowns, two client-ready charts, and exported stakeholder deliverables in CSV and Excel.",
        "tags": ["Python", "Pandas", "Matplotlib"],
        "featured": False
    },
    "StratumAnalytics": {
        "title": "Stratum Analytics",
        "desc": "A data engineering and predictive sports-analytics environment: ingests historical football fixture data into SQL Server, then models match outcome probabilities with a custom Poisson goal-expectancy engine, live standings tracking, and a historical backtester that scores model accuracy against past results.",
        "tags": ["Flask", "SQL Server", "pyodbc", "Poisson modeling"],
        "featured": False
    },
    "Thato-Learning-Architecture-TLA--Project": {
        "title": "The Thato Learning Architecture (TLA)",
        "desc": "A corporate talent-development platform concept: a Flask admin portal over a SQL Server star schema, an AI assessment generator (Gemini API) that turns curriculum documents into quiz banks, an algorithmic remediation engine, and a hybrid Power BI reporting layer for live and historical training data.",
        "tags": ["Flask", "SQL Server", "Gemini API", "Power BI"],
        "featured": False
    },
}


def fetch_live_github_repos():
    """Enrich the curated project copy with live star counts / language from the GitHub API.
    Falls back to static data (stars=0) if the API is unreachable or rate-limited.
    Display order always follows CV_PROJECT_DETAILS, never the API response order.
    """
    repos_by_name = {}
    try:
        response = requests.get("https://api.github.com/users/Mabals/repos", params={"per_page": 100}, timeout=5)
        if response.status_code == 200:
            for repo in response.json():
                repos_by_name[repo.get("name")] = repo
    except Exception:
        pass  # fall through to static fallback below

    projects = []
    for repo_name, details in CV_PROJECT_DETAILS.items():
        live = repos_by_name.get(repo_name)
        projects.append({
            "title": details["title"],
            "description": details["desc"],
            "tags": details["tags"],
            "featured": details["featured"],
            "github_url": (live.get("html_url") if live else None) or f"https://github.com/Mabals/{repo_name}",
            "stars": live.get("stargazers_count", 0) if live else 0,
        })
    return projects


@app.route('/')
def home():
    projects = fetch_live_github_repos()
    return render_template('index.html', profile=PROFILE_DATA, projects=projects)


@app.route('/download-cv')
def download_cv():
    return send_from_directory(
        directory='static',
        path='Thato_Khonkhe-CV_FullStack.pdf',
        as_attachment=True
    )


@app.route('/submit-contact', methods=['POST'])
def handle_contact():
    data = request.get_json(silent=True) or {}
    name = data.get('name', '').strip()
    email = data.get('email', '').strip()
    message = data.get('message', '').strip()

    if not name or not email or not message:
        return jsonify({"status": "error", "message": "All fields are required."}), 400

    # In production this would write to a database or send an email/Slack notification.
    print(f"[contact form] {name} <{email}>: {message}")

    return jsonify({"status": "success", "message": "Message received."})


if __name__ == '__main__':
    app.run(debug=True, port=5000)