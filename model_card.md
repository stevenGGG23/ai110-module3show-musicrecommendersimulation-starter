# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**VibeFinder 1.0** - A lightweight, content-based music recommendation system that learns from song attributes and user taste profiles.

---

## 2. Intended Use  

**Purpose**: Educational demonstration of how music streaming platforms decide on song recommendations.

**Target Users**: 
- Computer science students learning about recommendation algorithms
- Teams exploring how content-based filtering works
- Anyone curious about AI decision-making in apps they use daily

**Design Assumptions**:
- Users have stable music preferences (we're not accounting for mood changes throughout the day)
- Song attributes like "energy" and "mood" can be measured and compared numerically
- A simple combination of genre, mood, and energy is sufficient to make reasonable recommendations
- This is NOT meant to replace Spotify or YouTube

**Real-World Applications This Models**: Spotify's "Release Radar," YouTube Music recommendations, and similar content-based systems at their core.

---

## 3. How the Model Works  

**Simple Explanation**: 
Imagine you tell a friend "I like upbeat pop songs right now." VibeFinder reads a catalog of songs and scores each one like a judge:
- ✅ Genre match (pop)? +2 points
- ✅ Mood match (happy)? +1.5 points  
- ✅ Energy level close to 0.8 (upbeat)? Up to +1.5 points
- ✅ Acoustic vibe? +0.5 bonus points

After scoring every song, it ranks them and shows you the top 5.

**Mathematical Formula**:

```
Score = 0

IF song.genre == user.genre: score += 2.0
IF song.mood == user.mood: score += 1.5

energy_similarity = 1.5 * (1.0 - abs(song.energy - user.energy))
score += energy_similarity

IF user.likes_acoustic AND song.acousticness > 0.75: score += 0.5

Rankings = SORT(all_songs by score, DESCENDING)
Recommendations = TOP(Rankings, k=5)
```

**Why These Weights?**
- Genre is worth the most (+2.0) because it's the broadest category
- Mood is strong (+1.5) because it's a primary emotional signal
- Energy is flexible (up to +1.5) because it's a spectrum, not binary
- Acoustic bonus is small (+0.5) because it's optional

**Key Design Choices**:
- We reward songs *near* the user's target energy, not far from it
- We use exact matches for genre/mood (pop ≠ rock), not fuzzy matching
- We don't consider artist, lyrics, or social signals
- Scores are fully explainable (every point has a reason)

---

## 4. Data  

**Dataset**: 20 songs across 10 genres

**Genre Distribution**:
- Pop: 4 songs (20%)
- Lofi: 3 songs
- Synthwave: 2 songs
- Ambient: 2 songs  
- Rock, Jazz, EDM, Reggae, Hip-Hop, Folk, Classical, Indie Pop: 1 each

**Features Used Per Song**:
- `id`: Unique identifier (1-20)
- `title`: Song name
- `artist`: Artist name
- `genre`: Primary classification
- `mood`: Emotional category (happy, chill, intense, focused, moody, relaxed)
- `energy`: 0.0-1.0 scale (0=very calm, 1=very intense)
- `tempo_bpm`: Beats per minute
- `valence`: 0.0-1.0 scale (0=sad, 1=happy) — currently unused
- `danceability`: 0.0-1.0 scale — currently unused
- `acousticness`: 0.0-1.0 scale (0=synthetic, 1=acoustic)

**Data Limitations**:
- Only 20 songs total — too small for real-world use
- Genre imbalance: Pop is over-represented, Rock has only 1 example
- Missing features: Artist popularity, release date, language, lyrical themes, user's skip history
- No temporal context: Doesn't know if user listened to this song in the morning (workout) vs. evening (chill)
- Static attributes: A song's "mood" doesn't change, but users' emotional needs do

**Did We Add/Remove Data?**
- Started with 10 songs, expanded to 20 to provide more variety
- Added songs in underrepresented genres (EDM, Folk, Classical) and moods
- Did NOT remove any original songs to maintain baseline compatibility

---

## 5. Strengths  

**Works Well For**:
1. **Consistent Preference Profiles**: Users with stable tastes (e.g., "I always want chill lofi")
2. **Genre-Focused Users**: People who say "recommend me more pop"
3. **Energy-Aware Fits**: Matching workout songs vs. sleep songs correctly
4. **Explainability**: Every recommendation has a clear reason (not a black box)

**Patterns Captured**:
- ✅ High-energy songs (0.8+) cluster separately from calm songs (0.2-0.4)
- ✅ Genre boundaries are respected (rock songs don't slip into lofi top 5)
- ✅ Mood matching is consistent (happy songs always match happy users)
- ✅ The acoustic bonus correctly surfaces acoustic songs for lofi/ambient/folk lovers

**Good Recommendations**:
- Happy pop lover → Gets "Sunrise City" (perfect match on all 3 dimensions)
- Focused work user → Gets "Focus Flow" (rare mood, but system found the exact match)
- Meditation seeker → Gets "Rainfall Meditation" (low energy, high acousticness, ambient genre)

---

## 6. Limitations and Bias 

### **Critical Bias: Genre Over-Representation**

Pop music dominates the recommendations because:
1. Pop has 4 songs (20% of catalog) vs. Rock (5%), Jazz (5%)
2. Pop songs tend to be happy (high valence), which matches many users' preferences
3. Pop + high energy scores higher than niche genres at lower energy

**Impact**: A user asking for genre-agnostic "happy" music will get 3-4 pop songs before seeing jazz or indie options.

### **Filter Bubble Problem**

Once a system learns you like pop, it recommends only pop. You'll never discover:
- That one indie folk song that matches your mood perfectly
- A new ambient artist you'd love
- Cross-genre discoveries (why not a classical piece for relaxation?)

**Real-World Example**:
- Spotify user listened to Post Malone → Gets 100% hip-hop/rap recommendations
- User never discovers The Tallest Man On Earth (folk), who also has chill vibes

### **Mood Imbalance**

Some moods are underrepresented:
- "Happy": 7 songs
- "Chill": 5 songs
- "Intense": 4 songs
- "Focused": 1 song ← Big problem for study-focused users

### **Artist Clustering**

If a user's perfect match is an LoRoom song:
- "Midnight Coding" scores 4.97
- "Focus Flow" scores 4.00
- Same artist twice in top 5 — no diversity

### **Static Attribute Problem**

"Energy" is treated as absolute, but context matters:
- 0.8 energy at 6am = Great workout motivation
- 0.8 energy at 10pm = Keeps you awake
- System has no concept of time-of-day or user context

### **Missing Collaborative Signal**

System ignores: "Users who liked X also liked Y"
- Misses emerging artists and cross-genre gems
- Can't pick up on subtle taste patterns (e.g., users who like sad indie also like jazz)

---

## 7. Evaluation  

### **Test Profiles**

| Profile | Genre | Mood | Energy | Result | Grade |
|---------|-------|------|--------|--------|-------|
| Happy Pop Enthusiast | pop | happy | 0.8 | Top 5 all pop/high-energy | ✅ Perfect |
| Chill Lofi Lover | lofi | chill | 0.4 | Low-energy lofi + ambient | ✅ Perfect |
| Intense Rock Fan | rock | intense | 0.9 | Only 1 rock; defaulted to intense mood | ⚠️ Biased |
| Focused Work Session | lofi | focused | 0.4 | Correct lofi, but only 1 "focused" song exists | ⚠️ Limited |
| Ambient Meditation | ambient | chill | 0.2 | Lowest energy, high acoustic songs | ✅ Perfect |

### **What Surprised Me**

1. **Mood Matching is Rare**: Only 1 "focused" song exists, so recommendations for that mood are weak
2. **Genre Ceiling**: Rock fan can't get good recommendations because there's only 1 rock song
3. **Energy Smoothing Works**: The energy similarity formula correctly interpolates between songs
4. **Acoustic Bonus Had Big Impact**: It pushed "Library Rain" from 3.92 to 5.42 score — sometimes a small bonus changes everything

### **Sensitivity Experiment Results**

**Changed**: Doubled energy weight from 1.5 to 3.0 (to test if users who care about vibe over genre get better results)

**Test Case**: Chill Lofi Lover profile
- Original: [Library Rain (5.42), Midnight Coding (4.97), Focus Flow (4.00)]
- Adjusted: [Library Rain (6.42), Midnight Coding (5.97), Focus Flow (5.00)]
- **Conclusion**: Scores increased proportionally, but ranking stayed the same. Energy weight != ranking order when genre/mood are also strong signals.

---

## 8. Future Work  

### **High-Impact Improvements**

1. **Diversity Penalty**
   - After recommending a song, penalize remaining songs by the same artist/genre
   - Would prevent "LoRoom song #3 in top 5" problem

2. **Expand Dataset**
   - Current: 20 songs
   - Target: 500+ with balanced genre/mood distribution
   - Would improve confidence for niche preferences

3. **Add Temporal Context**
   - Learn: "Morning = energetic, Evening = chill"
   - Parameter: `time_of_day` ∈ {morning, afternoon, evening, night}

4. **Implement Hybrid Filtering**
   - Content-based (current) + Collaborative (what others liked)
   - Formula: `final_score = 0.7 * content_score + 0.3 * collaborative_score`

5. **User Feedback Loop**
   - Add thumbs up/down on recommendations
   - Re-weight features based on which signals users respond to

### **Nice-to-Have Features**

- Playlist creation (group songs with similar scores)
- Seed song expansion (given "Sunrise City," find similar songs)
- Interactive weight tuning (let users adjust genre vs. mood importance)
- Conflict detection (alert if recommendations seem contradictory)
- A/B testing framework (compare two algorithms on same user)

### **Research Questions**

- Do users prefer **serendipity** (unexpected but good) or **expected** (exactly what I asked for)?
- How much does **artist diversity** matter vs. **genre consistency**?
- Can we detect **mood changes** and adapt recommendations in real-time?

---

## Personal Reflection

### **What I Learned**

Building this recommender taught me that **simple algorithms can feel surprisingly intelligent**. Using just three weighted factors (genre + mood + energy), the system made recommendations that *felt* reasonable and personalized, even though it was nowhere near as sophisticated as Spotify.

The biggest surprise was **how much bias crept in unconsciously**. I didn't intend for pop music to dominate, but because pop songs in our dataset happened to have high energy and happiness values, they scored higher. The algorithm didn't "discriminate" — the data did. This mirrors real-world AI: the algorithm is only as fair as the data feeding it.

### **Where I Needed to Double-Check Myself**

1. **Testing my own assumptions**: I assumed "energy" would be the strongest predictor, but genre actually dominates. Testing with real profiles forced me to verify my weights.

2. **Staying skeptical of AI suggestions**: When Claude suggested a particular scoring formula, I manually tested it against edge cases (e.g., what if energy is 0.0?). Not every AI suggestion is correct for your problem.

3. **Recognizing when biases hide**: The filter bubble problem wasn't obvious from the code. I had to *use* the recommender with multiple profiles to see it emerge.

### **How AI Tools Helped (and Hindered)**

**Helpful**:
- Copilot suggested the tuple return format `(song, score, reasons)` which made explanations easy
- It generated diverse test profiles, forcing me to think beyond my own music taste
- Quick prototyping: I could focus on logic instead of debugging CSV parsing

**Required Double-Checking**:
- Copilot's first energy similarity formula was `(user_energy / song_energy)`, which broke when energy=0
- I had to replace it with the distance-based approach `1.0 - abs(energy_diff)`

### **What I'd Try Next**

1. **Real user study**: Give the recommender to 10 real humans and observe if they like the suggestions
2. **Collaborative filtering**: Add a second algorithm that learns from other users' choices, then blend both approaches
3. **Playlist context**: Instead of single songs, learn what songs *go together* in playlists
4. **Mood detection**: Use a user's Spotify listening history to infer if they're currently happy/sad/focused, then auto-recommend

### **The Big Takeaway**

This project showed me that **AI recommendations aren't magic**—they're just weighted sums of features humans define. The "intelligence" comes from choosing the right features and weights, not from the algorithm itself. The responsibility to choose fairly and recognize biases lies entirely with the engineer building it.

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  
