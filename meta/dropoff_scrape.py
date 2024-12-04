import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import logging
from typing import Dict, List, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AoCStatsScraper:
    def __init__(self, base_url: str = "https://adventofcode.com"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (compatible; AoCAnalysis/1.0; +http://example.com)'
        })

    def fetch_year_stats(self, year: int) -> Optional[Dict]:
        """Fetch completion statistics for all days in a given year."""
        url = f"{self.base_url}/{year}/stats"
        
        try:
            logger.info(f"Fetching stats for year {year}")
            response = self.session.get(url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            stats_data = []
            
            stats_pre = soup.find('pre', class_='stats')
            if not stats_pre:
                logger.error(f"No stats found for year {year}")
                return None
            
            for day_entry in stats_pre.find_all('a'):
                day, both, one, stars = day_entry.text.strip().split()
                stats_data.append({
                    'year': year,
                    'day': int(day),
                    'both_stars': int(both),
                    'one_star_only': int(one)
                })
            return stats_data
            
        except requests.RequestException as e:
            logger.error(f"Error fetching stats for year {year}: {e}")
            return None
        except ValueError as e:
            logger.error(f"Error parsing stats for year {year}: {e}")
            return None
    
    def fetch_all_years(self, start_year: int = 2015, end_year: int = 2023, delay: float = 1.0) -> List[Dict]:
        """Fetch stats for all years in range."""
        all_stats = []
        
        for year in range(start_year, end_year + 1):
            year_stats = self.fetch_year_stats(year)
            if year_stats:
                all_stats.extend(year_stats)
            time.sleep(delay)  # Be nice to the server
            
        return all_stats
    
    def save_to_csv(self, stats: List[Dict], output_prefix: str = "aoc_stats"):
        """Save stats to CSV files, one per year."""
        df = pd.DataFrame(stats)
        
        # Group by year and save separate files
        for year, year_df in df.groupby('year'):
            filename = f"dropoffs/{output_prefix}_{year}.csv"
            year_df.to_csv(filename, index=False)
            logger.info(f"Saved stats for year {year} to {filename}")

if __name__ == "__main__":
    scraper = AoCStatsScraper()
    
    # Fetch all years
    all_stats = scraper.fetch_all_years()
    
    # Save to CSV files
    scraper.save_to_csv(all_stats)