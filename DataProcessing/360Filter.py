"""
Filter out events that dont have 360 data

"""

import json
from pathlib import Path

#Config 
labeled_path = Path(r"E:\Masters\EPVProject\working_games\labeled")
output_path = Path(r"E:\Masters\EPVProject\working_games\labeled_360")


def main():
    
    print("=" * 60)
    print("Filtering to Events with 360 Data")
    print("=" * 60)
    
    # Create output folder
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Get all labeled files
    match_files = list(labeled_path.glob("*.json"))
    
    total_events = 0
    total_with_360 = 0
    
    print(f"\nProcessing {len(match_files)} matches...")
    print("-" * 60)
    
    for match_file in match_files:
        match_id = match_file.stem
        
        # Load labeled data
        with open(match_file, 'r', encoding='utf-8') as f:
            events = json.load(f)
        
        # Filter to only events with freeze frame data
        events_with_360 = [e for e in events if e.get('freeze_frame') and len(e['freeze_frame']) > 0]
        
        total_events += len(events)
        total_with_360 += len(events_with_360)
        
        # Save filtered data
        output_file = output_path / f"{match_id}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(events_with_360, f, indent=2, ensure_ascii=False)
        
        pct = (len(events_with_360) / len(events)) * 100 if events else 0
        print(f"Match {match_id}: {len(events_with_360)}/{len(events)} events ({pct:.1f}%)")
    
    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"\nTotal events: {total_events:,}")
    print(f"Events with 360 data: {total_with_360:,}")
    print(f"Coverage: {(total_with_360 / total_events) * 100:.1f}%")
    print(f"\nFiltered data saved to: {output_path}")


if __name__ == "__main__":
    main()