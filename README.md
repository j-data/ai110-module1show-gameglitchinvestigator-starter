# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

- [x] **Describe the game's purpose.**
  
  Game Glitch Investigator: The Impossible Guesser is a Streamlit number guessing game. The app picks a secret number within a range set by the difficulty (Easy: 1–20, Normal: 1–50, Hard: 1–100). You have a limited number of attempts to find it (Easy: 8, Normal: 6, Hard: 5). After each guess, the game tells you to go higher or lower and updates your score. You win by guessing the secret before you run out of attempts.

- [x] **Detail which bugs you found.**
  1. **The secret number changed type on every other guess.** On even attempts, the secret was turned into a string, so `check_guess` compared the numbers as text (`"9" > "50"`), and some hints and wins came out wrong.
  2. **The hints were backwards.** A guess above the secret said "Go HIGHER!" and a guess below it said "Go LOWER!".
  3. **The Normal and Hard ranges were swapped.** Normal used 1–100 and Hard used 1–50, so Hard was easier than Normal.
  4. **The Easy and Normal attempt limits were swapped.** Easy allowed 6 attempts and Normal allowed 8.
  5. **The prompt ignored difficulty.** The info box always said "Guess a number between 1 and 100", no matter which range the sidebar showed.
  6. **New Game didn't fully reset.** It picked the new secret from 1–100 on every difficulty and kept the old `status` and `history`, so a finished game still blocked new guesses. The first game also started at 1 attempt while new games started at 0.

- [x] **Explain what fixes you applied.**
  - Moved the game logic (`get_range_for_difficulty`, `parse_guess`, `check_guess`, `update_score`) out of `app.py` and into `logic_utils.py` so it can be tested with pytest.
  - Removed the code that turned the secret into a string. `check_guess` now converts both values to `int` before comparing them.
  - Swapped the hint messages so "Too High" says "📉 Go LOWER!" and "Too Low" says "📈 Go HIGHER!".
  - Corrected the ranges (Normal: 1–50, Hard: 1–100) and the attempt limits (Easy: 8, Normal: 6, Hard: 5).
  - Changed the info box to `f"Guess a number between {low} and {high}. "` so it uses the current difficulty's range.
  - New Game now picks the secret with `random.randint(low, high)` and resets `attempts`, `score`, `status` and `history`. Every game starts with `attempts = 0`.
  - Added pytest cases in `tests/test_game_logic.py` for the hint direction and the difficulty ranges.

## 🕹️ Demo Walkthrough

A sample game on **Normal** difficulty (range 1–50, 6 attempts). The secret number is **42**, which you can see in the "Developer Debug Info" panel.

1. The user starts the app with `python -m streamlit run app.py`. The sidebar shows `Range: 1 to 50` and `Attempts allowed: 6`, and the info box says "Guess a number between 1 and 50. Attempts left: 6".
2. The user enters a guess of **20** and clicks "Submit Guess 🚀". The game returns **"📈 Go HIGHER!"** (Too Low), and the score drops from 0 to **-5**.
3. The user enters a guess of **45**. The game returns **"📉 Go LOWER!"** (Too High). This is attempt 2, an even attempt, so `update_score` adds 5 points and the score goes to **0**.
4. The user enters a guess of **40**. The game returns **"📈 Go HIGHER!"** (Too Low), and the score drops to **-5**.
5. The user enters a guess of **42**. The game shows **"🎉 Correct!"**, balloons appear, and the message reads "You won! The secret was 42. Final score: 45". A win on attempt 4 is worth `100 - 10 × (4 + 1) = 50` points, and -5 + 50 = 45.
6. The game ends after the correct guess. If the user clicks Submit again, the game shows "You already won. Start a new game to play again." and doesn't accept the guess.
7. The user clicks "New Game 🔁". The Developer Debug Info panel shows a new secret between 1 and 50, with attempts, score and history all reset, and the user can start guessing again.

> **Note:** If the user ran out of all 6 attempts without guessing 42, the game would show "Out of attempts! The secret was 42." and stop accepting guesses until they start a new game.

## 🧪 Test Results

```
python -m pytest -v


tests/test_game_logic.py::test_winning_guess PASSED                           [ 14%]
tests/test_game_logic.py::test_guess_too_high PASSED                          [ 28%]
tests/test_game_logic.py::test_guess_too_low PASSED                           [ 42%]
tests/test_game_logic.py::test_normal_and_hard_ranges_not_swapped PASSED      [ 57%]
tests/test_game_logic.py::test_decimal_guess_is_not_truncated_to_a_win PASSED [ 71%]
tests/test_game_logic.py::test_negative_guess_is_rejected PASSED              [ 85%]
tests/test_game_logic.py::test_huge_guess_is_rejected PASSED                  [100%]

============================== 7 passed in 0.02s ==============================
```
