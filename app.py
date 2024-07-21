import streamlit as st
from together import Together
import pygments
from pygments.lexers import get_lexer_by_name, guess_lexer
from pygments.formatters import HtmlFormatter


# Initialize Together.ai client
def initialize_client(api_key):
    if not api_key:
        raise ValueError("API key is not set")
    return Together(api_key=api_key)


def convert_code(client, code, target_language):
    prompt = (
        f"You are an expert programmer in all programming languages. Convert the following code to {target_language} "
        f"and explain it in a multiline comment of that specific programming language in 5 simple lines:\n\n{code}\n\n"
        "DO NOT ADD ANY starter lines, JUST start providing the function directly followed by the multiline comment."
    )

    try:
        response = client.completions.create(
            model="meta-llama/Meta-Llama-3-70B-Instruct-Lite",
            prompt=prompt,
            max_tokens=512,
            temperature=0.7,
            top_p=0.7,
            top_k=50,
            repetition_penalty=1,
            stream=False
        )
        return response.choices[0].text.strip()
    except Exception as e:
        raise RuntimeError(f"Error during API call: {e}")


def highlight_code(code, language, font_size=14):
    try:
        lexer = get_lexer_by_name(language.lower())
    except:
        lexer = guess_lexer(code)
    formatter = HtmlFormatter(style="monokai", full=True, cssclass="highlight")
    highlighted_code = pygments.highlight(code, lexer, formatter)

    custom_css = f"""
    .highlight {{ font-size: {font_size}px; word-wrap: break-word; white-space: pre-wrap; }}
    .highlight .c {{ font-size: {font_size - 2}px; }}  /* Minimized font size for comments */
    """
    return highlighted_code, custom_css


def explain_code(client, code):
    prompt = (
        f"You are an expert programmer. Explain the following code in detail, including its functionality, "
        f"time and space complexity, and potential improvements:\n\n{code}\n\n"
    )

    try:
        response = client.completions.create(
            model="meta-llama/Meta-Llama-3-70B-Instruct-Lite",
            prompt=prompt,
            max_tokens=512,
            temperature=0.7,
            top_p=0.7,
            top_k=50,
            repetition_penalty=1,
            stream=False
        )
        return response.choices[0].text.strip()
    except Exception as e:
        raise RuntimeError(f"Error during API call: {e}")


def detect_errors(client, code):
    prompt = (
        f"You are an expert programmer. Detect any errors in the following code and suggest corrections:\n\n{code}\n\n"
    )

    try:
        response = client.completions.create(
            model="meta-llama/Meta-Llama-3-70B-Instruct-Lite",
            prompt=prompt,
            max_tokens=512,
            temperature=0.7,
            top_p=0.7,
            top_k=50,
            repetition_penalty=1,
            stream=False
        )
        return response.choices[0].text.strip()
    except Exception as e:
        raise RuntimeError(f"Error during API call: {e}")


def generate_unit_tests(client, code, language):
    prompt = (
        f"You are an expert programmer. Generate unit tests for the following {language} code:\n\n{code}\n\n"
    )

    try:
        response = client.completions.create(
            model="meta-llama/Meta-Llama-3-70B-Instruct-Lite",
            prompt=prompt,
            max_tokens=512,
            temperature=0.7,
            top_p=0.7,
            top_k=50,
            repetition_penalty=1,
            stream=False
        )
        return response.choices[0].text.strip()
    except Exception as e:
        raise RuntimeError(f"Error during API call: {e}")


def main():
    st.title("CodeAI - Advanced Code Translator and Analyzer")

    api_key = st.text_input("Enter your Together.ai API key:")
    client = None

    if api_key:
        try:
            client = initialize_client(api_key)
        except ValueError as e:
            st.error(e)
            return

    code_input = st.text_area("Enter your code here:", height=150)

    languages = ["Python", "JavaScript", "C++", "Other"]
    target_language = st.selectbox("Select the language you want to translate to:", languages)

    if target_language == "Other":
        target_language = st.text_input("Enter the language you want to translate to:")

    col1, col2, col3, col4 = st.columns(4)

    if col1.button("Translate"):
        if client and code_input and target_language:
            try:
                translated_code = convert_code(client, code_input, target_language)

                st.markdown("### Original Code")
                highlighted_code, css = highlight_code(code_input, "text", font_size=12)
                st.markdown(f'<style>{css}</style>{highlighted_code}', unsafe_allow_html=True)

                st.markdown("### Translated Code")
                highlighted_translated_code, css = highlight_code(translated_code, target_language, font_size=14)
                st.markdown(f'<style>{css}</style>{highlighted_translated_code}', unsafe_allow_html=True)

            except RuntimeError as e:
                st.error(e)
        else:
            st.error("Please enter both code and target language, and provide a valid API key.")

    if col2.button("Explain Code"):
        if client and code_input:
            try:
                explanation = explain_code(client, code_input)
                st.markdown("### Code Explanation")
                st.text_area("Explanation", explanation, height=250)
            except RuntimeError as e:
                st.error(e)
        else:
            st.error("Please enter the code and provide a valid API key.")

    if col3.button("Detect Errors"):
        if client and code_input:
            try:
                errors = detect_errors(client, code_input)
                st.markdown("### Error Detection")
                st.text_area("Errors", errors, height=250)
            except RuntimeError as e:
                st.error(e)
        else:
            st.error("Please enter the code and provide a valid API key.")

    if col4.button("Generate Unit Tests"):
        if client and code_input:
            try:
                unit_tests = generate_unit_tests(client, code_input, target_language)
                st.markdown("### Unit Tests")
                st.text_area("Unit Tests", unit_tests, height=250)
            except RuntimeError as e:
                st.error(e)
        else:
            st.error("Please enter the code and provide a valid API key.")


if __name__ == "__main__":
    main()
