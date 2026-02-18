"""
Quick check to verify merged files are complete
"""

import json
from pathlib import Path

merged_path = Path(r"E:\Masters\EPVProject\working_games\merged")

# Pick the first merged file
files = list(merged_path.glob("*.json"))

if not files:
    print("No merged files found!")
else:
    # Load one file
    test_file = files[0]
    print(f"Checking: {test_file.name}")
    
    with open(test_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"Total events in file: {len(data)}")
    
    # Check first and last event
    first = data[0]
    last = data[-1]
    
    print(f"\nFirst event:")
    print(f"  Minute: {first.get('minute')}")
    print(f"  Type: {first.get('type', {}).get('name')}")
    print(f"  Has freeze_frame: {len(first.get('freeze_frame', []))} players")
    
    print(f"\nLast event:")
    print(f"  Minute: {last.get('minute')}")
    print(f"  Type: {last.get('type', {}).get('name')}")
    print(f"  Has freeze_frame: {len(last.get('freeze_frame', []))} players")
    
    # Count events with 360 data
    with_360 = sum(1 for e in data if e.get('freeze_frame'))
    print(f"\nEvents with 360 data: {with_360} / {len(data)}")