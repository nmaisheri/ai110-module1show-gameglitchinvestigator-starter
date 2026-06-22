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

**Game purpose:** A number guessing game where the player tries to guess a secret number within a limited number of attempts. The game gives "Too High" or "Too Low" hints after each guess, updates a running score, and supports three difficulty levels (Easy: 1–20, Normal: 1–100, Hard: 1–200).

**Bugs found and fixed:**

| # | Bug | Fix Applied |
|---|-----|-------------|
| 1 | Hint messages were inverted — "Too High" said "Go HIGHER!" and "Too Low" said "Go LOWER!" | Swapped the return messages in `check_guess` |
| 2 | On even-numbered attempts, the secret was cast to a string, causing lexicographic comparison (e.g. `51 < "6"` alphabetically → wrong hint) | Removed the even-attempt string cast; secret is always compared as an int |
| 3 | Hard difficulty range was 1–50, making it narrower and easier than Normal (1–100) | Changed Hard range to 1–200 |
| 4 | Info banner hardcoded "between 1 and 100" regardless of selected difficulty | Updated to use `{low}` and `{high}` from the actual difficulty range |
| 5 | New Game button always generated a secret in range 1–100, ignoring the selected difficulty | Changed to `random.randint(low, high)` |
| 6 | New Game did not reset score, history, or game status — they carried over between games | Added resets for `score`, `history`, and `status` in the New Game handler |
| 7 | `attempts` was initialized to `1`, causing the attempt counter to display off by one on the first render | Changed initial value to `0` |
| 8 | Win score formula used `100 - 10 * (attempt_number + 1)`, over-penalizing wins (first-attempt win scored 70 instead of 90) | Removed the `+ 1`; formula is now `100 - 10 * attempt_number` |
| 9 | "Too High" on even-numbered attempts rewarded +5 points instead of deducting | Removed the even/odd branch; both wrong-guess outcomes always deduct 5 |

**Refactoring applied:** All game logic (`get_range_for_difficulty`, `parse_guess`, `check_guess`, `update_score`) was moved out of `app.py` and into `logic_utils.py`. `app.py` now imports these functions, keeping UI and logic cleanly separated.

## 📸 Demo Walkthrough

The following traces a full game on Normal difficulty (secret number: 55) to show end-to-end behavior after all fixes.

1. Player opens the app. The info banner correctly reads "Guess a number between 1 and 100. Attempts left: 8." Score starts at 0.
2. Player enters **40** and clicks Submit. Game returns "📈 Go HIGHER!" — correct hint since 40 < 55. Score updates to -5 (wrong guess, attempt 1 deducts 5).
3. Player enters **70**. Game returns "📉 Go LOWER!" — correct since 70 > 55. Score updates to -10.
4. Player enters **51**. Game returns "📈 Go HIGHER!" — correct since 51 < 55. Note: before the fix, `51` was compared as the string `"51"` on even attempts, and `"51" < "6"` lexicographically, which would have returned "Go LOWER!" incorrectly. Score updates to -15.
5. Player enters **55**. Game returns "🎉 Correct!" Balloons appear. Win points calculated as `100 - 10 * 4 = 60`, added to running score: final score is 45.
6. Player clicks **New Game**. Score resets to 0, history clears, status resets to "playing", and a new secret is generated within the current difficulty range. Before the fix, none of these fields were cleared.
7. Player switches to **Hard** difficulty in the sidebar. The banner now reads "Guess a number between 1 and 200" — before the fix, Hard used 1–50, which was easier than Normal.

## 🧪 Test Results

```
============================= test session starts ==============================
platform darwin -- Python 3.14.0, pytest-9.1.1, pluggy-1.6.0
rootdir: /Users/nmaisheri/ai110-module1show-gameglitchinvestigator-starter
collected 15 items

tests/test_game_logic.py::test_winning_guess PASSED                      [  6%]
tests/test_game_logic.py::test_guess_too_high PASSED                     [ 13%]
tests/test_game_logic.py::test_guess_too_low PASSED                      [ 20%]
tests/test_game_logic.py::test_too_high_message_says_go_lower PASSED     [ 26%]
tests/test_game_logic.py::test_too_low_message_says_go_higher PASSED     [ 33%]
tests/test_game_logic.py::test_numeric_comparison_not_lexicographic PASSED [ 40%]
tests/test_game_logic.py::test_numeric_comparison_not_lexicographic_lower PASSED [ 46%]
tests/test_game_logic.py::test_hard_range_wider_than_normal PASSED       [ 53%]
tests/test_game_logic.py::test_easy_range_narrower_than_normal PASSED    [ 60%]
tests/test_game_logic.py::test_too_high_on_even_attempt_deducts_points PASSED [ 66%]
tests/test_game_logic.py::test_too_high_on_odd_attempt_deducts_points PASSED [ 73%]
tests/test_game_logic.py::test_too_high_and_too_low_deduct_equally PASSED [ 80%]
tests/test_game_logic.py::test_win_on_first_attempt_scores_90 PASSED     [ 86%]
tests/test_game_logic.py::test_win_on_second_attempt_scores_80 PASSED    [ 93%]
tests/test_game_logic.py::test_win_score_floors_at_10 PASSED             [100%]

============================== 15 passed in 0.01s ==============================
```

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, describe the Enhanced UI changes here — a screenshot is optional]
