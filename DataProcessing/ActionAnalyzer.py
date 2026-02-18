"""
The goal of the file is to analyze the leverksuen games
and pull out how many actions there are
and how many of each type of action there are
and how many goals there are in each game
"""


import json
from pathlib import Path
from collections import Counter

#Config
games_path = Path(r"E:\Masters\EPVProject\working_games")
events_path = Path(r"E:\Masters\EPVProject\open-data-master\data\events")


def main():
    
    print("=" * 60)
    print("Analyzing Leverkusen 360 Data - Action Counts")
    print("=" * 60)
    
    #Get all match files in working_games folder    
    
    match_files = list(games_path.glob("*.json"))
    match_ids = [f.stem for f in match_files]  # Get filename without .json
    
    print(f"\nFound {len(match_ids)} matches in working_games folder")
    
    total_actions = 0
    action_counts = Counter()  # Counts each action type
    match_action_counts = []   # Actions per match
    goals = []                 # Track all goals
    
    print("\nLoading events...")
    print("-" * 60)
    
    for match_id in match_ids:
        
        # Load events file for this match
        events_file = events_path / f"{match_id}.json"
        
        if not events_file.exists():
            print(f"Match {match_id}: Events file not found!")
            continue
        
        with open(events_file, 'r', encoding='utf-8') as f:
            events = json.load(f)
        
        # Count actions in this match
        match_total = len(events)
        total_actions += match_total
        match_action_counts.append(match_total)
        
        # Count each action type
        for event in events:
            action_type = event.get('type', {}).get('name', 'Unknown')
            action_counts[action_type] += 1
            
            # Check if this is a goal (Shot with outcome = Goal)
            if action_type == 'Shot':
                outcome = event.get('shot', {}).get('outcome', {}).get('name', '')
                if outcome == 'Goal':
                    player = event.get('player', {}).get('name', 'Unknown')
                    team = event.get('team', {}).get('name', 'Unknown')
                    minute = event.get('minute', '?')
                    goals.append({
                        'match_id': match_id,
                        'minute': minute,
                        'player': player,
                        'team': team
                    })
        
        print(f"Match {match_id}: {match_total} actions")
    
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    
    print(f"\nTotal matches analyzed: {len(match_action_counts)}")
    print(f"Total actions: {total_actions:,}")
    print(f"Average actions per match: {total_actions / len(match_action_counts):.0f}")
    print(f"Min actions in a match: {min(match_action_counts):,}")
    print(f"Max actions in a match: {max(match_action_counts):,}")

    print("\n" + "=" * 60)
    print("GOALS")
    print("=" * 60)
    
    print(f"\nTotal goals: {len(goals)}")
    print(f"Total shots: {action_counts['Shot']}")
    print(f"Conversion rate: {len(goals) / action_counts['Shot'] * 100:.1f}%")
    
    # Count goals by team
    team_goals = Counter(g['team'] for g in goals)
    print("\nGoals by team:")
    for team, count in team_goals.most_common():
        print(f"  {team}: {count}")
    
    print("\n" + "=" * 60)
    print("ACTION TYPE BREAKDOWN")
    print("=" * 60)
    print(f"\n{'Action Type':<30} {'Count':>10} {'Percentage':>12}")
    print("-" * 54)
    
    # Sort by count (most common first)
    for action_type, count in action_counts.most_common():
        pct = (count / total_actions) * 100
        print(f"{action_type:<30} {count:>10,} {pct:>11.2f}%")
    
    print("-" * 54)
    print(f"{'TOTAL':<30} {total_actions:>10,} {'100.00%':>12}")


if __name__ == "__main__":
    main()