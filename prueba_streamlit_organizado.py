import os
import shutil
import streamlit as st
from pathlib import Path
import zipfile
from tkinter import filedialog
from tkinter import Tk

# Helper function to create directory structure
def create_directory_structure(base_path):
    """Create the project folder structure under the given base path."""
    dirs_to_create = {
        "01_docs": {
            "01_participant": "Demographics",
            "02_ethics": "Ethics approval documents",
            "03_dmn": "Project-specific design materials or domain model notes",
            "04_prereg": "Pre-registration documents"
        },
        "02_data": {
            "01_raw": "Raw data",
            "02_preproc": "Preprocessed data"
        },
        "03_scripts": {
            "01_exp": "Experimental scripts",
            "02_prep": "Data preparation scripts",
            "03_analysis": "Analysis scripts"
        },
        "04_results": {
            "01_output": "Raw output files",
            "02_figures": "Figures and visualizations",
            "03_tables": "Tables of results"
        },
        "05_meta": "Metadata and supplementary information"
    }
    
    # Create directories based on the structure
    for parent_dir, sub_dirs in dirs_to_create.items():
        parent_path = base_path / parent_dir
        parent_path.mkdir(parents=True, exist_ok=True)
        
        # If the sub_dir is a dictionary, create subfolders under the parent directory
        if isinstance(sub_dirs, dict):
            for sub_dir, description in sub_dirs.items():
                sub_path = parent_path / sub_dir
                sub_path.mkdir(parents=True, exist_ok=True)
                st.write(f"Created subfolder: {sub_path} - {description}")
        else:
            sub_path = parent_path / sub_dirs
            sub_path.mkdir(parents=True, exist_ok=True)
            st.write(f"Created folder: {sub_path}")

# Function to handle file uploads
def upload_files(category_name):
    """Upload files for the given category."""
    st.write(f"Upload {category_name} files here:")
    uploaded_files = st.file_uploader(f"Choose {category_name} files", accept_multiple_files=True)
    return uploaded_files

# Function to save files into a specific folder
def save_files(uploaded_files, target_folder):
    """Save uploaded files into the specified folder."""
    for uploaded_file in uploaded_files:
        # Create the folder path
        target_path = target_folder / uploaded_file.name
        # Save the file
        with open(target_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.write(f"Saved file: {uploaded_file.name} to {target_folder}")

# Function to organize and compress the files into a zip folder
def create_zip_folder(base_path, project_name):
    """Create a zip file of the project folder."""
    zip_filename = f"{project_name}.zip"
    zip_filepath = base_path / zip_filename

    # Create a Zip file with the entire project folder
    with zipfile.ZipFile(zip_filepath, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(base_path):
            for file in files:
                zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), base_path))
    
    st.write(f"Created zip file: {zip_filepath}")
    return zip_filepath

# Streamlit app structure
def streamlit_app():
    st.title("Project File Upload and Organization")
    
    # Ask for the project name
    project_name = st.text_input("Enter project name")
    
    if project_name:
        # Define base project folder
        base_path = Path(f"./{project_name}")
        
        # Create the folder structure
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
