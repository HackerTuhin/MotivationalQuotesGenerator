import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()

def call_openrouter(messages, system_prompt="", max_tokens=2000):
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key or not api_key.strip():
        return "💌 Please set your OPENROUTER_API_KEY in the .env file!"

    headers = {
        "Authorization": f"Bearer {api_key.strip()}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://motivational-quotes.streamlit.app",
        "X-Title": "Motivational Quotes Generator"
    }
    payload = {
        "model": "nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free",
        "messages": [{"role": "system", "content": system_prompt}] + messages if system_prompt else messages,
        "max_tokens": max_tokens,
        "temperature": 0.9
    }

    try:
        resp = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=60
        )
        print("API Response status:", resp.status_code)
        data = resp.json()
        print("API Response:", data)
        if "choices" in data:
            msg = data["choices"][0]["message"]
            content = msg.get("content") or ""
            return content.strip() or "Something went wrong — please try again!"
        elif "error" in data:
            return f"💔 Error: {data['error'].get('message', 'Something went wrong. Check your API key.')}"
        return "Something went wrong — please try again!"
    except requests.exceptions.Timeout:
        return "💌 The stars are busy... please try again in a moment!"
    except Exception as e:
        print("Exception:", str(e))
        return f"🌸 Oops! ({str(e)}) — try again?"

def generate_prompt(quote_types):
    quote_types_str = ", ".join(quote_types)
    pmt = f"Generate an emotional creative prompt to generate a motivational quote about {quote_types_str}. Give me only the prompt."
    messages = [{"role": "user", "content": pmt}]
    return call_openrouter(messages)

def generate_quotes(prompt):
    pmt = f'''You are an intelligent Quote generator. You can generate quote in English based on the given prompt.
    Also, you will give me a real-life example in easy words that will comply with the generated quotes. Below is the prompt.
    Prompt = {prompt}'''
    messages = [{"role": "user", "content": pmt}]
    return call_openrouter(messages, max_tokens=1000)

def main():
    st.title("🌟 Motivational Quotes Generator")
    
    try:
        search_query = st.text_input("🔍 Search Quote Type:", "")
        
        quote_options = {
            "Life": "🌿", "Love": "❤️", "Sorrow": "😢", "Pain": "💔", "Trust": "🤝", "Happiness": "😊",
            "Success": "🏆", "Friendship": "👬", "Courage": "🦁", "Hope": "🌟", "Wisdom": "🧠",
            "Perseverance": "🏋️", "Faith": "🙏", "Kindness": "💖", "Self-Confidence": "💪",
            "Dreams": "💭", "Hard Work": "⚒️", "Overcoming Failure": "🔄", "Patience": "⏳",
            "Strength": "🏋️‍♂️", "Motivation": "🚀", "Leadership": "👑", "Gratitude": "🙌",
            "Humility": "🕊️", "Compassion": "🤗", "Inspiration": "💡", "Resilience": "🌱",
            "Determination": "🔥", "Self-Love": "💙", "Forgiveness": "🤲", "Mindfulness": "🧘",
            "Positivity": "✨", "Creativity": "🎨", "Change": "🔄", "Empathy": "💞",
            "Growth": "📈", "Peace": "☮️", "Destiny": "🔮", "Freedom": "🕊️", "Power": "⚡",
            "Respect": "🙏", "Balance": "⚖️", "Self-Discovery": "🔍", "Adventure": "🏕️",
            "Ambition": "🏁", "Hustle": "🏃", "Discipline": "📅", "Health": "🍏",
            "Wealth": "💰", "Relationships": "💑", "Spirituality": "🛐", "Education": "📚",
            "Technology": "💻", "Science": "🔬", "Innovation": "🚀", "Artificial Intelligence": "🤖",
            "Networking": "🔗", "Negotiation": "💬", "Risk-Taking": "🎲", "Meditation": "🧘‍♂️",
            "Self-Growth": "🌱", "Generosity": "🎁", "Karma": "⚖️", "Patriotism": "🇮🇳", 
            "Loyalty": "🔒", "Honesty": "🛡️", "Ethics": "⚖️", "Justice": "⚖️", "Entrepreneurship": "💼",
            "Startups": "🚀", "Teamwork": "🤝", "Collaboration": "🔄", "Strategy": "📊",
            "Marketing": "📢", "Finance": "💰", "Investment": "📈", "Stock Market": "📊",
            "Cryptocurrency": "₿", "Time Management": "⏳", "Productivity": "🚀",
            "Mindset": "🧠", "Psychology": "🧠", "Philosophy": "📜", "History": "📖",
            "Universe": "🌌", "Space Exploration": "🚀", "Astronomy": "🔭","Effort" :"💪", 
            "Mathematics": "➗", "Physics": "⚛️", "Biology": "🧬", "Chemistry": "🧪",
            "Environmentalism": "🌱", "Sustainability": "♻️", "Veganism": "🥗",
            "Mind-Body Connection": "🧘", "Hiking": "🥾", "Travel": "✈️", "Photography": "📸",
            "Art": "🎨", "Music": "🎵", "Dance": "💃", "Writing": "📝", "Poetry": "📖",
            "Storytelling": "📖", "Journalism": "📰", "Filmmaking": "🎥", "Gaming": "🎮", 

            "Self-Doubt": "😞", "Breakup": "💔", "Heartbreak": "💔", "Darkness": "🌑",
            "Loneliness": "😔", "Fear": "😨", "Anxiety": "😰", "Depression": "😞",
            "Sadness": "😢", "Regret": "😣", "Betrayal": "🔪", "Failure": "💀",
            "Frustration": "😡", "Hopelessness": "😓", "Toxicity": "☠️", "Loss": "🕊️",
            "Anger": "🔥", "Revenge": "⚔️", "Guilt": "😔", "Suffering": "😖",
            "Jealousy": "🖤", "Insecurity": "😟", "Resentment": "😠", "Isolation": "🚪",
            "Doubt": "🤔", "Emptiness": "🕳️", "Grief": "🖤", "Despair": "💀",
            "Negativity": "⚫", "Misery": "😩", "Tears": "😭", "Destruction": "🔥",
            "Addiction": "🍷", "Paranoia": "😰", "Nightmares": "👁️‍🗨️", "Abandonment": "🚶‍♂️",
            "Manipulation": "🎭", "Gaslighting": "🌀", "Bullying": "💢", "Hatred": "🖤",
            "Obsession": "🔗", "Hopeless Love": "💔", "Suicidal Thoughts": "⚰️",
            "Mental Breakdown": "🤯", "Desperation": "😵‍💫", "Madness": "🌀",
            "Regretful Actions": "😞", "Crying Alone": "😭", "Tragedy": "⚰️",
            "Doom": "💀", "Fear of the Future": "⏳", "Fading Away": "🌫️",
            "Lies & Deception": "🎭", "Toxic Love": "☠️❤️", "Chronic Pain": "🩸",
            "Worthlessness": "😞", "Existential Crisis": "🌌💀", "Dead Inside": "🖤",
            "Broken Promises": "📜💔", "Manipulated Emotions": "🔄😢",
            "Abuse": "🚫", "Tears in Silence": "🤐😭", "Lonely Nights": "🌃💔",
            "Fear of Failure": "⚠️", "Hiding Pain": "😶💔"
        }
        
        filtered_quote_options = {key: value for key, value in quote_options.items() if search_query.lower() in key.lower()}
        
        st.subheader("Select Types of Quotes:")
        num_cols = 5
        quote_list = list(filtered_quote_options.items())
        
        cols = st.columns(num_cols)
        selected_quotes = []
        for index, (quote, icon) in enumerate(quote_list):
            col = cols[index % num_cols]
            if col.checkbox(f"{icon} {quote}"):
                selected_quotes.append(quote)
        
        if st.button("Generate Quotes"):
            if not selected_quotes:
                st.error("⚠️ Please select at least one quote type.")
                return
            
            with st.spinner("Generating prompt..."):
                prompt = generate_prompt(selected_quotes)
                if not prompt:
                    return
                st.write(f"**Generated Prompt:** {prompt}")
            
            with st.spinner("Generating quotes..."):
                quotes = generate_quotes(prompt)
                if not quotes:
                    return
            
            st.subheader("💬 Generated Motivational Quotes:")
            st.write(quotes)
    
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
