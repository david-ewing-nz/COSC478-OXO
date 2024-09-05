from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
import pandas as pd
from setup import main  # Import the main function from setup.py to get translations

# Simple tokenization using Python's split method
def simple_tokenize(text):
    return text.split()

# Function to calculate BLEU score for each translation
def calculate_bleu(reference, candidate):
    smooth = SmoothingFunction().method1
    # Use the simple_tokenize function to tokenize both reference and candidate
    reference_tokens = simple_tokenize(reference)
    candidate_tokens = simple_tokenize(candidate)
    # Calculate BLEU score with uniform weights for unigrams, bigrams, trigrams, and 4-grams
    bleu_score = sentence_bleu([reference_tokens], candidate_tokens, smoothing_function=smooth, weights=(0.25, 0.25, 0.25, 0.25))
    return bleu_score

# Get the reference and LLM translations from setup.py
reference_translations, llm_translations = main()

# Calculate BLEU score for each sentence
bleu_scores = []
for i in range(len(llm_translations)):
    reference = reference_translations[i]
    candidate = llm_translations[i][0]  # Extract the actual string from the list
    score = calculate_bleu(reference, candidate)
    bleu_scores.append(score)

# Display the BLEU scores
for i, score in enumerate(bleu_scores):
    print(f"Sentence {i+1} BLEU score: {score}")

# Optionally, store the results in a CSV file
output_df = pd.DataFrame({
    "Reference Translation": reference_translations,
    "LLM Translation": [llm[0] for llm in llm_translations],  # Extract strings from lists
    "BLEU Score": bleu_scores
})

# Save the BLEU scores to a CSV file (optional)
output_df.to_csv('./data/bleu_scores.csv', index=False)
