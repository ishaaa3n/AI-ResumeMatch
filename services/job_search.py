"""Job search service using RapidAPI JSearch"""
import requests
from utils.config import RAPIDAPI_KEY, JSEARCH_API_URL, JSEARCH_API_HOST

"""Job search service using RapidAPI JSearch"""
import requests
from utils.config import RAPIDAPI_KEY, JSEARCH_API_URL, JSEARCH_API_HOST

"""Job search service using RapidAPI JSearch"""
import requests
from utils.config import RAPIDAPI_KEY, JSEARCH_API_URL, JSEARCH_API_HOST

def search_jobs(keywords, location, date_posted="month", num_results=10, resume_info=None):
    """
    Search for jobs using RapidAPI JSearch with intelligent filtering
    
    Args:
        keywords (str): Job search keywords
        location (str): Job location
        date_posted (str): Time filter (month, week, 3days, today, all)
        num_results (int): Maximum number of results
        resume_info (dict): Resume information for intelligent filtering
        
    Returns:
        list: List of job dictionaries
    """
    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": JSEARCH_API_HOST
    }
    
    # Modify keywords based on experience level
    keywords = _enhance_keywords_by_experience(keywords, resume_info)
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
        for job in data.get("data", [])[:num_results * 2]:  # Get more to filter
            formatted_job = _format_job(job)
            
            # Apply intelligent filtering
            if resume_info and _is_job_match(formatted_job, resume_info):
                jobs.append(formatted_job)
            elif not resume_info:
                jobs.append(formatted_job)
            
            if len(jobs) >= num_results:
                break
        
        return jobs[:num_results]
        
    except requests.exceptions.HTTPError as he:
        if response.status_code == 403:
            raise Exception("Invalid API key or not subscribed")
        elif response.status_code == 429:
            raise Exception("Rate limit exceeded (150/month)")
        else:
            raise Exception(f"HTTP Error: {he}")
    except Exception as e:
        raise Exception(f"Search error: {str(e)}")

def _enhance_keywords_by_experience(keywords, resume_info):
    """
    Enhance search keywords based on experience level
    
    Args:
        keywords (str): Original search keywords
        resume_info (dict): Resume information
        
    Returns:
        str: Enhanced keywords
    """
    if not resume_info:
        return keywords.strip()
    
    years_exp = resume_info.get("years_experience", 0)
    keywords = keywords.strip()
    
    # Add experience-level qualifiers
    if years_exp == 0:
        # Student/fresher
        if not any(word in keywords.lower() for word in ["intern", "entry", "fresher", "junior", "trainee"]):
            keywords = f"entry level {keywords}"
    elif years_exp <= 2:
        # Junior level
        if not any(word in keywords.lower() for word in ["junior", "entry", "associate"]):
            keywords = f"junior {keywords}"
    elif years_exp <= 5:
        # Mid level (keep as is)
        pass
    else:
        # Senior level
        if not any(word in keywords.lower() for word in ["senior", "lead", "principal"]):
            keywords = f"senior {keywords}"
    
    return keywords

def _is_job_match(job, resume_info):
    """
    Check if job matches candidate's experience level
    
    Args:
        job (dict): Job information
        resume_info (dict): Resume information
        
    Returns:
        bool: True if job is a good match
    """
    years_exp = resume_info.get("years_experience", 0)
    job_title = job.get("title", "").lower()
    job_description = job.get("description", "").lower()
    
    # Define exclusion keywords for each experience level
    if years_exp == 0:
        # Fresher/Student - exclude senior/experienced positions
        exclude_keywords = [
            "senior", "sr.", "lead", "principal", "staff", "architect",
            "5+ years", "5 years", "6+ years", "7+ years", "8+ years",
            "experienced", "expert", "manager", "director"
        ]
        
        # Prefer entry-level keywords
        prefer_keywords = [
            "intern", "internship", "fresher", "entry level", "junior",
            "trainee", "graduate", "new grad", "0-1 years", "campus"
        ]
        
        # Check for exclusions
        for keyword in exclude_keywords:
            if keyword in job_title or keyword in job_description:
                return False
        
        # Boost jobs with preferred keywords (but don't require them)
        return True
        
    elif years_exp <= 2:
        # Junior level (1-2 years) - exclude very senior positions
        exclude_keywords = [
            "senior", "sr.", "lead", "principal", "staff", "architect",
            "5+ years", "6+ years", "7+ years", "8+ years",
            "manager", "director"
        ]
        
        for keyword in exclude_keywords:
            if keyword in job_title or keyword in job_description:
                return False
        
        return True
        
    elif years_exp <= 5:
        # Mid level (3-5 years) - exclude very senior and very junior
        exclude_senior = ["principal", "staff", "architect", "director", "10+ years"]
        exclude_junior = ["intern", "internship", "trainee"]
        
        for keyword in exclude_senior + exclude_junior:
            if keyword in job_title:
                return False
        
        return True
        
    else:
        # Senior level (5+ years) - exclude junior positions
        exclude_keywords = [
            "intern", "internship", "fresher", "entry level", 
            "junior", "trainee", "graduate"
        ]
        
        for keyword in exclude_keywords:
            if keyword in job_title:
                return False
        
        return True

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