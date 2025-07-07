## Online Graph Generator — Free & Open Source
A Streamlit-powered web app to generate customizable, downloadable charts from CSV, Excel, PDF, or manual data — no coding required!

Create Bar, Line, Pie, and Comparison charts with dynamic options like axis labels, multiple Y-columns, responsive design, and image export.

🚀 Features Overview

1️⃣ Smart Data Input

📂 Upload files in .csv, .xlsx, or .pdf format

✏️ Manually paste or enter tabular data directly in the app

2️⃣ Interactive Graph Generator

📈 Generate the following chart types:

Line Chart

Bar Chart (Vertical & Horizontal)

Grouped Bar Chart

Stacked Bar Chart

Pie Chart

🎨 Customize:

Chart title

Axis labels

Bar/line/pie colors

Auto-fix overlapping X-labels

Dynamic width adjustment for large datasets

3️⃣ Export & Download

💾 Save graphs as .png images with one click

🌐 No backend required — all runs locally or in-browser

🛠️ Tech Stack

Layer	Tools & Libraries

UI	Streamlit

Data	Pandas, NumPy

Graphs	Matplotlib

File Parsing	pdfplumber (for PDF)

Language	Python 3.x

🌐 Live Demo

👉 https://online-graph-generator-gxvumohpwacjzkusxtemd2.streamlit.app/

⚙️ Installation Guide

# 1. Clone the Repository

git clone https://github.com/Santoshh7/Online-Graph-Generator.git

cd Online-Graph-Generator

# 2. Create a Virtual Environment

python -m venv venv

# On Unix/Mac:

source venv/bin/activate

# On Windows:

venv\Scripts\activate

# 3. Install Dependencies

pip install -r requirements.txt

# 4. Run the App

streamlit run app.py

🗂️ Project Structure

📁 online-graph-generator/
├── 📄 app.py                  → Main Streamlit interface
├── 📄 graph_utils.py          → Chart generation & customization logic
├── 📄 file_parser.py          → File uploading & parsing (.csv, .xlsx, .pdf)
├── 📄 manual_input.py         → Manual data entry processor
├── 📄 requirements.txt        → Required Python packages
├── 📁 sample_data/            → Sample files for quick demo
└── 📄 README.md               → Full documentation (you are here)

📌 Sample Use Cases

📊 Teachers generating quick graphs from student marksheets

🧑‍💼 Business analysts visualizing sales reports

🧪 Researchers plotting experimental data

📚 Students needing clean visuals for presentations

⚠️ Disclaimer

This project is a free and open-source tool created for educational, demonstrative, and academic purposes.


👨‍💻 Developed By

**Santosh Thakur**

Passionate about building open-source, AI-powered, and visual analytics tools for real-world problems in data, governance, and public tech.
