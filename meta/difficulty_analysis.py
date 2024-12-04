import pandas as pd
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

def calculate_difficulty_metrics(leaderboard_df, stats_df):
    """Calculate both difficulty metrics for each problem."""
    
    # Calculate average completion time for top 100
    time_metrics = leaderboard_df.groupby(['year', 'day'])['seconds'].mean().reset_index()
    
    # Sort stats by year and day to calculate previous day completions
    stats_df = stats_df.sort_values(['year', 'day'])
    
    # Calculate completion ratio compared to previous day
    stats_df['prev_completions'] = stats_df.groupby('year')['both_stars'].shift(1)
    stats_df['completion_ratio'] = stats_df['both_stars'] / stats_df['prev_completions']
    
    # Merge the metrics
    metrics = pd.merge(time_metrics, 
                      stats_df[['year', 'day', 'both_stars', 'completion_ratio']], 
                      on=['year', 'day'])
    
    # Rename columns for clarity
    metrics = metrics.rename(columns={
        'seconds': 'avg_completion_time',
        'both_stars': 'total_completions'
    })
    
    return metrics.sort_values(['avg_completion_time', 'completion_ratio'], ascending=[True, False])

# Add function to find most difficult problems
def find_hardest_problems(metrics):
    """Find the hardest problems based on both metrics."""
    
    # Normalize metrics within each year
    metrics['time_zscore'] = metrics.groupby('year')['avg_completion_time'].transform(lambda x: (x - x.mean()) / x.std())
    metrics['completion_zscore'] = metrics.groupby('year')['completion_ratio'].transform(lambda x: (x.mean() - x) / x.std())
    
    # Create composite difficulty score (higher is harder)
    metrics['difficulty_score'] = metrics['time_zscore'] + metrics['completion_zscore']
    metrics.sort_values(['difficulty_score'], ascending=False).reset_index()
    return metrics

# Actual
leaderboard_df = load_leaderboard_data()
dropoff_df = load_completion_stats()
difficulty_df = calculate_difficulty_metrics(leaderboard_df, dropoff_df)
hardest_df = find_hardest_problems(difficulty_df)
hardest_df.to_csv('hardest.csv', index=False)