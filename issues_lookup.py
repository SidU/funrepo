#!/usr/bin/env python3
"""
GitHub Issues Lookup Tool

A simple utility to fetch and display active (open) issues from GitHub repositories.
Supports both public repositories and can be extended for authenticated access.
"""

import argparse
import json
import sys
from datetime import datetime
from urllib.parse import urljoin
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError


class GitHubIssuesLookup:
    """GitHub Issues API client for fetching repository issues."""
    
    BASE_URL = "https://api.github.com"
    
    def __init__(self, token=None):
        """Initialize the GitHub client.
        
        Args:
            token (str, optional): GitHub personal access token for authenticated requests
        """
        self.token = token
        self.headers = {
            'Accept': 'application/vnd.github.v3+json',
            'User-Agent': 'GitHub-Issues-Lookup/1.0'
        }
        if token:
            self.headers['Authorization'] = f'token {token}'
    
    def get_issues(self, owner, repo, state='open', per_page=30):
        """Fetch issues from a GitHub repository.
        
        Args:
            owner (str): Repository owner (username or organization)
            repo (str): Repository name
            state (str): Issue state ('open', 'closed', 'all')
            per_page (int): Number of issues per page (max 100)
            
        Returns:
            list: List of issue dictionaries
            
        Raises:
            Exception: If API request fails
        """
        url = f"{self.BASE_URL}/repos/{owner}/{repo}/issues"
        params = f"?state={state}&per_page={per_page}&sort=created&direction=desc"
        full_url = url + params
        
        try:
            request = Request(full_url, headers=self.headers)
            with urlopen(request) as response:
                if response.status == 200:
                    data = json.loads(response.read().decode('utf-8'))
                    # Filter out pull requests (they appear in issues API)
                    return [issue for issue in data if 'pull_request' not in issue]
                else:
                    raise Exception(f"API request failed with status {response.status}")
        except HTTPError as e:
            if e.code == 404:
                raise Exception(f"Repository '{owner}/{repo}' not found or not accessible")
            elif e.code == 403:
                raise Exception("API rate limit exceeded or access denied")
            else:
                raise Exception(f"HTTP error {e.code}: {e.reason}")
        except URLError as e:
            raise Exception(f"Network error: {e.reason}")
    
    def format_issue(self, issue):
        """Format a single issue for display.
        
        Args:
            issue (dict): Issue data from GitHub API
            
        Returns:
            str: Formatted issue string
        """
        number = issue['number']
        title = issue['title']
        author = issue['user']['login']
        created_at = datetime.fromisoformat(issue['created_at'].replace('Z', '+00:00'))
        formatted_date = created_at.strftime('%Y-%m-%d %H:%M UTC')
        state = issue['state'].upper()
        
        # Issue labels
        labels = [label['name'] for label in issue.get('labels', [])]
        labels_str = f" [{', '.join(labels)}]" if labels else ""
        
        # Comments count
        comments = issue['comments']
        comments_str = f" • {comments} comment{'s' if comments != 1 else ''}" if comments > 0 else ""
        
        return (f"#{number}: {title}\n"
                f"   └─ by @{author} • {formatted_date} • {state}{labels_str}{comments_str}")
    
    def display_issues(self, issues, owner, repo):
        """Display issues in a formatted list.
        
        Args:
            issues (list): List of issue dictionaries
            owner (str): Repository owner
            repo (str): Repository name
        """
        if not issues:
            print(f"📭 No open issues found in {owner}/{repo}")
            return
        
        print(f"🔍 Active Issues in {owner}/{repo}")
        print("=" * 60)
        print(f"Found {len(issues)} open issue{'s' if len(issues) != 1 else ''}:\n")
        
        for issue in issues:
            print(self.format_issue(issue))
            print()  # Empty line between issues


def parse_repository(repo_string):
    """Parse repository string in format 'owner/repo'.
    
    Args:
        repo_string (str): Repository in format 'owner/repo'
        
    Returns:
        tuple: (owner, repo) strings
        
    Raises:
        ValueError: If format is invalid
    """
    if '/' not in repo_string:
        raise ValueError("Repository must be in format 'owner/repo' (e.g., 'octocat/Hello-World')")
    
    parts = repo_string.split('/')
    if len(parts) != 2 or not parts[0] or not parts[1]:
        raise ValueError("Repository must be in format 'owner/repo' (e.g., 'octocat/Hello-World')")
    
    return parts[0], parts[1]


def main():
    """Main function to handle command line arguments and execute the lookup."""
    parser = argparse.ArgumentParser(
        description="Look up active issues in GitHub repositories",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s SidU/funrepo                    # Look up issues in SidU/funrepo
  %(prog)s microsoft/vscode --limit 10    # Show first 10 issues
  %(prog)s octocat/Hello-World --all      # Show all issues (open and closed)
  
For private repositories or higher rate limits, set GITHUB_TOKEN environment variable.
        """
    )
    
    parser.add_argument('repository', 
                       help='GitHub repository in format "owner/repo" (e.g., "octocat/Hello-World")')
    
    parser.add_argument('--limit', '-l', 
                       type=int, 
                       default=30, 
                       help='Maximum number of issues to display (default: 30, max: 100)')
    
    parser.add_argument('--all', '-a', 
                       action='store_true', 
                       help='Show all issues (including closed ones)')
    
    parser.add_argument('--token', '-t', 
                       help='GitHub personal access token (can also use GITHUB_TOKEN env var)')
    
    args = parser.parse_args()
    
    # Validate limit
    if args.limit < 1 or args.limit > 100:
        print("Error: Limit must be between 1 and 100", file=sys.stderr)
        sys.exit(1)
    
    # Parse repository
    try:
        owner, repo = parse_repository(args.repository)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    
    # Get token from argument or environment
    import os
    token = args.token or os.environ.get('GITHUB_TOKEN')
    
    # Initialize client and fetch issues
    client = GitHubIssuesLookup(token=token)
    
    try:
        state = 'all' if args.all else 'open'
        issues = client.get_issues(owner, repo, state=state, per_page=args.limit)
        client.display_issues(issues, owner, repo)
        
        if not args.all and len(issues) == args.limit:
            print(f"💡 Showing first {args.limit} issues. Use --limit to see more or --all for closed issues too.")
            
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()