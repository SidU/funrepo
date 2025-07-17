#!/usr/bin/env python3
"""
Global Health Data Fetcher

This script fetches global health data by country using the World Bank API.
It provides health statistics in a user-friendly format.

Usage:
    python health_data_fetcher.py <country_code>
    python health_data_fetcher.py --list-countries

Examples:
    python health_data_fetcher.py US
    python health_data_fetcher.py --list-countries
"""

import requests
import sys
import json
from typing import Dict, List, Optional
import argparse


class HealthDataFetcher:
    """Fetches and formats global health data by country."""
    
    BASE_URL = "https://api.worldbank.org/v2"
    
    # Health indicators from World Bank API
    HEALTH_INDICATORS = {
        "SP.DYN.LE00.IN": "Life expectancy at birth (years)",
        "SH.DYN.MORT": "Mortality rate, under-5 (per 1,000 live births)",
        "SH.STA.MALN.ZS": "Prevalence of malnutrition (% of children under 5)",
        "SH.XPD.CHEX.GD.ZS": "Current health expenditure (% of GDP)",
        "SH.MED.PHYS.ZS": "Physicians (per 1,000 people)",
        "SH.STA.BRTC.ZS": "Births attended by skilled health staff (% of total)",
        "SP.DYN.IMRT.IN": "Mortality rate, infant (per 1,000 live births)"
    }
    
    def fetch_country_data(self, country_code: str) -> Optional[Dict]:
        """Fetch health data for a specific country."""
        try:
            # Get country information first
            country_url = f"{self.BASE_URL}/country/{country_code}?format=json"
            country_response = requests.get(country_url, timeout=10)
            
            if country_response.status_code != 200:
                print(f"Error: Could not fetch country information for '{country_code}'")
                return None
                
            country_data = country_response.json()
            if len(country_data) < 2 or not country_data[1]:
                print(f"Error: Country '{country_code}' not found")
                return None
                
            country_info = country_data[1][0]
            country_name = country_info.get('name', country_code)
            
            print(f"\n🌍 Health Data for {country_name} ({country_code.upper()})")
            print("=" * 60)
            
            # Fetch health indicators
            health_data = {}
            for indicator_code, indicator_name in self.HEALTH_INDICATORS.items():
                data = self._fetch_indicator_data(country_code, indicator_code)
                if data:
                    health_data[indicator_name] = data
                    
            return {
                'country_name': country_name,
                'country_code': country_code.upper(),
                'health_data': health_data
            }
            
        except requests.RequestException as e:
            print(f"Error: Network request failed: {e}")
            return None
        except Exception as e:
            print(f"Error: Unexpected error occurred: {e}")
            return None
    
    def _fetch_indicator_data(self, country_code: str, indicator_code: str) -> Optional[Dict]:
        """Fetch data for a specific health indicator."""
        try:
            url = f"{self.BASE_URL}/country/{country_code}/indicator/{indicator_code}?format=json&date=2015:2023&per_page=10"
            response = requests.get(url, timeout=10)
            
            if response.status_code != 200:
                return None
                
            data = response.json()
            if len(data) < 2 or not data[1]:
                return None
                
            # Get the most recent data point
            for item in data[1]:
                if item.get('value') is not None:
                    return {
                        'value': item['value'],
                        'year': item['date'],
                        'unit': self._get_unit_from_indicator(indicator_code)
                    }
            return None
            
        except Exception:
            return None
    
    def _get_unit_from_indicator(self, indicator_code: str) -> str:
        """Get the appropriate unit for display based on indicator."""
        if 'ZS' in indicator_code:  # Percentage indicators
            return '%'
        elif 'MORT' in indicator_code or 'IMRT' in indicator_code:
            return 'per 1,000'
        elif 'LE00' in indicator_code:
            return 'years'
        else:
            return ''
    
    def display_health_data(self, data: Dict) -> None:
        """Display health data in a user-friendly format."""
        if not data or not data.get('health_data'):
            print("❌ No health data available for this country.")
            return
            
        print(f"\n📊 Latest Available Health Statistics:")
        print("-" * 60)
        
        for indicator_name, indicator_data in data['health_data'].items():
            value = indicator_data['value']
            year = indicator_data['year']
            unit = indicator_data['unit']
            
            # Format the value nicely
            if isinstance(value, float):
                if value >= 100:
                    formatted_value = f"{value:,.0f}"
                elif value >= 10:
                    formatted_value = f"{value:.1f}"
                else:
                    formatted_value = f"{value:.2f}"
            else:
                formatted_value = str(value)
            
            print(f"• {indicator_name}")
            print(f"  └─ {formatted_value} {unit} ({year})")
            print()
    
    def list_countries(self) -> None:
        """List available countries with their codes."""
        try:
            url = f"{self.BASE_URL}/country?format=json&per_page=500"
            response = requests.get(url, timeout=15)
            
            if response.status_code != 200:
                print("Error: Could not fetch country list")
                return
                
            data = response.json()
            if len(data) < 2 or not data[1]:
                print("Error: No country data available")
                return
                
            print("\n🌍 Available Countries (use the 3-letter code):")
            print("=" * 60)
            
            countries = []
            for country in data[1]:
                if country.get('name') and country.get('id'):
                    countries.append((country['name'], country['id']))
            
            # Sort countries alphabetically
            countries.sort()
            
            for name, code in countries:
                print(f"{name:<40} [{code}]")
                
            print(f"\nTotal countries available: {len(countries)}")
            print("\nExample usage: python health_data_fetcher.py USA")
            
        except Exception as e:
            print(f"Error: Could not fetch country list: {e}")


def main():
    """Main function to handle command line arguments and run the fetcher."""
    parser = argparse.ArgumentParser(
        description="Fetch global health data by country using World Bank API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python health_data_fetcher.py USA        # Get health data for United States
  python health_data_fetcher.py GBR        # Get health data for United Kingdom
  python health_data_fetcher.py --list-countries  # List all available countries
        """
    )
    
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('country_code', nargs='?', 
                      help='3-letter country code (e.g., USA, GBR, DEU)')
    group.add_argument('--list-countries', action='store_true',
                      help='List all available countries with their codes')
    
    args = parser.parse_args()
    
    fetcher = HealthDataFetcher()
    
    if args.list_countries:
        fetcher.list_countries()
    else:
        data = fetcher.fetch_country_data(args.country_code)
        if data:
            fetcher.display_health_data(data)
        else:
            print("\n❌ Failed to fetch health data. Please check the country code and try again.")
            print("Use --list-countries to see available country codes.")


if __name__ == "__main__":
    main()