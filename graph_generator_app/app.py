import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import io
import pdfplumber

st.set_page_config(page_title="AI-Driven Graph Generator", layout="centered")
st.title("AI-Driven Graph Generator")

# --- Input Method ---
input_method = st.radio("Select Input Method", ["Upload File", "Manual Entry"])

df = None

# --- File Upload ---
if input_method == "Upload File":
    uploaded_file = st.file_uploader("Upload CSV, Excel, or PDF", type=["csv", "xlsx", "pdf"])
    if uploaded_file:
        file_ext = uploaded_file.name.split(".")[-1].lower()
        try:
            if file_ext == "csv":
                df = pd.read_csv(uploaded_file)
            elif file_ext == "xlsx":
                df = pd.read_excel(uploaded_file)
            elif file_ext == "pdf":
                with pdfplumber.open(uploaded_file) as pdf:
                    all_text = ""
                    for page in pdf.pages:
                        text = page.extract_text()
                        if text:
                            all_text += text + "\n"
                    st.text_area("Extracted PDF Text", all_text, height=300)
                    st.warning("PDF parsing supports only text-based table structures.")
        except Exception as e:
            st.error(f"Error loading file: {e}")

# --- Manual Input ---
else:
    manual_data = st.text_area("Paste your table data (comma-separated rows, new line for new rows)", 
                               height=200, 
                               placeholder="Month, Sales A, Sales B\nJan, 100, 200\nFeb, 150, 180")
    if manual_data:
        try:
            from io import StringIO
            df = pd.read_csv(StringIO(manual_data))
        except Exception as e:
            st.error(f"Failed to parse manual data: {e}")

# --- Proceed if DataFrame is Ready ---
if df is not None:
    st.subheader("Data Preview")
    st.dataframe(df)

    st.markdown("---")

    x_axis = st.selectbox("Select X-axis column", df.columns)
    y_columns = st.multiselect("Select Y-axis column(s)", df.columns)

    # Auto-validate Y columns
    if y_columns:
        invalid_cols = [col for col in y_columns if not pd.api.types.is_numeric_dtype(df[col])]
        if invalid_cols:
            st.warning(f"The following Y-columns are not numeric and will be ignored: {', '.join(invalid_cols)}")
            y_columns = [col for col in y_columns if col not in invalid_cols]

    graph_type = st.selectbox(
        "Graph Type", 
        ["Line", "Bar", "Grouped Bar", "Stacked Bar", "Pie (only first Y column)"]
    )

    chart_title = st.text_input("Chart Title", "My Graph")
    x_label = st.text_input("X-axis Label", x_axis)
    y_label = st.text_input("Y-axis Label", ", ".join(y_columns))

    # Color pickers for each Y column
    color_map = {}
    if y_columns:
        st.markdown("### 🎨 Choose Colors for Each Y Series")
        for y_col in y_columns:
            color = st.color_picker(f"Color for {y_col}", "#1f77b4")  # default matplotlib blue
            color_map[y_col] = color

    if st.button("Generate Graph") and x_axis and y_columns:
        n_points = len(df[x_axis])
        width = max(6, min(n_points * 0.5, 20))  # Between 6 and 20 inches
        height = 5
        fig, ax = plt.subplots(figsize=(width, height))


        if graph_type in ["Line", "Bar"]:
            for y_col in y_columns:
                color = color_map.get(y_col, None)
                if graph_type == "Line":
                    ax.plot(df[x_axis], df[y_col], marker='o', label=y_col, color=color)
                elif graph_type == "Bar":
                    ax.bar(df[x_axis], df[y_col], label=y_col, color=color)

        elif graph_type == "Grouped Bar":
            x = np.arange(len(df[x_axis]))
            width = 0.8 / len(y_columns)
            for idx, y_col in enumerate(y_columns):
                color = color_map.get(y_col, None)
                ax.bar(x + idx * width, df[y_col], width, label=y_col, color=color)
            ax.set_xticks(x + width * (len(y_columns) - 1) / 2)
            ax.set_xticklabels(df[x_axis])

        elif graph_type == "Stacked Bar":
            bottom = np.zeros(len(df))
            for y_col in y_columns:
                color = color_map.get(y_col, None)
                ax.bar(df[x_axis], df[y_col], bottom=bottom, label=y_col, color=color)
                bottom += df[y_col].values

        elif graph_type == "Pie":
            y_col = y_columns[0]
            if not pd.api.types.is_numeric_dtype(df[y_col]):
                st.warning("Pie chart requires numeric Y values.")
            else:
                ax.pie(df[y_col], labels=df[x_axis], autopct='%1.1f%%', colors=[color_map.get(y_col, None) for y_col in y_columns])
        
        ax.set_title(chart_title)
        if graph_type != "Pie":
            ax.set_xlabel(x_label)
            ax.set_ylabel(y_label)
            ax.legend()
            ax.grid(True)

            if len(df[x_axis]) > 6:
                ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right")

        fig.tight_layout()

        st.pyplot(fig)

        buf = io.BytesIO()
        fig.savefig(buf, format="png")
        buf.seek(0)
        st.download_button("Download Chart as PNG", buf, file_name="chart.png", mime="image/png")
