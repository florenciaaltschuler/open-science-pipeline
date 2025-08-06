import os
from pathlib import Path
from datetime import datetime
from rich import print
from rich.table import Table
from rich.console import Console
from fpdf import FPDF, XPos, YPos
import json


class OpenScienceValidator:
    def __init__(self, project_path):
        self.project_path = Path(project_path)
        self.validation_results = {
            "passed": [],
            "failed": [],
            "warnings": [],
            "recommendations": []
        }

        # Required files (failures if missing)
        self.required_files = {
            "README.md": "Project overview with badges and quick-start guide"
        }

        # Recommended files (warnings if missing)
        self.recommended_files = {
            "LICENSE": "Permission & reuse information (recommend CC-BY-4.0)",
            "CITATION.cff": "How to cite the dataset and code"
        }

        # Required directories (failures if missing)
        self.required_dirs = {
            "01_docs": "Documentation related to the project. Protocols, consent, ethics, DMP",
            "01_docs/01_participants": "Demographics and participant data",
            "02_data": "Data collected and processed for the study (never edit in place)",
            "02_data/02_preproc": "Preprocessed and/or cleaned data",
            "03_scripts": "Code used across various stages of the research process",
            "03_scripts/02_prep": "Data preparation scripts",
            "03_scripts/03_analysis": "Statistical or computational analysis scripts",
            "04_results": "Outputs generated from analysis (stats tables, final figs)",
            "05_meta": "Metadata and supplementary information for reproducibility and FAIR principles"
        }

        # Recommended directories (warnings if missing)
        self.recommended_dirs = {
            "01_docs/02_ethics": "Ethics approval documents",
            "01_docs/03_dmp": "Data management plan",
            "01_docs/04_prereg": "Pre-registration documents",
            "02_data/01_raw": "Unaltered, original raw data",
            "03_scripts/01_exp": "Experimental scripts for data collection",
            "04_results/01_output": "Raw output files from analysis scripts",
            "04_results/02_figures": "Visualizations such as plots, charts, or brain maps",
            "04_results/03_tables": "Tabular data results"
        }

    def validate_structure(self):
        """Main validation function"""
        console = Console()
        console.print("[bold cyan]🔍 Starting Open Science Project Validation...[/bold cyan]\n")

        # Check if project exists
        if not self.project_path.exists():
            self.validation_results["failed"].append(f"Project path '{self.project_path}' does not exist")
            return

        # Validate files
        self._validate_files()

        # Validate directories
        self._validate_directories()

        # Check for additional best practices
        self._check_best_practices()

        # Generate FAIR recommendations
        self._generate_fair_recommendations()

        # Display results
        self._display_results()

        return self.validation_results

    def _validate_files(self):
        """Check for required and recommended files"""
        # Check required files (failures if missing)
        for file_name, description in self.required_files.items():
            file_path = self.project_path / file_name
            if file_path.exists():
                self.validation_results["passed"].append(f"✓ Found {file_name}")

                # Additional checks for specific files
                if file_name == "README.md":
                    self._check_readme_content(file_path)
            else:
                self.validation_results["failed"].append(
                    f"✗ Missing required file {file_name}: {description}"
                )

        # Check recommended files (warnings if missing)
        for file_name, description in self.recommended_files.items():
            file_path = self.project_path / file_name
            if file_path.exists():
                self.validation_results["passed"].append(f"✓ Found {file_name}")

                # Additional checks for specific files
                if file_name == "LICENSE":
                    self._check_license_content(file_path)
                elif file_name == "CITATION.cff":
                    self._check_citation_content(file_path)
            else:
                self.validation_results["warnings"].append(
                    f"⚠ Missing recommended file {file_name}: {description}"
                )

    def _validate_directories(self):
        """Check for required and recommended directory structure"""
        # Check required directories (failures)
        for dir_path, description in self.required_dirs.items():
            full_path = self.project_path / dir_path
            if full_path.exists() and full_path.is_dir():
                # Check if directory is empty
                if not any(full_path.iterdir()):
                    self.validation_results["warnings"].append(
                        f"⚠ Required directory '{dir_path}' exists but is empty"
                    )
                else:
                    self.validation_results["passed"].append(f"✓ Found {dir_path}/")
                    # Additional content checks for specific directories
                    self._check_directory_contents(dir_path, full_path)
            else:
                self.validation_results["failed"].append(
                    f"✗ Missing required directory '{dir_path}': {description}"
                )

        # Check recommended directories (warnings)
        for dir_path, description in self.recommended_dirs.items():
            full_path = self.project_path / dir_path
            if full_path.exists() and full_path.is_dir():
                if not any(full_path.iterdir()):
                    self.validation_results["warnings"].append(
                        f"⚠ Recommended directory '{dir_path}' exists but is empty"
                    )
                else:
                    self.validation_results["passed"].append(f"✓ Found {dir_path}/")
                    # Additional content checks
                    self._check_directory_contents(dir_path, full_path)
            else:
                self.validation_results["warnings"].append(
                    f"⚠ Missing recommended directory '{dir_path}': {description}"
                )

    def _check_directory_contents(self, dir_path, full_path):
        """Check specific directory contents and naming conventions"""

        # Check participant info for data files
        if dir_path == "01_docs/01_participants":
            data_files = list(full_path.glob("*.csv")) + list(full_path.glob("*.tsv"))
            if not data_files:
                self.validation_results["warnings"].append(
                    f"⚠ No CSV or TSV files found in {dir_path}. Expected participant data files."
                )
            else:
                self.validation_results["passed"].append(
                    f"✓ Found {len(data_files)} data file(s) in {dir_path}"
                )

        # Check data directories for proper structure and naming
        elif dir_path.startswith("02_data"):
            self._check_data_directory(dir_path, full_path)

        # Check scripts directories for code files
        elif dir_path == "03_scripts/02_prep":
            code_files = list(full_path.glob("*.py")) + list(full_path.glob("*.R")) + list(full_path.glob("*.ipynb")) + list(full_path.glob("*.m"))
            if not code_files:
                self.validation_results["warnings"].append(
                    f"⚠ No script files found in {dir_path}. Expected .py, .R, .ipynb, or .m files."
                )

        elif dir_path == "03_scripts/03_analysis":
            code_files = list(full_path.glob("*.py")) + list(full_path.glob("*.R")) + list(full_path.glob("*.ipynb")) + list(full_path.glob("*.m"))
            if not code_files:
                self.validation_results["warnings"].append(
                    f"⚠ No analysis scripts found in {dir_path}. Expected analysis code files."
                )

        # Check results directories
        elif dir_path == "04_results/02_figures":
            fig_files = list(full_path.glob("*.png")) + list(full_path.glob("*.jpg")) + list(full_path.glob("*.pdf")) + list(full_path.glob("*.svg"))
            if not fig_files:
                self.validation_results["warnings"].append(
                    f"⚠ No figure files found in {dir_path}. Expected .png, .jpg, .pdf, or .svg files."
                )

        elif dir_path == "04_results/03_tables":
            table_files = list(full_path.glob("*.csv")) + list(full_path.glob("*.xlsx")) + list(full_path.glob("*.txt"))
            if not table_files:  # This line is incorrectly indented!
                self.validation_results["warnings"].append(
                    f"⚠ No table files found in {dir_path}. Expected .csv, .xlsx, or .txt files."
                )

    def _check_data_directory(self, dir_path, full_path):
        """Check data directory structure and naming conventions"""

        # First, check if there are any folders in the data directory
        subdirs = [d for d in full_path.iterdir() if d.is_dir()]

        if not subdirs:
            self.validation_results["warnings"].append(
                f"⚠ No subdirectories found in {dir_path}. Expected 'raw' and 'preproc' folders."
            )
            return

        # Check if we have raw and preproc folders
        has_raw = False
        has_preproc = False
        raw_dirs = []
        preproc_dirs = []

        for subdir in subdirs:
            if "raw" in subdir.name.lower():
                has_raw = True
                raw_dirs.append(subdir)
            if "preproc" in subdir.name.lower():
                has_preproc = True
                preproc_dirs.append(subdir)

        # Warn if missing expected directories
        if not has_raw:
            self.validation_results["warnings"].append(
                f"⚠ No 'raw' data directory found in {dir_path}. Consider adding a folder containing 'raw' in its name."
            )

        if not has_preproc:
            self.validation_results["warnings"].append(
                f"⚠ No 'preproc' data directory found in {dir_path}. Consider adding a folder containing 'preproc' in its name."
            )

        # Now check the second level - subdirectories within raw and preproc
        for raw_dir in raw_dirs:
            self._check_data_subdirectory(raw_dir, "raw")

        for preproc_dir in preproc_dirs:
            self._check_data_subdirectory(preproc_dir, "preprocessed")

    def _check_data_subdirectory(self, data_dir, data_type):
        """Check subdirectories within raw/preproc folders"""

        # Get all items in this directory
        items = list(data_dir.iterdir())
        subdirs = [d for d in items if d.is_dir()]
        files = [f for f in items if f.is_file()]

        # Check if directory is empty
        if not items:
            self.validation_results["warnings"].append(
                f"⚠ {data_type.capitalize()} data directory '{data_dir.name}' is empty."
            )
            return

        # If there are subdirectories, check their naming convention
        if subdirs:
            # Expected naming patterns for data subdirectories (BIDS-like)
            expected_patterns = {
                "sub-": "subject/participant folders (e.g., sub-01, sub-002)",
                "ses-": "session folders (e.g., ses-01, ses-pre, ses-post)",
                "task-": "task-based data (e.g., task-rest, task-nback)",
                "run-": "run numbers (e.g., run-01, run-02)"
            }

            follows_convention = False
            for subdir in subdirs:
                for pattern in expected_patterns:
                    if subdir.name.startswith(pattern):
                        follows_convention = True
                        break

            if not follows_convention:
                self.validation_results["warnings"].append(
                    f"⚠ Subdirectories in {data_dir.name} don't follow recommended naming convention. "
                    f"Consider using: {', '.join(expected_patterns.keys())}"
                )

            # Check if subdirectories have content
            empty_subdirs = []
            for subdir in subdirs:
                if not any(subdir.iterdir()):
                    empty_subdirs.append(subdir.name)

            if empty_subdirs:
                self.validation_results["warnings"].append(
                    f"⚠ Empty subdirectories in {data_dir.name}: {', '.join(empty_subdirs)}"
                )

        # Check for data files
        data_extensions = ['.csv', '.tsv', '.json', '.npy', '.mat', '.h5', '.hdf5', '.parquet']
        data_files = []

        # Check both in current directory and subdirectories
        for ext in data_extensions:
            data_files.extend(list(data_dir.glob(f"*{ext}")))
            data_files.extend(list(data_dir.glob(f"**/*{ext}")))

        if not data_files:
            self.validation_results["warnings"].append(
                f"⚠ No data files found in {data_dir.name} or its subdirectories. "
                f"Expected files with extensions: {', '.join(data_extensions)}"
            )
        else:
            self.validation_results["passed"].append(
                f"✓ Found {len(data_files)} data file(s) in {data_dir.name}"
            )

        # Check for documentation (only for raw data)
        if data_type == "raw":
            has_readme = (data_dir / "README.md").exists() or (data_dir / "README.txt").exists()
            has_dict = any(f.name.lower() in ['data_dictionary.csv', 'data_dict.csv', 'codebook.csv'] for f in data_dir.glob("*"))

            if not has_readme:
                self.validation_results["warnings"].append(
                    f"⚠ No README found in {data_dir.name}. Consider adding data documentation."
                )

            if not has_dict:
                self.validation_results["warnings"].append(
                    f"⚠ No data dictionary found in {data_dir.name}. Consider adding a codebook or data_dictionary.csv"
                )

    def _check_readme_content(self, readme_path):
        """Check README.md for key sections"""
        with open(readme_path, 'r') as f:
            content = f.read().lower()

        sections = ["description", "installation", "usage", "citation", "license"]
        missing_sections = []

        for section in sections:
            if section not in content:
                missing_sections.append(section)

        if missing_sections:
            self.validation_results["warnings"].append(
                f"⚠ README.md missing sections: {', '.join(missing_sections)}"
            )

    def _check_license_content(self, license_path):
        """Check if license is CC-BY-4.0 or similar"""
        with open(license_path, 'r') as f:
            content = f.read().lower()

        if "cc" in content or "creative commons" in content:
            if "by" in content and "4.0" in content:
                self.validation_results["passed"].append("✓ License appears to be CC-BY-4.0")
            else:
                self.validation_results["warnings"].append(
                    "⚠ License is Creative Commons but not CC-BY-4.0"
                )
        else:
            self.validation_results["warnings"].append(
                "⚠ Consider using CC-BY-4.0 for open science compliance"
            )

    def _check_citation_content(self, citation_path):
        """Check CITATION.cff format"""
        with open(citation_path, 'r') as f:
            content = f.read()

        required_fields = ["cff-version", "authors", "title", "message"]
        missing_fields = []

        for field in required_fields:
            if field not in content:
                missing_fields.append(field)

        if missing_fields:
            self.validation_results["warnings"].append(
                f"⚠ CITATION.cff missing fields: {', '.join(missing_fields)}"
            )

    def _check_best_practices(self):
        """Check for additional best practices"""
        # Check for .gitignore
        if (self.project_path / ".gitignore").exists():
            self.validation_results["passed"].append("✓ Found .gitignore")
        else:
            self.validation_results["warnings"].append(
                "⚠ Consider adding .gitignore for version control"
            )

        # Check for requirements.txt or environment.yml in the right place
        env_files = ["requirements.txt", "environment.yml", "pyproject.toml"]
        found_env = False

        # Check in root
        for env_file in env_files:
            if (self.project_path / env_file).exists():
                found_env = True
                self.validation_results["passed"].append(f"✓ Found {env_file}")
                break

        # Check in scripts directory
        if not found_env:
            for env_file in env_files:
                if (self.project_path / "03_scripts" / env_file).exists():
                    found_env = True
                    self.validation_results["passed"].append(f"✓ Found {env_file} in 03_scripts/")
                    break

        if not found_env:
            self.validation_results["warnings"].append(
                "⚠ No environment specification found (requirements.txt, environment.yml, etc.)"
            )
        # Add check for data documentation
        data_docs = ["data_dictionary.csv", "codebook.csv", "variables.csv"]
        found_data_doc = False

        for doc in data_docs:
            if (self.project_path / "02_data" / doc).exists() or \
               (self.project_path / "05_meta" / doc).exists():
                found_data_doc = True
                self.validation_results["passed"].append(f"✓ Found data documentation: {doc}")
                break

        if not found_data_doc:
            self.validation_results["warnings"].append(
                "⚠ No data dictionary or codebook found. Consider adding variable descriptions."
            )

    def _generate_fair_recommendations(self):
        """Generate FAIR principle recommendations"""
        self.validation_results["recommendations"].extend([
            "📊 FINDABLE: Add persistent identifiers (DOI) when publishing",
            "🔓 ACCESSIBLE: Ensure data is in open formats (CSV, JSON, not proprietary)",
            "🔄 INTEROPERABLE: Use standard vocabularies and include data dictionaries",
            "♻️  REUSABLE: Include clear licensing and detailed provenance metadata"
        ])

        # Specific recommendations based on findings
        if any("01_raw" in warning for warning in self.validation_results["warnings"]):
            self.validation_results["recommendations"].append(
                "💡 Create 02_data/01_raw/ to preserve original data (never modify!)"
            )

        if any("LICENSE" in warning for warning in self.validation_results["warnings"]):
            self.validation_results["recommendations"].append(
                "📜 Add a LICENSE file (recommend CC-BY-4.0 for open science)"
            )

        if any("CITATION.cff" in warning for warning in self.validation_results["warnings"]):
            self.validation_results["recommendations"].append(
                "📚 Add CITATION.cff to make your work easily citable"
            )

    def _display_results(self):
        """Display validation results in console"""
        console = Console()

        # Summary table
        table = Table(title="Validation Summary")
        table.add_column("Status", style="cyan", no_wrap=True)
        table.add_column("Count", justify="right")

        table.add_row("✓ Passed", str(len(self.validation_results["passed"])))
        table.add_row("✗ Failed", str(len(self.validation_results["failed"])))
        table.add_row("⚠ Warnings", str(len(self.validation_results["warnings"])))

        console.print(table)
        console.print()

        # Detailed results
        if self.validation_results["failed"]:
            console.print("[bold red]Failed Checks:[/bold red]")
            for item in self.validation_results["failed"]:
                console.print(f"  {item}")
            console.print()

        if self.validation_results["warnings"]:
            console.print("[bold yellow]Warnings:[/bold yellow]")
            for item in self.validation_results["warnings"]:
                console.print(f"  {item}")

    def generate_pdf_report(self, output_path="validation_report.pdf"):
        """Generate a PDF report of validation results"""
        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)  # Add this

        # Helper function to clean Unicode characters
        def clean_text(text):
            # Remove common Unicode symbols
            replacements = {
                '✓': '[PASS]',
                '✗': '[FAIL]',
                '⚠': '[WARN]',
                '📊': '[F]',
                '🔓': '[A]',
                '🔄': '[I]',
                '♻️': '[R]',
                '💡': '[TIP]',
                '📜': '[LICENSE]',  # Add this line
                '📚': '[CITE]'      # Add this line too for CITATION.cff
            }
            for unicode_char, replacement in replacements.items():
                text = text.replace(unicode_char, replacement)
            return text

        # Use helvetica directly (it's a core font)
        pdf.set_font("helvetica", "B", 16)

        # Title
        pdf.cell(0, 10, "Open Science Project Validation Report", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
        pdf.set_font("helvetica", "", 10)
        pdf.cell(0, 10, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
        pdf.ln(10)

        # Project info
        pdf.set_font("helvetica", "B", 14)
        pdf.cell(0, 10, f"Project: {self.project_path.name}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.ln(5)

        # Summary
        pdf.set_font("helvetica", "B", 12)
        pdf.cell(0, 10, "Summary", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.set_font("helvetica", "", 10)
        pdf.cell(0, 8, f"Passed checks: {len(self.validation_results['passed'])}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.cell(0, 8, f"Failed checks: {len(self.validation_results['failed'])}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.cell(0, 8, f"Warnings: {len(self.validation_results['warnings'])}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.ln(5)

        # Failed checks
        if self.validation_results["failed"]:
            pdf.set_font("helvetica", "B", 12)
            pdf.set_text_color(255, 0, 0)
            pdf.cell(0, 10, "Failed Checks - Action Required", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            pdf.set_font("helvetica", "", 10)
            pdf.set_text_color(0, 0, 0)
            for item in self.validation_results["failed"]:
                # Clean and truncate if needed
                cleaned_item = clean_text(item)
                # Use text parameter explicitly and set width
                pdf.multi_cell(w=0, h=8, text=f"- {cleaned_item}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            pdf.ln(5)

        # Warnings
        if self.validation_results["warnings"]:
            pdf.set_font("helvetica", "B", 12)
            pdf.set_text_color(255, 165, 0)
            pdf.cell(0, 10, "Warnings - Recommended Improvements", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            pdf.set_font("helvetica", "", 10)
            pdf.set_text_color(0, 0, 0)
            for item in self.validation_results["warnings"]:
                cleaned_item = clean_text(item)
                pdf.multi_cell(w=0, h=8, text=f"- {cleaned_item}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            pdf.ln(5)

        # FAIR recommendations
        pdf.set_font("helvetica", "B", 12)
        pdf.cell(0, 10, "FAIR Principle Recommendations", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.set_font("helvetica", "", 10)
        for rec in self.validation_results["recommendations"]:
            cleaned_rec = clean_text(rec)
            pdf.multi_cell(w=0, h=8, text=f"- {cleaned_rec}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        # Add passed checks on new page if there are many
        if self.validation_results["passed"]:
            pdf.add_page()
            pdf.set_font("helvetica", "B", 12)
            pdf.set_text_color(0, 128, 0)
            pdf.cell(0, 10, "Passed Checks", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            pdf.set_font("helvetica", "", 10)
            pdf.set_text_color(0, 0, 0)
            for item in self.validation_results["passed"]:
                cleaned_item = clean_text(item)
                pdf.multi_cell(w=0, h=8, text=f"- {cleaned_item}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        # Save PDF
        pdf.output(output_path)
        print(f"[green]📄 PDF report saved to: {output_path}[/green]")


def validate_project(project_path):
    """Main function to validate a project"""
    validator = OpenScienceValidator(project_path)
    results = validator.validate_structure()

    # Generate PDF report
    report_path = Path(project_path) / "validation_report.pdf"
    validator.generate_pdf_report(report_path)

    return results
