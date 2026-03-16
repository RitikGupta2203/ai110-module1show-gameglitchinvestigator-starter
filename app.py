import random
import streamlit as st

#FIX: Collaboration with AI:
# gave AI proper prompt to understand the logic of the code.
# Used claude AI to accurately refactor the code  and generate test cases that test the code.
# Manually, verified the code if it solves the bug

# BUG FIX #3: Fixed swapped difficulty ranges
# ISSUE: Normal (1-100) and Hard (1-50) ranges were inverted
# This broke the difficulty scaling logic where easier levels have smaller ranges + more attempts
# SOLUTION: Swap the return values for Normal and Hard to match intended difficulty
def get_range_for_difficulty(difficulty: str):
    if difficulty == "Easy":
        return 1, 20  # ✓ Easy: 1-20 range, 6 attempts
    if difficulty == "Normal":
        return 1, 50  # ✓ Normal: 1-50 range, 8 attempts
    if difficulty == "Hard":
        return 1, 100  # ✓ Hard: 1-100 range, 5 attempts
    return 1, 100


def parse_guess(raw: str):
    if raw is None:
        return False, None, "Enter a guess."

    if raw == "":
        return False, None, "Enter a guess."

    try:
        if "." in raw:
            value = int(float(raw))
        else:
            value = int(raw)
    except Exception:
        return False, None, "That is not a number."

    return True, value, None

#FIX: Collaboration with AI:
# gave AI proper prompt to understand the logic of the code.
#Used claude AI to accurately refactor the code generate test cases that test the code.
# Manually, verified the code if it solves the bug  
def check_guess(guess, secret):
    if guess == secret:
        return "Win", "🎉 Correct!"

    try:
        # FIXED: Bug #1 - Hint logic was backwards. When guess > secret, user should go LOWER (not higher)
        # and when guess < secret, user should go HIGHER (not lower)
        # Original code had inverted messages which confused players with incorrect guidance
        if guess > secret:
            # OLD: return "Too High", "📈 Go HIGHER!"  # INCORRECT: said go higher when already too high
            return "Too High", "📉 Go LOWER!"  # CORRECT: guide user to guess lower
        else:
            # OLD: return "Too Low", "📉 Go LOWER!"  # INCORRECT: said go lower when already too low
            return "Too Low", "📈 Go HIGHER!"  # CORRECT: guide user to guess higher
    except TypeError:
        # BUG FIX #1b: TypeError path had string comparison bug
        # ISSUE: When secret is string and guess is int, string comparison is lexicographic not numeric
        # Example: "10" < "8" as strings (because "1" < "8"), but 10 > 8 as numbers
        # SOLUTION: Convert both to int before comparing
        try:
            guess_num = int(guess)
            secret_num = int(secret)
            if guess_num == secret_num:
                return "Win", "🎉 Correct!"
            if guess_num > secret_num:
                # OLD: return "Too High", "📈 Go HIGHER!"  # INCORRECT: said go higher when already too high
                return "Too High", "📉 Go LOWER!"  # CORRECT: guide user to guess lower
            # OLD: return "Too Low", "📉 Go LOWER!"  # INCORRECT: said go lower when already too low
            return "Too Low", "📈 Go HIGHER!"  # CORRECT: guide user to guess higher
        except (ValueError, TypeError):
            # Fallback for non-numeric string comparison (original behavior)
            g = str(guess)
            if g == secret:
                return "Win", "🎉 Correct!"
            if g > secret:
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

st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")

st.title("🎮 Game Glitch Investigator")
st.caption("An AI-generated guessing game. Something is off.")

st.sidebar.header("Settings")

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1,
)

attempt_limit_map = {
    "Easy": 6,
    "Normal": 8,
    "Hard": 5,
}
attempt_limit = attempt_limit_map[difficulty]

low, high = get_range_for_difficulty(difficulty)

st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")

if "secret" not in st.session_state:
    st.session_state.secret = random.randint(low, high)

if "attempts" not in st.session_state:
    st.session_state.attempts = 1

if "score" not in st.session_state:
    st.session_state.score = 0

if "status" not in st.session_state:
    st.session_state.status = "playing"

if "history" not in st.session_state:
    st.session_state.history = []

st.subheader("Make a guess")

st.info(
    f"Guess a number between 1 and 100. "
    f"Attempts left: {attempt_limit - st.session_state.attempts}"
)

with st.expander("Developer Debug Info"):
    st.write("Secret:", st.session_state.secret)
    st.write("Attempts:", st.session_state.attempts)
    st.write("Score:", st.session_state.score)
    st.write("Difficulty:", difficulty)
    st.write("History:", st.session_state.history)

raw_guess = st.text_input(
    "Enter your guess:",
    key=f"guess_input_{difficulty}"
)

col1, col2, col3 = st.columns(3)
with col1:
    submit = st.button("Submit Guess 🚀")
with col2:
    new_game = st.button("New Game 🔁")
with col3:
    show_hint = st.checkbox("Show hint", value=True)


#FIX: Collaboration with AI:
# gave AI proper prompt to understand the logic of the code.
#Used claude AI to accurately refactor the code generate test cases that test the code.
# Manually, verified the code if it solves the bug  


# BUG FIX : Reset all game state when "New Game" is clicked
# ISSUE: Previous code only reset attempts and secret, but did not reset status or history.
# This caused the app to stay in "won"/"lost" status and hit st.stop() below, breaking the submit button.
# SOLUTION: Reset all session state variables to initial values to allow new game to play properly.
if new_game:
    # Reset status from "won" or "lost" back to "playing" so the game continues
    st.session_state.status = "playing"
    # Clear guess history to start fresh game without previous guesses
    st.session_state.history = []
    # Reset attempts to 1 (matches initialization on line 97)
    st.session_state.attempts = 1
    # Generate new secret number for the new game using correct difficulty range
    # FIXED: Changed from hardcoded random.randint(1, 100) to use get_range_for_difficulty()
    # OLD: st.session_state.secret = random.randint(1, 100)  # ❌ Always used 1-100, ignored difficulty
    new_low, new_high = get_range_for_difficulty(difficulty)
    st.session_state.secret = random.randint(new_low, new_high)  # ✓ Uses correct range for current difficulty
    # Reset score to 0 for new game
    st.session_state.score = 0
    st.success("New game started.")
    st.rerun()

if st.session_state.status != "playing":
    if st.session_state.status == "won":
        st.success("You already won. Start a new game to play again.")
    else:
        st.error("Game over. Start a new game to try again.")
    st.stop()

if submit:
    st.session_state.attempts += 1

    ok, guess_int, err = parse_guess(raw_guess)

    if not ok:
        st.session_state.history.append(raw_guess)
        st.error(err)
    else:
        st.session_state.history.append(guess_int)

        if st.session_state.attempts % 2 == 0:
            secret = str(st.session_state.secret)
        else:
            secret = st.session_state.secret

        outcome, message = check_guess(guess_int, secret)

        if show_hint:
            st.warning(message)

        st.session_state.score = update_score(
            current_score=st.session_state.score,
            outcome=outcome,
            attempt_number=st.session_state.attempts,
        )

        if outcome == "Win":
            st.balloons()
            st.session_state.status = "won"
            st.success(
                f"You won! The secret was {st.session_state.secret}. "
                f"Final score: {st.session_state.score}"
            )
        else:
            if st.session_state.attempts >= attempt_limit:
                st.session_state.status = "lost"
                st.error(
                    f"Out of attempts! "
                    f"The secret was {st.session_state.secret}. "
                    f"Score: {st.session_state.score}"
                )

st.divider()
st.caption("Built by an AI that claims this code is production-ready.")
