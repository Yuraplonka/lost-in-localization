import streamlit as st
import time

# --- PAGE CONFIGURATION ---
# This sets the tab name in the browser
st.set_page_config(page_title="Lost in Localization", page_icon="🎮")

# --- CUSTOM DESIGN ---
st.markdown("""
    <style>
    .stApp {
        background-color: #0e1117;
        color: #00ff00;
        font-family: 'Courier New', Courier, monospace;
    }
    
    /* 1. BUTTON CONTAINER (The Box) */
    div.stButton > button {
        background-color: #00ff00 !important; /* Neon Green */
        border: 2px solid #004400 !important;
        width: 100%;
        transition: all 0.2s ease;
    }

    /* 2. BUTTON TEXT (The Words) - This fixes the bold issue */
    div.stButton > button p {
        color: #000000 !important;       /* Black Text */
        font-weight: 600 !important;     /* Max Bold */
        font-size: 18px !important;
    }

    /* 3. HOVER STATE (Mouse Over) */
    div.stButton > button:hover {
        background-color: #ffffff !important; /* Turns White */
        border-color: #00ff00 !important;
        transform: scale(1.02);
    }

    /* 4. HOVER TEXT - Ensures text stays black on white background */
    div.stButton > button:hover p {
        color: #000000 !important;
    }
    
    /* FIX ALERT BOXES (Correct/Failed) */
    div[data-testid="stAlert"] {
        height: 30px !important;         /* Fixed height to match buttons */
    }

    /* Force the text inside to center properly */
    div[data-testid="stAlert"] > div {
        height: 100% !important;
        display: flex !important;
        align-items: center !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- THE GAME DATA ---
levels = [
    {
        "glitch": "May the power accompany you.",
        "options": ["May the Force be with you.", "Hope you have strength.", "Let the energy stay close."],
        "correct": "May the Force be with you."
    },
    {
        "glitch": "It is myself, Mario!",
        "options": ["I am the one named Mario.", "It's a-me, Mario!", "Identity confirmed: Mario."],
        "correct": "It's a-me, Mario!"
    },
    {
        "glitch": "Must acquire the complete set.",
        "options": ["Gotta catch 'em all!", "Buy the whole collection.", "Secure all inventory."],
        "correct": "Gotta catch 'em all!"
    },
    {
        "glitch": "Why are you not smiling?",
        "options": ["Put on a happy face.", "Why so serious?", "Are you sad?"],
        "correct": "Why so serious?"
    },
     {
        "glitch": "End of the Game.",
        "options": ["Game Over.", "Match Finished.", "Stop Playing."],
        "correct": "Game Over."
    }
]

# --- GAME LOGIC ---
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'current_level' not in st.session_state:
    st.session_state.current_level = 0

# --- TITLE DISPLAY ---
st.title("LOST IN LOCALIZATION")
st.write("System Alert: Translation Database Corrupted.")

# Check if the game is still going
if st.session_state.current_level < len(levels):
    level_data = levels[st.session_state.current_level]
    
    st.subheader(f"Case #{st.session_state.current_level + 1}")
    st.error(f'CORRUPTED STRING: "{level_data["glitch"]}"')
    
    st.write("Select the correct localized patch:")
    
    # LOOP THROUGH OPTIONS
    for i, option in enumerate(level_data['options']):
        # Create two columns: Left for Button (0.7), Right for Result (0.3)
        col1, col2 = st.columns([0.7, 0.3])
        
        with col1:
            # We use 'key' to ensure every button is unique
            clicked = st.button(option, key=f"btn_{st.session_state.current_level}_{i}")
            
        if clicked:
            # If clicked, show the result in the RIGHT column (col2)
            with col2:
                if option == level_data['correct']:
                    st.success("✅ CORRECT")
                    time.sleep(1) # Let them see it for 1 second
                    st.session_state.score += 1
                    st.session_state.current_level += 1
                    st.rerun()
                else:
                    st.error("❌ FAILED")
                    time.sleep(1) # Let them see it for 1 second
                    st.session_state.current_level += 1
                    st.rerun()

else:
    # End of game screen
    st.title("JOB COMPLETE")
    st.write(f"Final Score: {st.session_state.score} / {len(levels)}")
    
    if st.session_state.score == len(levels):
        st.balloons()
        st.success("Rank: MASTER LOCALIZER")
    else:
        st.warning("Rank: JUNIOR TRANSLATOR")
        
    if st.button("REBOOT SYSTEM"):
        st.session_state.score = 0
        st.session_state.current_level = 0
        st.rerun()