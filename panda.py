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

    null_count = pd.DataFrame(df.isna().sum())

    st.write('Valores nulos', null_count)
    
    st.write("Resumo estatistico:", df.describe())

    st.subheader("Heatmap")
    plt.figure()
    sns.heatmap(df.corr(numeric_only=True), annot=False, linewidth=.5, cmap='Blues', vmin=-1, vmax=1)
    st.pyplot(plt)


    st.header("Agrupamento por coluna")
    # Checkbox for grouping by columns
    groupby_columns = st.selectbox("Selecione Colunas:", df.columns)

    if groupby_columns:
        # Create a dropdown for selecting an aggregate function
        aggregate_function = st.selectbox("Selecione uma função agregadora:", ["mean", "sum", "min", "max"])

        # Group the DataFrame by the selected columns and apply aggregate function
        grouped_df = df.groupby(groupby_columns).agg(aggregate_function, numeric_only= True)

        # Display grouped DataFrame
        st.write("DataFrame agrupado:", grouped_df)



    st.header("Remava observações por colunas")
    # Checkbox for grouping by columns
    col_choise = st.multiselect("Coluna(s):", df.columns)

    if col_choise:
        # Group the DataFrame by the selected columns and apply aggregate function
        df = df.dropna(subset= col_choise)

        # Display grouped DataFrame
        st.write("DataFrame:", pd.DataFrame(df.isna().sum()))
    


    # Option to create a histogram
    create_histogram = st.checkbox("Crie um Histograma")

    # Allow the user to select x and y axis columns for the histogram
    x_axis = st.selectbox("Selecione X-axis:", df.columns)
    y_axis = st.selectbox("Selecione Y-axis:", df.columns)

    if create_histogram:
        # Filter out rows with NaN values in the selected columns
        filtered_df = df.dropna(subset=[x_axis, y_axis])

        # Create and display the histogram using matplotlib
        plt.figure(figsize=(8, 6))
        plt.hist(filtered_df[x_axis], filtered_df[y_axis])
        plt.colorbar(label='Frequency')
        plt.xlabel(x_axis)
        plt.ylabel(y_axis)
        plt.title(f"Histogram of {x_axis} vs {y_axis}")
        st.pyplot(plt)
