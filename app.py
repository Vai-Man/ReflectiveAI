import streamlit as st
import pickle
from utils.preprocessing import preprocess
#from textblob import TextBlob
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
import random
import nltk
nltk.download('stopwords')

with open('utils/best_model.pkl', 'rb') as f:
    model = pickle.load(f)

st.set_page_config(page_title='ReflectiveAI: Enhanced Mental Health Assistant', page_icon=':brain:', layout='wide')

if 'interaction_history' not in st.session_state:
    st.session_state.interaction_history = []

def app():
    st.title("ReflectAI: Your Enhanced Mental Health Assistant :brain:")
    st.write("Hi there! I am here to help you reflect on your thoughts and emotions. Remember, everything you share is private. 😃")

    st.markdown("""
    <div style="text-align: center; background-color: #f0f8ff; padding: 20px;">
        <p>Take a moment to reflect, and we'll provide support along the way.</p>
        <p style="font-style: italic; color: #555;">Built for Hack-To-The-Future Hackathon</p>
    </div>
    """, unsafe_allow_html=True)

    gratitude_input = st.text_area("What are you grateful for today?", height=100, placeholder="Think about something small or big that you are thankful for...")

    if gratitude_input:
        st.write("Thank you for sharing your gratitude. Here's your positive thought for the day!")
        st.write(f"🌟 {gratitude_input}")

    mood = st.slider("How are you feeling today?", 0, 10, 5)
    mood_message = "neutral"
    if mood <= 3:
        mood_message = "low"
    elif mood >= 8:
        mood_message = "high"
    
    st.write(f"Mood check-in: You feel {mood_message}.")

    input_text = st.text_area('Share your thoughts or feelings here:', height=100, placeholder="Start typing...")

    if not input_text:
        st.write("💬 Enter some thoughts to analyze.")

    if st.button('Analyze Text'):
        if not input_text.strip(): 
            st.warning("Please enter some text before analyzing.")
        else:
            with st.spinner('Analyzing your thoughts...'):

                processed_array = preprocess(input_text)
                prediction = model.predict(processed_array)[0]
                
                """
                sentiment = TextBlob(input_text).sentiment
                if sentiment.polarity > 0.1:
                    emotion = "Positive 😊"
                elif sentiment.polarity < -0.1:
                    emotion = "Negative 😞"
                else:
                    emotion = "Neutral 😐"
                
                st.write(f"Emotional Analysis: {emotion}")
                """
                
                if prediction == 'suicide':
                    st.markdown('<p style="color: #FF4C4C; font-size: 20px;">⚠️ This text might indicate self-harm. Please reach out to someone you trust or consult a mental health professional.</p>', unsafe_allow_html=True)
                    st.write("Helpful resources:")
                    st.write("[National Helpline](https://www.samhsa.gov/find-help/national-helpline) | [Mental Health Resources](https://www.mentalhealth.gov/)")
                elif prediction == 'non-suicide':
                    st.success("✅ Your text does not indicate any signs of self-harm.")
                    st.write("It’s wonderful that you’re reflecting on your thoughts! Consider talking to a friend or family member if you'd like to share more.")
                
                
                st.markdown("### Daily Affirmation")
                affirmation = "You are strong, capable, and deserving of happiness."
                if mood <= 3:
                    affirmation = "Every day is a fresh start. Take it one step at a time."
                elif mood >= 8:
                    affirmation = "Keep spreading your positivity! You’re an inspiration."

                quotes = [
                    "The only way to do great work is to love what you do. - Steve Jobs",
                    "You are never too old to set another goal or to dream a new dream. - C.S. Lewis",
                    "Believe you can and you're halfway there. - Theodore Roosevelt",
                    "The future belongs to those who believe in the beauty of their dreams. - Eleanor Roosevelt"
                ]
                # Mental Health Tip of the Day
                tips = {
                    'low': "Tip: Try taking a few deep breaths and focus on the present moment. Mindfulness can help calm your mind.",
                    'neutral': "Tip: Stay positive and active today. Small movements like stretching can improve your mood.",
                    'high': "Tip: Keep spreading positivity! Consider sharing a kind word or doing something nice for someone else today."
                }

                mental_health_tip = tips.get(mood_message, "Tip: Remember, it's okay to take breaks and recharge when needed.")
                st.markdown("### Mental Health Tip of the Day")
                st.write(f"💡 {mental_health_tip}")

                
                daily_quote = random.choice(quotes)
                st.markdown("### Daily Motivational Quote")
                st.write(f"🌟 {daily_quote}")

                
                st.write(f"🌱 {affirmation}")
                
                # Coping Mechanism Links
                st.markdown("#### Helpful Resources for Self-Care")
                st.write("• [Meditation Guide](https://www.headspace.com/meditation/meditation-for-beginners)")
                st.write("• [Breathing Exercises](https://www.healthline.com/health/breathing-exercise)")

                
                interaction_data = {
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'mood': mood,
                    'input_text': input_text,
                    'prediction': prediction,
                    'emotion': emotion,
                    'affirmation': affirmation,
                }
                st.session_state.interaction_history.append(interaction_data)
            
            
            st.markdown("### How accurate was the analysis?")
            feedback = st.radio("Please rate the prediction:", ('Very Accurate', 'Somewhat Accurate', 'Not Accurate'))

            if feedback:
                st.write(f"Thank you for your feedback: {feedback}")

                
                last_interaction = st.session_state.interaction_history[-1]
                last_interaction['feedback'] = feedback

    
    if input_text:
        st.markdown("### Journaling Prompt")
        st.write("Keep going! Reflect on something positive that happened recently or a small goal you’d like to achieve.")
    
    
    if st.session_state.interaction_history:
        st.markdown("### Your Previous Reflections")
        history_df = pd.DataFrame(st.session_state.interaction_history)
        st.write(history_df[['timestamp', 'mood', 'emotion', 'prediction', 'affirmation']])

if __name__ == '__main__':
    app()
