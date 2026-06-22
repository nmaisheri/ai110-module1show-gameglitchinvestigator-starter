# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

The hint kept saying go higher, even though i was past the 100 mark.  When you click New Game to play again, nothing actually happens. The page stays the exact same. The hard difficulty is actually easier than normal. the info banner also hardcodes 1 and 100. attempts is initalized to 1 not 0, so the first render is off by 1.

**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
| 51  |    Go Lower hint        Go Higher! hint            
| New Game A new game would start Nothing happend
| 400       Too High" hint        go higher hint shown

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

I decided to use Claude Sonnet 4.6 for this project. One AI suggestion that was correct was the two main problems that were found in the game. The AI was able to correctly identify that the hint messages in check_guess are inverted, where if a number is too high it will say go lower and vice versa. I verfied this by looking at the code myself, and also noticing the error when I first tried debugging the code without the help of an AI. However, while reading the output that the AI gave me, I did not notice any AI suggestiosn that were incorrect or misleading.
---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?


To decide whether a bug was really fixed or not, I decided to test the game myself to see if the errors were still occuring or not. I used the same inputs as before, and I also tested with new inputs and edge cases to see if they were working. For example, when I first noticed an issue, I had typed 400 and expceted the game to give a hint that sas Go Lower, but instead, it said go Higher. After the AI had made the changes, I typed in 400 again and this time, the game had correctly said Go Lower. AI helped me find edge cases to test, and using those edge cases combined with some of my own, I was able to thoughly test the game glitch investigator.
---

## 4. What did you learn about Streamlit and state?

- Everytime a user interacts with a Streamlit app, such as clicking a button or moving a slider, Streamlit reruns the entire python script from scratch. This means that all regular variables reset to their initial values. A special directory called st.session-state survives these reruns, which allows you to persist values liek counters or user choices across ineractions. For example, this was used to save the difficulty setting across sessions.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.

One habit that I want to resuye in future projects is seperates myt chats with AI for different tasks, as this reduces token usage and keep all code and messages clean and easy to parse through in the future. I used to have all my chats in the exact same message. 
One this I want to do differently is better word my prompts to be better suited for the task that I am giving the AI. Oftentimes, I was not explaining what I needed the AI to do properly, and this caused some issues and and led to me wasting more token to better word my messages.
This project changed the way I think about AI generated code becuase it thaught me how powerful the tool really is. Nowdays, AI can do pretty much everything, but it still has limitations. Without proper guidance and observation, the AI will fail and produce wrong code, but if done correctly, makes everyones days much easier and more productive.