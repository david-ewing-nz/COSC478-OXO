import csv

# Function to read and process the CSV file
def read_csv_file(csv_file_path):
    reference_translations = {}
    llm_translations = {'1': {}, '2': {}}  # Store translations for both LLMs
    questions = {}
    who_names = {'reference': {}, 'llm_1': {}, 'llm_2': {}}  # Store 'who' column for both reference and LLMs

    # Open and read the CSV file
    with open(csv_file_path, mode='r', encoding='utf-8') as csvfile:
        csvreader = csv.reader(csvfile)

        # Skip the header row
        headers = next(csvreader)

        # Iterate over each row in the CSV file
        for row in csvreader:
            if len(row) < 6:  # Ensure the row has at least 6 columns
                continue

            who_name = row[0]  # "who_name" column
            question_number = row[1]  # "question" column
            llm_value = row[3]  # "LLM" column ('1' or '2')
            expert_value = row[4]  # "expert" column ('1', '2', '3', '4')
            sentence = row[5].strip()  # Strip leading/trailing spaces from sentence

            # Only process rows related to questions 1 to 4
            if question_number in ['1', '2', '3', '4']:
                # Store the question for output in the CSV later
                questions[question_number] = question_number

                # If the row is marked as an LLM-generated translation ('1' or '2')
                if llm_value in ['1', '2']:
                    if llm_value == '1':
                        llm_translations['1'][question_number] = sentence
                        who_names['llm_1'][question_number] = who_name
                    elif llm_value == '2':
                        llm_translations['2'][question_number] = sentence
                        who_names['llm_2'][question_number] = who_name

                # If the row is marked as an expert reference translation ('1' only)
                if expert_value == '1' and question_number not in reference_translations:
                    reference_translations[question_number] = sentence
                    who_names['reference'][question_number] = who_name

    return reference_translations, llm_translations, questions, who_names


# Main function to control the flow
def main():
    csv_file_path = r'./data/book2.csv'  # Adjust the path as necessary

    # Read the CSV file and get the reference translations, LLM translations, and questions
    reference_translations, llm_translations, questions, who_names = read_csv_file(csv_file_path)

    # Return the collected data for further use
    return reference_translations, llm_translations, questions, who_names


if __name__ == "__main__":
    main()
