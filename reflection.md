# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the secret number kept changing" or "the hints were backwards").

1. the hints were backwards. As noted, if my secret number was 40 and guessed number was 20. the hint section displayed "go lower"  
  Ideal Behaviour: The ideal hint in that case should be "go higher" as the guessed number was smaller than the secret.
  Screenshot: ![alt text](Bugs/Bug1.png)

2. once we win the game, the new game Button gives the new secret number but submit guess button doesn't work and the array having all the previous game values doesn't reset to start from beginning.  
  Ideal Behaviour: 
  1. When a user starts a new game after winning the game, 1.the list should reset and start the attempts from 0.
  2. The submit guess button should work accordingly.
  Screenshot: 1.Game Won: ![alt text](Bugs/Bug2.1.png) 
              2.New Game:![alt text](Bugs/Bug2.2.png)


3. The different level are marked as differently like Easy : 1 -20, Normal: 1-100 and Hard: 1 - 50. which is not accurate.
  Ideal Behaviour: it should be Easy- 1-20 (6 attempts), Normal 1-50 (8 attempts), Hard 1-100 (5 attempts)
  Screenshot: 1. Easy: ![alt text](Bugs/Bug3.1.png) 
              2. Normal: ![alt text](Bugs/Bug3.2.png) 
              3.Hard: ![alt text](Bugs/Bug3.3.png)
---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

---

## 4. What did you learn about Streamlit and state?

- In your own words, explain why the secret number kept changing in the original app.
- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
- What change did you make that finally gave the game a stable secret number?

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.


