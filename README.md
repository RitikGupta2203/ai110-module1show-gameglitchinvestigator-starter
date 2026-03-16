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

- [ ] Describe the game's purpose.
According to my experience, the game's main purpose was to make us understand how we can collaborate with AI and improve our efficiency.
Though the AI requires some manual supervision but with deep details, proper prompting, AI can help us achieve the task much faster.It can help us understand the code base swiftly by summarising all details.

- [ ] Detail which bugs you found.
Bug 1: Backwards Hint Messages
When comparing guess to secret, the directional hints were inverted. If your guess was too low, it said "Go LOWER" instead of "Go HIGHER," and vice versa. This made the game unwinnable because players received opposite guidance.

Bug 2: Swapped Difficulty Ranges
The difficulty scaling was broken. Easy had 1-20 (correct), but Normal was set to 1-100 and Hard to 1-50, making Hard easier than Normal. The game uses inverse scaling (easier = smaller range + more attempts), so these ranges needed to be swapped: Normal should be 1-50 and Hard should be 1-100.

Bug 3: Broken "New Game" Reset
After winning a game, clicking "New Game" generated a new secret number but disabled the Submit button and didn't clear the history. The root cause: the status was never reset from "won" to "playing," so the game logic hit st.stop() and stopped rendering the page. Additionally, the history array and score were never cleared, causing old data to persist.

- [ ] Explain what fixes you applied.

Fix #1: 
Swapped Hint Messages
Reversed the directional hints in check_guess():

When guess > secret: Changed from "Go HIGHER!" to "Go LOWER!"
When guess < secret: Changed from "Go LOWER!" to "Go HIGHER!"
Applied in both the try and except (TypeError) blocks

Fix #2: 
Corrected Difficulty Ranges
Swapped Normal and Hard ranges in get_range_for_difficulty():

Normal: 
Changed from 1-100 → 1-50
Hard: Changed from 1-50 → 1-100
Easy stayed at 1-20 (correct)

Fix #3: 
Full Game State Reset on New Game (lines 145-160)
Modified the "New Game" button handler to reset all variables:

status: "won"/"lost" → "playing" (critical for button functionality)
history: Preserved old guesses → cleared []
attempts: Kept old count → reset to 1
secret: Generated with get_range_for_difficulty() instead of hardcoded random.randint(1, 100)
score: Carried from previous game → reset to 0



## 📸 Demo

- [ ] [Insert a screenshot of your fixed, winning game here]

Bug 1 Fixed: ![alt text](<Fixed Screenshots/Bug1.1.png>)
   ![alt text](<Fixed Screenshots/Bug1.2.png>)

Bug 2 Fixed:Easy: ![alt text](<Fixed Screenshots/Bug2.1.png>) 
   Normal: ![alt text](<Fixed Screenshots/Bug2.2.png>)
   Hard: ![alt text](<Fixed Screenshots/Bug2.3.png>)

Bug 3 Fixed:
Game WOn: ![alt text](<Fixed Screenshots/Bug3.1.png>)
New Game Reset: ![alt text](<Fixed Screenshots/Bug3.2.png>)



