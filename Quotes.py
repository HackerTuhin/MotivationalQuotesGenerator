import streamlit as st
from autogen import ConversableAgent
import shutil
import os
from config import config

def delete_cache_folder():
    cache_path = ".cache"
    try:
        if os.path.exists(cache_path):
            shutil.rmtree(cache_path)
    except Exception as e:
        st.error(f"Error deleting cache folder: {e}")

# OpenAI Agent Config

# Initialize AI Agents with error handling
try:
    prompt_agent = ConversableAgent(
        name="PromptGenerator",
        llm_config=config,
        code_execution_config=False,
        human_input_mode="NEVER",
        description="Generates a well-structured prompt based on selected quote types.",
    )
    quote_agent = ConversableAgent(
        name="QuoteGenerator",
        llm_config=config,
        code_execution_config=False,
        human_input_mode="NEVER",
        description="Generates motivational quotes based on the given prompt.",
    )
except Exception as e:
    st.error(f"Error initializing AI agents: {e}")

# Function to create messages for the Prompt Generator Agent
def generate_prompt(quote_types):
    try:
        quote_types_str = ", ".join(quote_types)
        pmt = f"Generate an emotional creative prompt to generate a motivational quote about {quote_types_str}. Give me only the prompt."
        message = [{"role": "user", "content": [{"type": "text", "text": pmt}]}]
        response = prompt_agent.generate_reply(messages=message)
        if not response:
            raise ValueError("Empty response from prompt agent.")
        return response
    except Exception as e:
        st.error(f"Error generating prompt: {e}")
        return None

# Function to generate quotes
def generate_quotes(prompt):
    try:
        if not prompt:
            raise ValueError("Prompt is empty.")
        
        pmt = f'''You are an intelligent Quote generator. You can generate quote in English based on the given prompt.
        Also, you will give me a real-life example in easy words that will comply with the generated quotes. Below is the prompt.
        Prompt = {prompt}'''
        
        message = [{"role": "user", "content": [{"type": "text", "text": pmt}]}]
        response = quote_agent.generate_reply(messages=message)
        if not response:
            raise ValueError("Empty response from quote agent.")
        return response
    except Exception as e:
        st.error(f"Error generating quotes: {e}")
        return None

# Streamlit UI
def main():
    st.title("🌟 Motivational Quotes Generator")
    
    try:
        search_query = st.text_input("🔍 Search Quote Type:", "")
        
        # Define some sample quote options
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
    delete_cache_folder()
