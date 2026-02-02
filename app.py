import streamlit as st
import time

# --- 1. PAGE SETUP ---
st.set_page_config(page_title="Lost in Localization", page_icon="🎮")

# --- 2. THE VISUAL STYLE (CSS) ---
st.markdown("""
    <style>
    /* MAIN BACKGROUND: Deep Black */
    .stApp {
        background-color: #0e1117;
        font-family: 'Courier New', Courier, monospace;
    }

    /* HEADERS: Neon Green */
    h1, h2, h3 {
        color: #00ff00 !important;
        text-shadow: 0px 0px 5px #003300;
    }
    
    /* TEXT: Standard Console Text */
    p, label {
        color: #ccffcc;
        font-size: 16px;
    }

    /* --- THE "CORRUPTED" BOX --- */
    /* This targets the specific error box style */
    div[data-testid="stAlert"] {
        background-color: #220000 !important; /* Dark Red Background */
        border: 2px solid #ff0000 !important; /* Bright Red Border */
        color: #ffcccc !important;            /* Light Red Text */
        padding: 20px !important;
        border-radius: 5px;
        font-weight: bold;
        font-size: 18px !important;
    }
    /* Fix for the icon/text inside alert boxes */
    div[data-testid="stAlert"] > div {
        display: flex !important;
        align-items: center;
    }

    /* --- THE BUTTONS --- */
    div.stButton > button {
        background-color: #00ff00 !important; /* Neon Green */
        border: 2px solid #004400 !important;
        color: #000000 !important;            /* Black Text */
        font-weight: 800 !important;          /* Extra Bold */
        font-size: 18px !important;
        height: 60px !important;              /* FIXED HEIGHT */
        width: 100%;
        border-radius: 5px;
        transition: transform 0.1s;
    }
    
    /* FORCE TEXT COLOR INSIDE BUTTONS */
    div.stButton > button p {
        color: #000000 !important;
        font-size: 18px !important;
    }

    /* HOVER EFFECT */
    div.stButton > button:hover {
        background-color: #ffffff !important; /* White */
        border-color: #00ff00 !important;
        transform: scale(1.02);
    }
    div.stButton > button:hover p {
        color: #000000 !important;
    }

    /* --- CUSTOM RESULT BOX (The box that appears next to the button) --- */
    .result-box-success {
        background-color: #00ff00;
        color: black;
        font-weight: bold;
        padding: 10px;
        border-radius: 5px;
        text-align: center;
        height: 60px; /* MATCH BUTTON HEIGHT */
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 18px;
        border: 2px solid #004400;
    }
    .result-box-fail {
        background-color: #ff0000;
        color: white;
        font-weight: bold;
        padding: 10px;
        border-radius: 5px;
        text-align: center;
        height: 60px; /* MATCH BUTTON HEIGHT */
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 18px;
        border: 2px solid #550000;
    }

    </style>
    """, unsafe_allow_html=True)

# --- 3. THE DATA ---
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

# --- 4. GAME LOGIC ---
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'current_level' not in st.session_state:
    st.session_state.current_level = 0
if 'feedback' not in st.session_state:
    st.session_state.feedback = None  # To store "Success" or "Fail" state

# Header
st.title("LOST IN LOCALIZATION")
st.write("System Alert: Translation Database Corrupted.")
st.markdown("---")

# Main Game Loop
if st.session_state.current_level < len(levels):
    level_data = levels[st.session_state.current_level]
    
    st.subheader(f"CASE #{st.session_state.current_level + 1}")
    
    # The Corrupted String Display
    st.error(f'CORRUPTED STRING: "{level_data["glitch"]}"')
    
    st.write("Select the localized patch:")
    
    # Button Loop
    for i, option in enumerate(level_data['options']):
        # Create 2 Columns: Button (75%) | Result (25%)
        col1, col2 = st.columns([0.75, 0.25])
        
        with col1:
            # Unique key for every button
            btn = st.button(option, key=f"btn_{st.session_state.current_level}_{i}")
        
        if btn:
            if option == level_data['correct']:
                # Show success in the right column
                with col2:
                    st.markdown('<div class="result-box-success">✅ CORRECT</div>', unsafe_allow_html=True)
                time.sleep(1)
                st.session_state.score += 1
                st.session_state.current_level += 1
                st.rerun()
            else:
                # Show failure in the right column
                with col2:
                    st.markdown('<div class="result-box-fail">❌ FAILED</div>', unsafe_allow_html=True)
                time.sleep(1)
                st.session_state.current_level += 1
                st.rerun()

else:
    # --- END SCREEN ---
    st.title("JOB COMPLETE")
    st.markdown("---")
    
    # Calculate Rank
    if st.session_state.score == len(levels):
        rank = "MASTER LOCALIZER"
        color = "#00ff00"
        st.balloons()
    elif st.session_state.score >= 3:
        rank = "JUNIOR TRANSLATOR"
        color = "orange"
    else:
        rank = "GOOGLE TRANSLATE BOT"
        color = "red"

    st.markdown(f"""
    <div style="background-color: #111; padding: 20px; border: 2px solid {color}; text-align: center; border-radius: 10px;">
        <h2 style="color: {color} !important; margin: 0;">FINAL SCORE: {st.session_state.score} / {len(levels)}</h2>
        <h3 style="color: white !important; margin-top: 10px;">RANK: {rank}</h3>
    </div>
    """, unsafe_allow_html=True)
    
    st.write("")
    if st.button("REBOOT SYSTEM"):
        st.session_state.score = 0
        st.session_state.current_level = 0
        st.rerun()