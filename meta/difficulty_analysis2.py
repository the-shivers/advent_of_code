import pandas as pd
import numpy as np
import glob
from pathlib import Path

def load_leaderboard_data():
    """Load and combine all two-star leaderboard data."""
    all_data = []
    pattern = "leaderboards/aoc_*_leaderboard_two_star.csv"
    for filepath in glob.glob(pattern):
        df = pd.read_csv(filepath)
        all_data.append(df)
    return pd.concat(all_data, ignore_index=True)

def load_completion_stats():
    """Load and combine all completion statistics."""
    all_stats = []
    pattern = "dropoffs/aoc_stats_*.csv"
    for filepath in glob.glob(pattern):
        df = pd.read_csv(filepath)
        all_stats.append(df)
    return pd.concat(all_stats, ignore_index=True)

def calculate_historical_baseline(row, stats_df):
    """Calculate the baseline completion count for a given day based on historical data."""
    year, day = row['year'], row['day']
    
    if day == 1:
        return np.nan
    elif day == 2:
        # Use day 1 as baseline
        return stats_df[(stats_df['year'] == year) & (stats_df['day'] == 1)]['both_stars'].iloc[0]
    elif day == 3:
        # Use average of days 1 and 2
        prev_days = stats_df[(stats_df['year'] == year) & (stats_df['day'].isin([1, 2]))]['both_stars']
        return prev_days.mean()
    else:
        # Use average of 2 and 3 days prior
        prev_days = stats_df[
            (stats_df['year'] == year) & 
            (stats_df['day'].isin([day-3, day-2]))
        ]['both_stars']
        return prev_days.mean()

def calculate_difficulty_metrics(leaderboard_df, stats_df):
    """Calculate enhanced difficulty metrics for each problem."""
    
    # Calculate average completion time for top 100
    time_metrics = leaderboard_df.groupby(['year', 'day'])['seconds'].mean().reset_index()
    
    # Sort stats by year and day
    stats_df = stats_df.sort_values(['year', 'day'])
    
    # Calculate historical baseline for each day
    metrics = stats_df.apply(
        lambda row: pd.Series({
            'year': row['year'],
            'day': row['day'],
            'both_stars': row['both_stars'],
            'historical_baseline': calculate_historical_baseline(row, stats_df)
        }), 
        axis=1
    ).reset_index(drop=True)
    
    # Calculate completion ratio compared to historical baseline
    metrics['completion_ratio'] = metrics['both_stars'] / metrics['historical_baseline']
    
    # Merge with time metrics
    metrics = pd.merge(
        metrics,
        time_metrics,
        on=['year', 'day']
    )
    
    # Rename columns for clarity
    metrics = metrics.rename(columns={
        'seconds': 'avg_completion_time',
        'both_stars': 'total_completions'
    })
    
    return metrics

def find_hardest_problems(metrics):
    """Find the hardest problems based on both metrics using global normalization."""
    
    # Remove rows where we couldn't calculate completion ratio (day 1)
    metrics = metrics.dropna(subset=['completion_ratio'])
    
    # Calculate global z-scores (not per-year)
    metrics['time_zscore'] = (metrics['avg_completion_time'] - metrics['avg_completion_time'].mean()) / metrics['avg_completion_time'].std()
    metrics['completion_zscore'] = (metrics['completion_ratio'].mean() - metrics['completion_ratio']) / metrics['completion_ratio'].std()
    
    # Create composite difficulty score (higher is harder)
    metrics['difficulty_score'] = metrics['time_zscore'] + metrics['completion_zscore']
    
    return metrics.sort_values('difficulty_score', ascending=False).reset_index(drop=True)

# Main execution
def main():
    leaderboard_df = load_leaderboard_data()
    dropoff_df = load_completion_stats()
    difficulty_df = calculate_difficulty_metrics(leaderboard_df, dropoff_df)
    hardest_df = find_hardest_problems(difficulty_df)
    hardest_df.to_csv('hardest2.csv', index=False)
    
    # Print top 10 hardest problems
    print("\nTop 10 Hardest Problems:")
    print(hardest_df[['year', 'day', 'difficulty_score', 'avg_completion_time', 'completion_ratio']].head(10))
    
    # Print yearly difficulty averages
    yearly_avg = hardest_df.groupby('year')['difficulty_score'].mean().sort_values(ascending=False)
    print("\nYearly Average Difficulty:")
    print(yearly_avg)

if __name__ == "__main__":
    main()