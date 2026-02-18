"""
The idea for this file to combine
freeze frames and events into one file for each match
so that we can easily analyze them together

This is done using the event_uuid tag 
"""
"""
Merge 360 Freeze Frame Data with Events Data
=============================================

Takes the 360 and events files and merges them into single files.
Each event gets its freeze_frame and visible_area attached.

Input:
  - working_games/three-sixty/
  - working_games/events/

Output:
  - working_games/merged/

"""

import json
from pathlib import Path

# =============================================================================
# CONFIGURATION
# =============================================================================
working_path = Path(r"E:\Masters\EPVProject\working_games")
threesixty_path = working_path / "three-sixty"
events_path = working_path / "events"
merged_path = working_path / "merged"


def merge_match(match_id: str) -> dict:
    """
    Merge 360 and events data for a single match.
    
    Returns dict with stats about the merge.
    """
    
    # Load events
    events_file = events_path / f"{match_id}.json"
    with open(events_file, 'r', encoding='utf-8') as f:
        events = json.load(f)
    
    # Load 360 data
    threesixty_file = threesixty_path / f"{match_id}.json"
    with open(threesixty_file, 'r', encoding='utf-8') as f:
        frames = json.load(f)
    
    # Create lookup dict: event_uuid -> 360 data
    frames_lookup = {}
    for frame in frames:
        event_uuid = frame.get('event_uuid')
        if event_uuid:
            frames_lookup[event_uuid] = {
                'freeze_frame': frame.get('freeze_frame', []),
                'visible_area': frame.get('visible_area', [])
            }
    
    # Merge: add 360 data to each event
    merged_events = []
    events_with_360 = 0
    
    for event in events:
        event_id = event.get('id')
        
        # Check if this event has 360 data
        if event_id in frames_lookup:
            event['freeze_frame'] = frames_lookup[event_id]['freeze_frame']
            event['visible_area'] = frames_lookup[event_id]['visible_area']
            events_with_360 += 1
        else:
            # No 360 data for this event
            event['freeze_frame'] = []
            event['visible_area'] = []
        
        merged_events.append(event)
    
    # Save merged file
    merged_file = merged_path / f"{match_id}.json"
    with open(merged_file, 'w', encoding='utf-8') as f:
        json.dump(merged_events, f, indent=2, ensure_ascii=False)
    
    return {
        'match_id': match_id,
        'total_events': len(events),
        'events_with_360': events_with_360,
        'frames_in_360_file': len(frames)
    }


def main():
    
    print("=" * 60)
    print("Merging 360 and Events Data")
    print("=" * 60)
    
    # Create output folder
    merged_path.mkdir(parents=True, exist_ok=True)
    
    # Get all match IDs from the three-sixty folder
    match_files = list(threesixty_path.glob("*.json"))
    match_ids = [f.stem for f in match_files]
    
    print(f"\nFound {len(match_ids)} matches to merge")
    print("-" * 60)
    
    # Merge each match
    total_events = 0
    total_with_360 = 0
    
    for match_id in match_ids:
        
        # Check that events file exists
        if not (events_path / f"{match_id}.json").exists():
            print(f"Match {match_id}: SKIPPED - no events file")
            continue
        
        # Merge
        stats = merge_match(match_id)
        
        total_events += stats['total_events']
        total_with_360 += stats['events_with_360']
        
        pct = (stats['events_with_360'] / stats['total_events']) * 100
        print(f"Match {match_id}: {stats['total_events']} events, {stats['events_with_360']} with 360 ({pct:.1f}%)")
    
    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"\nMatches merged: {len(match_ids)}")
    print(f"Total events: {total_events:,}")
    print(f"Events with 360 data: {total_with_360:,}")
    print(f"Coverage: {(total_with_360 / total_events) * 100:.1f}%")
    print(f"\nMerged files saved to: {merged_path}")


if __name__ == "__main__":
    main()