# 🎸 Reflection: Music Recommender Simulation

## Project Overview

This project revealed how **seemingly simple algorithms can create meaningful (and biased) results**. By implementing a weighted-scoring recommender with just three core features (genre, mood, energy), I learned that recommendation systems are products of their data, not magic.

The biggest insight: **real-world bias is accidental**. I didn't consciously design the system to over-recommend pop music—it emerged naturally because pop songs in the dataset had higher energy and valence values. This taught me that fairness in AI requires deliberate choices about data and weights, not just unbiased code.

---

## Per-Profile Analysis

### Profile 1: Happy Pop Enthusiast
**Preferences**: Genre=pop, Mood=happy, Energy=0.8, Acoustic=false

**Top Recommendation**: "Sunrise City" (Score: 4.97)
**Why It Works**: Full triple match on core signals:
- ✅ Genre match: pop (+2.0)
- ✅ Mood match: happy (+1.5)  
- ✅ Energy compatibility: 0.8 target ≈ 0.8 song energy (+1.5)

**Observation**: This profile is the system's "ideal case." The algorithm rewards discrete matches (pop, happy) heavily, and continuous energy matching works perfectly. Result: **All top 5 songs are high-energy pop tracks**. The algorithm functions as intended.

**System Behavior**: Genre weighting (+2.0) dominates, making pop the unquestionable first signal. This is strategic but creates a bias toward the dataset's majority genre.

---

### Profile 2: Chill Lofi Lover  
**Preferences**: Genre=lofi, Mood=chill, Energy=0.4, Acoustic=true

**Top Recommendation**: "Library Rain" (Score: 5.42)
**Why It Works**: Hits all scoring dimensions:
- ✅ Genre match: lofi (+2.0)
- ✅ Mood match: chill (+1.5)
- ✅ Energy compatibility: 0.4 target ≈ 0.3 song energy (+1.4)
- ✅ Acoustic bonus: acousticness > 0.75 (+0.5)

**Observation**: The acoustic bonus (likes_acoustic=true) tipped this profile into the highest score. **Result: Low-energy, acoustic-leaning songs ranked highest**. The `likes_acoustic` flag successfully surfaced the right songs.

**Comparison to Happy Pop Enthusiast**:
- This profile achieves *higher scores* (5.42 vs 4.97 max) because of the acoustic bonus
- Energy range is lower (0.3-0.5) vs (0.7-0.95)
- Dataset actually has more lofi songs that match this exact profile
- **Key insight**: Lofi lovers get broader variety (multiple lofi tracks fit), while pop lovers get narrower results due to pop's high-energy clustering

---

### Profile 3: Intense Rock Fan
**Preferences**: Genre=rock, Mood=intense, Energy=0.9, Acoustic=false

**Top Recommendation**: "Storm Runner" (Score: 4.98)
**Why It Works**: 
- ✅ Genre match: rock (+2.0)
- ✅ Mood match: intense (+1.5)
- ✅ Energy compatibility: 0.9 target ≈ 0.95 song energy (+1.48)

**Observation**: Despite perfect scoring logic, this profile exposes a critical **DATASET BIAS**. The dataset has **only 1 rock song**, so the system can only recommend:
1. The one rock song (top pick)
2. Other high-energy songs from different genres (pop, synthwave, EDM)

**Comparison to Lofi Lover**:
- Rock: 1 song (5%) - **severely under-served**
- Lofi: 3 songs (15%) - well-represented
- Result: Rock fan's top 5 includes pop tracks that shouldn't be there
- Pop sneaks into rock recommendations because "Upbeat Anthem" (pop, happy, energy=0.95) scores 4.7, close to "Storm Runner" (4.98)

**System Behavior**: The algorithm is working correctly, but the *data* is wrong. This is a lesson in **garbage in, garbage out**. No algorithm can overcome severe genre imbalance.

---

### Profile 4: Focused Work Session
**Preferences**: Genre=lofi, Mood=focused, Energy=0.4, Acoustic=true

**Top Recommendation**: "Focus Flow" (Score: 5.00)
**Why It Works**: Perfect match (a song literally exists with genre=lofi, mood=focused, energy=0.4)

**Observation**: This profile works *by accident* — there's exactly one "focused" song in the dataset, and it's lofi. **Result: Consistent lofi recommendations**. If the user had picked mood=thoughtful or mood=meditative, those moods barely exist in the dataset (maybe 1 song each).

**Comparison to Happy Pop & Intense Rock**:
- Happy pop: 7+ songs match preferences
- Intense rock: 1-2 songs match preferences  
- Focused work: 1-2 songs match preferences + lofi padding
- **Scalability issue**: As mood diversity increases in the dataset, this profile breaks. The algorithm assumes moods are well-distributed.

---

### Profile 5: Ambient Meditation
**Preferences**: Genre=ambient, Mood=chill, Energy=0.2, Acoustic=true

**Top Recommendation**: "Rainfall Meditation" (Score: 5.42)
**Why It Works**: Hits the full spectrum:
- ✅ Genre match: ambient (+2.0)
- ✅ Mood match: chill (+1.5)
- ✅ Energy compatibility: 0.2 target ≈ 0.1 song energy (+1.42)
- ✅ Acoustic bonus (+0.5)

**Observation**: **Result: Very low-energy, acoustic-heavy songs**. This profile gets extremely consistent recommendations—all ambient/lofi songs under 0.35 energy.

**Comparison to All Others**:
- Energy range diversity: Lowest (0.1-0.35)
- Genre diversity: None (pure ambient + possibly lofi padding)  
- **Filter bubble alert**: This user will *never* discover upbeat ambient music or meditative pop. The system locks them into one playlist forever.

---

## Cross-Profile Insights

### Energy Similarity Actually Works
Comparing the energy distributions:
- Pop (0.7-1.0) wants high energy: ✅ Algorithm rewards
- Lofi (0.2-0.5) wants low energy: ✅ Algorithm rewards  
- Rock (0.8-1.0) wants high energy: ✅ Algorithm rewards
- Ambient (0.1-0.35) wants very low energy: ✅ Algorithm rewards

**Conclusion**: Energy similarity (the continuous dimension) actually produces sensible results. The linear distance-based approach (1.5 × (1 - |diff|)) works well.

### Genre Weight Dominates, But Dataset Imbalance Wins
- A pop profile overrides low energy (gets upbeat pop)
- A rock profile can't override dataset sparsity (gets pop/synth)
- A lofi profile can balance genre + energy because there are enough lofi songs

**Lesson**: Weighting alone doesn't fix dataset bias. The weights (genre=2.0, mood=1.5, energy=1.5) are reasonable, but they expose whatever imbalances exist in the data.

### Mood Matching Reveals Data Sparsity  
- Happy ≅ 7+ songs (super common)
- Chill ≅ 4+ songs (common)
- Focused ≅ 1 song (rare)
- Intense ≅ 2 songs (rare)
- Moody ≅ 1 song (rare)

When a user picks a rare mood, the algorithm falls back to energy and genre. This is correct behavior, but it highlights that the mood feature is bottlenecked by dataset size.

---

## Key Learnings

### 1. Bias Is Structural, Not Intentional
I didn't write code that says "over-recommend pop songs." The bias emerged because:
- Pop songs in the dataset have higher energy
- Energy matching is a strong signal
- Ergo, pop surfaces more often

**Real-world parallel**: Spotify's algorithm isn't programmed to favor certain artists—it learns from what users listen to (which is already biased toward mainstream music).

### 2. Fairness Requires Deliberate Design
To solve the rock fan problem, I would need to:
- Add 10+ more rock songs (data fix)
- Or add a "genre diversity penalty" (algorithm fix)
- Or lower the genre weight (trade-off: less precise matching)

Every fix has side effects. Real companies struggle with this constantly.

### 3. Filter Bubbles Are a Feature, Not a Bug
The algorithm is *designed* to recommend similar songs. This is good for consistency but bad for discovery. Real platforms add exploration techniques:
- Collaborative filtering ("users like you also enjoyed...")
- Serendipity injection (intentional diverse picks)
- Context switching (different playlists for different moods)

This recommender does none of that, so it creates isolated filter bubbles by design.

### 4. Small Datasets Expose Algorithm Assumptions
With 20 songs, I can see exactly what the algorithm does. With 50 million songs (Spotify), the behavior is hidden. The core lesson is the same: **the algorithm is only as good as its data**.

### 5. The Cost of Simplicity
Our three-feature approach (genre, mood, energy) is explainable and fast. But it misses:
- Artist popularity (why recommend a 0.1% listener band?)
- Temporal patterns (disco at 3 AM makes no sense)
- Social signals (what are friends listening to?)
- Feedback loops (did you skip the recommendation?)

Real systems use hundreds of signals. The trade-off: accuracy vs. interpretability.

---

## What I'd Do Differently Next Time

1. **Expand the dataset first**, then build the algorithm (I did the reverse)
2. **A/B test the weights** with actual users before shipping (I guessed at 2.0, 1.5, 1.5)
3. **Track rejection rates** per profile (did rock fans hate the recommendations?)
4. **Add a diversity penalty** to top-k results (ensure variety)
5. **Implement user feedback** (thumbs up/down) to improve recommendations over time
6. **Monitor for filter bubbles** explicitly (flag users with <3 genres in top 10)

---

## Final Reflection

This project taught me that **recommendation systems are mirrors of their training data**. By building and testing mine with 5 distinct user profiles, I discovered that the same algorithm produces wildly different behaviors depending on dataset representation.

The rock fan gets mediocre recommendations not because the algorithm is broken, but because rock is under-represented in the data. The lofi lover gets excellent recommendations because lofi has 15% of the songs. The pop fan lives in abundance (20% of songs).

**This is how real bias enters AI systems**: not through malice, but through imbalanced data meeting simple optimization rules.

Understanding this—and making students experience it firsthand with a small dataset—is the real value of this project.
