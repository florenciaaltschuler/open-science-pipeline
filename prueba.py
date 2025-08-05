import os
import shutil
from rich import print
from pathlib import Path

def ask_and_copy_files(target_dir, category_name):
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
            else:
                print(f"[red]File {src} not found. Try again.[/red]")
    else:
        print(f"[yellow]{category_name.capitalize()} folder will be empty.[/yellow]")

def create_directory_structure(base_path):
    """Creates the main project structure under '/file'."""
    dirs_to_create = {
        "file/data/raw": "raw data",
        "file/data/processed": "processed data",
        "file/code/analysis": "analysis code",
        "file/code/src": "source code",
        "file/code/notebooks": "Jupyter notebooks",
        "file/code/env": "environment files",
        "file/results/figures": "figures",
        "file/results/tables": "tables",
        "docs": "documentation files",
        "output-report": "output reports"
    }

    # Create directories and ask to copy files into them
    for relative_path, category_name in dirs_to_create.items():
        dir_path = base_path / relative_path
        dir_path.mkdir(parents=True, exist_ok=True)
        print(f"[green]Created {dir_path}[/green]")
        ask_and_copy_files(dir_path, category_name)

def create_metadata_files(file_base_path):
    """Creates the metadata files (README.md, LICENSE, CITATION.cff, .gitignore)."""
    # README.md
    readme_path = file_base_path / "README.md"
    with open(readme_path, "w") as f:
        f.write("# Project Title\n\n## Description\n\n## How to Run\n")
    print(f"[cyan]Created {readme_path}[/cyan]")

    # .gitignore
    gitignore_path = file_base_path / ".gitignore"
    with open(gitignore_path, "w") as f:
        f.write("*.pyc\n__pycache__/\n.env\n")
    print(f"[cyan]Created {gitignore_path}[/cyan]")

    # LICENSE
    license_path = file_base_path / "LICENSE"
    with open(license_path, "w") as f:
        f.write("Creative Commons Attribution 4.0 International (CC BY 4.0)\n")
    print(f"[cyan]Created {license_path}[/cyan]")

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

def create_project_structure(project_name: str):
    print(f"[bold green]Creating project structure for '{project_name}'[/bold green]")

    base_path = Path(project_name)
    if base_path.exists():
        print(f"[red]Directory '{project_name}' already exists. Aborting.[/red]")
        return

    # Create the directory structure and ask for file inputs
    create_directory_structure(base_path)

    # Create metadata files in /file
    file_base_path = base_path / "file"
    create_metadata_files(file_base_path)

    print(f"[bold green]Project '{project_name}' structure created successfully![/bold green]")
