import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time
import pandas as pd
from typing import List, Dict, Tuple
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AoCLeaderboardScraper:
    def __init__(self, base_url: str = "https://adventofcode.com"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (compatible; AoCAnalysis/1.0; +http://example.com)'
        })
        
    def _parse_time(self, time_str: str) -> int:
        """Convert time string (HH:MM:SS) to seconds since day start."""
        time_parts = time_str.split()[-1].split(':')
        return int(time_parts[0]) * 3600 + int(time_parts[1]) * 60 + int(time_parts[2])
    
    def _extract_leaderboard_entries(self, html: str) -> Tuple[List[Dict], List[Dict]]:
        """Extract both one-star and two-star leaderboard entries from page HTML."""
        soup = BeautifulSoup(html, 'html.parser')
        
        two_star_entries = []
        one_star_entries = []
        
        main = soup.find('main')
        if not main:
            return [], []

        elements = main.find_all(['p', 'div'])
        
        current_section = None
        for elem in elements:
            if elem.name == 'p':
                # Check if this paragraph contains the section header
                span = elem.find('span', class_='leaderboard-daydesc-both')
                current_section = 'two_star' if span else 'one_star'
                continue
                
            if elem.get('class') == ['leaderboard-entry']:
                entry_text = elem.text.strip()
                position_str, remainder = entry_text.split(')', 1)
                position = int(position_str)
                clean_remainder = remainder.replace('  ', ' ')
                parts = clean_remainder.strip().split(' ') 
                month_str, date_str, time_str, *username_parts = parts
                username = ' '.join(username_parts)
                entry_data = {
                    'position': position,
                    'seconds': self._parse_time(time_str),
                    'username': username
                }
                if current_section == 'two_star':
                    two_star_entries.append(entry_data)
                elif current_section == 'one_star':
                    one_star_entries.append(entry_data)
        
        return one_star_entries, two_star_entries
    
    def fetch_day_data(self, year: int, day: int) -> Dict:
        """Fetch and parse leaderboard data for a specific day."""
        url = f"{self.base_url}/{year}/leaderboard/day/{day}"
        
        try:
            logger.info(f"Fetching data for {year} day {day}")
            response = self.session.get(url)
            response.raise_for_status()
            
            one_star, two_star = self._extract_leaderboard_entries(response.text)
            
            return {
                'year': year,
                'day': day,
                'one_star': one_star,
                'two_star': two_star
            }
            
        except requests.RequestException as e:
            logger.error(f"Error fetching data for {year} day {day}: {e}")
            return None
    
    def fetch_year_data(self, year: int, delay: float = 2.0) -> List[Dict]:
        """Fetch data for all days in a given year."""
        results = []
        for day in range(1, 26):
            day_data = self.fetch_day_data(year, day)
            if day_data:
                results.append(day_data)
            time.sleep(delay)  # Be nice to the server
        return results
    
    def save_to_csv(self, data: List[Dict], output_file: str):
        """Save the collected data to CSV files."""
        one_star_rows = []
        two_star_rows = []
        
        for day_data in data:
            year = day_data['year']
            day = day_data['day']
            
            for entry in day_data['one_star']:
                one_star_rows.append({
                    'year': year,
                    'day': day,
                    'position': entry['position'],
                    'seconds': entry['seconds'],
                    'username': entry['username']
                })
                
            for entry in day_data['two_star']:
                two_star_rows.append({
                    'year': year,
                    'day': day,
                    'position': entry['position'],
                    'seconds': entry['seconds'],
                    'username': entry['username']
                })

        pd.DataFrame(one_star_rows).to_csv(f'leaderboards/{output_file}_one_star.csv', index=False)
        pd.DataFrame(two_star_rows).to_csv(f'leaderboards/{output_file}_two_star.csv', index=False)

# Example usage
if __name__ == "__main__":
    for year in [
        # 2015,
        # 2016,
        # 2017,
        # 2018,
        # 2019,
        # 2020,
        # 2021,
        # 2022,
        # 2023,
        2024
    ]:
        scraper = AoCLeaderboardScraper()
        year_data = scraper.fetch_year_data(year)
        scraper.save_to_csv(year_data, f"aoc_{year}_leaderboard")