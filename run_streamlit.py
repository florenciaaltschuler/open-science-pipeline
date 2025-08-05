# run_streamlit.py
from utils.streamlit_app_utils import create_directory_structure, upload_files, save_files, create_zip_folder
import streamlit as st
from pathlib import Path

# Streamlit app structure
def streamlit_app():
    st.title("Project File Upload and Organization")
    
    # Ask for the project name
    project_name = st.text_input("Enter project name")
    
    if project_name:
        # Define base project folder
        base_path = Path(f"./{project_name}")
        
        # Create the folder structure (even if no files are uploaded)
        create_directory_structure(base_path)
        
        # Upload files for each subfolder, showing uploaders inside each subfolder's expander
        st.header("Documentation (01_docs)")
        uploaded_code_files = upload_files("Participant (01_participant)")
        if uploaded_code_files:
            save_files(uploaded_code_files, base_path / "01_docs/01_participant")
        
        uploaded_code_files = upload_files("Ethics (02_ethics)")
        if uploaded_code_files:
            save_files(uploaded_code_files, base_path / "01_docs/02_ethics")

        uploaded_code_files = upload_files("Domain Model (03_dmn)")
        if uploaded_code_files:
            save_files(uploaded_code_files, base_path / "01_docs/03_dmn")

        uploaded_code_files = upload_files("Pre-registration (04_prereg)")
        if uploaded_code_files:
            save_files(uploaded_code_files, base_path / "01_docs/04_prereg")

        st.header("Data (02_data)")
        uploaded_data_files = upload_files("Raw data (01_raw)")
        if uploaded_data_files:
            save_files(uploaded_data_files, base_path / "02_data/01_raw")
        
        uploaded_data_files = upload_files("Preprocessed data (02_preproc)")
        if uploaded_data_files:
            save_files(uploaded_data_files, base_path / "02_data/02_preproc")

        st.header("Scripts (03_scripts)")
        uploaded_code_files = upload_files("Experimental scripts (01_exp)")
        if uploaded_code_files:
            save_files(uploaded_code_files, base_path / "03_scripts/01_exp")
        
        uploaded_code_files = upload_files("Data preparation scripts (02_prep)")
        if uploaded_code_files:
            save_files(uploaded_code_files, base_path / "03_scripts/02_prep")
        
        uploaded_code_files = upload_files("Analysis scripts (03_analysis)")
        if uploaded_code_files:
            save_files(uploaded_code_files, base_path / "03_scripts/03_analysis")

        st.header("Results (04_results)")
        uploaded_result_files = upload_files("Output (01_output)")
        if uploaded_result_files:
            save_files(uploaded_result_files, base_path / "04_results/01_output")

        uploaded_result_files = upload_files("Figures (02_figures)")
        if uploaded_result_files:
            save_files(uploaded_result_files, base_path / "04_results/02_figures")

        uploaded_result_files = upload_files("Tables (03_tables)")
        if uploaded_result_files:
            save_files(uploaded_result_files, base_path / "04_results/03_tables")

        st.header("Metadata (05_meta)")
        uploaded_result_files = upload_files("Metadata")
        if uploaded_result_files:
            save_files(uploaded_result_files, base_path / "05_meta")
        
        # Organize the project into a zip file for download
        zip_filepath = create_zip_folder(base_path, project_name)
        
        # Provide a download link for the zip file
        st.download_button(
            label="Download Project Files",
            data=open(zip_filepath, "rb"),
            file_name=zip_filepath.name,
            mime="application/zip"
        )

# Run the app
if __name__ == "__main__":
    streamlit_app()
