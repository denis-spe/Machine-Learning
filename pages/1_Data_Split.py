import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split

# Set the page main title
st.set_page_config(
    page_title="ML | Data Spliting",
)

# Load Css file
def load_css(path):
    with open(path, mode='r') as file:
        st.markdown(f"<style>{file.read()}</style>", unsafe_allow_html=True)


# loading the css file 
load_css("style.css")

# Page title and sidebar title.
st.markdown("# Data Split")
st.sidebar.markdown("# Data Cleaning")

for data_name in st.session_state:
    if 'train' in data_name and data_name not in ["train_X", "train_y"]:
        # Get the train dataset
        datasets = st.session_state[data_name]

        st.markdown(f"<h3 class='sub-title'>{data_name.capitalize()}</h3>", unsafe_allow_html=True)

        # Insert the target feature
        target = st.selectbox("Target variable", options=datasets.columns, help="response variable")

        # Create the input box
        train_rows = st.number_input("Train split samples(Rows)", min_value=0.0, max_value=1.0, value=.75, help="train size")
        valid_rows = st.number_input("Validation split samples(Rows)", min_value=0.0, max_value=1.0, value=.25, help="test size")
        random_state = st.number_input("Random state", value=0, help="number of seeds")

        # Add select box to sidebar
        stratify = st.sidebar.selectbox("Stratify", options=datasets.columns.insert(0, None), help="label")

        # Add a line break
        st.sidebar.write("---")

        # Add a shuffle select box
        shuffle = st.sidebar.selectbox("Shuffle", options=[True, False], help="Shuffle data")

        if st.button("Split"):
            X = datasets.drop(target, axis=1)
            y = datasets[target]
            try:
                train_X, valid_X, train_y,  valid_y = train_test_split(
                    X, 
                    y, 
                    train_size=train_rows, 
                    test_size=valid_rows, 
                    random_state=random_state,
                    shuffle=shuffle,
                    stratify=datasets[stratify]
                    )
            except (KeyError, ValueError):
                train_X, valid_X, train_y,  valid_y = train_test_split(
                    X, 
                    y, 
                    train_size=train_rows, 
                    test_size=valid_rows, 
                    random_state=random_state,
                    shuffle=shuffle
                    )

            # Add datasets to the session
            st.session_state['train_X'] = train_X
            st.session_state['valid_X'] = valid_X
            st.session_state['train_y'] = train_y
            st.session_state['valid_y'] = valid_y

            # Add the name of the target variable
            st.session_state['target_name'] = target

            st.info(f"""
            Train_X:\n
    
            \tRows: {train_X.shape[0]}\n
            \tColumns:{train_X.shape[1]}\n
            Valid_X:\n
            \tRows: {valid_X.shape[0]}\n
            \tColumns:{valid_X.shape[1]}\n
            Train_y:\n
            \tRows: {train_y.shape[0]}\n
            valid_y:\n
            \tRows: {valid_y.shape[0]}\n
            stratify: {stratify}\n
            Shuffle: {shuffle}\n
            """)
        
        st.sidebar.markdown("<h1 style='font-size: 15px;'><center>Machine Learning</center></h1>", unsafe_allow_html=True)
        st.sidebar.markdown("<center style='font-size: 13px;'>Copyright@2022</center>", unsafe_allow_html=True)

if 'train' not in st.session_state:
    st.markdown("""
    <p>Please add train file in order to split the data.</p>
    <p>The inserted train file must be named <b><i>train.csv.</i></b></p>
    """, unsafe_allow_html=True)

st.markdown("<h1 style='font-size: 15px;'><center>Machine Learning</center></h1>", unsafe_allow_html=True)
st.markdown("<center style='font-size: 13px;'>Copyright@2022</center>", unsafe_allow_html=True)





