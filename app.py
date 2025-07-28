import streamlit as st
import json
import pandas as pd
from datetime import datetime
from evaluate_prompt import evaluate_prompt, improve_prompt, compare_prompts

st.set_page_config(page_title="Prompt Quality Checker")

# Initialize prompt history if not set
if "history" not in st.session_state:
    st.session_state.history = []

st.title("🎯 Prompt Quality Checker")
st.write("Paste a prompt below and get a score from our AI expert.")

prompt = st.text_area("✍️ Enter your prompt here:")

if st.button("Check Quality"):
    if not prompt.strip():
        st.warning("❗ Please enter a prompt.")
    elif len(prompt.strip()) < 5 or not any(char.isalpha() for char in prompt):
        st.warning("⚠️ This prompt looks too short or may be gibberish. Please enter a more meaningful one.")
    else:
        with st.spinner("Evaluating..."):
            result = evaluate_prompt(prompt)
        try:
            data = result

            st.success("✅ Prompt evaluated!")

            st.subheader("📊 Scores")
            for key in ["clarity", "specificity", "context", "creativity", "relevance", "ambiguity"]:
                st.write(f"**{key.capitalize()}**: {data[key]} / 5")

            st.markdown(f"### 🧮 **Total Score:** {data['total_score']} / 25")

            st.subheader("🔍 Issues Found")
            st.write(data["issues"])

            st.subheader("💡 Suggestions")
            st.write(data["suggestions"])

            # Save to history
            entry = {
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Prompt": prompt,
                "Clarity": data["clarity"],
                "Specificity": data["specificity"],
                "Context": data["context"],
                "Creativity": data["creativity"],
                "Relevance": data["relevance"],
                "Ambiguity": data["ambiguity"],
                "Total Score": data["total_score"]
            }
            st.session_state.history.append(entry)

        except Exception as e:
            st.error("Couldn't parse the response. Here's the raw reply:")
            st.code(str(e))

if st.button("🔧 Auto-Improve This Prompt"):
    if not prompt.strip():
        st.warning("Please enter a prompt.")
    else:
        with st.spinner("Thinking..."):
            improved = improve_prompt(prompt)
        st.subheader("✨ Improved Prompt")
        st.code(improved, language="markdown")

st.markdown("---")
st.subheader("🆚 Compare Two Prompts")

col1, col2 = st.columns(2)
with col1:
    prompt1 = st.text_area("Prompt 1", key="p1")
with col2:
    prompt2 = st.text_area("Prompt 2", key="p2")

if st.button("Compare Prompts"):
    if not prompt1.strip() or not prompt2.strip():
        st.warning("Please enter both prompts.")
    else:
        with st.spinner("Comparing..."):
            try:
                result = compare_prompts(prompt1, prompt2)
                data = json.loads(result)

                st.success(f"🏆 Better Prompt: **{data['better_prompt'].capitalize()}**")
                st.write("### 🤖 Reason")
                st.write(data["reason"])
                st.write("### ✍️ Suggestions")
                st.write(data["suggestions"])

                for label in ["prompt1", "prompt2"]:
                    st.write(f"### 📊 {label.capitalize()} Scores")
                    for k, v in data[label].items():
                        st.write(f"{k.capitalize()}: {v}")

            except Exception as e:
                st.error("Could not parse response.")
                st.code(str(e))  # ✅ Fix here!



        


st.markdown("---")
st.subheader("📜 Prompt History")

if st.session_state.history:
    df = pd.DataFrame(st.session_state.history)
    st.dataframe(df, use_container_width=True)

    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="⬇️ Download History as CSV",
        data=csv,
        file_name='prompt_history.csv',
        mime='text/csv'
    )
else:
    st.info("No prompts evaluated yet.")
