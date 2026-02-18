"""
The idea behind this file is going to be for the initial
going over of the data and such stuff to understand what I have

"""


#Sort through the 36 frames to pull out the bayern leverkusen games
#move them to another folder


#From there I can pull out how many actions there are
#From there I can pull out the different types of actions and how many of each there are
#Then we can determine how many goals there are in each game
import json
import shutil
from pathlib import Path

# =============================================================================
# CONFIGURATION - Update these paths
# =============================================================================
file_path = Path(r"E:\Masters\EPVProject\open-data-master\data")
threesixty_path = file_path / "three-sixty"
matches_path = file_path / "matches"
competitions_path = file_path / "competitions.json"

# Output folder for Leverkusen games
output_path = Path(r"E:\Masters\EPVProject\working_games")


def main():
    
    print("=" * 60)
    print("Finding Bayer Leverkusen Matches")
    print("=" * 60)
    
    # -------------------------------------------------------------------------
    # Step 1: Find Bundesliga 2023/24 competition
    # -------------------------------------------------------------------------
    
    with open(COMPETITIONS_PATH, 'r', encoding='utf-8') as f:
        competitions = json.load(f)
    
    # Look for Bundesliga 2023/24
    comp_id = None
    season_id = None
    
    for comp in competitions:
        if 'Bundesliga' in comp.get('competition_name', ''):
            if '2023' in comp.get('season_name', ''):
                comp_id = comp['competition_id']
                season_id = comp['season_id']
                print(f"Found: {comp['competition_name']} {comp['season_name']}")
                print(f"  comp_id={comp_id}, season_id={season_id}")
                break
    
    if comp_id is None:
        print("Could not find Bundesliga 2023/24!")
        return
    
    # -------------------------------------------------------------------------
    # Step 2: Load matches and find Leverkusen games
    # -------------------------------------------------------------------------
    
    matches_file = MATCHES_PATH / str(comp_id) / f"{season_id}.json"
    
    with open(matches_file, 'r', encoding='utf-8') as f:
        matches = json.load(f)
    
    print(f"\nTotal matches in Bundesliga: {len(matches)}")
    
    # Find Leverkusen matches
    leverkusen_match_ids = []
    
    print("\nBayer Leverkusen matches:")
    print("-" * 60)
    
    for match in matches:
        home = match['home_team']['home_team_name']
        away = match['away_team']['away_team_name']
        
        # Check if Leverkusen is playing
        if 'Leverkusen' in home or 'Leverkusen' in away:
            match_id = match['match_id']
            date = match.get('match_date', '?')
            home_score = match.get('home_score', '?')
            away_score = match.get('away_score', '?')
            
            leverkusen_match_ids.append(match_id)
            print(f"{date}: {home} {home_score}-{away_score} {away} (ID: {match_id})")
    
    print(f"\nTotal Leverkusen matches: {len(leverkusen_match_ids)}")
    
    # -------------------------------------------------------------------------
    # Step 3: Check which have 360 data and copy to working folder
    # -------------------------------------------------------------------------
    
    print("\n" + "=" * 60)
    print(f"Copying 360 files to: {OUTPUT_PATH}")
    print("=" * 60)
    
    # Create output folder
    OUTPUT_PATH.mkdir(parents=True, exist_ok=True)
    
    copied = 0
    missing = []
    
    for match_id in leverkusen_match_ids:
        source = THREE_SIXTY_PATH / f"{match_id}.json"
        dest = OUTPUT_PATH / f"{match_id}.json"
        
        if source.exists():
            shutil.copy2(source, dest)
            print(f"Copied: {match_id}.json")
            copied += 1
        else:
            print(f"MISSING: {match_id}.json")
            missing.append(match_id)
    
    # -------------------------------------------------------------------------
    # Summary
    # -------------------------------------------------------------------------
    
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Leverkusen matches found: {len(leverkusen_match_ids)}")
    print(f"360 files copied: {copied}")
    print(f"360 files missing: {len(missing)}")
    
    if missing:
        print(f"\nMissing match IDs: {missing}")
    
    print(f"\nFiles saved to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()