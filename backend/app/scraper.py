import requests
from bs4 import BeautifulSoup
from config.settings import GITHUB_TRENDING_URL, GITHUB_TRENDING_DEVELOPERS_URL, MAX_PROJECTS_TO_SCRAPE, GH_TOKEN
from app.github_api import get_repo_details, get_entity_details, get_entity_repos
from config.logging_config import get_logger
import time

logger = get_logger('scraper', 'INFO')

def scrape_github_trending():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    logger.info(f"⏳ Fetching top {MAX_PROJECTS_TO_SCRAPE} projects from GitHub Trending...")
    if not GH_TOKEN:
        logger.info("ℹ️ GH_TOKEN not set — will use basic scraped data only (no README, no detailed stats).")
    try:
        response = requests.get(GITHUB_TRENDING_URL, headers=headers, timeout=20)
        response.raise_for_status()
    except requests.RequestException as e:
        logger.error(f"❌ Error fetching GitHub page: {e}")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')
    repo_list = []
    for repo_element in soup.find_all('article', class_='Box-row')[:MAX_PROJECTS_TO_SCRAPE]:
        title_element = repo_element.find('h2', class_='h3')
        if not title_element:
            continue
            
        repo_name_raw = title_element.get_text(strip=True)
        # A more robust way to clean the repo name: remove all whitespace and then replace the slash.
        repo_name = "".join(repo_name_raw.split()).replace("/", "/")
        repo_url = "https://github.com" + title_element.find('a')['href']
        # The repo name for the API call should be extracted directly from the URL
        # to ensure it's always correct.
        api_repo_name = "/".join(repo_url.split('/')[-2:])
        
        logger.info(f"🔍 Processing repository: {repo_name}")

        # Scrape basic info
        description_element = repo_element.find('p', class_='col-9')
        scraped_description = description_element.get_text(strip=True) if description_element else "No description provided."
        
        language_element = repo_element.find('span', itemprop='programmingLanguage')
        scraped_language = language_element.get_text(strip=True) if language_element else "N/A"
        
        # Fetch detailed info from GitHub API
        api_details = get_repo_details(api_repo_name)
        
        if api_details:
            logger.info(f"API details fetched for {repo_name}")
            # Combine scraped data with API data
            repo_data = {
                "name": repo_name,
                "url": repo_url,
                "description": api_details.get("description", scraped_description),
                "language": api_details.get("language", scraped_language),
                "stars": api_details.get("stars", 0),
                "forks": api_details.get("forks", 0),
                "tags": api_details.get("tags", []),
                "created_at": api_details.get("created_at"),
                "updated_at": api_details.get("updated_at"),
                "open_issues": api_details.get("open_issues", 0),
                "watchers": api_details.get("watchers", 0),
                "contributor_count": api_details.get("contributor_count", 0),
                "readme_content": api_details.get("readme_content", "")
            }
        else:
            # Fallback to scraped data if API fails
            logger.warning(f"API details fetch failed for {repo_name}, using scraped data as fallback.")
            star_element = repo_element.find('a', href=f"{repo_url.replace('https://github.com','').strip()}/stargazers")
            repo_stars = 0
            if star_element:
                try:
                    repo_stars = int(star_element.get_text(strip=True).replace(',', ''))
                except (ValueError, TypeError):
                    repo_stars = 0
            
            fork_element = repo_element.find('a', href=f"{repo_url.replace('https://github.com','').strip()}/forks")
            repo_forks = 0
            if fork_element:
                try:
                    repo_forks = int(fork_element.get_text(strip=True).replace(',', ''))
                except (ValueError, TypeError):
                    repo_forks = 0

            repo_data = {
                "name": repo_name,
                "url": repo_url,
                "description": scraped_description,
                "language": scraped_language,
                "stars": repo_stars,
                "forks": repo_forks,
                "tags": [],
                "created_at": "N/A",
                "updated_at": "N/A",
                "open_issues": "N/A",
                "watchers": "N/A",
                "contributor_count": "N/A"
            }
        
        repo_list.append(repo_data)
        time.sleep(1) # Respect API rate limits

    logger.info(f"✅ Successfully processed {len(repo_list)} repositories.")
    return repo_list


def scrape_trending_developers():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    limit = min(MAX_PROJECTS_TO_SCRAPE, 25)
    logger.info(f"⏳ Fetching top {limit} developers from GitHub Trending Developers...")
    try:
        response = requests.get(GITHUB_TRENDING_DEVELOPERS_URL, headers=headers, timeout=20)
        response.raise_for_status()
    except requests.RequestException as e:
        logger.error(f"❌ Error fetching GitHub trending developers page: {e}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    developer_list = []

    for article in soup.find_all('article', class_='Box-row')[:limit]:
        # Extract username from the profile link
        name_link = article.find('a', href=lambda h: h and h.startswith('/') and not h.startswith('/trending'))
        if not name_link:
            h2 = article.find(['h1', 'h2'])
            name_link = h2.find('a') if h2 else None
        if not name_link:
            continue

        href = name_link.get('href', '')
        username = href.strip('/').split('/')[0].split('?')[0]
        if not username:
            continue

        # Get display name from the heading
        heading = article.find(['h1', 'h2'])
        display_name = username
        if heading:
            full_text = heading.get_text(strip=True)
            parts = full_text.split()
            if parts:
                display_name = parts[0]

        # Try to get the trending repo from the card
        trending_repo_name = None
        trending_repo_url = None
        repo_link = article.find('a', href=lambda h: h and '/' in h and h.count('/') >= 2 and 'trending' not in h)
        if not repo_link:
            repo_links = article.find_all('a')
            for rl in repo_links:
                href = rl.get('href', '')
                parts = href.strip('/').split('/')
                if len(parts) >= 2 and parts[0] not in ('', 'trending', 'settings'):
                    repo_link = rl
                    break
        if repo_link:
            repo_href = repo_link.get('href', '')
            parts = repo_href.strip('/').split('/')
            if len(parts) >= 2:
                trending_repo_name = f"{parts[0]}/{parts[1]}"
                trending_repo_url = f"https://github.com/{trending_repo_name}"

        logger.info(f"🔍 Processing developer: {username}")

        # Enrich with GitHub API data
        entity_details = get_entity_details(username) if GH_TOKEN else None
        entity_repos = get_entity_repos(username) if GH_TOKEN else []

        if entity_details:
            languages = [r['language'] for r in entity_repos if r.get('language') and r['language'] != 'N/A']
            from collections import Counter
            main_languages = list(dict.fromkeys(
                lang for lang, _ in Counter(languages).most_common(3)
            )) if languages else []

            dev_data = {
                "username": username,
                "display_name": entity_details.get("name", display_name),
                "type": entity_details.get("type", "User"),
                "bio": entity_details.get("bio", ""),
                "followers": entity_details.get("followers", 0),
                "public_repos": entity_details.get("public_repos", 0),
                "created_at": entity_details.get("created_at", ""),
                "avatar_url": f"https://github.com/{username}.png",
                "profile_url": f"https://github.com/{username}",
                "trending_repo": trending_repo_name,
                "trending_repo_url": trending_repo_url,
                "top_repos": entity_repos,
                "main_languages": main_languages,
            }
        else:
            dev_data = {
                "username": username,
                "display_name": display_name,
                "type": "User",
                "bio": "",
                "followers": 0,
                "public_repos": 0,
                "created_at": "",
                "avatar_url": f"https://github.com/{username}.png",
                "profile_url": f"https://github.com/{username}",
                "trending_repo": trending_repo_name,
                "trending_repo_url": trending_repo_url,
                "top_repos": [],
                "main_languages": [],
            }

        developer_list.append(dev_data)
        time.sleep(0.5)

    logger.info(f"✅ Successfully processed {len(developer_list)} developers.")
    return developer_list
