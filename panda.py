import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from io import StringIO

import warnings 
warnings.filterwarnings('ignore')
st.set_option('deprecation.showPyplotGlobalUse', False)

# Define the Streamlit app title
st.title("Analisador de Tabelas")

# Define a delimiter selection widget with labels
delimiter_options = {',': ',', ';': ';', '\t': 'Tab', ' ': 'Space', '|': '|'}
delimiter = st.selectbox("Selecione o delimitador usado:", list(delimiter_options.values()))

# Get the actual delimiter character based on the selected label
selected_delimiter = [k for k, v in delimiter_options.items() if v == delimiter][0]

# Create a file upload widget
uploaded_file = st.file_uploader("Upload de arquivos CSV", type=["csv"])

# Check if a file has been uploaded
if uploaded_file is not None:
    # Read the uploaded file as text
    file_contents = uploaded_file.read().decode("utf-8")

    # Use StringIO to create a file-like object for pandas
    data = StringIO(file_contents)

    # Read the CSV file into a DataFrame with the selected delimiter
    df = pd.read_csv(data, delimiter=delimiter)

    # Display the DataFrame
    st.write("DataFrame:", df)

    # You can perform various operations on the DataFrame here
    # For example, you can display a summary of the DataFrame:
    
    st.write("Resumo estatistico:", df.describe())

    st.subheader("Heatmap")
    plt.figure()
    sns.heatmap(df.corr(numeric_only=True), annot=False, linewidth=.5, cmap='Blues', vmin=-1, vmax=1)
    st.pyplot(plt)

    st.header("Agrupamento de dados")

# Check if a DataFrame has been created

    # Create a checkbox for grouping by columns
    groupby_columns = st.multiselect("Selecione Colunas:", df.columns)

    if groupby_columns:
        # Create a dropdown for selecting an aggregate function
        aggregate_function = st.selectbox("Selecione uma função agregadora:", ["mean", "sum", "min", "max"])

        # Group the DataFrame by the selected columns and apply the aggregate function
        grouped_df = df.groupby(groupby_columns).agg(aggregate_function)

        # Display the grouped DataFrame
        st.write("DataFrame agrupado:", grouped_df)

# Optionally, you can add other widgets and interact with the DataFrame further.

