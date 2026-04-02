# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

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

Our recommender scores each song like this:

```
Base Score = 0

IF song.genre == user.favorite_genre
    score += 2.0  (strong signal: right category)

IF song.mood == user.favorite_mood
    score += 1.0  (good signal: right feeling)

Energy Compatibility = 2.0 * (1.0 - abs(song.energy - user.target_energy))
    (rewards songs close to user's target energy)

Final Score = Base Score + Energy Compatibility

Ranking: Sort all songs by score (highest first) and return top K
```

### Why This Works

- **Simple**: Easy to debug and understand
- **Explainable**: We can show users *why* a song was recommended
- **Fast**: Runs instantly on any size dataset
- **Modular**: Easy to add new features later (artist popularity, release decade, etc.)

### Known Limitations

- **Filter Bubble**: Users only get songs similar to what they already like
- **Genre Bias**: If most songs are pop, the system might over-recommend pop
- **Tiny Dataset**: With only 10 songs, results are limited
- **No Hybrid Logic**: Doesn't combine collaborative + content-based filtering

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
python -m pytest tests/test_recommender.py -v
```

**Test Output:**

![Test Results](screenshots/Screenshot%202026-04-01%20at%209.40.24%20PM.png)

All tests pass successfully! You can add more tests in `tests/test_recommender.py`.

---

## Experiments You Tried

### Test Results: 5 Distinct User Profiles

The recommender was tested with these profiles:

**1. Happy Pop Enthusiast** (Genre: pop, Mood: happy, Energy: 0.8)
- Top Pick: "Sunrise City" (Score: 4.97) - Perfect triple match (genre + mood + energy)
- Result: All top songs are high-energy pop tracks
- Observation: System correctly prioritizes upbeat pop music

**2. Chill Lofi Lover** (Genre: lofi, Mood: chill, Energy: 0.4)
- Top Pick: "Library Rain" (Score: 5.42) - Genre + mood + energy + acoustic bonus
- Result: Low-energy, acoustic-leaning songs ranked highest
- Observation: Acoustic bonus (likes_acoustic=True) helped surface appropriate songs

**3. Intense Rock Fan** (Genre: rock, Mood: intense, Energy: 0.9)
- Top Pick: "Storm Runner" (Score: 4.98) - Full match on all core features
- Result: High-energy songs dominate, but limited rock in dataset
- Observation: **BIAS IDENTIFIED**: Only 1 rock song in dataset, so system defaults to intense mood + high energy

**4. Focused Work Session** (Genre: lofi, Mood: focused, Energy: 0.4)
- Top Pick: "Focus Flow" (Score: 5.00) - Perfect match
- Result: Consistent lofi recommendations
- Observation: "Focused" mood is rare; system correctly matched the one song

**5. Ambient Meditation** (Genre: ambient, Mood: chill, Energy: 0.2)
- Top Pick: "Rainfall Meditation" (Score: 5.42) - Genre + mood + energy + acoustic bonus
- Result: Very low-energy, acoustic-heavy songs
- Observation: System effectively finds calm, meditative music

### Sensitivity Experiment: Doubling Energy Weight

**Original Weights:**
- Genre match: +2.0
- Mood match: +1.5
- Energy similarity: +1.5 (max)

**Modified Weights (Energy x2):**
- Genre match: +2.0
- Mood match: +1.5
- Energy similarity: +3.0 (max)

Testing with "Chill Lofi Lover" profile:
- Original rank: [Library Rain (5.42), Midnight Coding (4.97), Focus Flow (4.00)]
- Result: Slight reordering, "Rainfall Meditation" and "Spacewalk Thoughts" moved up due to lower energy matching
- Conclusion: Energy weight **does affect rankings**, but mood/genre are still dominant because they're discrete matches

### Key Findings

✅ **What Works Well:**
- Genre matching (+2.0) is the strongest signal
- Energy similarity smoothly rewards songs near the target
- Acoustic bonus helps for lofi/ambient users
- System correctly differentiates profiles

⚠️ **Limitations Discovered:**
1. **Genre Imbalance**: Pop (4 songs) vs Rock (1 song) vs Jazz (1 song)
2. **Mood Over-Representation**: "Happy" songs appear in most profiles' top 5
3. **Filter Bubble Risk**: Users who like "pop/happy" get similar songs repeatedly
4. **Dataset Size**: 20 songs is too small for real variety
5. **Missing Features**: No artist popularity, no explicit diversity penalty

---

## Limitations and Risks

### System Limitations

1. **Filter Bubble Problem**: The system only recommends songs similar to user preferences, meaning users never discover new genres or styles they might enjoy. A "pop fan" will only get pop recommendations forever.

2. **Dataset Bias**: The 20-song catalog has:
   - 4 pop songs (20%)
   - 3 lofi songs
   - 1 rock song (8%)
   - 1 jazz song
   - 2 ambient songs
   - This means rock fans are severely under-served

3. **Mood Imbalance**: The dataset has many "happy" and "chill" songs but few "focused" or "moody" songs. Users with those preferences get limited options.

4. **No Artist Diversity**: If a user's top pick is from artist "LoRoom," they might get all 3 LoRoom songs in the top 5, with no variety.

5. **Missing Features**: Real Spotify uses:
   - User's listening history (what did *you* actually stream?)
   - Playlist context (songs people listen to together)
   - Explicit ratings or skips
   - Social signals (what are your friends listening to?)
   - Temporal patterns (what do you listen to at different times?)

6. **Energy Gap Simplification**: Energy is treated as a continuous linear value, but musical taste is subjective. Two songs with energy=0.5 might feel very different (one is moody, one is jazz).

### Recommendations for Improvement

1. Expand the dataset to 500+ songs with balanced genre representation
2. Add a "diversity penalty" to prevent artist/genre repetition in top 5
3. Implement collaborative filtering (learn from similar users)
4. Add user feedback loop (thumbs up/down after recommendation)
5. Consider mood/energy interaction (moody + high energy = intense, not contradictory)

---

## Reflection

### Key Takeaways

This project revealed how **seemingly simple algorithms can create meaningful (and biased) results**. By implementing a weighted-scoring recommender with just three core features (genre, mood, energy), I learned that recommendation systems are products of their data, not magic.

The biggest insight: **real-world bias is accidental**. I didn't consciously design the system to over-recommend pop music—it emerged naturally because pop songs in the dataset had higher energy and valence values. This taught me that fairness in AI requires deliberate choices about data and weights, not just unbiased code.

Testing with five distinct user profiles showed that while the algorithm works well for consistent preferences, it creates "filter bubbles" where users never discover new genres. This mirrors real problems in Spotify, YouTube, and TikTok.

Using AI tools (Copilot) to help design the algorithm was valuable for rapid prototyping, but I had to verify every suggestion against edge cases. The AI's first energy similarity formula broke when energy=0, forcing me to implement a more robust distance-based approach.

### Files and Evidence

- **Recommender Implementation**: [src/recommender.py](src/recommender.py) with load_songs(), score_song(), recommend_songs()
- **User Profile Examples**: [src/main.py](src/main.py) with 5 distinct test profiles
- **Dataset**: [data/songs.csv](data/songs.csv) with 20 songs across diverse genres
- **Full Documentation**: [model_card.md](model_card.md) captures design decisions, biases, and improvements
- **Test Output**: Above in "Experiments You Tried" section

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this


---

## 7. `model_card_template.md`

Combines reflection and model card framing from the Module 3 guidance. :contentReference[oaicite:2]{index=2}  

```markdown
# 🎧 Model Card - Music Recommender Simulation

## 1. Model Name

Give your recommender a name, for example:

> VibeFinder 1.0

---

## 2. Intended Use

- What is this system trying to do
- Who is it for

Example:

> This model suggests 3 to 5 songs from a small catalog based on a user's preferred genre, mood, and energy level. It is for classroom exploration only, not for real users.

---

## 3. How It Works (Short Explanation)

Describe your scoring logic in plain language.

- What features of each song does it consider
- What information about the user does it use
- How does it turn those into a number

Try to avoid code in this section, treat it like an explanation to a non programmer.

---

## 4. Data

Describe your dataset.

- How many songs are in `data/songs.csv`
- Did you add or remove any songs
- What kinds of genres or moods are represented
- Whose taste does this data mostly reflect

---

## 5. Strengths

Where does your recommender work well

You can think about:
- Situations where the top results "felt right"
- Particular user profiles it served well
- Simplicity or transparency benefits

---

## 6. Limitations and Bias

Where does your recommender struggle

Some prompts:
- Does it ignore some genres or moods
- Does it treat all users as if they have the same taste shape
- Is it biased toward high energy or one genre by default
- How could this be unfair if used in a real product

---

## 7. Evaluation

How did you check your system

Examples:
- You tried multiple user profiles and wrote down whether the results matched your expectations
- You compared your simulation to what a real app like Spotify or YouTube tends to recommend
- You wrote tests for your scoring logic

You do not need a numeric metric, but if you used one, explain what it measures.

---

## 8. Future Work

If you had more time, how would you improve this recommender

Examples:

- Add support for multiple users and "group vibe" recommendations
- Balance diversity of songs instead of always picking the closest match
- Use more features, like tempo ranges or lyric themes

---

## 9. Personal Reflection

A few sentences about what you learned:

- What surprised you about how your system behaved
- How did building this change how you think about real music recommenders
- Where do you think human judgment still matters, even if the model seems "smart"

