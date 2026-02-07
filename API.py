import sys
import json
import requests
import csv
import random
import re

def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python songs.py artist_name")
    
    artist = sys.argv[1]
    try:
        response = requests.get(f"https://itunes.apple.com/search?entity=song&limit=10&term={artist}")
        data = response.json()
    except:
        sys.exit("API error")
    
    tracks = []
    for result in data.get("results", []):
        track_name = result.get("trackName", "Unknown")
        # Validate with regex: only letters, numbers, spaces
        if re.search(r"^[a-zA-Z0-9 ]+$", track_name):
            tracks.append({"artist": artist, "track": track_name})
        else:
            print(f"Skipping invalid track: {track_name}")
    
    if not tracks:
        print("No valid tracks found")
        return
    
    # Write to CSV
    with open("songs.csv", "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["artist", "track"])
        writer.writeheader()
        for track in tracks:
            writer.writerow(track)
    
    # Read back and stats
    read_tracks = []
    with open("songs.csv", "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            read_tracks.append(row["track"])
    
    print(f"Total tracks: {len(read_tracks)}")
    random_track = random.choice(read_tracks)
    print(f"Random pick: {random_track}")

if __name__ == "__main__":
    main()
