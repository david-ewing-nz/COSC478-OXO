import os
import csv

# Fetch OpenAI API key from environment variable
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("No OpenAI API key found in environment variables. Please set the 'OPENAI_API_KEY' environment variable.")


# Get and print the current working directory
current_directory = os.getcwd()
print("Current Working Directory:", current_directory)
# Path to the CSV file
csv_file_path = r'.\data\book1.csv'
import csv
import csv

# Function to read and process the CSV file
def read_csv_file(csv_file_path):
    reference_translations = {}
    llm_translations = {}

    # Open and read the CSV file
    with open(csv_file_path, mode='r', encoding='utf-8') as csvfile:
        csvreader = csv.reader(csvfile)

        # Skip the header row
        headers = next(csvreader)

        # Iterate over each row in the CSV file
        for row in csvreader:
            if len(row) < 6:  # Ensure the row has at least 6 columns
                continue

            question_number = row[1]  # "question" column
            llm_value = int(row[3])   # "LLM" column
            expert_value = int(row[4])  # "expert" column
            sentence = row[5].strip()  # Strip leading/trailing spaces from sentence

            # Only process rows related to questions 1 to 4
            if question_number in ['1', '2', '3', '4']:
                # If the row is marked as an LLM-generated translation
                if llm_value == 1 and question_number not in llm_translations:
                    llm_translations[question_number] = sentence
                # If the row is marked as an expert reference translation and not already recorded
                if expert_value == 1 and question_number not in reference_translations:
                    reference_translations[question_number] = sentence

    # Check if all required reference translations and LLM translations are collected
    for i in range(1, 5):
        q = str(i)
        if q not in reference_translations:
            print(f"Warning: Missing reference translation for question {q}")
        if q not in llm_translations:
            print(f"Warning: Missing LLM translation for question {q}")

    # Convert the dictionary values to lists in the correct order (1, 2, 3, 4)
    reference_translations_list = [reference_translations.get(str(i), '') for i in range(1, 5)]
    llm_translations_list = [[llm_translations.get(str(i), '')] for i in range(1, 5)]

    return reference_translations_list, llm_translations_list

# Main function to control the flow
def main():
    csv_file_path = r'.\data\book1.csv'  # Adjust the path as necessary

    # Read the CSV file and get the reference and LLM translations
    reference_translations, llm_translations = read_csv_file(csv_file_path)

    # Return the collected data for further use
    return reference_translations, llm_translations

# Entry point of the script
if __name__ == '__main__':
    reference_translations, llm_translations = main()
    print("Reference Translations: ", reference_translations)
    print("LLM Translations: ", llm_translations)
