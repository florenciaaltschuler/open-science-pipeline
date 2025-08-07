import streamlit as st
from pathlib import Path
from utils.streamlit_app_utils import create_directory_structure, upload_files, save_files, create_zip_folder
from utils.validator_class import OpenScienceValidator

def main():
    # Set the page config to set a custom logo as the favicon
    logo_path = Path("image/logo.png")  # Ruta del logo
    st.set_page_config(page_title="FAIR Science Project Manager", page_icon=str(logo_path))  # Usamos el logo como ícono de la página

    # Mostrar el logo en la parte superior de la página
    st.image(str(logo_path), width=200)  # Puedes ajustar el tamaño del logo

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
        
        uploaded_code_files = upload_files("Participant (01_participant)", allowed_types=["csv", "tsv", "xlsx", "txt"])
        if uploaded_code_files:
            save_files(uploaded_code_files, base_path / "01_docs/01_participant")
        
        uploaded_code_files = upload_files("Ethics (02_ethics)")
        if uploaded_code_files:
            save_files(uploaded_code_files, base_path / "01_docs/02_ethics")

        uploaded_code_files = upload_files("Data Management Plan (03_dmp)")
        if uploaded_code_files:
            save_files(uploaded_code_files, base_path / "01_docs/03_dmp")

        uploaded_code_files = upload_files("Preregistration (04_prereg)")
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
        
        uploaded_code_files = upload_files("Analyses scripts (03_analyses)")
        if uploaded_code_files:
            save_files(uploaded_code_files, base_path / "03_scripts/03_analyses")

        st.header("Results (04_results)")
        uploaded_result_files = upload_files("Output (01_output)")
        if uploaded_result_files:
            save_files(uploaded_result_files, base_path / "04_results/01_output")

        uploaded_result_files = upload_files("Figures (02_figures)", allowed_types=["jpg", "png", "svg", "pdf"])
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
    
    # Check if we're showing results
    if 'show_validation_results' in st.session_state and st.session_state.show_validation_results:
        display_validation_results()
    else:
        show_validation_input()


def show_validation_input():
    """Show the input interface for validation"""
    # Option 1: Text input for path
    project_path = st.text_input(
        "Enter the path to your project directory",
        placeholder="/path/to/your/project"
    )
    
    # Option 2: Folder picker
    st.markdown("**OR**")
    
    # Upload a zip file to validate
    uploaded_zip = st.file_uploader("Upload project as ZIP file", type=['zip'])
    
    if st.button("🚀 Run Validation", type="primary"):
        if project_path and Path(project_path).exists():
            run_validation(project_path)
            st.session_state.show_validation_results = True
            st.session_state.is_temp_project = False
            st.rerun()
        elif uploaded_zip:
            # Extract to a persistent location instead of temp
            import zipfile
            import os
            
            # Create a persistent temp directory
            temp_base = Path("temp_validations")
            temp_base.mkdir(exist_ok=True)
            
            # Create unique folder for this validation
            import time
            temp_dir = temp_base / f"validation_{int(time.time())}"
            temp_dir.mkdir(exist_ok=True)
            
            # Extract zip
            with zipfile.ZipFile(uploaded_zip, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)
            
            # Find the project root
            project_dirs = [d for d in temp_dir.iterdir() if d.is_dir()]
            if project_dirs:
                project_path = str(project_dirs[0])
                run_validation(project_path)
                st.session_state.show_validation_results = True
                st.session_state.is_temp_project = True
                st.session_state.temp_project_path = project_path
                st.rerun()
            else:
                st.error("Could not find project directory in uploaded ZIP")
        else:
            st.error("Please provide a valid project path or upload a ZIP file")


def display_validation_results():
    """Display the validation results"""
    if 'validation_results' not in st.session_state:
        st.error("No validation results found")
        return
    
    results = st.session_state.validation_results
    
    # Add a back button
    if st.button("← Back to validation input"):
        st.session_state.show_validation_results = False
        st.rerun()
    
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
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📄 Generate PDF Report", type="primary"):
            generate_pdf_report()
    
    with col2:
        if 'pdf_generated' in st.session_state and st.session_state.pdf_generated:
            with open(st.session_state.pdf_path, "rb") as pdf_file:
                st.download_button(
                    label="📥 Download PDF Report",
                    data=pdf_file.read(),
                    file_name="validation_report.pdf",
                    mime="application/pdf",
                    type="secondary"
                )


def run_validation(project_path):
    """Run the validation and store results in session state"""
    validator = OpenScienceValidator(project_path)
    
    # Show progress
    with st.spinner("🔍 Validating project structure..."):
        results = validator.validate_structure()
    
    # Store everything in session state
    st.session_state.validation_results = results
    st.session_state.current_validator = validator
    st.session_state.current_project_path = project_path
    st.session_state.pdf_generated = False


def generate_pdf_report():
    """Generate the PDF report"""
    if 'current_validator' in st.session_state and 'current_project_path' in st.session_state:
        # For temp projects, save PDF to a different location
        if st.session_state.get('is_temp_project', False):
            # Save to current directory instead
            report_path = Path("validation_report.pdf")
        else:
            report_path = Path(st.session_state.current_project_path) / "validation_report.pdf"
        
        with st.spinner("Generating PDF report..."):
            st.session_state.current_validator.generate_pdf_report(report_path)
            st.session_state.pdf_path = report_path
            st.session_state.pdf_generated = True
            st.success("✅ PDF Report generated successfully!")
            
            # Clean up temp files after generating PDF
            if st.session_state.get('is_temp_project', False):
                # Optional: clean up the temp directory
                import shutil
                try:
                    shutil.rmtree(Path(st.session_state.temp_project_path).parent)
                except:
                    pass
            
            st.rerun()


# Run the app
if __name__ == "__main__":
    main()
