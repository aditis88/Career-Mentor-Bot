import requests
from bs4 import BeautifulSoup

def fetch_job_links(role, location="India", limit=5):
    query = role.replace(" ", "+")
    url = f"https://www.google.com/search?q={query}+jobs+in+{location}"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code != 200:
            return []

        soup = BeautifulSoup(response.text, "html.parser")
        links = []

        for link in soup.find_all("a", href=True):
            href = link["href"]
            if "url?q=" in href and ("linkedin.com/jobs" in href or "indeed.com" in href or "naukri.com" in href):
                job_url = href.split("url?q=")[1].split("&")[0]
                links.append({
                    "title": f"{role} Job",
                    "company": "Listed via Search",
                    "location": location,
                    "url": job_url
                })
            if len(links) >= limit:
                break

        return links

    except Exception:
        return []

def find_mock_jobs(role):
    return [
        {
            "title": f"{role} at TechNova",
            "company": "TechNova",
            "location": "Remote",
            "url": "https://example.com/job1"
        },
        {
            "title": f"Junior {role} at InnovateX",
            "company": "InnovateX",
            "location": "Bangalore",
            "url": "https://example.com/job2"
        },
        {
            "title": f"{role} Specialist at AIWorks",
            "company": "AIWorks",
            "location": "Hyderabad",
            "url": "https://example.com/job3"
        }
    ]
