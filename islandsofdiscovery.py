import streamlit as st
import random

# --- Initialize state ---
if "initialized" not in st.session_state:
    st.session_state.islands = ["Island A", "Island B", "Island C", "Island D", "Island E"]
    st.session_state.correct_island = random.randint(0, 4)
    st.session_state.clues_found = [None] * 5
    st.session_state.excavated = [False] * 5
    st.session_state.turns = 5
    st.session_state.score = 0
    st.session_state.game_over = False
    st.session_state.selected_island = None
    st.session_state.message = "🌍 Welcome to Islands of Discovery!"
    st.session_state.initialized = True

# --- Game functions ---
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
    check_end()
    st.session_state.selected_island = None

def excavate(island_index):
    if st.session_state.excavated[island_index]:
        st.session_state.message = f"You already excavated {st.session_state.islands[island_index]}."
        st.session_state.selected_island = None
        return

    st.session_state.excavated[island_index] = True

    if island_index == st.session_state.correct_island:
        st.session_state.score += 100
        st.session_state.message = f"🎉 You excavated {st.session_state.islands[island_index]} and found the ruins! 🏆 Final Score: {st.session_state.score}"
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
    check_end()
    st.session_state.selected_island = None

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
    st.session_state.selected_island = None
    st.session_state.message = "🌍 New expedition started!"

# --- UI ---
st.title("🏝️ Islands of Discovery")
st.markdown("Help an archaeologist survey 5 islands and uncover the lost ruins. You have **5 turns**!")

# Stats
st.markdown(f"⭐ **Score**: {st.session_state.score} | ⏳ **Turns Left**: {st.session_state.turns}")

# Restart button
if st.button("🔄 Restart Game"):
    reset_game()

# Main message
st.info(st.session_state.message)

# Step 1: select island
if not st.session_state.game_over:
    if st.session_state.selected_island is None:
        st.subheader("Step 1: Select an island")
        for i, name in enumerate(st.session_state.islands):
            if st.session_state.excavated[i]:
                label = f"{name} ⛏ Excavated"
            elif st.session_state.clues_found[i]:
                label = f"{name} ({st.session_state.clues_found[i]})"
            else:
                label = f"{name}"
            st.button(label, key=f"island_{i}", on_click=lambda i=i: st.session_state.__setitem__("selected_island", i))
    else:
        # Step 2: select action
        st.subheader(f"Step 2: Choose action for {st.session_state.islands[st.session_state.selected_island]}")
        st.button("🔎 Survey", on_click=survey, args=(st.session_state.selected_island,))
        st.button("⛏ Excavation", on_click=excavate, args=(st.session_state.selected_island,))

# Map at bottom
st.subheader("🗺️ Expedition Map")
for i, name in enumerate(st.session_state.islands):
    if st.session_state.excavated[i]:
        status = "⛏ Excavated"
    elif st.session_state.clues_found[i]:
        status = st.session_state.clues_found[i]
    else:
        status = "❓ Unknown"
    st.markdown(f"**{name}** → {status}")
