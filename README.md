# Funrepo

**Funrepo** is a lightweight repository for experimenting with automation workflows, bot integrations, and small utility scripts.

The goal is to keep the repo simple and open-ended, allowing tools like GitHub Copilot to contribute meaningful and reusable code through natural interactions — including from chat platforms like Microsoft Teams.

## Current Scripts

- **`health_data_fetcher.py`** - Fetches global health data by country using the World Bank API

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
```

### Health Data Fetcher

Fetch global health statistics by country:

```bash
# Install dependencies
pip install -r requirements.txt

# Get health data for a specific country (use 3-letter country codes)
python health_data_fetcher.py USA
python health_data_fetcher.py GBR
python health_data_fetcher.py DEU

# List all available countries
python health_data_fetcher.py --list-countries

# Get help
python health_data_fetcher.py --help
```

The health data fetcher provides statistics including:
- Life expectancy at birth
- Mortality rates (under-5 and infant)
- Health expenditure as % of GDP
- Physicians per 1,000 people
- Malnutrition prevalence
- Birth attendance by skilled health staff
