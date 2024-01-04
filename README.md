# Vendor Database Standardization and Consolidation Project

## Table of Contents
1. [Introduction](##Introduction)
2. [Folder Structure](##Folder_Structure)
4. [How to Use](##How_to_Use)

## Introduction
This project contains scripts for address parsing and database standardization for vendor databases.

## Folder Structure
The project has two main folders:

1. **Address Parsing Scripts**: This folder contains scripts for parsing addresses. There are two main scripts in this folder:
    - **RPA Script and Address Parse**: These scripts uses regex for address parsing, it is not entirely accurate as there are constant edge cases and incorrect address inputs.
    - **API Address Parse**: This script uses the OpenCage API for more accurate address parsing. Please insert your own API key found at [OpenCage](https://opencagedata.com/api#quickstart). Please note that this script has API rate limits.

2. **Database Standardization Script Trials**: This folder contains all the trial files we made to standardize the databases. These files are not accurate and up-to-date, but they serve as a foundation for our project. The folder includes two MVP main files that leads to:
    - **peter_ingestion_mapping.ipynb**: This is the final version of our database standardization script.
    - **sejal_ingestion_mapping.ipynb**: This script is niched for a certain database.

## How to Use
Here are the steps on how to operate `peter_ingestion_mapping.ipynb`:

1. Open the `peter_ingestion_mapping.ipynb` file in Jupyter Notebook or Jupyter Lab.
2. To include files for upload, navigate to the section of the script where file uploading is handled. Follow the instructions in the script comments to include your files.
3. Run the script cells in order as they appear in the notebook.
4. Make note that some cells are specific to certain databases, do not run them if you're not parsing the sepcific database.

Please ensure you have the necessary Python packages installed and that your files are in the correct format as specified in the script comments.

## Contact
If you have any questions or need further clarification, feel free to reach out.

