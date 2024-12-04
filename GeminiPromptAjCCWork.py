# -*- coding: utf-8 -*-
"""
Created on Sat Oct 26 17:44:51 2024

@author: faaa272
"""

# -*- coding: utf-8 -*-
"""
Created on Sat Oct 26 16:24:05 2024

@author: faaa272
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Oct 25 17:34:11 2024

@author: faaa272
"""

# -*- coding: utf-8 -*-
import vertexai
from vertexai.preview.generative_models import GenerativeModel, ChatSession

import pandas as pd
import logging
import google.generativeai as genai
import google.generativeai as genai
import vertexai
from vertexai.generative_models import GenerativeModel

#1036843331742
vertexai.init(project="generativeajcc", location="us-central1")
# Set your Google API key
API_KEY = ""
genai.configure(api_key=API_KEY)


model = GenerativeModel("Gemini 1.5 Flash")
#model = genai.GenerativeModel("Gemini 1.5 Pro")

chat = model.start_chat()
def get_chat_response(chat: ChatSession, prompt: str):
    response = chat.send_message(prompt)
    return response.text

# Function to extract values from response
#this is working with chatGPT
import re


def extract_values_from_response(response_message):
    """
    Extract the T, N, M, and AJCC Stage values from the natural language response.
    If any value is missing or not available, return None.
    """
    t_value = n_value = m_value = stage_value = None

    # Flexible regex patterns to match different formats
    t_match = re.search(r"(?:\*\*?)?\s*T(?: in 8th Edition)?\s*[:\*]?\s*\**\s*(T[0-9X]{0,2}[a-c]?)", response_message)
    n_match = re.search(r"(?:\*\*?)?\s*N(?: in 8th Edition)?\s*[:\*]?\s*\**\s*(N[0-9X]{0,2}[a-c]?)", response_message)
    m_match = re.search(r"(?:\*\*?)?\s*M(?: in 8th Edition)?\s*[:\*]?\s*\**\s*(M[0-9X]{0,2}[a-c]?)", response_message)
    stage_match = re.search(r"(?:\*\*?)?\s*TNM Stage(?: AJCC 8th Edition)?\s*[:\*]?\s*\**\s*([IVXLCDM]+[AB]?\d*)", response_message)

    # Extract matches or set to None if not found
    t_value = t_match.group(1) if t_match and "cannot be determined" not in t_match.group(1) else None
    n_value = n_match.group(1) if n_match and "cannot be determined" not in n_match.group(1) else None
    m_value = m_match.group(1) if m_match and "cannot be determined" not in m_match.group(1) else None
    stage_value = stage_match.group(1) if stage_match and "Unable to determine" not in stage_match.group(1) else None

    return t_value, n_value, m_value, stage_value






# Initialize logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Function to process each row with Gemini model responses
def process_file_locally(file_path, output_file_path):
    try:
        df = pd.read_csv(file_path)
        logger.info("CSV file read into DataFrame successfully.")
    except Exception as e:
        logger.error(f"Error reading CSV file: {str(e)}")
        return

    # Add new columns for 8th edition staging
    df['T in 8th Edition'] = ''
    df['N in 8th Edition'] = ''
    df['M in 8th Edition'] = ''
    df['TNM Stage AJCC 8th Edition'] = ''

    # Initialize the model
    model = GenerativeModel("gemini-1.0-pro-002")
    chat = model.start_chat()

    # Iterate over each row and send values to the model for processing
    for index, row in df.iterrows():
        prompt = f"""
        You are an expert in lung cancer staging. Using the historical data from different AJCC editions provided, please derive the most appropriate values for:
        - T in 8th Edition
        - N in 8th Edition
        - M in 8th Edition
        - TNM Stage AJCC 8th Edition

        Here’s the information available:

        - T value based on AJCC 3rd (1988-2003): {row.get('T value - based on AJCC 3rd (1988-2003)', 'Unknown')}
        - Derived AJCC T, 6th ed (2004-2015): {row.get('Derived AJCC T, 6th ed (2004-2015)', 'Unknown')}
        - Derived SEER Combined T (2016-2017): {row.get('Derived SEER Combined T (2016-2017)', 'Unknown')}
        - Derived EOD 2018 T (2018+): {row.get('Derived EOD 2018 T (2018+)', 'Unknown')}
        - CS tumor size (2004-2015): {row.get('CS tumor size (2004-2015)','Unknown')}
        
        

        - N value based on AJCC 3rd (1988-2003): {row.get('N value - based on AJCC 3rd (1988-2003)', 'Unknown')}
        - Derived AJCC N, 6th ed (2004-2015): {row.get('Derived AJCC N, 6th ed (2004-2015)', 'Unknown')}
        - Derived SEER Combined N (2016-2017): {row.get('Derived SEER Combined N (2016-2017)', 'Unknown')}
        - Derived EOD 2018 N (2018+): {row.get('Derived EOD 2018 N (2018+)', 'Unknown')}
        - CS lymph nodes (2004-2015): {row.get('CS lymph nodes (2004-2015)','Unknown')}

        - M value based on AJCC 3rd (1988-2003): {row.get('M value - based on AJCC 3rd (1988-2003)', 'Unknown')}
        - Derived AJCC M, 6th ed (2004-2015): {row.get('Derived AJCC M, 6th ed (2004-2015)', 'Unknown')}
        - Derived SEER Combined M (2016-2017): {row.get('Derived SEER Combined M (2016-2017)', 'Unknown')}
        - Derived EOD 2018 M (2018+): {row.get('Derived EOD 2018 M (2018+)', 'Unknown')}
        - CS extension (2004-2015): {row.get('CS extension (2004-2015)','Unknown')}

        Please infer and return the T, N, M, and TNM Stage AJCC 8th Edition values, format the summary as shown below:.
        
           T in 8th Edition: value 
           N in 8th Edition: value 
           M in 8th Edition: value
          TNM Stage AJCC 8th Edition: value
        
        """

        # Get model response
        try:
            response_message = get_chat_response(chat, prompt)

            # Print the response for debugging
            print(f"Response for row {index}:\n{response_message}\n")

            # Extract T, N, M, and Stage values from the response
            t_value, n_value, m_value, stage_value = extract_values_from_response(response_message)
            print("Check if it is .....")
            print("Check if it is .....")
            print(":::: ")
            print(t_value)
            print(n_value)
            print(m_value)
            print(stage_value)

            # Store values in DataFrame
            df.at[index, 'T in 8th Edition'] = t_value if t_value else ''
            df.at[index, 'N in 8th Edition'] = n_value if n_value else ''
            df.at[index, 'M in 8th Edition'] = m_value if m_value else ''
            df.at[index, 'TNM Stage AJCC 8th Edition'] = stage_value if stage_value else ''

        except Exception as e:
            logger.error(f"Error processing row {index}: {e}")
            continue

    # Save DataFrame to output file
    try:
        df.to_csv(output_file_path, index=False)
        logger.info(f"Modified CSV saved successfully: {output_file_path}")
    except Exception as e:
        logger.error(f"Error saving the modified CSV file: {str(e)}")
# Example usage
#input_file_path = 'selected_data.csv'





input_file_path = 'Data16.csv'
output_file_path = 'Data1016.csv'
process_file_locally(input_file_path, output_file_path)