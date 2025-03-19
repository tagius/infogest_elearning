import streamlit as st

def main():
    # Configure pages
    introduction = st.Page("pages/introduction.py", title="Introduction", icon=":material/home:")
    fundamentals = st.Page("pages/fundamentals.py", title="Fundamentals", icon=":material/123:")
    first_steps = st.Page("pages/first_steps.py", title="First steps", icon=":material/sort:")
    solution_prep = st.Page("pages/solution_prep.py", title="Preparation Stock Solutions", icon=":material/experiment:")
    sdf_prep = st.Page("pages/sdf_prep.py", title="Preparation Simulated Digestive Fluids", icon=":material/experiment:")
    quick_start = st.Page("pages/quick_start.py", title="Quick Start Protocol", icon=":material/rocket_launch:")
    quiz = st.Page("pages/quiz.py", title="Quiz", icon=":material/quiz:")
    dashboard = st.Page("pages/dashboard.py", title="Dashboard", icon=":material/dashboard:")
    files = st.Page("pages/files.py", title="Files to download", icon=":material/draft:")
    changelog = st.Page("pages/changelog.py", title="Changelog", icon=":material/logo_dev:")

    pg = st.navigation(
        {
            "Get Started": [introduction, fundamentals],
            "INFOGEST Protocol": [first_steps, solution_prep, sdf_prep, quick_start],
            "Evaluation": [quiz],
            "Tools": [dashboard, files, changelog],
        }
    )

    pg.run()

if __name__ == "__main__":
    main()