import streamlit as st
import graph_utils
import graph_coverage

def main():
    # st.title("Graph Coverage Prime Paths")
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Select a page:", ["Home", "Test Path"])

    if page == "Home":
        graph_utils.display_home_page()
    elif page == "Test Path":
        graph_coverage.display_test_path_page()

if __name__ == "__main__":
    main()
