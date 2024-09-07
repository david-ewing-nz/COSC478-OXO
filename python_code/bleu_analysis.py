import math
from collections import Counter
import pandas as pd
from setup import main  # Import the main function from setup.py to get translations

# Function to calculate n-grams
def ngrams(tokens, n):
    return [tuple(tokens[i:i+n]) for i in range(len(tokens)-n+1)]

# Function to calculate precision for n-grams
def precision(reference_tokens, candidate_tokens, n):
    ref_ngrams = Counter(ngrams(reference_tokens, n))
    cand_ngrams = Counter(ngrams(candidate_tokens, n))

    # Count how many n-grams from the candidate are in the reference
    match_count = sum(min(cand_ngrams[ng], ref_ngrams[ng]) for ng in cand_ngrams)

    # Total n-grams in the candidate translation
    total_count = len(cand_ngrams)

    # If no n-grams are found, return 0 precision
    if total_count == 0:
        return 0

    # Return precision
    return match_count / total_count

# Function to calculate brevity penalty
def brevity_penalty(reference_length, candidate_length):
    if candidate_length > reference_length:
        return 1
    elif candidate_length == 0:
        return 0
    else:
        return math.exp(1 - (reference_length / candidate_length))

# Function to calculate BLEU score manually
def calculate_bleu_manual(reference, candidate):
    reference_tokens = reference.split()
    candidate_tokens = candidate.split()

    # Calculate precisions for n-grams (1 to 4)
    p1 = precision(reference_tokens, candidate_tokens, 1)
    p2 = precision(reference_tokens, candidate_tokens, 2)
    p3 = precision(reference_tokens, candidate_tokens, 3)
    p4 = precision(reference_tokens, candidate_tokens, 4)

    # Geometric mean of precisions (if any precision is 0, return 0)
    if p1 * p2 * p3 * p4 == 0:
        geometric_mean = 0
    else:
        geometric_mean = (p1 * p2 * p3 * p4) ** (1/4)

    # Brevity Penalty
    bp = brevity_penalty(len(reference_tokens), len(candidate_tokens))

    # Final BLEU score
    return bp * geometric_mean


# Get the reference and LLM translations from setup.py
reference_translations, llm_translations, questions, who_names = main()

# Initialize lists for storing results
bleu_scores = []
reference_who = []
llm_who = []
llm_translations_list = []
reference_translations_list = []

# Compare each LLM (both '1' and '2') against the reference
for llm_key in ['1', '2']:
    for i, question in enumerate(questions.values()):
        reference = reference_translations[question]
        candidate = llm_translations[llm_key][question]

        # Calculate BLEU score
        score = calculate_bleu_manual(reference, candidate)
        bleu_scores.append(score)

        # Store other relevant data
        reference_who.append(who_names['reference'][question])
        llm_who.append(who_names[f'llm_{llm_key}'][question])
        reference_translations_list.append(reference)
        llm_translations_list.append(candidate)

# Create a DataFrame with the required columns
output_df = pd.DataFrame({
    "Question": list(questions.values()) * 2,
    "BLEU Score": bleu_scores,
    "REFERENCE_WHO": reference_who,
    "LLM_WHO": llm_who,
    "Reference Translation": reference_translations_list,
    "LLM Translation": llm_translations_list
})

# Save the BLEU scores to a CSV file
output_df.to_csv('./data/bleu_scores.csv', index=False)
