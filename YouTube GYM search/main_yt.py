import streamlit as st
from googleapiclient.discovery import build
from groq import Groq
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# API Keys
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Initialize clients
youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
groq_client = Groq(api_key=GROQ_API_KEY)

def get_recommendations(keyword):
    try:
        # Add "gym" to the search keyword to get gym-related videos
        gym_keyword = f"gym {keyword}"
        
        # Search for videos using YouTube API
        search_response = youtube.search().list(
            q=gym_keyword,
            part='snippet',
            type='video',
            maxResults=5,
            relevanceLanguage='en',
            safeSearch='moderate'
        ).execute()

        recommendations = []
        for item in search_response.get('items', []):
            if len(recommendations) >= 5:
                break
                
            video_id = item['id']['videoId']
            title = item['snippet']['title']
            
            if len(video_id) == 11:  # Validate video ID length
                recommendations.append({
                    'title': title,
                    'video_id': video_id
                })

        return recommendations

    except Exception as e:
        st.error(f"Error generating recommendations: {str(e)}")
        return []

def main():
    st.set_page_config(page_title="Gym Video Recommender", page_icon="💪")
    
    # Custom CSS for background and styling
    st.markdown("""
    <style>
    .stApp {
        background-image: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)), url("https://images.unsplash.com/photo-1534438327276-14e5300c3a48?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80");
        background-size: cover;
        background-position: center;
    }
    .title {
        color: white !important;
    }
    .subtitle {
        color: #f0f0f0 !important;
    }
    /* Override Streamlit's default text colors */
    p, div, label, .stTextInput > label, .stButton, .css-1lsmgbg, .css-16idsys p, 
    .stAlert > div, .stMarkdown, .stText, .stCaption {
        color: white !important;
    }
    
    /* Change the background color of the text input to dark and text to white */
    .stTextInput > div > div > input {
        background-color: rgba(0, 0, 0, 0.5) !important;
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.5) !important;
    }
    
    /* Focus state for input */
    .stTextInput > div > div > input:focus {
        border-color: #FFD700 !important;
        box-shadow: 0 0 0 0.2rem rgba(255, 215, 0, 0.25) !important;
    }
    
    /* Make captions specifically brighter and italic */
    .stCaption {
        font-style: italic !important;
        font-weight: 500 !important;
        font-size: 1.05rem !important;
        color: #FFD700 !important; /* Gold color for better visibility */
        opacity: 0.9 !important;
    }
    
    /* Placeholder text color */
    ::placeholder {
        color: rgba(255, 255, 255, 0.7) !important;
        opacity: 1 !important;
    }
    
    /* Make warning/error messages visible */
    .stAlert {
        background-color: rgba(255, 255, 255, 0.2) !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<h1 class="title">Gym Video Recommender 💪</h1>', unsafe_allow_html=True)
    st.markdown('<h3 class="subtitle">Find the best fitness videos for your workout</h3>', unsafe_allow_html=True)
    
    # User input with description - using markdown instead of caption for better visibility
    st.markdown("**🔍 Search for workout routines, exercises, or fitness tips:**")
    keyword = st.text_input("Enter a topic or keyword:", placeholder="e.g., beginner workout, abs, weightlifting")
    
    if st.button("Get Recommendations", type="primary"):
        if keyword:
            with st.spinner("🔍 Searching for the best gym videos..."):
                recommendations = get_recommendations(keyword)
                
                if recommendations:
                    for i, video in enumerate(recommendations, 1):
                        if video.get('video_id'):
                            video_id = video['video_id']
                            # Create embedded video player
                            st.write(f"### {i}. {video['title']}")
                            st.video(f"https://youtu.be/{video_id}")
                            
                            # Add direct link below video
                            st.markdown(f"[▶️ Watch on YouTube](https://youtu.be/{video_id})")
                            st.divider()
                else:
                    st.error("No recommendations found. Please try a different keyword.")
        else:
            st.warning("⚠️ Please enter a keyword")

if __name__ == "__main__":
    main()