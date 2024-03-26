import streamlit as st
from helper.dataclass import Dataclass
from helper.split_data import split_data
from helper.load_css import load_css

# Set the page main title
st.set_page_config(
    page_title="ML | Data Splitting",
)

# loading the css file 
load_css("resources/styles/style.css")

# Page title and sidebar title.
st.markdown("# Data Split")
st.sidebar.markdown("# Data Splitting")

# Side bar
SIDERBAR = st.sidebar


if len(Dataclass.SESSION) > 0:
    # Names of the datasets
    data_names = list(Dataclass.SESSION.to_dict().keys())

    selected_data_name = st.selectbox("Select the dataset", options=data_names, index=0)

    datasets = Dataclass.SESSION[selected_data_name]

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

        train_X, train_y, valid_X, valid_y = split_data(
                datasets, 
                target, 
                train_rows, 
                valid_rows, 
                random_state,
                shuffle,
                stratify
            )
        

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

    if st.button("Data Cleaning"):
        st.switch_page("pages/2_🧹_Data_Cleaning.py")


        st.sidebar.markdown("<h1 style='font-size: 15px;'><center>Machine Learning</center></h1>", unsafe_allow_html=True)
        st.sidebar.markdown("<center style='font-size: 13px;'>Copyright@2022</center>", unsafe_allow_html=True)
else:
    st.image("resource/images/clean_up.png")

st.markdown("<h1 style='font-size: 15px;'><center>Machine Learning</center></h1>", unsafe_allow_html=True)
st.markdown("<center style='font-size: 13px;'>Copyright@2022</center>", unsafe_allow_html=True)





