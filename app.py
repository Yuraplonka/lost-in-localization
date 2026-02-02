import streamlit as st
import time
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# --- PAGE CONFIGURATION ---
# This sets the tab name in the browser
st.set_page_config(page_title="Lost in Localization", page_icon="🎮")

# --- GOOGLE SHEETS SETUP ---
SCOPE = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

def get_google_sheet():
    """Connects to Google Sheets using Streamlit Secrets."""
    try:
        # Load credentials from Streamlit Secrets
        creds_dict = dict(st.secrets["gcp_service_account"])
        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, SCOPE)
        client = gspread.authorize(creds)
        
        # OPEN THE SHEET BY NAME - CHANGE THIS TO YOUR EXACT SHEET NAME
        sheet = client.open("Localization Leaderboard").sheet1
        return sheet
    except Exception as e:
        st.error(f"Database Error: {e}")
        return None

def save_score(name, score):
    """Appends a row to Google Sheets ONLY if a name is provided."""
    # If name is empty or just spaces, DO NOT SAVE.
    if not name or name.strip() == "":
        return 
        
    sheet = get_google_sheet()
    if sheet:
        sheet.append_row([name, score])

def get_top_scores():
    """Reads all records from Google Sheets and sorts them."""
    sheet = get_google_sheet()
    if not sheet:
        return []

    try:
        # Get all records
        data = sheet.get_all_records()
        
        # Sort by Score (assuming column name is 'Score')
        # We use a safe sort just in case of bad data
        sorted_data = sorted(data, key=lambda x: int(x['Score']) if str(x['Score']).isdigit() else 0, reverse=True)
        return sorted_data[:10]
    except:
        return []

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
        height: 40px !important;         /* Fixed height to match buttons */
    }

    /* Force the text inside to center properly */
    div[data-testid="stAlert"] > div {
        height: 100% !important;
        display: flex !important;
        align-items: center !important;
    }
    
    /* HIDE 'Press Enter to apply' */
    div[data-testid="InputInstructions"] > span:nth-child(1) {
        visibility: hidden;
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
        "glitch": "Slumber is prohibited. Entities are in proximity.",
        "options": ["Sleeping is not allowed in here.", "Enemies are too close to bed to lay down.", "You may not rest now, there are monsters nearby."],
        "correct": "You may not rest now, there are monsters nearby."
    }
]

# --- GAME LOGIC ---
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'current_level' not in st.session_state:
    st.session_state.current_level = 0
if 'game_over' not in st.session_state:
    st.session_state.game_over = False
if 'player_name' not in st.session_state:
    st.session_state.player_name = ""

# --- TITLE DISPLAY ---
st.title("LOST IN LOCALIZATION")
st.write("System Alert: Translation Database Corrupted.")
st.markdown("<br>", unsafe_allow_html=True)

# --- ASK FOR NAME (Only at start) ---
if st.session_state.current_level == 0 and not st.session_state.game_over:
    st.session_state.player_name = st.text_input("ENTER AGENT NAME (Optional):", 
                                                 value=st.session_state.player_name, 
                                                 placeholder="Type your name here...")
    st.markdown("<br>", unsafe_allow_html=True)
    
# Check if the game is still going
if st.session_state.current_level < len(levels):
    level_data = levels[st.session_state.current_level]
    
    st.subheader(f"Case #{st.session_state.current_level + 1}")
    st.error(f'CORRUPTED STRING: "{level_data["glitch"]}"')
    
    st.write("Select the correct localized patch:")
    
    # LOOP THROUGH OPTIONS
    for i, option in enumerate(level_data['options']):
        # Create two columns: Left for Button (0.7), Right for Result (0.3)
        col1, col2 = st.columns([0.8, 0.2])
        
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
    st.title("JOB COMPLETE")
    st.write(f"Final Score: {st.session_state.score} / {len(levels)}")
    
    # SAVE SCORE TO GOOGLE SHEETS
    if not st.session_state.game_over:
        save_score(st.session_state.player_name, st.session_state.score)
        st.session_state.game_over = True
    
    # --- RANK LOGIC ---
    rank_titles = [
        "CORRUPTED SAVE FILE",       # Score 0
        "GOOGLE TRANSLATE BOT",      # Score 1
        "AUTO-CORRECT VICTIM",       # Score 2
        "JUNIOR TRANSLATOR",         # Score 3
        "SENIOR EDITOR",             # Score 4
        "MASTER LOCALIZER"           # Score 5
    ]
    
    # Get Rank safely
    final_rank = rank_titles[st.session_state.score] if st.session_state.score < len(rank_titles) else rank_titles[-1]

    # Display Rank with Colors
    if st.session_state.score == 5:
        st.balloons()
        st.success(f"RANK: {final_rank}")
    elif st.session_state.score >= 3:
        st.warning(f"RANK: {final_rank}")
    else:
        st.snow()
        st.error(f"RANK: {final_rank}")

    st.subheader("🏆 GLOBAL LEADERBOARD")
    
    # LOAD SCORES FROM GOOGLE SHEETS
    top_scores = get_top_scores()
    
    if top_scores:
        for rank, agent in enumerate(top_scores):
            st.write(f"**#{rank + 1} {agent['Player']}** - {agent['Score']} pts")
    else:
        st.write("Connecting to Global Database...")
        
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("REBOOT SYSTEM"):
        st.session_state.score = 0
        st.session_state.current_level = 0
        st.session_state.game_over = False
        st.session_state.player_name = "" 
        st.rerun()