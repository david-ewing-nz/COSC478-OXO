import math
from collections import Counter
import pandas as pd
from setup import main  # Import the main function from setup.py to get translations

# Function to calculate unordered n-grams (as sets of tokens, ignoring order)
def ngrams(tokens, n):
    return [frozenset(tokens[i:i+n]) for i in range(len(tokens)-n+1)]

# Function to calculate precision for n-grams, treating order as independent
def precision(reference_tokens, candidate_tokens, n):
    ref_ngrams = Counter(ngrams(reference_tokens, n))
    cand_ngrams = Counter(ngrams(candidate_tokens, n))
    
    # Count how many n-grams from the candidate are in the reference (ignoring order)
    match_count = sum(min(cand_ngrams[ng], ref_ngrams[ng]) for ng in cand_ngrams)
    
    # Total n-grams in the candidate translation
    total_count = len(cand_ngrams)
    
    # If no n-grams are found, return 0 precision
    if total_count == 0:
        return 0
    
    # Return precision
    return match_count / total_count

# Function to calculate brevity penalty
#def brevity_penalty(reference_length, candidate_length):
#    if candidate_length > reference_length:
#        return 1
#    elif candidate_length == 0:
#        return 0
#    else:
#        return math.exp(1 - (reference_length / candidate_length))

# Function to calculate BLEU score manually with unordered n-grams
def calculate_bleu_manual(reference, candidate):
    reference_tokens = reference.split()
    candidate_tokens = candidate.split()
    
    # Calculate precisions for n-grams (1 to 4) with unordered n-grams
    p1 = precision(reference_tokens, candidate_tokens, 1)  # Unigrams
    p2 = precision(reference_tokens, candidate_tokens, 2)  # Bigrams
    p3 = precision(reference_tokens, candidate_tokens, 3)  # Trigrams
    p4 = precision(reference_tokens, candidate_tokens, 4)  # 4-grams
    
    print(f"Unigram Precision: {p1:.4f},\nBigram  Precision: {p2:.4f},\nTrigram Precision: {p3:.4f},\n4-gram  Precision: {p4:.4f}")
    
    # Geometric mean of precisions (if any precision is 0, return 0)
    if p1 == 0 or p2 == 0 or p3 == 0 or p4 == 0:
        geometric_mean = 0
    else:
        geometric_mean = (p1 * p2 * p3 * p4) ** (1/4)
    
    # Brevity Penalty
    # bp = brevity_penalty(len(reference_tokens), len(candidate_tokens))
    # print(f"Brevity Penalty: {bp}")
    #bp = 1
    # Final BLEU score
    #bleu = bp * geometric_mean
    return geometric_mean

# Get the reference and LLM translations from setup.py
reference_translations, llm_translations = main()

# Calculate BLEU score for each sentence
bleu_scores = []
for i in range(len(llm_translations)):
    reference = reference_translations[i]
    candidate = llm_translations[i][0]  # Extract the actual string from the list
    print(f"Processing Sentence {i+1}:")
    print(f"Reference: {reference}")
    print(f"Candidate: {candidate}")
    score = calculate_bleu_manual(reference, candidate)  # Use the manual BLEU calculation
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
output_df.to_csv('./data/bleu_scores_manual_unordered.csv', index=False)
