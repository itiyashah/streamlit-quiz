import streamlit as st

# This is the first line which is a must while writing a streamlit app.This title will be shown on tab.
st.set_page_config(page_title="Streamlit Master Quiz", page_icon="🧠", layout="centered")

st.title("🧠 Streamlit Mastery Quiz") # This title will be shown on main page
st.caption("Test your Streamlit knowledge and master session state!")# Sub-heading

# Questions database ( a list of python dictionaries)
questions = [
    {
        "question": "Which decorator is used to cache heavy data loading functions in Streamlit?",
        "options": ["@st.cache_data", "@st.memo", "@st.cache_resource", "@st.store"],
        "answer": "@st.cache_data",
        "explanation": "`@st.cache_data` is recommended for functions that return serializable data objects (like DataFrames, lists, or dicts)."
    },
    {
        "question": "How do you preserve variables across script reruns for a user session?",
        "options": ["st.memory", "st.session_state", "global variables", "st.preserve"],
        "answer": "st.session_state",
        "explanation": "Streamlit reruns the entire python script from top to bottom on every user input. `st.session_state` acts as persistent memory."
    },
    {
        "question": "Which component allows you to place elements side-by-side horizontally?",
        "options": ["st.tabs()", "st.sidebar", "st.columns()", "st.container()"],
        "answer": "st.columns()",
        "explanation": "`st.columns()` splits the main container into horizontal columns."
    },
    {
        "question": "What happens when a user clicks a button in Streamlit?",
        "options": ["Only the button callback runs", "The whole script reruns top-to-bottom", "The page reloads from the server", "Nothing changes until refresh"],
        "answer": "The whole script reruns top-to-bottom",
        "explanation": "Streamlit's core design runs the script from line 1 to the end every time a user triggers an interaction."
    },
    {
        "question": "Which component allows you to put widgets into a left-hand navigation panel?",
        "options": ["st.sidebar", "st.panel", "st.drawer", "st.menu"],
        "answer": "st.sidebar",
        "explanation": "`st.sidebar` moves controls, filters, or inputs into a dedicated slide-out sidebar panel on the left."
    },
    {
        "question": "Why would you wrap input widgets inside `st.form()`?",
        "options": [
            "To make the widgets look prettier", 
            "To prevent the app from rerunning until the user clicks submit", 
            "To encrypt user input data", 
            "To save data directly to a database"
        ],
        "answer": "To prevent the app from rerunning until the user clicks submit",
        "explanation": "Forms batch multiple inputs together so Streamlit doesn't rerun the whole script on every single typing action or slider drag."
    },
    {
        "question": "Which function renders an interactive, sortable, and scrollable data table?",
        "options": ["st.show_table()", "st.dataframe()", "st.display_csv()", "st.grid()"],
        "answer": "st.dataframe()",
        "explanation": "`st.dataframe()` renders dynamic, sortable Pandas tables, whereas `st.table()` renders a static HTML table."
    },
    {
        "question": "What is the primary function used to let users upload files in Streamlit?",
        "options": ["st.upload()", "st.file_uploader()", "st.input_file()", "st.get_file()"],
        "answer": "st.file_uploader()",
        "explanation": "`st.file_uploader()` accepts files (CSVs, images, PDFs) directly from the user's local machine."
    },
    {
        "question": "Which decorator allows a specific function to rerun independently without rerunning the entire page?",
        "options": ["@st.fragment", "@st.isolate", "@st.part", "@st.cache_data"],
        "answer": "@st.fragment",
        "explanation": "`@st.fragment` lets you isolate components (like a live chart or toggle) so interacting with them only reruns that specific block of code."
    },
    {
        "question": "Which elements are built specifically for creating ChatGPT-style conversational interfaces?",
        "options": [
            "st.chat_input() and st.chat_message()", 
            "st.text_input() and st.write()", 
            "st.prompt() and st.response()", 
            "st.input_box() and st.dialog()"
        ],
        "answer": "st.chat_input() and st.chat_message()",
        "explanation": "`st.chat_message()` creates speech bubbles with custom avatars, and `st.chat_input()` pins a floating text input bar to the bottom."
    }
]

# Here we initialize session state variable which will be set to default / initial state when rerun() runs.
if "q_index" not in st.session_state:
    st.session_state.q_index = 0
if "score" not in st.session_state:
    st.session_state.score = 0
if "quiz_over" not in st.session_state:
    st.session_state.quiz_over = False
if "answered" not in st.session_state:
    st.session_state.answered = False
if "is_correct" not in st.session_state:
    st.session_state.is_correct = False

# The below code is self-explanatory.
if st.session_state.quiz_over:
    st.balloons()
    st.success("🎉 Quiz Completed!")
    
    total_q = len(questions)
    score_percentage = int((st.session_state.score / total_q) * 100)
    
    col1, col2 = st.columns(2)# Helps in vertical division 
    col1.metric(label="Final Score", value=f"{st.session_state.score} / {total_q}")
    col2.metric(label="Accuracy", value=f"{score_percentage}%")

    if score_percentage == 100:
        st.subheader("🏆 Perfect Score! You're a Streamlit Pro!")
    elif score_percentage >= 50:
        st.subheader("👍 Good effort! Review the concepts and try again.")
    else:
        st.subheader("📚 Keep practicing! Practice makes perfect.")

    if st.button("🔄 Restart Quiz", type="primary"): # Restarting the quiz , so the user's session again will start from default
        st.session_state.q_index = 0
        st.session_state.score = 0
        st.session_state.quiz_over = False
        st.session_state.answered = False
        st.session_state.is_correct = False
        st.rerun()


else: # this block works if quiz is not over
    current_q = questions[st.session_state.q_index]
    total_q = len(questions)

    
    progress_val = (st.session_state.q_index) / total_q # Formula of how progress will be calculated
    st.progress(progress_val, text=f"Question {st.session_state.q_index + 1} of {total_q}")

    st.subheader(f"Q{st.session_state.q_index + 1}: {current_q['question']}")

    user_choice = st.radio(
        "Select your answer:", 
        current_q["options"], 
        key=f"radio_q_{st.session_state.q_index}",
        disabled=st.session_state.answered # Here the user's answer gets locked for submission and cannot be altered
    )

    submit_btn = st.button("Submit Answer", disabled=st.session_state.answered)
    
    
    if submit_btn:
        st.session_state.answered = True
        st.session_state.is_correct = (user_choice == current_q["answer"])
        if st.session_state.is_correct:
            st.session_state.score += 1
        st.rerun()

    
    if st.session_state.answered:
        if st.session_state.is_correct:
            st.success("✅ Correct!")
        else:
            st.error(f"❌ Incorrect. The correct answer was: **{current_q['answer']}**")

        with st.expander("💡 View Explanation", expanded=True):
            st.write(current_q["explanation"])

        st.divider() # Divides the page into two parts horizontally , clean ui
        
       
        if st.session_state.q_index + 1 < total_q: # This code block executes if still the questions are left to attempt.
            if st.button("Next Question ➡️", type="primary"):
                st.session_state.q_index += 1
                st.session_state.answered = False
                st.session_state.is_correct = False
                st.rerun()
        else:
            if st.button("See Final Results 🏆", type="primary"):
                st.session_state.quiz_over = True
                st.rerun()
# End of the code. Thankyou!!
