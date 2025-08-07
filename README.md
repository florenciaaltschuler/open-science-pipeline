README
======

Project title:
FAIRyTale 
Give your data a happily-ever-after

Description: 
This project provides a program to automatically create a local repository structured according to **FAIR** (Findable, Accessible, Interoperable, Reusable) and **Open Science** principles. It is designed to help researchers organize and prepare their materials for publication in open repositories like OSF, Zenodo, or GitHub.

Creators:
Florencia Altschuler

Annika Andersson

Jaime Rios

Iliana Sandoval

Responsible organization:
Neurohackademy | UW eScience Institute

Features:
-Creates a local repository
- Automated creation of FAIR-aligned folder structured and organized
- Templates for metadata and README files
- Promotes reproducibility and transparency
- Compatible with OSF, Zenodo, GitHub

License:
MIT License

Project Structure:

The repository will include the following folders:

FAIRyTale project/

**README.md**

**01_docs/                    Documentation related to the project. Protocols, consent, ethics, DMP**

01_participant/               Demographics

02_ethics/                        Ethics approval documents

03_dmp/                           Data management plan

04_prereg/                       Pre-registration documents

**02_data/                    Data collected and processed for the study. *never edit in place***

01_raw/                           Unaltered, original raw data

02_preproc/                     Preprocessed and/or cleaned data

**03_scripts/                 Code used across various stages of the research process**

01_exp/                             Experimental scripts for data collection

02_prep/                           Data preparation scripts

03_analysis/                     Statistical or computational analysis scripts

**04_results/                 Outputs generated from analysis (stats tables, final figs)**

 01_output/                      Raw output files from analysis scripts, such as logs or model outputs.

 02_figures/                      Visualizations such as plots, charts, or brain maps

 03_tables/                        Tabular data results

 **05_meta/                          Metadata and supplementary information for reproducibility and FAIR principles, such as dataset descriptors, codebooks, or provenance logs**


Software needed to read the data files.
- Python 3.7+ 

Installation:

Step-by-step instructions on how to install or set up the project locally.


Clone the repository:


```
git clone https://github.com/NeuroHackademy2025/open-science-pipeline.git
```


Navigate to the project directory

```
cd your-repository
```

Create and activate a virtual environment

```
conda create -n FAIRyTale python=3.12
```
```
conda activate FAIRyTale
```

Install the required dependencies

With the virtual environment activated, install the required packages by running:
```
pip install -r requirements.txt
```

Run the application
After the dependencies are installed, you can run the Streamlit app. Use the following command to start the app:
```
streamlit run run_FAIRyTale_pipeline.py
```

This should launch the Streamlit application in your web browser. 

See the (webpage)......
 

| FAIR Principle    | How This Project Supports It                      |
| ----------------- | ------------------------------------------------- |
| **Findable**      | Structured metadata, README, searchable folders   |
| **Accessible**    | Open license,  open and standard web protocol     |
| **Interoperable** | Metadata standards, code versioning               |
| **Reusable**      | Documentation, provenance, open formats           |



