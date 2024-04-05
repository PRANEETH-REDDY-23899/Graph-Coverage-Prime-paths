import streamlit as st
import graph_utils
import graph_coverage

def main():
    # st.markdown(
    #     """
    #     <style>
    #         .navbar {
    #             overflow: hidden;
    #             background-color: #333;
    #             position: fixed;
    #             top: 0;
    #             width: 100%;
    #         }

    #         .navbar a {
    #             float: left;
    #             display: block;
    #             color: #f2f2f2;
    #             text-align: center;
    #             padding: 14px 20px;
    #             text-decoration: none;
    #             font-size: 17px;
    #         }

    #         .navbar a:hover {
    #             background-color: #ddd;
    #             color: black;
    #         }

    #         .content {
    #             margin-top: 50px; /* Adjust this value based on navbar height */
    #         }
    #     </style>
    #     """
    # , unsafe_allow_html=True)

    # st.markdown(
    #     """
    #     <div class="navbar">
    #         <a href="#home">Home</a>
    #         <a href="#test_path">Test Path</a>
    #     </div>
    #     """
    # , unsafe_allow_html=True)

    # st.title("Graph Coverage Prime Paths")
    st.markdown("<div class='content'>", unsafe_allow_html=True)

    # Sidebar
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Home", "Test Path"])

    if page == "Home":
        st.session_state.home = True
    else:
        st.session_state.test_path = True

    if page == "Home":
        graph_utils.display_home_page()
    else:
        graph_coverage.display_test_path_page()

    # # Page content
    # if 'home' in st.session_state:
    #     graph_utils.display_home_page()
    # elif 'test_path' in st.session_state:
    #     graph_coverage.display_test_path_page()

if __name__ == "__main__":
    main()
