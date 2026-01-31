"""Job search service using RapidAPI JSearch"""
import requests
from utils.config import RAPIDAPI_KEY, JSEARCH_API_URL, JSEARCH_API_HOST

def search_jobs(keywords, location, date_posted="month", num_results=10):
    """
    Search for jobs using RapidAPI JSearch
    
    Args:
        keywords (str): Job search keywords
        location (str): Job location
        date_posted (str): Time filter (month, week, 3days, today, all)
        num_results (int): Maximum number of results
        
    Returns:
        list: List of job dictionaries
    """
    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": JSEARCH_API_HOST
    }
    
    keywords = (keywords or "developer").strip()
    location = (location or "India").strip()
    query = f"{keywords} in {location}"
    
    querystring = {
        "query": query,
        "page": "1",
        "num_pages": "1",
        "date_posted": date_posted
    }
    
    try:
        response = requests.get(JSEARCH_API_URL, headers=headers, params=querystring, timeout=15)
        response.raise_for_status()
        data = response.json()
        
        jobs = []
        for job in data.get("data", [])[:num_results]:
            jobs.append(_format_job(job))
        
        return jobs
        
    except requests.exceptions.HTTPError as he:
        if response.status_code == 403:
            raise Exception("Invalid API key or not subscribed")
        elif response.status_code == 429:
            raise Exception("Rate limit exceeded (150/month)")
        else:
            raise Exception(f"HTTP Error: {he}")
    except Exception as e:
        raise Exception(f"Search error: {str(e)}")

def _format_job(job):
    """Format job data from API response"""
    title = job.get("job_title") or "N/A"
    company = job.get("employer_name") or "N/A"
    city = job.get("job_city") or ""
    country = job.get("job_country") or ""
    location_str = f"{city}, {country}".strip(", ") or "N/A"
    description = (job.get("job_description") or "No description available")[:500] + "..."
    link = job.get("job_apply_link") or "#"
    posted = (job.get("job_posted_at_datetime_utc") or "N/A")[:10]
    employment_type = job.get("job_employment_type") or "N/A"
    source = job.get("job_publisher") or "N/A"
    
    # Format salary
    salary = ""
    if job.get("job_min_salary") and job.get("job_max_salary"):
        currency = job.get("job_salary_currency") or ""
        min_sal = job.get("job_min_salary") or 0
        max_sal = job.get("job_max_salary") or 0
        salary = f"{currency} {min_sal:,} - {max_sal:,}"
    
    return {
        "title": title,
        "company": company,
        "location": location_str,
        "description": description,
        "link": link,
        "posted": posted,
        "salary": salary,
        "employment_type": employment_type,
        "source": source
    }