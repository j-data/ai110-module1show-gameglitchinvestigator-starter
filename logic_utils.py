def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    #FIX: Swapped the difficulty ranges between Normal and Hard and refactored logic into logic_utils.py using agent mode
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 50
    if difficulty == "Hard":
        return 1, 100
    return 1, 100

def parse_guess(raw: str, low: int = 1, high: int = 100):
    #FIX: Decimals were truncated ("50.9" -> 50, a false win), and negative or huge
    # numbers were accepted. Reject non-whole numbers and anything outside low-high.
    if raw is None or raw.strip() == "":
        return False, None, "Enter a guess."

    try:
        number = float(raw)
    except ValueError:
        return False, None, "That is not a number."

    if not number.is_integer():
        return False, None, "Please enter a whole number."

    value = int(number)
    if value < low or value > high:
        return False, None, f"Guess must be between {low} and {high}."

    return True, value, None


def check_guess(guess, secret):
    """
    Compare guess to secret and return (outcome, message).

    outcome examples: "Win", "Too High", "Too Low"
    """
    #FIX: Hint messages were swapped (Too High said "Go HIGHER"), and a str secret
    # fell back to alphabetical comparison ("9" > "50"). Compare as ints instead.
    guess = int(guess)
    secret = int(secret)

    if guess == secret:
        return "Win", "🎉 Correct!"
    if guess > secret:
        return "Too High", "📉 Go LOWER!"
    return "Too Low", "📈 Go HIGHER!"

def update_score(current_score: int, outcome: str, attempt_number: int):
    if outcome == "Win":
        points = 100 - 10 * (attempt_number + 1)
        if points < 10:
            points = 10 
        return current_score + points

    if outcome == "Too High":
        if attempt_number % 2 == 0:
            return current_score + 5
        return current_score - 5

    if outcome == "Too Low":
        return current_score - 5

    return current_score
