"""
Command line runner for the Music Recommender Simulation.

This demonstrates the recommender with multiple diverse user profiles
to show how the scoring algorithm behaves for different tastes.
"""

from src.recommender import load_songs, recommend_songs


def print_recommendations(profile_name: str, user_prefs: dict, songs: list, k: int = 5):
    """Pretty-print recommendations for a user profile."""
    print(f"\n{'='*70}")
    print(f"Profile: {profile_name}")
    print(f"Preferences: Genre={user_prefs['genre']}, Mood={user_prefs['mood']}, Energy={user_prefs['energy']:.1f}")
    print(f"{'='*70}\n")
    
    recommendations = recommend_songs(user_prefs, songs, k=k)
    
    if not recommendations:
        print("No recommendations found.")
        return
    
    for rank, (song, score, explanation) in enumerate(recommendations, 1):
        print(f"{rank}. {song['title']}")
        print(f"   Artist: {song['artist']}")
        print(f"   Score: {score:.2f}")
        print(f"   Reasons: {explanation}")
        print()


def main() -> None:
    # Load the song catalog
    songs = load_songs("data/songs.csv")
    print(f"✓ Loaded {len(songs)} songs from catalog\n")
    
    # Define diverse user profiles
    profiles = {
        "Happy Pop Enthusiast": {
            "genre": "pop",
            "mood": "happy",
            "energy": 0.8,
            "likes_acoustic": False,
        },
        "Chill Lofi Lover": {
            "genre": "lofi",
            "mood": "chill",
            "energy": 0.4,
            "likes_acoustic": True,
        },
        "Intense Rock Fan": {
            "genre": "rock",
            "mood": "intense",
            "energy": 0.9,
            "likes_acoustic": False,
        },
        "Focused Work Session": {
            "genre": "lofi",
            "mood": "focused",
            "energy": 0.4,
            "likes_acoustic": False,
        },
        "Ambient Meditation": {
            "genre": "ambient",
            "mood": "chill",
            "energy": 0.2,
            "likes_acoustic": True,
        },
    }
    
    # Generate recommendations for each profile
    for profile_name, user_prefs in profiles.items():
        print_recommendations(profile_name, user_prefs, songs, k=5)
    
    print(f"\n{'='*70}")
    print("Analysis Complete")
    print(f"{'='*70}")


if __name__ == "__main__":
    main()

