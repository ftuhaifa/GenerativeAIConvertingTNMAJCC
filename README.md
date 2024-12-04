





#Chat GPT

Lung Cancer Staging with OpenAI GPT-4 and Python


This repository provides a Python script for automating the transformation of historical lung cancer staging data into the AJCC 8th Edition staging system using OpenAI's GPT-4. The script processes TNM staging data from various historical AJCC editions and derives consistent staging values for analysis and reporting.

Features:


Integration with OpenAI GPT-4:


Uses the OpenAI GPT-4 model to infer AJCC 8th Edition staging values (T, N, M, and TNM Stage`) from historical data.


Dynamic Prompting:


Constructs detailed prompts based on each patient's staging data for accurate inference.


Automated Workflow:


Reads input CSV files.


Sends row-wise data to the GPT-4 model for inference.


Extracts and formats results using parsing logic.


Outputs the processed data to a new CSV file.


Error Logging:


Captures and logs errors for smooth debugging and troubleshooting.


Prerequisites:
An OpenAI API key with access to GPT-4.
A dataset in CSV format containing historical lung cancer staging data from multiple AJCC editions.
Usage:
Update the input_file_path and output_file_path in the script with the paths to your input and output CSV files.
Run the script to process the dataset.
The output file will include the derived AJCC 8th Edition staging values.
Output:
The resulting CSV file will include additional columns:

T in 8th Edition ChatGPT
N in 8th Edition ChatGPT
M in 8th Edition ChatGPT
TNM Stage AJCC 8th Edition ChatGPT
Ideal Use Case:
This script is ideal for researchers and clinicians needing to standardize and harmonize historical lung cancer staging data for advanced analysis, reporting, or integration with modern clinical workflows.
