import streamlit as st

st.set_page_config(page_title="BestiesCheck 💖", page_icon="💖", layout="centered")

# App title
st.title("💖 BestiesCheck")
st.subheader("How well do you know your bestie? Let’s find out!")

# Session State Setup
if "stage" not in st.session_state:
    st.session_state.stage = "setup"
    st.session_state.qas = []
    st.session_state.friend_answers = []
    st.session_state.q_index = 0

# Stage 1: Setup questions and answers
if st.session_state.stage == "setup":
    st.info("👤 Player 1: Enter 5 questions and your answers.")
    with st.form("setup_form"):
        questions = []
        answers = []
        for i in range(5):
            q = st.text_input(f"Q{i+1}: Your question", key=f"q{i}")
            a = st.text_input(f"Answer to Q{i+1}", key=f"a{i}")
            questions.append(q)
            answers.append(a)

        submitted = st.form_submit_button("Start Quiz for Bestie 💬")
        if submitted and all(questions) and all(answers):
            st.session_state.qas = list(zip(questions, answers))
            st.session_state.stage = "quiz"
            st.rerun()
        elif submitted:
            st.warning("Please fill in all questions and answers!")

# Stage 2: Friend answers the quiz
elif st.session_state.stage == "quiz":
    index = st.session_state.q_index
    total = len(st.session_state.qas)

    if index < total:
        question = st.session_state.qas[index][0]
        st.success("👯‍♀️ Player 2: Try to answer!")
        st.markdown(f"**Q{index+1}: {question}**")
        answer = st.text_input("Your answer:", key=f"friend_answer_{index}")
        if st.button("Next ➡️"):
            if answer.strip() == "":
                st.warning("Please type an answer before continuing.")
            else:
                st.session_state.friend_answers.append(answer.strip())
                st.session_state.q_index += 1
                st.rerun()
    else:
        st.session_state.stage = "result"
        st.rerun()

# Stage 3: Show result
elif st.session_state.stage == "result":
    st.balloons()
    st.header("🎉 Results are in!")

    score = 0
    for i, (q, your_ans) in enumerate(st.session_state.qas):
        friend_ans = st.session_state.friend_answers[i]
        correct = your_ans.strip().lower() == friend_ans.strip().lower()
        if correct:
            score += 1
        st.markdown(f"**Q{i+1}: {q}**")
        st.markdown(f"- 💁 You said: `{your_ans}`")
        st.markdown(f"- 🧑‍🤝‍🧑 Your bestie said: `{friend_ans}` {'✅' if correct else '❌'}")
        st.write("---")

    st.subheader(f"💯 Final Score: `{score} / {len(st.session_state.qas)}`")

    # Fun message
    if score == 5:
        st.success("🌟 Besties Forever! You know each other so well!")
    elif score >= 3:
        st.info("💗 Pretty good! You know each other quite well!")
    else:
        st.warning("👀 Hmm... you two should talk more often!")

    # Restart button
    if st.button("🔁 Play Again"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
