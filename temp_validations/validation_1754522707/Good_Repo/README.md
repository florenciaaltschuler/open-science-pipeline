README
======

Dataset title:
[Repeat the dataset title here]

Creators:
[List the dataset creators (authors), but not their affiliations or ORCIDs. If you have already entered the creator list in DORIS, you can just copy the author list from the provisional citation on your dataset’s preview page! For privacy reasons, avoid email addresses in the README - public contact information can be provided in DORIS or via your ORCID profile.]

Responsible organization:
[Usually the university or research organization of the person depositing the data.]

[We recommend that you keep the next sentence -->] See the Researchdata.se catalogue entry for this dataset for complete metadata, including the dataset description, recommended citation, contact information, and information about how to obtain the dataset. 

Description: [A short description of the dataset to help users understand the its content, context, and relevance. You can copy or summarize the Description from the metadata.]

License: [State any license you are imposing and explain any exceptions for particular files or data.]

Access restrictions: [If the dataset cannot be freely redistributed by third parties (for example, because it contains personal data or copyrighted material), then include the following -->] This dataset contains [eg personal data] and is subject to legal protections. This dataset can be requested from the Researchdata.se research data catalog.

Essential information for dataset reuse.
----------------------------------------

Provide essential information about the data collection that secondary users will need to know in order to reuse the dataset or understand its contents. This typically includes information about sampling, experiment or survey configurations, which are especially important if different datafiles contain measurements for different times, locations, levels, population samples, etc.

If any special software is needed to read the data files, note how to obtain it.

If the dataset includes code, provide basic instructions for how to run the code. 

Dataset organization
--------------------

Provide an overview of the data and documentation files. For simpler datasets with few files and no zip-files or subfolders, you can skip this section and simply describe the datafiles. 

The contents of datafiles are often interrelated, typically through sample- or respondent-IDs. If so, explain how the data files are connected to each other and which documentation files correspond to which data files, where appropriate. 

If many files/folders have the same format but contain data for different experiments/samples/etc., describe the file/folder naming convention and how it identifies the associated experiment/sample/etc.

If the dataset has nested folders, it can be useful to embed short explanations in a visual map of the dataset:

README.txt
Folder_A/
 Files of type A
Folder_B/
 Sub_Folder_1/
 Data files of type B for thing 1
 Sub_Folder_2/
 Data files of type B for thing 2 

Datafile descriptions
----------------------

For each type of file or folder in the dataset, provide a short, generalized description of what it contains. 

For hierarchical datafiles (e.g. .xlsx files with sheets, or nested data structures in .mat or .json), describe how the contents are organized. Describe any formatting (especially colors) used in .xlsx files. 

For tabular datafiles (e.g. .csv or .xlsx files) with relatively few variables, include an inventory of each file’s contents in the README. For each file:
  - Summarize what is contained in the file. One sentence is usually sufficient. 
  - Describe each of the variables in a few words.
  - Give the units for the variables, any conventions used, or the meanings of codes and classifications.

Example:

Weather.csv – composite hourly weather timeseries.
Columns:
  Date [yyyy-mm-dd]. Date.
  Hour [hh]. Hour, local timezone (CET+1), no daylight savings. Data for hour 00 cover the interval 00:00≤hour<01:00.
  Temp [°C]. Average temperature.
  Temp_code [numeric, 1-3]. Source code flag for Temp: 1=average of observed values, 2=average of nearby stations, 3=average of preceding and following hours. 

Reference information
---------------------

Non-essential and reference information. This can be information that other researchers in your own field will already know, but which researchers from other fields may need. Include any of the following items, if they are relevant.

Abbreviations:
Abbreviations used in file or folder names.

Data sources:
If this is an aggregated dataset (i.e., it includes data from other datasets), list the data sources, summarize why you have permission to reuse these data (e.g. a license, you obtained private permission, the data are in the public domain…), and indicate which data in your dataset come from which sources.

Version control:
If this dataset contains static copies of files that are under version control (usually source code files on a Git repository), note this and provide a link to the main repository.

Source code information:
Provide information on the versions of software used to run any code. Where possible, provide the versions of any libraries that are required.

Data Quality:
Note any quality assurance work (data validation, checking), data manipulations or modifications, known biases, missing data, or other limitations that you think a secondary user needs to be aware of. Potential limitations can be mentioned.
