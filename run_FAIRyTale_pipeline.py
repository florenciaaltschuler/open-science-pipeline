import streamlit as st
from pathlib import Path
from utils.streamlit_app_utils import create_directory_structure, upload_files, save_files, create_zip_folder
from utils.validator_class import OpenScienceValidator


def main():
    st.set_page_config(page_title="FAIR Science Project Manager", page_icon="🔬")
    st.title("🔬 FAIR Science Project Manager")
    st.markdown("---")
    
    # Main menu selection
    mode = st.radio(
        "What would you like to do?",
        ["🏗️ Create New Project", "✅ Validate Existing Project"],
        horizontal=True
    )
    
    st.markdown("---")
    
    if mode == "🏗️ Create New Project":
        create_project_interface()
    else:
        validate_project_interface()


def create_project_interface():
    """Interface for creating a new project"""
    st.header("📁 Create New Open Science Project")
    
    # Ask for the project name
    project_name = st.text_input("Enter project name")
    
    if project_name:
        # Define base project folder
        base_path = Path(f"./{project_name}")
        
        # Create the folder structure (even if no files are uploaded)
        create_directory_structure(base_path)
        
        # Upload files for each subfolder
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


def validate_project_interface():
    """Interface for validating an existing project"""
    st.header("🔍 Validate Existing Project")
    
    # Option 1: Text input for path
    project_path = st.text_input(
        "Enter the path to your project directory",
        placeholder="/path/to/your/project"
    )
    
    # Option 2: Folder picker (if you want to be fancy)
    st.markdown("**OR**")
    
    # Upload a zip file to validate
    uploaded_zip = st.file_uploader("Upload project as ZIP file", type=['zip'])
    
    if st.button("🚀 Run Validation", type="primary"):
        if project_path and Path(project_path).exists():
            run_validation(project_path)
        elif uploaded_zip:
            # Extract and validate the zip
            import tempfile
            import zipfile
            
            with tempfile.TemporaryDirectory() as temp_dir:
                # Extract zip
                with zipfile.ZipFile(uploaded_zip, 'r') as zip_ref:
                    zip_ref.extractall(temp_dir)
                
                # Find the project root (first directory in temp_dir)
                project_dirs = [d for d in Path(temp_dir).iterdir() if d.is_dir()]
                if project_dirs:
                    run_validation(str(project_dirs[0]))
                else:
                    st.error("Could not find project directory in uploaded ZIP")
        else:
            st.error("Please provide a valid project path or upload a ZIP file")


def run_validation(project_path):
    """Run the validation and display results in Streamlit"""
    validator = OpenScienceValidator(project_path)
    
    # Show progress
    with st.spinner("🔍 Validating project structure..."):
        results = validator.validate_structure()
    
    # Display results in Streamlit UI
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("✅ Passed", len(results["passed"]))
    with col2:
        st.metric("❌ Failed", len(results["failed"]))
    with col3:
        st.metric("⚠️ Warnings", len(results["warnings"]))
    
    # Show detailed results
    if results["failed"]:
        st.error("### Failed Checks")
        for item in results["failed"]:
            st.write(f"- {item}")
    
    if results["warnings"]:
        st.warning("### Warnings")
        for item in results["warnings"]:
            st.write(f"- {item}")
    
    if results["passed"]:
        with st.expander("✅ Passed Checks", expanded=False):
            for item in results["passed"]:
                st.write(f"- {item}")
    
    # FAIR Recommendations
    st.info("### FAIR Principle Recommendations")
    for rec in results["recommendations"]:
        st.write(f"- {rec}")
    
    # Generate PDF report
    if st.button("📄 Generate PDF Report"):
        report_path = Path(project_path) / "validation_report.pdf"
        validator.generate_pdf_report(report_path)
        
        # Offer download
        with open(report_path, "rb") as pdf_file:
            st.download_button(
                label="Download Validation Report",
                data=pdf_file.read(),
                file_name="validation_report.pdf",
                mime="application/pdf"
            )


# Run the app
if __name__ == "__main__":
    main()
