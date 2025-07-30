# Funrepo

**Funrepo** is a lightweight repository for experimenting with automation workflows, bot integrations, and small utility scripts.

The goal is to keep the repo simple and open-ended, allowing tools like GitHub Copilot to contribute meaningful and reusable code through natural interactions — including from chat platforms like Microsoft Teams.

## Current Scripts

### `issues_lookup.py`
A command-line tool for looking up active issues in GitHub repositories.

**Features:**
- Fetch open issues from any public GitHub repository
- Display issues with title, author, creation date, and labels
- Support for limiting results and showing closed issues
- Clean, readable output format
- Proper error handling for invalid repositories and network issues

**Usage:**
```bash
# Look up active issues in this repository
python3 issues_lookup.py SidU/funrepo

# Look up issues in any repository
python3 issues_lookup.py microsoft/vscode --limit 10

# Show all issues (including closed)
python3 issues_lookup.py octocat/Hello-World --all

# Get help
python3 issues_lookup.py --help
```

**Optional Setup:**
For private repositories or higher rate limits, set a GitHub token:
```bash
export GITHUB_TOKEN=your_token_here
python3 issues_lookup.py private-org/private-repo
```

## Ideas

We're gradually adding scripts for:
- Data analysis
- Developer productivity
- Global insights

## Getting Started

Clone the repo and explore:
```bash
git clone https://github.com/your-org/funrepo.git
cd funrepo
