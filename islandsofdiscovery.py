import streamlit as st
import random

# --- Initialize session state ---
if "initialized" not in st.session_state:
    st.session_state.islands = ["Island A", "Island B", "Island C", "Island D", "Island E"]
    st.session_state.correct_island = random.randint(0, 4)
    st.session_state.clues_found = [None] * 5
    st.session_state.excavated = [False] * 5
    st.session_state.turns = 5
    st.session_state.score = 0
    st.session_state.game_over = False
    st.session_state.message = "🌍 Welcome to Islands of Discovery!"
    st.session_state.action_taken = False
    st.session_state.initialized = True

# --- Game logic ---
def survey(island_index):
    distance = abs(island_index - st.session_state.correct_island)
    if distance == 0:
        clue = "🏺 Ruins markings"
    elif distance == 1:
        clue = "🔎 Pottery fragments"
    elif distance == 2:
        clue = "🦴 Ancient bones"
    else:
        clue = "🌊 Just shells"

    st.session_state.clues_found[island_index] = clue
    st.session_state.message = f"Survey at {st.session_state.islands[island_index]}: {clue}"
    st.session_state.turns -= 1
    st.session_state.action_taken = True
    check_end()

def excavate(island_index):
    if st.session_state.excavated[island_index]:
        st.session_state.message = f"You already excavated {st.session_state.islands[island_index]}."
        st.session_state.action_taken = True
        return

    st.session_state.excavated[island_index] = True

    if island_index == st.session_state.correct_island:
        st.session_state.score += 100
        st.session_state.message = f"🎉 You found the ancient ruins on {st.session_state.islands[island_index]}! 🏆 Final Score: {st.session_state.score}"
        st.session_state.game_over = True
    else:
        finds = [
            ("🪨 Broken pottery shard", 5),
            ("🪓 Old stone tool", 10),
            ("🦴 Animal bones", 3),
            ("🌱 Charcoal remains", 7),
            ("❌ Nothing significant", 0)
        ]
        find, points = random.choice(finds)
        st.session_state.score += points
        st.session_state.message = f"Excavation at {st.session_state.islands[island_index]}: {find} (+{points} points)"

    st.session_state.turns -= 1
    st.session_state.action_taken = True
    check_end()

def check_end():
    if st.session_state.turns <= 0 and not st.session_state.game_over:
        st.session_state.message += f"\n⏳ Out of time! The ruins remain undiscovered. Final Score: {st.session_state.score}"
        st.session_state.game_over = True

def reset_game():
    st.session_state.islands = ["Island A", "Island B", "Island C", "Island D", "Island E"]
    st.session_state.correct_island = random.randint(0, 4)
    st.session_state.clues_found = [None] * 5
    st.session_state.excavated = [False] * 5
    st.session_state.turns = 5
    st.session_state.score = 0
    st.session_state.game_over = False
    st.session_state.message = "🌍 New expedition started!"
    st.session_state.action_taken = False

def next_turn():
    st.session_state.message = "Choose your next action."
    st.session_state.action_taken = False

# --- UI ---
st.title("🏝️ Islands of Discovery")

st.sidebar.header("📊 Expedition Stats")
st.sidebar.write(f"⭐ Score: **{st.session_state.score}**")
st.sidebar.write(f"⏳ Turns Left: **{st.session_state.turns}**")
if st.sidebar.button("🔄 Restart Game"):
    reset_game()

# --- Info Dropdown ---
with st.expander("ℹ️ How to Play"):
    st.markdown("""
    **🎯 Goal:** Discover the hidden ruins before you run out of turns!  
    Each action uses **1 turn**, and you start with **5 turns**.

    **🔎 Survey:**  
    - Searches the surface for clues.  
    - Results may include:  
        - 🏺 **Ruins markings** → The correct island!  
        - 🔎 **Pottery fragments** → Very close.  
        - 🦴 **Ancient bones** → Activity nearby.  
        - 🌊 **Just shells** → Nothing nearby.

    **⛏️ Excavate:**  
    - Digs deeper on the chosen island.  
    - You might find valuable artifacts for points.  
    - Find the ruins → **100 points** and instant victory! 🏆
    """)

# --- Main Layout ---
st.info(st.session_state.message)

if not st.session_state.game_over:
    if not st.session_state.action_taken:
        island_choice = st.selectbox("🌴 Choose an island:", st.session_state.islands)
        island_index = st.session_state.islands.index(island_choice)
        action = st.radio("Select an action:", ["Survey", "Excavate"])
        st.button("✅ Confirm", on_click=survey if action == "Survey" else excavate, args=(island_index,))
    else:
        st.button("➡️ Next Turn", on_click=next_turn)
else:
    st.success("Game over! Try again for a better score.")

# --- Expedition Map ---
st.subheader("🗺️ Expedition Map")
for i, name in enumerate(st.session_state.islands):
    if st.session_state.excavated[i]:
        status = "⛏ Excavated"
    elif st.session_state.clues_found[i]:
        status = st.session_state.clues_found[i]
    else:
        status = "❓ Unknown"
    st.markdown(f"**{name}** → {status}")
