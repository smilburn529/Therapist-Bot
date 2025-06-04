# Botline Bling 🪩

Botline Bling is a simple web app where you can chat with an AI therapist in a calm, supportive environment. It’s designed for anyone who wants a safe place to talk, reflect, and feel heard: anytime, anywhere.

# [Demo Video!](https://www.youtube.com/watch?v=wjhCqigRCSs)

# What This App Does:
- You can sign up or log in with a username and password.
- Once logged in, you can chat with the AI therapist.
- The AI is designed to be kind and supportive, not judgemental. It does not diagnose.
- The app remembers your previous conversations and shows them when you come back.
- If your chat gets really long, it summarizes older messages. That way, the AI can still respond thoughtfully but efficiently.
- It starts each session with a Zen quote to set a peaceful mood.

# Why We Made This
A lot of people struggle to access therapy, whether it's due to cost, time, or stigma. Botline Bling is not meant to replace therapy, but it offers a private, easy way to get emotional support or talk things through when you need it.

# How To Use It
1. Download the code from this Github repo.
2. Open a terminal and go into the folder.
3. Run pip install -r requirements.txt
4. Add a file called .env in your folder and paste in your AWS access keys as follows:
     AWS_ACCESS_KEY_ID=your_key
     AWS_SECRET_ACCESS_KEY=your_secret
5. Then, just run streamlit run app.py in your terminal.

# What's Happening Behind The Scenes
- We used Streamlit to build the user interface.
- When you talk to the AI, it uses Claude 3 Sonnet, a language model from Anthropic, via AWS Bedrock.
- We use a SQLite database to store chat messages and user accounts.
- Passwords are safely encrypted using bcrypt.
- If your chat history gets too long, we call the LLM to summarize earlier parts so the app stays fast and efficient.

# What We'd Add With More Time
- Letting users name or customize their AI therapist.
- Mood tracking or charts that showcase an individuals emotional state over time.

# Created By
Roee Morag
Steve Milburn
