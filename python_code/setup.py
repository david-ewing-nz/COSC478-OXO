import os
import csv

# Fetch OpenAI API key from environment variable
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("No OpenAI API key found in environment variables. Please set the 'OPENAI_API_KEY' environment variable.")

# Path to the CSV file
csv_file_path = r'.\data\book1.csv'

# Initialize an empty list to store the data
data_array = []

# Read the CSV file
with open(csv_file_path, mode='r', encoding='utf-8') as csvfile:
    csvreader = csv.reader(csvfile)
    
    # Iterate over each row in the CSV file
    for row in csvreader:
        if len(row) < 3:
            continue  # Skip rows that don't have at least 3 columns
        
        # Extract the name, numeric value, and sentence
        name = row[0]
        number = int(row[1])
        sentence = row[2]
        
        # Split the sentence into words
        words = sentence.split()
        
        # Store the data in the array
        data_array.append([name, number, words])

# Output the processed data for verification
for entry in data_array:
    print(f"Name: {entry[0]}, Number: {entry[1]}, Words: {entry[2]}")
