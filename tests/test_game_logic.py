from logic_utils import check_guess, get_range_for_difficulty, update_score

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    outcome, _ = check_guess(50, 50)
    assert outcome == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    outcome, _ = check_guess(60, 50)
    assert outcome == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    outcome, _ = check_guess(40, 50)
    assert outcome == "Too Low"

# Bug 1: hint messages were inverted — "Too High" said "Go HIGHER!" and "Too Low" said "Go LOWER!"
def test_too_high_message_says_go_lower():
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"
    assert "LOWER" in message, f"Expected 'LOWER' in message for too-high guess, got: {message!r}"

def test_too_low_message_says_go_higher():
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"
    assert "HIGHER" in message, f"Expected 'HIGHER' in message for too-low guess, got: {message!r}"

# Bug 2: on even attempts, secret was cast to str, causing lexicographic comparison.
# "51" < "6" lexicographically (because "5" < "6"), so check_guess(51, "6") would
# incorrectly return "Too Low" instead of "Too High".
def test_numeric_comparison_not_lexicographic():
    # 51 > 6 numerically → Too High; but "51" < "6" lexicographically → would give Too Low
    outcome, _ = check_guess(51, 6)
    assert outcome == "Too High", (
        f"Expected 'Too High' for 51 > 6 (numeric), got '{outcome}'. "
        "Likely caused by secret being cast to string (lexicographic comparison)."
    )

def test_numeric_comparison_not_lexicographic_lower():
    # Mirror case: 9 < 10 numerically → Too Low; but "9" > "10" lexicographically → would give Too High
    outcome, _ = check_guess(9, 10)
    assert outcome == "Too Low", (
        f"Expected 'Too Low' for 9 < 10 (numeric), got '{outcome}'. "
        "Likely caused by secret being cast to string (lexicographic comparison)."
    )


# Bug 3: Hard difficulty range (1–50) was narrower than Normal (1–100), making it easier.
# Fixed: Hard is now 1–200.
def test_hard_range_wider_than_normal():
    _, normal_high = get_range_for_difficulty("Normal")
    _, hard_high = get_range_for_difficulty("Hard")
    assert hard_high > normal_high, (
        f"Hard upper bound ({hard_high}) should exceed Normal ({normal_high}). "
        "Hard was accidentally set to 1–50, making it easier than Normal."
    )

def test_easy_range_narrower_than_normal():
    _, easy_high = get_range_for_difficulty("Easy")
    _, normal_high = get_range_for_difficulty("Normal")
    assert easy_high < normal_high, (
        f"Easy upper bound ({easy_high}) should be less than Normal ({normal_high})."
    )


# Bug 4: update_score gave +5 points for a "Too High" guess on even attempt numbers.
# Fixed: wrong guesses always deduct 5 regardless of attempt parity.
def test_too_high_on_even_attempt_deducts_points():
    score = update_score(50, "Too High", attempt_number=2)
    assert score < 50, (
        f"Expected score to decrease for a 'Too High' guess on attempt 2 (even), got {score}. "
        "Bug: even-attempt 'Too High' was rewarding +5 instead of deducting."
    )

def test_too_high_on_odd_attempt_deducts_points():
    score = update_score(50, "Too High", attempt_number=3)
    assert score < 50, f"Expected score to decrease for 'Too High' on odd attempt, got {score}."

def test_too_high_and_too_low_deduct_equally():
    score_high = update_score(50, "Too High", attempt_number=2)
    score_low = update_score(50, "Too Low", attempt_number=2)
    assert score_high == score_low, (
        f"'Too High' ({score_high}) and 'Too Low' ({score_low}) should deduct the same points. "
        "Bug: 'Too High' on even attempts gave +5 while 'Too Low' always gave -5."
    )


# Bug 5: Win score formula used (attempt_number + 1), over-penalizing wins.
# A correct guess on attempt 1 should score 100 - 10*1 = 90, not 100 - 10*2 = 70.
def test_win_on_first_attempt_scores_90():
    score = update_score(0, "Win", attempt_number=1)
    assert score == 90, (
        f"Expected 90 for a win on attempt 1, got {score}. "
        "Bug: formula used (attempt_number + 1), inflating the penalty by one extra step."
    )

def test_win_on_second_attempt_scores_80():
    score = update_score(0, "Win", attempt_number=2)
    assert score == 80, f"Expected 80 for a win on attempt 2, got {score}."

def test_win_score_floors_at_10():
    # At attempt 10+, points would go negative without the floor
    score = update_score(0, "Win", attempt_number=15)
    assert score == 10, f"Expected score to floor at 10 for late wins, got {score}."
