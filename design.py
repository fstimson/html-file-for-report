import streamlit as st
import pandas as pd
from datetime import datetime
import re
import base64
import os

# Page configuration
st.set_page_config(layout="wide", page_title="Dataset Tracker")

# Initialize session state
if 'selected_report' not in st.session_state:
    st.session_state.selected_report = None

# Load Reports data
@st.cache_data
def load_cross_reference_data():
    file_path = r"C:\Users\fstim\OneDrive\Remotasks\report creation\cross reference report.xlsx"
    df = pd.read_excel(file_path)
    df = df.fillna('')
    return df

@st.cache_data
def load_matching_report_data():
    file_path = r"C:\Users\fstim\OneDrive\Remotasks\report creation\matching report.xlsx"
    df = pd.read_excel(file_path)
    df = df.fillna('')
    return df

@st.cache_data
def load_master_list_data():
    file_path = r"C:\Users\fstim\OneDrive\Remotasks\report creation\master list.xlsx"
    df = pd.read_excel(file_path)
    df = df.fillna('')
    return df
    
@st.cache_data
def load_timeline_data():
    file_path = r"C:\Users\fstim\OneDrive\Remotasks\report creation\timeline.xlsx"
    df = pd.read_excel(file_path)
    df = df.fillna('')
    return df 

@st.cache_data
@st.cache_data
def load_rejected_html_files():
    file_path = r"C:\Users\fstim\OneDrive\Remotasks\images\new html file and path.xlsx"
    df = pd.read_excel(file_path)
    return df['html file path and folder'].tolist()
 
    


# Load all reports
report_df = load_cross_reference_data()
matching_df = load_matching_report_data()
master_list_df = load_master_list_data()
timeline_df = load_timeline_data()


# Image file paths
approved_svg_path = r"C:\Users\fstim\OneDrive\Remotasks\images\SVG Images\approved.svg"
rejected_svg_path = r"C:\Users\fstim\OneDrive\Remotasks\images\SVG Images\rejected.svg"
approved_img_path = r"C:\Users\fstim\OneDrive\Remotasks\images\Compressed\APPROVED CHECK_compressed.png"

rejected_img_path = r"C:\Users\fstim\OneDrive\Remotasks\images\Compressed\REJECT X_compressed.png"
folder_icon_png_path = r"C:\Users\fstim\OneDrive\Remotasks\images\folder_icon.png"



# Date formatting function
def format_date(date_str):
    if pd.notna(date_str):
        try:
            return pd.to_datetime(date_str).strftime('%m/%d/%y')
        except:
            return ''
    return ''
    
def calculate_date_difference(start_date, end_date):
    if pd.isna(start_date) or pd.isna(end_date):
        return ""
    
    try:
        # Convert to datetime if they're strings
        if isinstance(start_date, str):
            start_date = pd.to_datetime(start_date)
        if isinstance(end_date, str):
            end_date = pd.to_datetime(end_date)
        
        # Calculate the difference
        diff = end_date - start_date
        total_days = diff.days
        
        # Calculate months and remaining days
        months = total_days // 30
        remaining_days = total_days % 30
        
        # Format the output
        if months > 0 and remaining_days > 0:
            return f"{months} months {remaining_days} days"
        elif months > 0:
            return f"{months} months"
        else:
            return f"{remaining_days} days"
    except:
        return ""  

# Custom CSS for styling
st.markdown("""
<style>
    /* Root variables */
    :root {
        --rust-red: #A33614;
        --gray-bg: #81858D;
        --dark-brown: #3E3432;
        --light-gray: #D9D7D6;
        --orange: #DA8419;
        --reject-red: #C63C14;
        --approve-green: #28a745;
    }

    /* Base layout and containers */
    body {
        padding-top: 60px;
    }

    .stApp {
        margin-top: 5px;
    }

    .search-header {
        position: sticky;
        top: 0;
        background-color: #0E1117;
        padding: 10px;
        border-bottom: 2px solid #2E2E2E;
        z-index: 1000;
    }

    .stContainer {
        position: sticky;
        top: 0;
        background-color: #0E1117;
        z-index: 1000;
        padding: 10px;
    }

    /* Dataset list styling */
    .dataset-list-container {
        margin-top: 20px;
        max-height: calc(100vh - 200px);
        overflow-y: auto;
        padding: 10px;
        background-color: #1E1E1E;
        border-radius: 5px;
        text-align: left;
    }

    .dataset-row {
        display: flex;
        align-items: center;
        gap: 4px;
        padding: 2px;
        margin-bottom: 0px;
    }

    .dataset-item {
        display: flex;
        align-items: center;
        padding: 2px 4px;
        background-color: rgba(255,255,255,0.05);
        border-radius: 1px;
        text-align: left;
        justify-content: flex-start;
    }

    /* Navigation styling */
    .nav-container {
        position: fixed;
        top: 0;
        left: 0;
        width: 25%;
        z-index: 1000;
        background-color: #0E1117;
        padding: 10px 0;
        border-bottom: 1px solid #3E3432;
    }

    .nav-buttons {
        display: flex;
        justify-content: center;
        gap: 5px;
        padding: 5px;
    }

    .nav-button {
        background-color: var(--light-gray);
        border: 2px solid var(--dark-brown);
        border-radius: 12px;
        padding: 6px 6px;
        color: white;
        cursor: pointer;
        display: inline-flex;
        align-items: center;
        text-decoration: none;
        font-weight: bold;
        justify-content: center;
    }

    .nav-button:hover {
        opacity: 0.8;
        transform: scale(1.05);
    }

    /* Status styling */
    .status-container {
        padding: 2px 6px;
        border-radius: 3px;
        font-size: 0.8em;
        margin-left: 8px;
    }

    .status-rejected {
        background-color: var(--reject-red);
        color: white;
    }

    .status-approved {
        background-color: var(--approve-green);
        color: white;
    }

    /* Component styling */
    .question-container {
        background-color: rgba(255,255,255,0.1);
        padding: 6px;
        margin-bottom: 4px;
        border-radius: 3px;
    }

    .divider {
        margin: 0.15rem 0;
        border-top: 1px solid var(--dark-brown);
    }

    .scrollable-container {
        max-height: 150px;
        overflow-y: auto;
        padding-right: 4px;
    }

    /* Button colors */
    .search-btn { background-color: var(--reject-red); }
    .summary-btn { background-color: var(--dark-brown); }
    .questions-btn { background-color: var(--gray-bg); }
    .datasets-btn { background-color: var(--light-gray); }
    .timeline-btn { background-color: var(--orange); }

    /* DataFrames */
    .stDataFrame {
        color: var(--light-gray) !important;
    }

    .tab-active {
        background-color: var(--dark-brown) !important;
        color: white !important;
    }
    </style>
""", unsafe_allow_html=True)

# Title with minimal spacing
st.markdown('<h1 style="margin: 2px 0;">Dataset Tracker</h1>', unsafe_allow_html=True)

# Initialize session state for tab selection
if "selected_tab" not in st.session_state:
    st.session_state.selected_tab = "Search"

def select_tab(tab_name):
    st.session_state.selected_tab = tab_name

st.markdown('</div></div>', unsafe_allow_html=True)


# Navigation buttons
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    if st.button('🔍 Search', key='search', use_container_width=True):
        select_tab("Search")

with col2:
    if st.button('📊 Summary', key='summary', use_container_width=True):
        select_tab("Summary")

with col3:
    if st.button('❓ Questions', key='questions', use_container_width=True):
        select_tab("Questions")

with col4:
    if st.button('📁 Datasets', key='datasets', use_container_width=True):
        select_tab("Datasets")

with col5:
    if st.button('⏱️ Timeline', key='timeline', use_container_width=True):
        select_tab("Timeline")

st.markdown('<hr class="divider">', unsafe_allow_html=True)


# Search Tab
st.header("Search Datasets")
search_query = st.text_input("Search datasets...")

# Load HTML files in the search section
html_files = load_html_files()

# Track selected dataset
if "selected_report" not in st.session_state:
    st.session_state.selected_report = None

# Display available reports as buttons with selection effect
for report_name in html_files:
    if report_name.endswith(".html"):  # Ensure only HTML files are processed
        is_selected = st.session_state.selected_report == report_name
        button_style = "border: 2px solid red;" if is_selected else ""
        col1, col2 = st.columns([4, 1])
        with col1:
            if st.button(f"{report_name}", key=f"report_{report_name}", use_container_width=True):
                st.session_state.selected_report = report_name
                st.rerun()
        with col2:
            st.markdown(f'<div style="{button_style}"></div>', unsafe_allow_html=True)

if not html_files:
    st.warning("No datasets found matching your search.")

# Question Tab
if st.session_state.selected_tab == "Questions":
    if st.session_state.selected_report:
        st.markdown('<h1 style="margin: 2px 0;">Question Comparison</h1>', unsafe_allow_html=True) 
        
    
        left_col, right_col = st.columns(2)
        
        # Rejected Questions Column (Left)
        with left_col:
            st.markdown("""
                <div style='background-color: #DA8419; padding: 10px; color: white;'>
                    <h3 style='margin: 0;'>Rejected Questions</h3>
                </div>
            """, unsafe_allow_html=True)
            
            # Find questions for the selected report
            rejected_questions = matching_df[
                (matching_df['Tracker File Name_current'] == st.session_state.selected_report)
            ]
            
            st.markdown(f"""
                <div style='background-color: #868D8E; padding: 10px;'>
                    <span style='color: white; font-weight: bold;'>{st.session_state.selected_report}</span>
                </div>
            """, unsafe_allow_html=True)
            
            for _, row in rejected_questions.iterrows():
                st.markdown(f"""
                    <div class='question-container'>
                        <p style='color: white; margin: 0;'>{row['QUESTIONS_current']}</p>
                    </div>
                """, unsafe_allow_html=True)
        
        # Matched Questions Column (Right)
        with right_col:
            st.markdown("""
                <div style='background-color: #DA8419; padding: 10px; color: white;'>
                    <h3 style='margin: 0;'>Approved Questions</h3>
                </div>
            """, unsafe_allow_html=True)
            
            # Find the matched tracker file name
            matched_file = rejected_questions['Matched_Tracker_File_Name'].iloc[0] if not rejected_questions.empty else None
            
            if matched_file:
                st.markdown(f"""
                    <div style='background-color: #868D8E; padding: 5px;'>
                        <span style='color: white; font-weight: bold;'>{matched_file}</span>
                    </div>
                """, unsafe_allow_html=True)
                
                for _, row in rejected_questions.iterrows():
                    if pd.notna(row['Matched_ID']):
                        matched_questions = matching_df[
                            (matching_df['Tracker File Name_current'] == matched_file) & 
                            (matching_df['ID'] == row['Matched_ID'])
                        ]
                        
                        if not matched_questions.empty:
                            approved_question = matched_questions.iloc[0]
                            st.markdown(f"""
                                <div class='question-container'>
                                    <p style='color: white; margin: 0;'>{approved_question['QUESTIONS_match']}</p>
                                </div>
                            """, unsafe_allow_html=True)
         
    else:
        st.info("Please select a dataset from the Search")
         
# Summary Page
elif st.session_state.selected_tab == "Summary":
    # Main header with icon
    st.header("📊 Dataset Summary")

    if st.session_state.selected_report:
        # Get data from cross reference report
        report_rows = report_df[report_df['Tracker File Name_current'].str.strip() == str(st.session_state.selected_report).strip()]

        if not report_rows.empty:
            report_info = report_rows.iloc[0]

            # Get status and corresponding PNG image
            status = report_info.get('STATUS_current', '')
            image_path = rejected_img_path if status == 'REJECTED' else approved_img_path

            # Display dataset details in a **single column** (same layout as before)
            st.markdown("### Dataset Details")
            st.write(f"**Rate:** ${report_info.get('DS Rate', '300')}")
            st.write(f"**DS Submitted:** {format_date(report_info.get('Date Sent'))}")
            st.write(f"**Rejected Date:** {format_date(report_info.get('Rejection Date'))}")
            st.write(f"**Reason for Rejection:** {report_info.get('Reason for Rejection', '')}")
            st.write(f"**Date of Appeal:** {format_date(report_info.get('Date Of Appeal'))}")
            st.write(f"**Date of Appeal Rejection:** {format_date(report_info.get('Date of Appeal Rejection'))}")
            st.write(f"**Reason for Appeal Rejection:** {report_info.get('Reason for Appeal Rejection', '')}")
            st.write(f"**Reason for Rejection #3:** {report_info.get('Reason for Rejection_3', '')}")
            st.write(f"**# of Days:** {calculate_date_difference(report_info.get('Date Sent'), report_info.get('Date of Appeal Rejection'))}")
            
   
        else:
            st.warning("No report data found for this dataset.")
    else:
        st.info("Please select a dataset from the Search page")         


elif st.session_state.selected_tab == "Timeline":

    # Status Image Mapping
    status_images = {
        'Rejected': r"C:\Users\fstim\OneDrive\Remotasks\images\Status balls\Rejected Red Ball.png",
        'Review': r"C:\Users\fstim\OneDrive\Remotasks\images\Status balls\Review yellow ball.png",
        'Approved': r"C:\Users\fstim\OneDrive\Remotasks\images\Status balls\Approved - green ball.png",
        'Paid': r"C:\Users\fstim\OneDrive\Remotasks\images\Status balls\Paid purple ball.png",
        'Removed': r"C:\Users\fstim\OneDrive\Remotasks\images\Status balls\Removed - pink ball.png",
        'Appeal Rejected': r"C:\Users\fstim\OneDrive\Remotasks\images\Status balls\Appeal Rejected - brown ball.png",
        'DS submitted': r"C:\Users\fstim\OneDrive\Remotasks\images\Status balls\Lt blue ball submitted.png",
        'Appeal': r"C:\Users\fstim\OneDrive\Remotasks\images\Status balls\Submitted - orange ball.png"
    }

    # If a dataset is selected, filter the timeline
    if st.session_state.selected_report:
        timeline_df = timeline_df[timeline_df['Dataset Filename'] == st.session_state.selected_report]

    # Convert PERIOD to datetime and sort
    timeline_df['PERIOD'] = pd.to_datetime(timeline_df['PERIOD'])
    timeline_df = timeline_df.sort_values('PERIOD', ascending=False)
    timeline_df['PERIOD'] = timeline_df['PERIOD'].dt.strftime('%m-%d-%y')
    
    timeline_df['PERIOD'] = "📅 " + timeline_df['PERIOD']
    timeline_df['DS Status'] = "🛠 " + timeline_df['DS Status']
    

    # Ensure 'Status_Image' column exists
    timeline_df['Status_Image'] = timeline_df['DS Status'].map(lambda x: status_images.get(x.split(' ', 1)[1].strip(), None))

    # Display timeline with images
    st.markdown("<h2>📌 Timeline Overview</h2>", unsafe_allow_html=True)
    
     # Display timeline table with adjusted column widths and status images
    st.dataframe(
        timeline_df[['PERIOD', 'DS Status', 'Status_Image', 'Dataset Filename', 'Notes']],  # Include necessary columns
        use_container_width=True,
        hide_index=True,
        column_config={
            'PERIOD': st.column_config.TextColumn("Date", width=20),  # Adjust width for Date column
            'DS Status': st.column_config.TextColumn("Status"),  # Status column
            'Status_Image': st.column_config.ImageColumn("Status Image", width=20),  # Adjust width for Status Image column
            'Dataset Filename': st.column_config.TextColumn("Dataset", width=100),  # Adjust width for Dataset column
            'Notes': st.column_config.TextColumn("Notes", width=200)  # Adjust width for Notes column (no wrap here)
        }
    )


        
       # Dataset tracker 
elif st.session_state.selected_tab == "Datasets":
    # Get the dataset status from the master list
    dataset_status = master_list_df.groupby('Tracker File Name')['Status'].first()
    rejected_datasets = dataset_status[dataset_status == 'REJECTED'].index.tolist()
    approved_datasets = dataset_status[dataset_status == 'APPROVED'].index.tolist()

    # --- Approved Datasets Container ---
    st.markdown("""
        <div style='background-color: #DA8419; padding: 10px; color: white;'>
            <h3 style='margin: 0;'>Approved Datasets</h3>
        </div>
    """, unsafe_allow_html=True)

    if approved_datasets:
        for dataset_name in approved_datasets:
            st.write(dataset_name)
    else:
        st.info("No approved datasets found.")

    # --- Rejected Datasets Container ---
    st.markdown("""
        <div style='background-color: #DA8419; padding: 10px; color: white;'>
            <h3 style='margin: 0;'>Rejected Datasets</h3>
        </div>
    """, unsafe_allow_html=True)

    if rejected_datasets:
        for dataset_name in rejected_datasets:
            st.write(dataset_name)
    else:
        st.info("No rejected datasets found.")