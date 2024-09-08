import math
from collections import Counter
import pandas as pd
from setup import main  # Import the main function from setup.py 

# n-grams
def ngrams(tokens, n):
    return [tuple(tokens[i:i+n]) for i in range(len(tokens)-n+1)]

# calculate precision for n-grams
def precision(reference_tokens, candidate_tokens, n):
    ref_ngrams  = Counter(ngrams(reference_tokens, n))
    cand_ngrams = Counter(ngrams(candidate_tokens, n))
    
    # count  match of n-grams from the candidate 
    match_count = sum(min(cand_ngrams[ng], ref_ngrams[ng]) for ng in cand_ngrams)
    
    # Tcount   n-grams from the candidate 
    total_count = len(cand_ngrams)
    
    # If no n-grams are found, return 0 precision
    if total_count == 0:
        return 0
    
    #  precision
    return match_count / total_count

#  calculate brevity penalty
def brevity_penalty(reference_length, candidate_length):
    if candidate_length > reference_length:
        return 1
    elif candidate_length == 0:
        return 0
    else:
        return math.exp(1 - (reference_length / candidate_length))

#  calculate BLEU score manually with per n-gram scores
def calculate_bleu_manual(reference, candidate):
    reference_tokens = reference.split()
    candidate_tokens = candidate.split()
    
    # calculate precisions for n-grams (1 to 4)
    p1 = precision(reference_tokens, candidate_tokens, 1)  # Unigrams
    p2 = precision(reference_tokens, candidate_tokens, 2)  # Bigrams
    p3 = precision(reference_tokens, candidate_tokens, 3)  # Trigrams
    p4 = precision(reference_tokens, candidate_tokens, 4)  # 4-grams
    
    # Geometric mean of precisions (if any precision is 0, return 0)
    if p1 * p2 * p3 * p4 == 0:
        geometric_mean = 0
    else:
        geometric_mean = (p1 * p2 * p3 * p4) ** (1/4)
    
    # bBrevity penalty
    bp = brevity_penalty(len(reference_tokens), len(candidate_tokens))
    
    # Final BLEU score
    bleu = bp * geometric_mean
    return bleu, p1, p2, p3, p4

# return from setup.py
reference_translations, llm_translations, questions, who_names = main()

#  lists for storing results (without n-gram scores in the CSV)
data = []

# process each LLM (both '1' and '2') and compare to the reference
for llm_key in ['1', '2']:
    for question in questions.values():
        reference = reference_translations[question]
        candidate = llm_translations[llm_key][question]

        # calculate BLEU score and individual n-gram precisions
        bleu_score, p1, p2, p3, p4 = calculate_bleu_manual(reference, candidate)

        # truncate individual n-gram scores to 4 decimal places for display
        p1 = round(p1, 4)
        p2 = round(p2, 4)
        p3 = round(p3, 4)
        p4 = round(p4, 4)

        #  results to the data list for the CSV file (excluding n-grams)
        data.append({
            "Question": question,
            "BLEU Score": bleu_score,
            "REFERENCE_WHO": who_names['reference'][question],
            "LLM_WHO": who_names[f'llm_{llm_key}'][question],
            "Reference Translation": reference,
            "LLM Translation": candidate
        })

        # Print the detailed information for each comparison
        print(f"Question: {question}")
        print(f"REFERENCE_WHO: {who_names['reference'][question]}")
        print(f"Reference Translation: {reference}")
        print(f"LLM_WHO: {who_names[f'llm_{llm_key}'][question]}")
        print(f"LLM Translation: {candidate}")
        print(f"Score Unigram: {p1}")
        print(f"Score Bigram:  {p2}")
        print(f"Score Trigram: {p3}")
        print(f"Score 4-gram:  {p4}")
        print(f"Final BLEU Score: {bleu_score}")
        print("\n" + "-"*50 + "\n")

# Create a DataFrame to store the results
output_df = pd.DataFrame(data)

# Save the BLEU scores to a CSV file (without n-gram scores)
output_df.to_csv('./data/bleu_scores.csv', index=False)
