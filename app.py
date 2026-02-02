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
    div.stButton > button {
        color: #0e1117;
        background-color: #00ff00;
        border: 2px solid #004400;
        width: 100%;
        font-weight: bold;
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
st.markdown("---")

# Check if the game is still going
if st.session_state.current_level < len(levels):
    level_data = levels[st.session_state.current_level]
    
    st.subheader(f"Ticket #{st.session_state.current_level + 1}")
    st.error(f'CORRUPTED STRING: "{level_data["glitch"]}"')
    
    st.write("Select the correct localized patch:")
    
    for option in level_data['options']:
        if st.button(option):
            if option == level_data['correct']:
                st.success("✅ PATCH SUCCESSFUL!")
                time.sleep(1)
                st.session_state.score += 1
                st.session_state.current_level += 1
                st.rerun()
            else:
                st.error("❌ PATCH FAILED.")
                time.sleep(1)
                st.session_state.current_level += 1
                st.rerun()

else:
    # End of game screen
    st.title("JOB COMPLETE")
    st.write(f"Final QA Score: {st.session_state.score} / {len(levels)}")
    
    if st.session_state.score == len(levels):
        st.balloons()
        st.success("Rank: MASTER LOCALIZER")
    else:
        st.warning("Rank: JUNIOR TRANSLATOR")
        
    if st.button("REBOOT SYSTEM"):
        st.session_state.score = 0
        st.session_state.current_level = 0
        st.rerun()