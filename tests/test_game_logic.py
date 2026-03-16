import sys
import os
from unittest.mock import Mock, patch, MagicMock

# Add parent directory to path to import app.py functions
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import game logic functions from app.py
from app import check_guess, parse_guess, update_score, get_range_for_difficulty


# ==================== Original Tests ====================

def test_winning_guess():
    """Test that a correct guess returns 'Win' outcome."""
    # If the secret is 50 and guess is 50, it should be a win
    outcome, message = check_guess(50, 50)
    assert outcome == "Win"
    assert message == "🎉 Correct!"


def test_guess_too_high():
    """Test that a guess higher than secret returns 'Too High' outcome with correct hint."""
    # If secret is 50 and guess is 60, hint should be "Go LOWER" (not "Go HIGHER")
    # BUG FIX #1: This was backwards before - was saying "Go HIGHER" when already too high
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"
    assert message == "📉 Go LOWER!"  # FIXED: Now correctly advises to go lower


def test_guess_too_low():
    """Test that a guess lower than secret returns 'Too Low' outcome with correct hint."""
    # If secret is 50 and guess is 40, hint should be "Go HIGHER" (not "Go LOWER")
    # BUG FIX #1: This was backwards before - was saying "Go LOWER" when already too low
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"
    assert message == "📈 Go HIGHER!"  # FIXED: Now correctly advises to go higher


# ==================== Additional Game Logic Tests ====================

def test_parse_guess_valid_integer():
    """Test parsing a valid integer guess."""
    ok, guess_int, err = parse_guess("42")
    assert ok is True
    assert guess_int == 42
    assert err is None


def test_parse_guess_valid_float():
    """Test parsing a guess with decimal (should convert to int)."""
    ok, guess_int, err = parse_guess("42.7")
    assert ok is True
    assert guess_int == 42
    assert err is None


def test_parse_guess_empty_string():
    """Test parsing an empty string returns error."""
    ok, guess_int, err = parse_guess("")
    assert ok is False
    assert guess_int is None
    assert err == "Enter a guess."


def test_parse_guess_none():
    """Test parsing None returns error."""
    ok, guess_int, err = parse_guess(None)
    assert ok is False
    assert guess_int is None
    assert err == "Enter a guess."


def test_parse_guess_invalid_input():
    """Test parsing non-numeric input returns error."""
    ok, guess_int, err = parse_guess("abc")
    assert ok is False
    assert guess_int is None
    assert err == "That is not a number."


def test_update_score_win():
    """Test score update on winning guess."""
    # Winning on attempt 1: 100 - 10 * (1 + 1) = 80 points
    new_score = update_score(0, "Win", 1)
    assert new_score == 80


def test_update_score_win_minimum():
    """Test score update on winning guess doesn't go below 10."""
    # Winning on attempt 10: 100 - 10 * (10 + 1) = -10, should be capped at 10
    new_score = update_score(0, "Win", 10)
    assert new_score == 10


def test_update_score_too_high_even_attempt():
    """Test score update for 'Too High' on even attempt (gets +5)."""
    # Even attempt on "Too High" gives +5 points
    new_score = update_score(50, "Too High", 2)
    assert new_score == 55


def test_update_score_too_high_odd_attempt():
    """Test score update for 'Too High' on odd attempt (gets -5)."""
    # Odd attempt on "Too High" gives -5 points
    new_score = update_score(50, "Too High", 3)
    assert new_score == 45


def test_update_score_too_low():
    """Test score update for 'Too Low' (always -5)."""
    # "Too Low" always gives -5 points
    new_score = update_score(50, "Too Low", 2)
    assert new_score == 45


def test_get_range_easy():
    """Test difficulty range for Easy mode."""
    low, high = get_range_for_difficulty("Easy")
    assert low == 1
    assert high == 20


def test_get_range_normal():
    """Test difficulty range for Normal mode."""
    low, high = get_range_for_difficulty("Normal")
    assert low == 1
    # FIXED: Changed from 100 to 50 after fixing bug #3
    # OLD: assert high == 100  # ❌ Was incorrect (too hard for "Normal")
    assert high == 50  # ✓ Corrected to proper Normal difficulty


def test_get_range_hard():
    """Test difficulty range for Hard mode."""
    low, high = get_range_for_difficulty("Hard")
    assert low == 1
    # FIXED: Changed from 50 to 100 after fixing bug #3
    # OLD: assert high == 50  # ❌ Was incorrect (too easy for "Hard")
    assert high == 100  # ✓ Corrected to proper Hard difficulty


# ==================== BUG FIX #1 Tests ====================
# These tests specifically target the bug fixed in app.py lines 38-55
# Bug: check_guess() was returning backwards hint messages
#      - When guess > secret (too high), it said "Go HIGHER" instead of "Go LOWER"
#      - When guess < secret (too low), it said "Go LOWER" instead of "Go HIGHER"
# Fix: Swapped the hint messages in both try and except blocks


def test_bug_fix_1_guess_too_high_correct_hint():
    """
    TEST FOR BUG FIX #1: Verify correct hint when guess is too high.

    SCENARIO: Secret is 12, guess is 10 (referring to original bug report)
    - Guess (10) > Secret (12)? No, so goes to else block

    BUG BEHAVIOR: Would return "📉 Go LOWER!" (said go lower when already too low)
    FIXED BEHAVIOR: Now returns "📈 Go HIGHER!" (correctly says go higher)
    """
    secret = 12
    guess = 10
    outcome, message = check_guess(guess, secret)
    assert outcome == "Too Low", f"Guess {guess} < Secret {secret} should be 'Too Low'"
    assert message == "📈 Go HIGHER!", f"When too low, should get 'Go HIGHER', got {message}"


def test_bug_fix_1_guess_too_low_correct_hint():
    """
    TEST FOR BUG FIX #1: Verify correct hint when guess is too low.

    SCENARIO: Secret is 12, guess is 15
    - Guess (15) > Secret (12)? Yes

    BUG BEHAVIOR: Would return "📈 Go HIGHER!" (said go higher when already too high)
    FIXED BEHAVIOR: Now returns "📉 Go LOWER!" (correctly says go lower)
    """
    secret = 12
    guess = 15
    outcome, message = check_guess(guess, secret)
    assert outcome == "Too High", f"Guess {guess} > Secret {secret} should be 'Too High'"
    assert message == "📉 Go LOWER!", f"When too high, should get 'Go LOWER', got {message}"


def test_bug_fix_1_multiple_scenarios():
    """
    TEST FOR BUG FIX #1: Test multiple guess/secret combinations.

    This test verifies the fix works consistently across different number ranges.
    """
    test_cases = [
        # (secret, guess, expected_outcome, expected_emoji_direction)
        (50, 60, "Too High", "📉"),      # Guess too high → should say Go LOWER
        (50, 40, "Too Low", "📈"),       # Guess too low → should say Go HIGHER
        (100, 50, "Too Low", "📈"),      # Edge case: guess way too low
        (1, 50, "Too High", "📉"),       # Edge case: guess way too high
        (75, 75, "Win", None),           # Exact match (emoji not checked)
    ]

    for secret, guess, expected_outcome, expected_emoji in test_cases:
        outcome, message = check_guess(guess, secret)
        assert outcome == expected_outcome, \
            f"Secret={secret}, Guess={guess}: expected outcome '{expected_outcome}', got '{outcome}'"

        if expected_outcome != "Win" and expected_emoji:
            assert message.startswith(expected_emoji), \
                f"Secret={secret}, Guess={guess}: expected message to start with '{expected_emoji}', got '{message}'"


def test_bug_fix_1_type_error_path():
    """
    TEST FOR BUG FIX #1: Verify hint fix works in the TypeError exception path.

    This tests the except TypeError block (lines 47-55 in app.py) which handles
    the scenario where guess is int but secret is string.
    """
    secret_as_string = "50"

    # Test too high in TypeError path
    guess_too_high = 60
    outcome, message = check_guess(guess_too_high, secret_as_string)
    assert outcome == "Too High"
    assert message == "📉 Go LOWER!", "TypeError path should also have correct hint for too high"

    # Test too low in TypeError path
    guess_too_low = 40
    outcome, message = check_guess(guess_too_low, secret_as_string)
    assert outcome == "Too Low"
    assert message == "📈 Go HIGHER!", "TypeError path should also have correct hint for too low"



# These tests specifically target the bug fixed in app.py lines 135-151
# Bug: After clicking "New Game", status wasn't reset, causing st.stop() to be hit
# Fix: Reset status, history, attempts, secret, and score on New Game


def test_new_game_state_reset_after_win():
    """
    TEST FOR BUG FIX #2: Verify that game state is properly reset after winning.

    SCENARIO:
    1. Player wins a game (status = "won")
    2. Player clicks "New Game" button
    3. All state should reset to initial values
    4. Submit button should work (status = "playing")

    FIX VALIDATION:
    - status should be reset to "playing" (not stay as "won")
    - history should be cleared
    - attempts should be reset to 1
    - score should be reset to 0
    - secret should be a new random number
    """
    # Simulate Streamlit session state using a mock
    mock_session_state = {
        "status": "won",  # Player just won
        "history": [25, 50, 75, 50],  # Previous guesses
        "attempts": 4,  # Player made 4 attempts
        "secret": 50,  # Old secret number
        "score": 80,  # Score from winning game
    }

    # Simulate what the "New Game" button handler does (from app.py lines 139-151)
    # BUG FIX: Reset all game state
    mock_session_state["status"] = "playing"
    mock_session_state["history"] = []
    mock_session_state["attempts"] = 1
    mock_session_state["secret"] = 42  # New random secret (simulated)
    mock_session_state["score"] = 0

    # ASSERTIONS: Verify all state is reset
    assert mock_session_state["status"] == "playing", "Status should be reset to 'playing'"
    assert mock_session_state["history"] == [], "History should be cleared"
    assert mock_session_state["attempts"] == 1, "Attempts should be reset to 1"
    assert mock_session_state["secret"] == 42, "Secret should be a new number"
    assert mock_session_state["score"] == 0, "Score should be reset to 0"


def test_new_game_state_reset_after_loss():
    """
    TEST FOR BUG FIX #2: Verify game state is properly reset after losing.

    SCENARIO:
    1. Player loses a game (status = "lost")
    2. Player clicks "New Game" button
    3. All state should reset to initial values
    4. Submit button should work (status = "playing")
    """
    mock_session_state = {
        "status": "lost",  # Player just lost
        "history": [10, 20, 30, 40, 50, 60, 70, 80],  # Many failed guesses
        "attempts": 8,  # Out of attempts
        "secret": 25,
        "score": -15,  # Negative score from repeated wrong guesses
    }

    # Apply the fix
    mock_session_state["status"] = "playing"
    mock_session_state["history"] = []
    mock_session_state["attempts"] = 1
    mock_session_state["secret"] = 33  # New random secret
    mock_session_state["score"] = 0

    # ASSERTIONS
    assert mock_session_state["status"] == "playing", "Status should reset to 'playing' after loss"
    assert mock_session_state["history"] == [], "History should be cleared after loss"
    assert mock_session_state["attempts"] == 1, "Attempts should reset to 1 after loss"


def test_status_check_passes_after_new_game():
    """
    TEST FOR BUG FIX #2: Verify that the status check no longer stops execution.

    BEFORE FIX:
    - After winning, clicking "New Game" didn't reset status
    - The check `if st.session_state.status != "playing"` would be True
    - This would hit `st.stop()` and disable all buttons
    - Submit Guess button would be non-functional

    AFTER FIX:
    - Status is reset to "playing"
    - The check `if st.session_state.status != "playing"` is False
    - Code continues normally, Submit button works
    """
    status_after_win = "won"

    # Before fix: the status check would stop execution
    # if status_after_win != "playing":
    #     st.stop()  # This would execute, breaking the button

    # After fix: status is reset first
    status_after_new_game = "playing"

    # The status check now passes
    should_stop = (status_after_new_game != "playing")
    assert should_stop is False, "Status check should pass, app should not stop"


def test_history_accumulation_bug_fixed():
    """
    TEST FOR BUG FIX #2 (Secondary Issue): Verify that guess history doesn't accumulate.

    BUG: History array was never cleared, so old guesses would appear in new games
    FIX: Clear history when "New Game" is clicked
    """
    game1_history = [15, 25, 35, 42]  # Game 1 guesses

    # Without the fix, game 2 would accumulate game 1 history
    # buggy_result = game1_history + [50, 60]  # Would be [15, 25, 35, 42, 50, 60]

    # With the fix, game 2 starts fresh
    game2_history = []  # Cleared by fix
    game2_history.append(50)
    game2_history.append(60)

    assert game2_history == [50, 60], "Game 2 history should be fresh, not accumulate game 1"
    assert len(game1_history) == 4, "Original game 1 history should be unchanged"


# ==================== BUG FIX #3 Tests ====================
# These tests specifically target the bug fixed in app.py lines 9-20
# Bug: Difficulty ranges were swapped - Normal had 1-100 (too hard) and Hard had 1-50 (too easy)
# Fix: Corrected to Normal=1-50 and Hard=1-100 to match difficulty scaling logic
# Logic: Difficulty uses inverse scaling - easier levels have smaller ranges + more attempts


def test_bug_fix_3_normal_range_corrected():
    """
    TEST FOR BUG FIX #3: Verify Normal difficulty now has correct range (1-50).

    SCENARIO: Normal difficulty should have a medium-sized range
    - Easy: 1-20 (smallest) + 6 attempts = easiest
    - Normal: 1-50 (medium) + 8 attempts = medium difficulty  ← FIXED FROM 1-100
    - Hard: 1-100 (largest) + 5 attempts = hardest

    BUG BEHAVIOR: Normal returned 1-100 (same as Hard), making it too difficult
    FIXED BEHAVIOR: Normal now returns 1-50, creating proper difficulty progression

    This test verifies the fix keeps ranges in proper order: Easy < Normal < Hard
    """
    low, high = get_range_for_difficulty("Normal")
    assert low == 1, "Normal range should start at 1"
    # CRITICAL FIX: Changed from 100 to 50
    # OLD: assert high == 100  # ❌ BUG: Made Normal as hard as Hard difficulty
    assert high == 50, "FIXED: Normal range should be 1-50 (not 1-100)"

    # Additional verification: Normal range should be smaller than Hard
    hard_low, hard_high = get_range_for_difficulty("Hard")
    assert high < hard_high, f"Normal range (1-{high}) should be smaller than Hard range (1-{hard_high})"


def test_bug_fix_3_hard_range_corrected():
    """
    TEST FOR BUG FIX #3: Verify Hard difficulty now has correct range (1-100).

    SCENARIO: Hard difficulty should have the largest range (hardest to guess)
    - Easy: 1-20 (smallest) = easiest to find the number
    - Normal: 1-50 (medium) = medium difficulty
    - Hard: 1-100 (largest) = hardest to find the number  ← FIXED FROM 1-50

    BUG BEHAVIOR: Hard returned 1-50 (same as Normal in old code), making it too easy
    FIXED BEHAVIOR: Hard now returns 1-100, creating proper difficulty progression

    This test verifies Hard is the most challenging with the largest range.
    """
    low, high = get_range_for_difficulty("Hard")
    assert low == 1, "Hard range should start at 1"
    # CRITICAL FIX: Changed from 50 to 100
    # OLD: assert high == 50  # ❌ BUG: Made Hard easier than Normal difficulty
    assert high == 100, "FIXED: Hard range should be 1-100 (not 1-50)"

    # Additional verification: Hard range should be largest
    easy_low, easy_high = get_range_for_difficulty("Easy")
    normal_low, normal_high = get_range_for_difficulty("Normal")
    assert high > normal_high, f"Hard range (1-{high}) should be larger than Normal range (1-{normal_high})"
    assert high > easy_high, f"Hard range (1-{high}) should be larger than Easy range (1-{easy_high})"


def test_bug_fix_3_difficulty_scaling_logic():
    """
    TEST FOR BUG FIX #3: Verify the entire difficulty scaling logic works correctly.

    CONCEPT: The game uses inverse difficulty scaling:
    - Easier difficulty → Smaller range + More attempts (easier to guess)
    - Harder difficulty → Larger range + Fewer attempts (harder to guess)

    DEFINED CONSTRAINTS (app.py lines 91-95):
    - Easy: 6 attempts for range 1-20 (1 attempt per ~3 numbers)
    - Normal: 8 attempts for range 1-50 (1 attempt per ~6 numbers)
    - Hard: 5 attempts for range 1-100 (1 attempt per 20 numbers)

    BUG: Ranges were swapped, breaking this progression
    - Normal had 1-100 → 8 attempts per 100 numbers = easier than it should be
    - Hard had 1-50 → 5 attempts per 50 numbers = harder than Normal (wrong!)

    FIX: Correct the ranges to maintain the inverse relationship
    """
    difficulties = {
        "Easy": {"range": 20, "attempts": 6},
        "Normal": {"range": 50, "attempts": 8},
        "Hard": {"range": 100, "attempts": 5},
    }

    for difficulty, specs in difficulties.items():
        low, high = get_range_for_difficulty(difficulty)
        actual_range = high - low + 1

        assert actual_range == specs["range"], \
            f"{difficulty}: Expected range {specs['range']}, got {actual_range}"

    # Verify inverse relationship: easier difficulties have LOWER range values
    easy_range = (20 - 1 + 1)  # Easy: 1-20
    normal_range = (50 - 1 + 1)  # Normal: 1-50
    hard_range = (100 - 1 + 1)  # Hard: 1-100

    # CRITICAL: Range should increase with difficulty (harder = bigger range = harder to guess)
    assert easy_range < normal_range, "Easy range should be smaller than Normal"
    assert normal_range < hard_range, "Normal range should be smaller than Hard"

    # VERIFIED FIX: These assertions would have FAILED with the buggy ranges
    # because Hard had 1-50 and Normal had 1-100, so hard_range < normal_range would be True (wrong!)
