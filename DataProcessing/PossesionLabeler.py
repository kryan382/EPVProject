"""
This file is labeling posseions
1 = the possesion ended in a goal
0 - the possesion did not end in a goal
simple
"""

import json
from pathlib import Path

#Config
merged_path = Path(r"E:\Masters\EPVProject\working_games\merged")
output_path = Path(r"E:\Masters\EPVProject\working_games\labeled")


def is_goal(event):
    """Check if this event is a goal."""
    if event.get('type', {}).get('name') != 'Shot':
        return False
    
    outcome = event.get('shot', {}).get('outcome', {}).get('name', '')
    return outcome == 'Goal'


def label_match(match_id):
    """Label all events in a match with possession outcome."""
    
    # Load merged data
    with open(merged_path / f"{match_id}.json", 'r', encoding='utf-8') as f:
        events = json.load(f)
    
    # Find which possessions ended in a goal
    goal_possessions = set()
    
    for event in events:
        if is_goal(event):
            goal_possessions.add(event.get('possession'))
    
    # Label each event
    for event in events:
        poss = event.get('possession')
        event['label'] = 1 if poss in goal_possessions else 0
    
    # Save labeled data
    with open(output_path / f"{match_id}.json", 'w', encoding='utf-8') as f:
        json.dump(events, f, indent=2, ensure_ascii=False)
    
    return len(events), len(goal_possessions)


def main():
    
    print("=" * 60)
    print("Labeling Events with Possession Outcome")
    print("=" * 60)
    
    # Create output folder
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Get all match files
    match_files = list(merged_path.glob("*.json"))
    
    total_events = 0
    total_goals = 0
    
    for match_file in match_files:
        match_id = match_file.stem
        n_events, n_goals = label_match(match_id)
        total_events += n_events
        total_goals += n_goals
        print(f"Match {match_id}: {n_events} events, {n_goals} goals")
    
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Matches labeled: {len(match_files)}")
    print(f"Total events: {total_events:,}")
    print(f"Total goal possessions: {total_goals}")
    print(f"Saved to: {output_path}")


if __name__ == "__main__":
    main()