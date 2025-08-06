# utils/streamlit_app_utils.py

import os
import shutil
import streamlit as st
from pathlib import Path
import zipfile

# Helper function to create directory structure
def create_directory_structure(base_path):
    """Create the project folder structure under the given base path."""
    dirs_to_create = {
        "01_docs": {
            "01_participant": "Demographics",
            "02_ethics": "Ethics approval documents",
            "03_dmp": "Data Management Plan",
            "04_prereg": "Preregistration documents"
        },
        "02_data": {
            "01_raw": "Raw data",
            "02_preproc": "Preprocessed data"
        },
        "03_scripts": {
            "01_exp": "Experimental scripts",
            "02_prep": "Data preparation scripts",
            "03_analyses": "Analyses scripts"
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

    # Create a Zip file with the entire project folder (excluding the zip file itself)
    with zipfile.ZipFile(zip_filepath, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(base_path):
            for file in files:
                # Exclude the zip file from being added to the zip
                if file != zip_filename:  # Ensure the zip file isn't added
                    zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), base_path))
            # Also add directories if empty
            for dir in dirs:
                dir_path = os.path.join(root, dir)
                if dir != zip_filename:  # Ensure the zip file's directory isn't included
                    zipf.write(dir_path, os.path.relpath(dir_path, base_path))

    st.write(f"Created zip file: {zip_filepath}")
    return zip_filepath
