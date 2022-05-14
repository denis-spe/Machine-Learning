import streamlit as st
import pandas as pd

all_dataset = list()


def load():
    # Setting  Screen layout
    asidebar = st.sidebar
    col1, col2 = st.columns(2)

    asidebar.markdown("""
    <h2 class='sub-title'>Files</h2>
    """, unsafe_allow_html=True)
    with st.expander("Upload the file"):
        upload_file = asidebar.file_uploader("Please upload the csv file", accept_multiple_files=True)
    
    if upload_file:
        try:
            # ********* Data Descriptive Analysis **********
            with col1:
                df_1 = pd.read_csv(upload_file[0])
                data_name_1 = upload_file[0].name.split('.')[0]
                
                st.markdown(f"<h3 class='sub-title'>{data_name_1.capitalize()}</h3>", unsafe_allow_html=True)
                # ****** Show the data shape *****
                shape = df_1.shape
                st.markdown(f"""
                **Shape: <br>{shape[0]}-rows**<br>**{shape[1]}-columns**
                """, unsafe_allow_html=True)

                # ***** show the DataFrame ******
                with st.expander("DataFrame"):
                    rows = list(range(10, 110, 5))
                    rows.append('all')
                    n_row = st.selectbox(f'{data_name_1}_rows', options=rows)
                    if n_row == 'all':
                        st.write(df_1)
                    else:
                        st.write(df_1.head(n_row))
                    
                    # Set column as index
                    columns = list(df_1.columns)
                    columns.insert(0, None)
                    set_index_col = st.selectbox('Set column as index', options=columns)
                    if set_index_col:
                        df_1 = df_1.set_index(set_index_col)
                # append tuple with dataset and data name
                all_dataset.append([df_1, data_name_1])

                # Display all dataframe column names
                with st.expander("columns"):
                    st.write(", ".join([col for col in df_1.columns]))
                
                # View the data description
                with st.expander('Data Description'):
                    st.write(df_1.describe())

            if len(upload_file) == 2:
                df_2 = pd.read_csv(upload_file[1])
                with col2:
                    data_name_2 = upload_file[1].name.split('.')[0]
                    st.markdown(f"<h3 class='sub-title'>{data_name_2.capitalize()}</h3>", unsafe_allow_html=True)

                    # ****** Show the data shape *****
                    shape = df_2.shape
                    st.markdown(f"""
                    **Shape: <br>{shape[0]}-rows**<br>**{shape[1]}-columns**
                    """, unsafe_allow_html=True)

                    # ***** show the DataFrame ******
                    with st.expander("DataFrame"):
                        rows = list(range(10, 110, 5))
                        rows.append('all')
                        n_row = st.selectbox(f'{data_name_2}_rows', options=rows)
                        if n_row == 'all':
                            st.write(df_2)
                        else:
                            st.write(df_2.head(n_row))
                        
                        # Set column as index
                        columns = list(df_2.columns)
                        columns.insert(0, None)
                        set_index_col = st.selectbox('Set column as index', options=columns)
                        if set_index_col:
                            df_2 = df_2.set_index(set_index_col)

                    # append tuple with dataset and data name
                    all_dataset.append([df_2, data_name_2])

                    # Display all dataframe column names
                    with st.expander("columns"):
                        st.write(", ".join([col for col in df_2.columns]))

                    # View the data description
                    with st.expander('Data Description'):
                        st.write(df_2.describe())
                        
                    
            
        except IndexError:
            st.error("Too many file have been insert")

    else:
        st.markdown(
        """
        ## **Please Insert A Files**
        **Insert one or two csv files from the sidebar**
        
        """
        )
        st.image("undraw_add_file_re_s4qf.svg")