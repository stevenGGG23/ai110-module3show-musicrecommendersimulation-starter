import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Score and rank all songs, returning top k."""
        scored = [(song, score_song(user, song)[0]) for song in self.songs]
        ranked = sorted(scored, key=lambda x: x[1], reverse=True)
        return [song for song, score in ranked[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Generate explanation for why this song was recommended."""
        score, reasons = score_song(user, song)
        return f"Score: {score:.2f} - " + " | ".join(reasons)

def load_songs(csv_path: str) -> List[Dict]:
    """Load songs from CSV file and return list of song dictionaries."""
    songs = []
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Convert numeric fields to appropriate types
            song = {
                'id': int(row['id']),
                'title': row['title'],
                'artist': row['artist'],
                'genre': row['genre'],
                'mood': row['mood'],
                'energy': float(row['energy']),
                'tempo_bpm': float(row['tempo_bpm']),
                'valence': float(row['valence']),
                'danceability': float(row['danceability']),
                'acousticness': float(row['acousticness']),
            }
            songs.append(song)
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Score a single song based on user preferences.
    
    Returns:
        Tuple of (score: float, reasons: list of explanation strings)
    """
    score = 0.0
    reasons = []
    
    # 1. Genre match (strongest signal)
    if song['genre'].lower() == user_prefs['genre'].lower():
        score += 2.0
        reasons.append("genre match (+2.0)")
    
    # 2. Mood match (strong signal)
    if song['mood'].lower() == user_prefs['mood'].lower():
        score += 1.5
        reasons.append("mood match (+1.5)")
    
    # 3. Energy compatibility (numerical similarity)
    energy_diff = abs(song['energy'] - user_prefs['energy'])
    energy_score = 1.5 * (1.0 - energy_diff)
    if energy_score > 0:
        score += energy_score
        reasons.append(f"energy compatibility (+{energy_score:.2f})")
    
    # 4. Optional acoustic bonus
    if user_prefs.get('likes_acoustic', False) and song['acousticness'] > 0.75:
        score += 0.5
        reasons.append("acoustic bonus (+0.5)")
    
    if not reasons:
        reasons = ["generic match (no strong preferences matched)"]
    
    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Generate ranked music recommendations.
    
    Args:
        user_prefs: Dict with keys 'genre', 'mood', 'energy', optional 'likes_acoustic'
        songs: List of song dictionaries from load_songs()
        k: Number of top recommendations to return
    
    Returns:
        List of tuples (song: dict, score: float, explanation: str) sorted by score descending
    """
    # Score all songs
    scored_songs = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        explanation = " | ".join(reasons)
        scored_songs.append((song, score, explanation))
    
    # Sort by score (highest first)
    ranked = sorted(scored_songs, key=lambda x: x[1], reverse=True)
    
    # Return top k
    return ranked[:k]
