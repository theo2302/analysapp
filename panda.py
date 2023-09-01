import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from io import StringIO

import warnings 
warnings.filterwarnings('ignore')
st.set_option('deprecation.showPyplotGlobalUse', False)

# Define the Streamlit app title
st.title("CSV DataFrame Creator")

# Define a delimiter selection widget with labels
delimiter_options = {',': ',', ';': ';', '\t': 'Tab', ' ': 'Space', '|': '|'}
delimiter = st.selectbox("Select the CSV delimiter:", list(delimiter_options.values()))

# Get the actual delimiter character based on the selected label
selected_delimiter = [k for k, v in delimiter_options.items() if v == delimiter][0]

# Create a file upload widget
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

# Check if a file has been uploaded
if uploaded_file is not None:
    # Read the uploaded file as text
    file_contents = uploaded_file.read().decode("utf-8")

    # Use StringIO to create a file-like object for pandas
    data = StringIO(file_contents)

    # Read the CSV file into a DataFrame with the selected delimiter
    df = pd.read_csv(data, delimiter=delimiter)

    # Display the DataFrame
    st.write("Uploaded DataFrame:", df)

    # You can perform various operations on the DataFrame here
    # For example, you can display a summary of the DataFrame:
    st.write("Information", df.info())
    
    st.write("DataFrame Summary:", df.describe())

    st.subheader("Correlation Heatmap")
    plt.figure()
    sns.heatmap(df.corr(numeric_only=True), annot=False, linewidth=.5, cmap='Blues', vmin=-1, vmax=1)
    st.pyplot(plt)

    st.header("Data Manipulation")

# Check if a DataFrame has been created

    # Create a checkbox for grouping by columns
    groupby_columns = st.multiselect("Select columns to group by:", df.columns)

    if groupby_columns:
        # Create a dropdown for selecting an aggregate function
        aggregate_function = st.selectbox("Select an aggregate function:", ["mean", "sum", "min", "max"])

        # Group the DataFrame by the selected columns and apply the aggregate function
        grouped_df = df.groupby(groupby_columns).agg(aggregate_function)

        # Display the grouped DataFrame
        st.write("Grouped DataFrame:", grouped_df)

# Optionally, you can add other widgets and interact with the DataFrame further.

