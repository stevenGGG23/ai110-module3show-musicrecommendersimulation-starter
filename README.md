# 🎵 Music Recommender Simulation

## Project Summary

This project builds and explains a small content-based music recommender system. It represents songs and user "taste profiles" as data, uses a weighted scoring algorithm to rank songs by relevance, evaluates bias and limitations, and reflects on how this mirrors real-world AI recommenders like Spotify.

---

## How The System Works

### Design Approach

Real platforms like Spotify use two main strategies:
1. **Collaborative Filtering**: "What did users like you enjoy?"
2. **Content-Based Filtering**: "Does this song match YOUR taste?"

This simulation uses **Content-Based Filtering** because it's intuitive and doesn't require millions of users. We analyze song attributes directly and match them to a user's preferences.

### Features Our System Uses

Each **Song** has:
- **Basic Info**: id, title, artist
- **Audio Attributes**: genre, mood, energy (0.0–1.0), tempo_bpm, valence, danceability, acousticness
  - *Energy*: measures intensity (0.0 = calm lofi, 1.0 = intense rock)
  - *Valence*: measures happiness/positivity (0.0 = sad, 1.0 = happy)
  - *Danceability*: how rhythm-forward a track is

Each **UserProfile** stores:
- **favorite_genre**: The user's preferred music style (e.g., "pop", "lofi", "rock")
- **favorite_mood**: The emotional vibe they want (e.g., "happy", "chill", "intense")
- **target_energy**: A 0.0–1.0 value for the intensity they want right now
- **likes_acoustic**: Boolean for whether acoustic instruments matter to them

### Scoring Algorithm (The "Recipe")

```
Base Score = 0

IF song.genre == user.favorite_genre
    score += 2.0  (strong signal: right category)

IF song.mood == user.favorite_mood
    score += 1.5  (good signal: right feeling)

Energy Compatibility = 1.5 * (1.0 - abs(song.energy - user.target_energy))
    (rewards songs close to user's target energy)

IF user.likes_acoustic AND song.acousticness > 0.75
    score += 0.5  (acoustic bonus)

Ranking: Sort all songs by score (highest first) and return top K
```

### Why This Works

- **Simple**: Easy to debug and understand
- **Explainable**: We can show users *why* a song was recommended
- **Fast**: Runs instantly on any size dataset
- **Modular**: Easy to add new features later

### Known Limitations

- **Filter Bubble**: Users only get songs similar to what they already like
- **Genre Bias**: If most songs are pop, the system might over-recommend pop
- **Tiny Dataset**: With only 20 songs, results are limited
- **No Hybrid Logic**: Doesn't combine collaborative + content-based filtering

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

```bash
python -m venv .venv
source .venv/bin/activate      # Mac or Linux
.venv\Scripts\activate         # Windows
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

```bash
python -m pytest tests/test_recommender.py -v
```

**Test Output:**

![Test Results](<screenshots/Screenshot 2026-04-01 at 9.40.24 PM.png>)

---

## Experiments You Tried

### Test Results: 5 Distinct User Profiles

**1. Happy Pop Enthusiast** (Genre: pop, Mood: happy, Energy: 0.8)
- Top Pick: "Sunrise City" (Score: 4.97) — Perfect triple match (genre + mood + energy)
- Observation: System correctly prioritizes upbeat pop music

**2. Chill Lofi Lover** (Genre: lofi, Mood: chill, Energy: 0.4)
- Top Pick: "Library Rain" (Score: 5.42) — Genre + mood + energy + acoustic bonus
- Observation: Acoustic bonus (likes_acoustic=True) helped surface appropriate songs

**3. Intense Rock Fan** (Genre: rock, Mood: intense, Energy: 0.9)
- Top Pick: "Storm Runner" (Score: 4.98) — Full match on all core features
- Observation: **BIAS IDENTIFIED** — Only 1 rock song in dataset, system defaults to intense mood + high energy songs from other genres

**4. Focused Work Session** (Genre: lofi, Mood: focused, Energy: 0.4)
- Top Pick: "Focus Flow" (Score: 5.00) — Perfect match
- Observation: "Focused" mood is rare in dataset; system correctly matched the one song

**5. Ambient Meditation** (Genre: ambient, Mood: chill, Energy: 0.2)
- Top Pick: "Rainfall Meditation" (Score: 5.42) — Genre + mood + energy + acoustic bonus
- Observation: System effectively finds calm, meditative music

### Sensitivity Experiment: Doubling Energy Weight

| | Genre Match | Mood Match | Energy Similarity |
|---|---|---|---|
| **Original** | +2.0 | +1.5 | +1.5 max |
| **Modified** | +2.0 | +1.5 | +3.0 max |

Testing with "Chill Lofi Lover": slight reordering occurred — "Rainfall Meditation" and "Spacewalk Thoughts" moved up due to closer energy matching. Conclusion: energy weight affects rankings, but discrete genre/mood matches remain dominant.

### Key Findings

✅ **What Works Well:**
- Genre matching is the strongest signal
- Energy similarity smoothly rewards near-target songs
- Acoustic bonus helps lofi/ambient users
- System correctly differentiates between all 5 profiles

⚠️ **Limitations Discovered:**
1. **Genre Imbalance**: Pop (4 songs) vs Rock (1 song) vs Jazz (1 song)
2. **Mood Over-Representation**: "Happy" songs surface in most profiles' top 5
3. **Filter Bubble Risk**: Pop/happy users get near-identical results repeatedly
4. **Dataset Size**: 20 songs is too small for real variety
5. **Missing Features**: No artist popularity or diversity penalty

---

## Limitations and Risks

1. **Filter Bubble**: A "pop fan" will only ever get pop recommendations
2. **Dataset Bias**: Rock fans are severely under-served (1 out of 20 songs)
3. **Mood Imbalance**: Few "focused" or "moody" songs exist in the catalog
4. **No Artist Diversity**: A single artist could dominate the top 5
5. **Missing Real-World Signals**: No listening history, skips, social signals, or temporal patterns
6. **Energy Oversimplification**: Two songs with energy=0.5 can feel very different in reality

### Recommendations for Improvement

1. Expand to 500+ songs with balanced genre representation
2. Add a diversity penalty to prevent genre/artist repetition
3. Implement collaborative filtering
4. Add user feedback loop (thumbs up/down)
5. Model mood/energy interactions more precisely

---

## Reflection

### Key Takeaways

This project showed how simple algorithms can create meaningful — and biased — results. By building a weighted-score recommender with just three core features (genre, mood, energy), I learned that recommendation systems are products of their data, not magic.

The biggest insight was that real-world bias is accidental. I didn't design the system to over-recommend pop — it emerged naturally because pop songs in the dataset had higher energy and valence values. Fairness in AI requires deliberate data and weight choices, not just unbiased code.

Testing five distinct profiles showed that while the algorithm works well for consistent preferences, it creates filter bubbles. This mirrors real problems in Spotify, YouTube, and TikTok.

### Files and Evidence

- **Recommender Logic**: [src/recommender.py](src/recommender.py)
- **User Profiles**: [src/main.py](src/main.py)
- **Dataset**: [data/songs.csv](data/songs.csv)
- **Model Card**: [model_card.md](model_card.md)
- **Reflection**: [reflection.md](reflection.md)
