from logic_utils import check_guess, get_range_for_difficulty

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    outcome, _ = check_guess(50, 50)
    assert outcome == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    # Bug: the message said "Go HIGHER!" when the guess was already too high
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"
    assert "LOWER" in message

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    # Bug: the message said "Go LOWER!" when the guess was already too low
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"
    assert "HIGHER" in message

def test_normal_and_hard_ranges_not_swapped():
    # Bug: Normal returned 1-100 and Hard returned 1-50, so Hard was easier than Normal
    assert get_range_for_difficulty("Normal") == (1, 50)
    assert get_range_for_difficulty("Hard") == (1, 100)
