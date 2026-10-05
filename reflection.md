# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?

- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").
1. **Difficulty ranges are swapped between Normal and Hard.**
   - **Input / trigger:** Selecting "Normal" and then "Hard" in the sidebar Difficulty dropdown.
   - **Expected:** Difficulty should increase the range, so Normal should be `Range: 1 to 50` and Hard should be `Range: 1 to 100`.
   - **Actual:** Normal showed `Range: 1 to 100` and Hard showed `Range: 1 to 50`, which made Hard mode easier than Normal mode.
   - **Code-level cause:** `get_range_for_difficulty` in `app.py` (lines 4–11). The return values for `"Normal"` (line 8, `return 1, 100`) and `"Hard"` (line 10, `return 1, 50`) are reversed.
2. **Hints point in the wrong direction.**
   - **Input / trigger:** Guessing a number near the maximum (e.g. 99) when the secret was much lower, or a number near the minimum (e.g. 1) when the secret was much higher. This happened in every difficulty mode.
   - **Expected:** A guess above the secret should say "Go LOWER!", and a guess below the secret should say "Go HIGHER!".
   - **Actual:** A guess of 99 still told me "📈 Go HIGHER!", and a guess of 1 told me "📉 Go LOWER!", so following the hints moved me away from the secret.
   - **Code-level cause:** `check_guess` in `app.py` (lines 32–47). When `guess > secret` (line 37), the function returns the "📈 Go HIGHER!" message (line 38), and the `else` branch returns "📉 Go LOWER!" (line 40). The same pattern repeats in the `except TypeError` branch (lines 45–47). The hint message does not match the comparison result.
3. **Easy mode allows fewer attempts than Normal mode.**
   - **Input / trigger:** Switching between "Easy" and "Normal" in the sidebar and reading the "Attempts allowed" caption.
   - **Expected:** Easy should give the most attempts, more than Normal, and Hard should give the fewest.
   - **Actual:** Easy showed `Attempts allowed: 6` and Normal showed `Attempts allowed: 8`, so the easier mode gave me fewer chances.
   - **Code-level cause:** The `attempt_limit_map` dictionary in `app.py` (lines 80–84). `"Easy": 6` (line 81) and `"Normal": 8` (line 82) are reversed.
4. **The prompt ignores difficulty.**
   - **Input / trigger:** Selecting "Easy" (or "Normal") in the sidebar and reading the blue info box above the guess input.
   - **Expected:** The info box should match the sidebar range, e.g. "Guess a number between 1 and 20" on Easy.
   - **Actual:** The info box always said "Guess a number between 1 and 100", even though the sidebar showed `Range: 1 to 20`.
   - **Code-level cause:** The `st.info(...)` call in `app.py` (lines 109–112). Line 110 hardcodes `"Guess a number between 1 and 100. "` instead of using the `low` and `high` values from `get_range_for_difficulty`.
   - **Fix:** Changed the message to `f"Guess a number between {low} and {high}. "` so it uses the current difficulty's range.
5. **New Game doesn't fully reset.**
   - **Input / trigger:** Finishing a game (win or lose) on "Easy", then clicking "New Game 🔁".
   - **Expected:** A fresh game: a secret inside the Easy range (1–20), the full number of attempts, an empty history, and the ability to make guesses again.
   - **Actual:** The secret was picked from 1–100 no matter the difficulty, history from the last game was still shown in Developer Debug Info, and after a win or loss the game still said "You already won" / "Game over" and would not accept guesses. Attempts also restarted at 0, while the first game started at 1, so the "Attempts left" count was inconsistent between games.
   - **Code-level cause:** The `if new_game:` block in `app.py` (lines 134–138). Line 135 sets `attempts = 0` (but line 96 starts the first game at `1`), line 136 uses `random.randint(1, 100)` instead of the difficulty's range, and `status` and `history` are never reset, so the `st.stop()` check on lines 140–145 still ends the game.
   - **Fix:** In the `if new_game:` block, pick the secret with `random.randint(low, high)` and reset `score` to `0`, `status` to `"playing"`, and `history` to `[]`. Also changed the first-game `attempts` setup from `1` to `0`, so every game starts at 0 and the player gets the full attempt limit.


**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input Used | Expected Behavior | Actual Behavior | Console Error / Output | Suspected Code Location |
|------------|-------------------|-----------------|------------------------|-------------------------|
| Select "Normal" then "Hard" in the Difficulty dropdown | Normal: `Range: 1 to 50`; Hard: `Range: 1 to 100` | Normal: `Range: 1 to 100`; Hard: `Range: 1 to 50` | none | `app.py`, `get_range_for_difficulty` (lines 7–10) |
| Guess of 99 when the secret is lower (e.g. 42) | "📉 Go LOWER!" hint | "📈 Go HIGHER!" hint shown | none | `app.py`, `check_guess` (lines 37–40, 45–47) |
| Guess of 1 when the secret is higher (e.g. 42) | "📈 Go HIGHER!" hint | "📉 Go LOWER!" hint shown | none | `app.py`, `check_guess` (lines 37–40, 45–47) |
| Select "Easy" then "Normal" in the Difficulty dropdown | Easy allows more attempts than Normal | Easy: `Attempts allowed: 6`; Normal: `Attempts allowed: 8` | none | `app.py`, `attempt_limit_map` (lines 80–84) |
| Select "Easy" and read the info box | "Guess a number between 1 and 20" | "Guess a number between 1 and 100" shown | none | `app.py`, `st.info(...)` (line 110) |
| On "Easy", finish a game (win or lose), then click "New Game 🔁" | Secret within 1–20, empty history, status reset so guesses are accepted | Secret picked from 1–100, old history kept, "You already won" / "Game over" still blocks guesses | none | `app.py`, `if new_game:` block (lines 134–138) |

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
Claude
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
Claude correctly identified that the prompt ignores difficulty by always stating "Guess a number between 1 and 100" even on Easy mode, where the range is 1 to 20. It suggested replacing the hardcoded text with `f"Guess a number between {low} and {high}. "` so the message uses the values from `get_range_for_difficulty`. I checked the fix by running the app and switching between Easy, Normal and Hard. Each time, the info box matched the sidebar's `Range:` caption.
- Give one example of an AI suggestion you did not accept as written (including what the AI suggested, why you rejected or changed it, and how you verified your version). It does not have to be a suggestion that was wrong: over-engineered, out of scope, harder to read, or a poor fit for this codebase all count.
I ignored a "difficulty-switch problem" identified by Claude as a bug as I considered that to be over-engineering for this project, considering the "New Game" button already picks a new secret from the current difficulty's range, which handles the situation well enough. I checked this by switching to Easy, clicking "New Game", and confirming in Developer Debug Info that the new secret was between 1 and 20.


---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
For bugs in the game logic functions (`check_guess` and `get_range_for_difficulty`), I wrote new pytest cases or updated the existing ones in `tests/test_game_logic.py`, and I counted a bug as fixed once those tests passed. For bugs in the UI or session state in `app.py`, such as the info box text and the New Game reset, I tested by hand in the running Streamlit app. I compared what I saw on screen with the sidebar captions and the Developer Debug Info panel.
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
  I ran `test_guess_too_high`, which calls `check_guess(60, 50)` and asserts that the outcome is "Too High" and that the message contains "LOWER". It showed me that the comparison in `check_guess` was already correct and that only the hint messages were swapped. That meant the fix was to swap the messages, not the `>` operator I first suspected. After the fix, the test passed, as did its partner `test_guess_too_low`.
- Did AI help you design or understand any tests? How?
Yes. Claude helped me design `test_normal_and_hard_ranges_not_swapped` to check my fix for the difficulty ranges. The test asserts that `get_range_for_difficulty("Normal")` returns `(1, 50)` and `get_range_for_difficulty("Hard")` returns `(1, 100)`. It checks the exact ranges, not just that Normal is lower. If someone swaps the values back, the test fails right away.

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
Each time you interact with a Streamlit app (click a button, type in a box, change a dropdown), Streamlit runs the whole Python script again from top to bottom. That's a "rerun". So an ordinary variable like `secret = random.randint(1, 100)` would get a new value on every click. `st.session_state` is a dictionary that survives reruns, so the game uses it to remember the secret, the attempts, the score and the history.
---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
- This could be a testing habit, a prompting strategy, or a way you used Git.
Writing a small pytest case for each bug before or right after fixing it. Moving the logic out of `app.py` into `logic_utils.py` made the functions easy to test without starting the app. Each test also documents the bug, so it can't quietly come back.
- What is one thing you would do differently next time you work with AI on a coding task?
I would ask the AI to clearly explain why something is a bug before accepting its fix, and manually evaluate that against the code myself.
- In one or two sentences, describe how this project changed the way you think about AI generated code.
AI-generated code can look clean and "production-ready" and still have logic bugs that only show up when you run and test it.