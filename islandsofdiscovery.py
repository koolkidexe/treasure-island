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
    st.session_state.selected_island = None
    st.session_state.action_taken = False
    st.session_state.revealed_coords = False
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
    st.session_state.selected_island = None
    check_end()

def excavate(island_index):
    if st.session_state.excavated[island_index]:
        st.session_state.message = f"You already excavated {st.session_state.islands[island_index]}."
        st.session_state.action_taken = True
        st.session_state.selected_island = None
        return

    st.session_state.excavated[island_index] = True

    if island_index == st.session_state.correct_island:
        st.session_state.score += 100
        st.session_state.message = f"🎉 You found the ancient ruins on {st.session_state.islands[island_index]}!"
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
    st.session_state.selected_island = None
    check_end()

def check_end():
    # End due to turns
    if st.session_state.turns <= 0 and not st.session_state.game_over:
        st.session_state.game_over = True
        st.session_state.message = (
            f"⏳ Out of time! The ruins remain undiscovered.<br>"
            f"Final Score: {st.session_state.score}"
        )

    # Reveal coordinates if score >= 100, only once
    if st.session_state.score >= 100 and not st.session_state.revealed_coords:
        st.session_state.message += (
            f"<br><div style='background-color: #d4edda; color: #155724; padding: 10px; border-radius: 5px;'>"
            f"📍🏆 You won! You got {st.session_state.score} points.<br>"
            f"📍 Here are the coordinates: (32N, 48E)"
            f"</div>"
        )
        st.session_state.revealed_coords = True


    # Reveal coordinates if score >= 100, only once
    if st.session_state.score >= 100 and not st.session_state.revealed_coords:
        st.session_state.message += (
            f"\n📍🏆 You won! You got {st.session_state.score} points.\n"
            f"📍 Here are the coordinates: (32N, 48E)"
        )
        st.session_state.revealed_coords = True


    # Reveal coordinates if score >= 100, only once
    if st.session_state.score >= 100 and not st.session_state.revealed_coords:
        st.session_state.message += (
            f"<br><span style='color:green; font-weight:bold;'>"
            f"📍🏆 You won! You got {st.session_state.score} points.<br>"
            f"📍 Here are the coordinates: (32N, 48E)"
            f"</span>"
        )
        st.session_state.revealed_coords = True
    # Reveal coordinates if score >= 100, only once
    if st.session_state.score >= 100 and not st.session_state.revealed_coords:
        st.session_state.message += (
            f"<br>🏆 You won! You got {st.session_state.score} points.<br>"
            f"📍 Here are the coordinates: (32N, 48E)"
        )
        st.session_state.revealed_coords = True

def reset_game():
    st.session_state.islands = ["Island A", "Island B", "Island C", "Island D", "Island E"]
    st.session_state.correct_island = random.randint(0, 4)
    st.session_state.clues_found = [None] * 5
    st.session_state.excavated = [False] * 5
    st.session_state.turns = 5
    st.session_state.score = 0
    st.session_state.game_over = False
    st.session_state.message = "🌍 New expedition started!"
    st.session_state.selected_island = None
    st.session_state.action_taken = False
    st.session_state.revealed_coords = False

def next_turn():
    st.session_state.message = "Choose your next island."
    st.session_state.action_taken = False

# --- UI ---
st.title("🏝️ Islands of Discovery")

st.sidebar.header("📊 Expedition Stats")
st.sidebar.write(f"⭐ Score: **{st.session_state.score}**")
st.sidebar.write(f"⏳ Turns Left: **{st.session_state.turns}**")
if st.sidebar.button("🔄 Restart Game"):
    reset_game()

# --- Info dropdown ---
with st.expander("ℹ️ How to Play"):
    st.markdown("""
    **🎯 Goal:** Find the hidden ruins before you run out of turns!  
    Each action uses **1 turn**, and you start with **5 turns**.

    **🔎 Survey:**  
    - Searches the surface for clues.  
      - 🏺 Ruins markings → The correct island  
      - 🔎 Pottery fragments → Very close  
      - 🦴 Ancient bones → Nearby activity  
      - 🌊 Just shells → Nothing nearby  

    **⛏️ Excavation:**  
    - Digs deeper on that island.  
    - You may find ancient items for points or even the ruins (100 pts)!
    """)

# Display message using Markdown for proper line breaks
st.markdown(st.session_state.message, unsafe_allow_html=True)

if not st.session_state.game_over:
    if not st.session_state.action_taken:
        if st.session_state.selected_island is None:
            st.subheader("🌴 Choose an island:")
            cols = st.columns(2)
            for i, island in enumerate(st.session_state.islands):
                if i % 2 == 0:
                    with cols[0]:
                        st.button(island, key=f"island_{i}", on_click=lambda idx=i: st.session_state.update(selected_island=idx))
                else:
                    with cols[1]:
                        st.button(island, key=f"island_{i}", on_click=lambda idx=i: st.session_state.update(selected_island=idx))
        else:
            island_name = st.session_state.islands[st.session_state.selected_island]
            st.subheader(f"🏝️ {island_name}")
            st.write("What would you like to do here?")
            col1, col2, col3 = st.columns([1, 1, 1])
            with col1:
                st.button("🔎 Survey", on_click=survey, args=(st.session_state.selected_island,))
            with col2:
                st.button("⛏️ Excavation", on_click=excavate, args=(st.session_state.selected_island,))
            with col3:
                st.button("↩️ Back", on_click=lambda: st.session_state.update(selected_island=None))
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
