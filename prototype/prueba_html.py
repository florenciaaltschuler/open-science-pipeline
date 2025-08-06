import os
import shutil
from rich import print
from pathlib import Path
from datetime import datetime

def ask_and_copy_files(target_dir, category_name, report_data):
    """Asks user if they want to add files to a given category and copies them."""
    has_files = input(f"Do you have {category_name} files to add? (y/n): ").strip().lower()

    if has_files == 'y':
        while True:
            file_path = input(f"Enter the path to the {category_name} file (or 'done' to finish): ").strip()
            if file_path.lower() == 'done':
                break
            src = Path(file_path)
            if src.exists() and src.is_file():
                shutil.copy(src, target_dir)
                print(f"[green]Copied {src.name} to {target_dir}[/green]")
                report_data["added_files"].append(f"File {src.name} copied to {target_dir}")
            else:
                print(f"[red]File {src} not found. Try again.[/red]")
                report_data["errors"].append(f"File {src} not found")
    else:
        print(f"[yellow]{category_name.capitalize()} folder will be empty.[/yellow]")
        report_data["added_files"].append(f"{category_name.capitalize()} folder will be empty.")

def create_directory_structure(base_path, report_data):
    """Creates the main project structure under 'file' and outside."""
    dirs_to_create = {
        # These directories will go under the 'file' folder
        "file/data/raw": "raw data",
        "file/data/processed": "processed data",
        "file/code/analysis": "analysis code",
        "file/code/src": "source code",
        "file/code/notebooks": "Jupyter notebooks",
        "file/code/env": "environment files",
        "file/results/figures": "figures",
        "file/results/tables": "tables",
        
        # These folders will go outside of 'file' folder
        "docs": "documentation files",
        "output-report": "output reports"
    }

    # Create directories and ask to copy files into them
    for relative_path, category_name in dirs_to_create.items():
        dir_path = base_path / relative_path
        dir_path.mkdir(parents=True, exist_ok=True)
        report_data["created_folders"].append(f"Created {dir_path}")
        print(f"[green]Created {dir_path}[/green]")
        ask_and_copy_files(dir_path, category_name, report_data)

def create_metadata_files(file_base_path, report_data):
    """Creates the metadata files (README.md, LICENSE, CITATION.cff, .gitignore)."""
    # README.md
    readme_path = file_base_path / "README.md"
    with open(readme_path, "w") as f:
        f.write("# Project Title\n\n## Description\n\n## How to Run\n")
    print(f"[cyan]Created {readme_path}[/cyan]")
    report_data["created_files"].append(f"Created {readme_path}")

    # .gitignore
    gitignore_path = file_base_path / ".gitignore"
    with open(gitignore_path, "w") as f:
        f.write("*.pyc\n__pycache__/\n.env\n")
    print(f"[cyan]Created {gitignore_path}[/cyan]")
    report_data["created_files"].append(f"Created {gitignore_path}")

    # LICENSE
    license_path = file_base_path / "LICENSE"
    with open(license_path, "w") as f:
        f.write("Creative Commons Attribution 4.0 International (CC BY 4.0)\n")
    print(f"[cyan]Created {license_path}[/cyan]")
    report_data["created_files"].append(f"Created {license_path}")

    # CITATION.cff
    citation_path = file_base_path / "CITATION.cff"
    with open(citation_path, "w") as f:
        f.write(
            "cff-version: 1.2.0\n"
            "authors:\n"
            "  - family-names: Doe\n"
            "    given-names: Jane\n"
            "message: 'If you use this, please cite it.'\n"
            "title: 'Project Title'\n"
        )
    print(f"[cyan]Created {citation_path}[/cyan]")
    report_data["created_files"].append(f"Created {citation_path}")

def generate_report(report_data, project_name):
    """Generates a report and saves it as a TXT file in output-report."""
    # Ensure output-report folder exists
    output_txt = Path(project_name) / "output-report" / "report.txt"
    
    # Create report content
    report_content = f"Project: {project_name}\n"
    report_content += f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    
    report_content += "Created Folders:\n"
    for folder in report_data["created_folders"]:
        report_content += f"  - {folder}\n"
    
    report_content += "\nCreated Files:\n"
    for file in report_data["created_files"]:
        report_content += f"  - {file}\n"
    
    report_content += "\nAdded Files:\n"
    for file in report_data["added_files"]:
        report_content += f"  - {file}\n"
    
    report_content += "\nErrors:\n"
    for error in report_data["errors"]:
        report_content += f"  - {error}\n"

    # Save the report content to a text file
    output_txt.parent.mkdir(parents=True, exist_ok=True)  # Ensure output-report folder exists
    with open(output_txt, "w") as f:
        f.write(report_content)

    print(f"[cyan]Report generated at {output_txt}[/cyan]")

def create_project_structure(project_name: str):
    print(f"[bold green]Creating project structure for '{project_name}'[/bold green]")

    base_path = Path(project_name)
    if base_path.exists():
        print(f"[red]Directory '{project_name}' already exists. Aborting.[/red]")
        return

    # Initialize the report data
    report_data = {
        "created_folders": [],
        "created_files": [],
        "added_files": [],
        "errors": []
    }

    # Create the directory structure and ask for file inputs
    create_directory_structure(base_path, report_data)

    # Create metadata files in /file
    file_base_path = base_path / "file"
    create_metadata_files(file_base_path, report_data)

    # Generate the report (TXT)
    generate_report(report_data, project_name)

    print(f"[bold green]Project '{project_name}' structure created successfully![/bold green]")
