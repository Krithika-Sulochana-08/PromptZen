import streamlit as st
from evaluate_prompt import evaluate_prompt, improve_prompt, compare_prompts

st.set_page_config(page_title="PromptZen", page_icon="✨")

st.title("✨ PromptZen - Prompt Quality Checker")

prompt = st.text_area("📝 Enter your prompt:", height=200)

if st.button("Check Quality"):
    with st.spinner("Evaluating prompt..."):
        result = evaluate_prompt(prompt)
        if "error" in result:
            st.error("❌ " + result["error"])
            st.text(result["details"])
        else:
            st.subheader("📊 Scores")
            for key in ["clarity", "specificity", "context", "creativity", "relevance", "ambiguity"]:
                st.write(f"**{key.capitalize()}**: {result[key]}")
            st.write("**Total Score**: ", result["total_score"])
            st.subheader("🧐 Issues")
            st.write(result["issues"])
            st.subheader("💡 Suggestions")
            st.write(result["suggestions"])

    if st.button("✨ Improve Prompt"):
        improved = improve_prompt(prompt)
        st.subheader("✅ Improved Prompt")
        st.code(improved, language="markdown")

        comparison = compare_prompts(prompt, improved)
        st.subheader("🔍 Comparison")
        st.write(comparison)
