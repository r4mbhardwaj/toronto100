import os
import requests
import pandas as pd
import time
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')

if not GITHUB_TOKEN:
    raise ValueError(
        "GitHub token not found. Please set GITHUB_TOKEN in your .env file.")

# GitHub API endpoints
SEARCH_URL = 'https://api.github.com/search/users'
USER_URL = 'https://api.github.com/users/{}'
REPOS_URL = 'https://api.github.com/users/{}/repos'

# Headers for authentication
headers = {
    'Authorization': f'token {GITHUB_TOKEN}',
    'Accept': 'application/vnd.github.v3+json'
}

# Function to clean company names


def clean_company(company):
    if not company:
        return ''
    company = company.strip()
    if company.startswith('@'):
        company = company[1:]
    return company.upper()


# =============================
# Part 1: Fetching Users
# =============================
users_csv_path = 'users.csv'

if os.path.exists(users_csv_path):
    print(f"Loading existing {users_csv_path}...")
    users_df = pd.read_csv(users_csv_path)
    print(f"Loaded {len(users_df)} users from {users_csv_path}.")
else:
    # Parameters for searching users
    query = 'location:Toronto followers:>100'
    per_page = 100  # Maximum allowed per_page value
    users = []
    page = 1

    print("Fetching users from GitHub API...")

    while True:
        params = {
            'q': query,
            'per_page': per_page,
            'page': page
        }
        response = requests.get(SEARCH_URL, headers=headers, params=params)

        if response.status_code != 200:
            print(f'Error fetching users: {response.status_code}')
            print(response.json())
            break

        data = response.json()
        batch = data.get('items', [])
        if not batch:
            break

        users.extend(batch)
        print(f'Fetched page {page}, total users fetched: {len(users)}')

        if 'next' not in response.links:
            break
        page += 1
        time.sleep(1)  # To respect rate limits

    print(f'Total users fetched: {len(users)}')

    # Fetch detailed user information
    detailed_users = []
    print("Fetching detailed user information...")

    for idx, user in enumerate(users, start=1):
        user_login = user.get('login')
        if not user_login:
            continue  # Skip if login is missing

        user_response = requests.get(
            USER_URL.format(user_login), headers=headers)

        if user_response.status_code == 200:
            detailed_users.append(user_response.json())
        else:
            print(
                f"Error fetching user {user_login}: {user_response.status_code}")

        if idx % 50 == 0:
            print(f'Fetched details for {idx} users...')

        time.sleep(0.5)  # To respect rate limits

    print(f'Total detailed users fetched: {len(detailed_users)}')

    # Create users.csv
    print("Creating users.csv...")
    users_data = []
    for user in detailed_users:
        users_data.append({
            'login': user.get('login', ''),
            'name': user.get('name') or '',
            'company': clean_company(user.get('company')),
            'location': user.get('location') or '',
            'email': user.get('email') or '',
            'hireable': user.get('hireable') if user.get('hireable') is not None else '',
            'bio': user.get('bio') or '',
            'public_repos': user.get('public_repos', 0),
            'followers': user.get('followers', 0),
            'following': user.get('following', 0),
            'created_at': user.get('created_at') or ''
        })

    users_df = pd.DataFrame(users_data)
    users_df.to_csv(users_csv_path, index=False)
    print(f'{users_csv_path} created successfully.')

# =============================
# Part 2: Fetching Repositories
# =============================
repositories_csv_path = 'repositories.csv'

if os.path.exists(repositories_csv_path):
    print(f"Loading existing {repositories_csv_path}...")
    repos_df = pd.read_csv(repositories_csv_path)
    print(f"Loaded {len(repos_df)} repositories from {repositories_csv_path}.")
else:
    print("Fetching repositories for each user...")

    repositories = []
    total_users = len(users_df)
    print(f'Total users to fetch: {total_users}')
    for idx, user in users_df.iterrows():
        login = user['login']
        if not login:
            continue  # Skip if login is missing

        repo_page = 1  # Only fetch the first page (up to 1000 repos)
        params = {
            'per_page': 1000,
            'page': repo_page,
            'sort': 'pushed',
            'direction': 'desc'
        }
        repo_response = requests.get(REPOS_URL.format(
            login), headers=headers, params=params)

        if repo_response.status_code != 200:
            print(
                f"Error fetching repos for {login}: {repo_response.status_code}")
            continue

        repos = repo_response.json()
        if not repos:
            continue  # No repositories for this user

        for repo in repos:
            # Handle cases where 'repo' might be None
            if not repo:
                continue

            # Safely extract license name
            license_info = repo.get('license')
            license_name = license_info.get('name') if license_info else ''

            repositories.append({
                'login': login,
                'full_name': repo.get('full_name', ''),
                'created_at': repo.get('created_at', ''),
                'stargazers_count': repo.get('stargazers_count', 0),
                'watchers_count': repo.get('watchers_count', 0),
                'language': repo.get('language') or '',
                'has_projects': repo.get('has_projects') if repo.get('has_projects') is not None else '',
                'has_wiki': repo.get('has_wiki') if repo.get('has_wiki') is not None else '',
                'license_name': license_name or ''
            })

        if (idx + 1) % 50 == 0 or (idx + 1) == total_users:
            print(
                f'Fetched repositories for {idx + 1} out of {total_users} users.')

        print(f'Fetched repositories for {login}...')

        time.sleep(0.5)  # To respect rate limits

    print(f'Total repositories fetched: {len(repositories)}')

    # Create repositories.csv
    print("Creating repositories.csv...")
    repos_df = pd.DataFrame(repositories)
    repos_df.to_csv(repositories_csv_path, index=False)
    print(f'{repositories_csv_path} created successfully.')
