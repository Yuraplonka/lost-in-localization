import streamlit as st
import time

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Lost in Localization", page_icon="🎮")

# --- CUSTOM DESIGN ---
# I changed the CSS below to force the button text to be BLACK.
st.markdown("""
    <style>
    /* Main Background */
    .stApp {
        background-color: #0e1117;
        color: #00ff00;
        font-family: 'Courier New', Courier, monospace;
    }
    
    /* Buttons */
    div.stButton > button {
        color: #000000 !important; /* Force text to be BLACK */
        background-color: #00ff00 !important; /* Neon Green Background */
        border: 2px solid #004400;
        border-radius: 5px;
        font-weight: 900 !important; /* Extra Bold */
        font-size: 18px !important;
        padding: 10px;
        width: 100%;
        transition: all 0.3s ease;
    }
    
    /* Button Hover Effect (Optional: makes it white on hover) */
    div.stButton > button:hover {
        background-color: #ffffff !important;
        color: #000000 !important;
        border: 2px solid #00ff00;
    }

    /* Subheader/Mission text color */
    h3 {
        color: #00ff00 !important;
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
    
    # CHANGED "Ticket" to "Mission"
    st.subheader(f"Case #{st.session_state.current_level + 1}")
    
    # I added a larger font size for the glitch text so it stands out
    st.markdown(f"**CORRUPTED STRING:**") 
    st.error(f'"{level_data["glitch"]}"')
    
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
    st.markdown("---")
    st.write(f"Final QA Score: {st.session_state.score} / {len(levels)}")
    
    if st.session_state.score == len(levels):
        st.balloons()
        st.success("RANK: MASTER LOCALIZER")
    elif st.session_state.score >= 3:
        st.warning("RANK: JUNIOR TRANSLATOR")
    else:
        st.error("RANK: GOOGLE TRANSLATE BOT")
        
    if st.button("REBOOT SYSTEM"):
        st.session_state.score = 0
        st.session_state.current_level = 0
        st.rerun()