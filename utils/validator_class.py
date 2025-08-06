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
        # Expected structure
        self.required_files = {
            "README.md": "Project overview with badges and quick-start guide",
            "LICENSE": "Permission & reuse information (recommend CC-BY-4.0)",
            "CITATION.cff": "How to cite the dataset and code"
        }
        
        self.required_dirs = {
            "01_docs": "Human-readable documentation related to the project. Protocols, consent, ethics, DMP",
            "01_docs/01_participant_info": "Demographics and participant data",
            "01_docs/02_ethics": "Ethics(IRB) approval documents",
            "01_docs/03_dmp": "Data Management Plan",
            "01_docs/04_prereg": "Pre-registration documents",
            "02_data": "Data storage (never edit in place)",
            "02_data/01_raw": "Original raw data files (deidentified/anonymised)",
            "02_data/02_preproc": "Analysis-ready data (processed, cleaned, transformed)",
            "03_scripts": "Code used across various stages of the research process",
            "03_scripts/01_exp": "Experimental scripts for data collection",
            "03_scripts/02_prep": "Data preparation scripts (cleaning, preprocessing, transformation)",
            "03_scripts/03_analysis": "Statistical or computational analysis scripts",
            "04_results": "Outputs generated from analysis (stats tables, final figs).",
            "04_results/01_output": "Raw output files from analysis scripts, such as logs or model outputs.",
            "04_results/02_figures": "Visualizations such as plots, charts, or brain maps",
            "04_results/03_tables": "Tabular data results",
            "05_metadata": "Metadata files describing the data and code (dataset descriptors, codebooks, or provenance logs)",
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
        """Check for required files"""
        for file_name, description in self.required_files.items():
            file_path = self.project_path / file_name
            if file_path.exists():
                self.validation_results["passed"].append(f"✓ Found {file_name}")
                
                # Additional checks for specific files
                if file_name == "README.md":
                    self._check_readme_content(file_path)
                elif file_name == "LICENSE":
                    self._check_license_content(file_path)
                elif file_name == "CITATION.cff":
                    self._check_citation_content(file_path)
            else:
                self.validation_results["failed"].append(
                    f"✗ Missing {file_name}: {description}"
                )

    def _validate_directories(self):
        """Check for required directory structure"""
        for dir_path, description in self.required_dirs.items():
            full_path = self.project_path / dir_path
            if full_path.exists() and full_path.is_dir():
                # Check if directory is empty
                if not any(full_path.iterdir()):
                    self.validation_results["warnings"].append(
                        f"⚠ Directory '{dir_path}' exists but is empty"
                    )
                else:
                    self.validation_results["passed"].append(f"✓ Found {dir_path}/")
            else:
                self.validation_results["failed"].append(
                    f"✗ Missing directory '{dir_path}': {description}"
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
        
        # Check for requirements.txt or environment.yml
        env_files = ["requirements.txt", "environment.yml", "pyproject.toml"]
        found_env = False
        for env_file in env_files:
            if (self.project_path / "code" / "env" / env_file).exists():
                found_env = True
                self.validation_results["passed"].append(f"✓ Found {env_file}")
                break
        
        if not found_env:
            self.validation_results["warnings"].append(
                "⚠ No environment specification found (requirements.txt, environment.yml, etc.)"
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
        if "raw" in str(self.validation_results["failed"]):
            self.validation_results["recommendations"].append(
                "💡 Create data/raw/ to preserve original data (never modify!)"
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
                '💡': '[TIP]'
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
