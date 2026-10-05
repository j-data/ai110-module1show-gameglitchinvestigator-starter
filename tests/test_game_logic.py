from logic_utils import check_guess, get_range_for_difficulty, parse_guess

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

def test_decimal_guess_is_not_truncated_to_a_win():
    # Bug: "50.9" was truncated to 50 and counted as a correct guess
    ok, value, _ = parse_guess("50.9")
    assert not ok or value != 50

def test_negative_guess_is_rejected():
    # Bug: negative numbers were accepted and cost an attempt
    ok, _, _ = parse_guess("-5")
    assert ok is False

def test_huge_guess_is_rejected():
    # Bug: no upper limit, so absurdly large guesses were accepted
    ok, _, _ = parse_guess("99999999999999999999")
    assert ok is False

