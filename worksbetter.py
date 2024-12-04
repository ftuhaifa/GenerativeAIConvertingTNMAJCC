import openai
import pandas as pd
import logging
import json

# Set OpenAI API key
openai.api_key = 'Add your key here'

#this is working with chatGPT
def extract_values_from_response(response_message):
    """
    Extract the T, N, M, and AJCC Stage values from the natural language response.
    If any value is missing or not available, return None or an empty string.
    """
    t_value = n_value = m_value = stage_value = None

    # Check if the response contains each value and extract it
    if "T in 8th Edition" in response_message:
        t_value = response_message.split("T in 8th Edition: ")[1].split("\n")[0].strip()
    
    if "N in 8th Edition" in response_message:
        n_value = response_message.split("N in 8th Edition: ")[1].split("\n")[0].strip()
    
    if "M in 8th Edition" in response_message:
        m_value = response_message.split("M in 8th Edition: ")[1].split("\n")[0].strip()
        if "Data not available" in m_value:
            m_value = None
    
    if "TNM Stage AJCC 8th Edition" in response_message:
        stage_value = response_message.split("TNM Stage AJCC 8th Edition: ")[1].split("\n")[0].strip()
        if "Cannot be determined" in stage_value:
            stage_value = None

    return t_value, n_value, m_value, stage_value


# Initialize logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def process_file_locally(file_path, output_file_path):
    # Read the CSV file into a pandas DataFrame
    try:
        df = pd.read_csv(file_path)
        logger.info("CSV file read into DataFrame successfully.")
    except Exception as e:
        logger.error(f"Error reading CSV file: {str(e)}")
        return

    # Add new columns for the 8th edition staging
    df['T in 8th Edition ChatGPT'] = ''
    df['N in 8th Edition ChatGPT'] = ''
    df['M in 8th Edition ChatGPT'] = ''
    df['TNM Stage AJCC 8th Edition ChatGPT'] = ''

    # Iterate over each row and send the TNM values to ChatGPT for processing
    for index, row in df.iterrows():
        # Construct the zero-shot prompt based on the available data for that row
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

        # Use the ChatCompletion API to get a response from ChatGPT
        try:
            response = openai.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an AI that processes lung cancer data and derives TNM staging for the AJCC 8th edition."},
                    {"role": "user", "content": prompt}
                ]
            )

            # Extract the response content as plain text
            response_message = response.choices[0].message.content

            # Print the response from ChatGPT for debugging
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

            # Extract T, N, M, and Stage values from the response
            t_value, n_value, m_value, stage_value = extract_values_from_response(response_message)

            # Store the derived values in the DataFrame
            df.at[index, 'T in 8th Edition'] = t_value if t_value else ''
            df.at[index, 'N in 8th Edition'] = n_value if n_value else ''
            df.at[index, 'M in 8th Edition'] = m_value if m_value else ''
            df.at[index, 'TNM Stage AJCC 8th Edition'] = stage_value if stage_value else ''

        except Exception as e:
            logger.error(f"Error processing row {index}: {e}")
            continue

    # Save the modified DataFrame back as a CSV
    try:
        df.to_csv(output_file_path, index=False)
        logger.info(f"Modified CSV saved successfully: {output_file_path}")
    except Exception as e:
        logger.error(f"Error saving the modified CSV file: {str(e)}")

# Example usage
input_file_path = 'unique_patient_data.csv'
output_file_path = 'ChatGPTDATAAjcc.csv'
process_file_locally(input_file_path, output_file_path)