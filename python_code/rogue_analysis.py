from rouge_score import rouge_scorer

#  
def get_openai_key()
    with open('openai_key.txt', 'r') as file:
        key = file.read().replace('\n', '')
    return key

def read_csv(file_path)
    with open(file_path, 'r') as file:
        lines = file.readlines()
    return lines



def calculate_rouge_scores(reference_texts, model_texts):
    scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rouge3', 'rouge4'], use_stemmer=True)
    rouge_scores = []

    for ref, model in zip(reference_texts, model_texts):
        scores = scorer.score(ref, model)
        rouge_scores.append({
            "ROUGE-1": round(scores['rouge1'].fmeasure, 4),
            "ROUGE-2": round(scores['rouge2'].fmeasure, 4),
            "ROUGE-3": round(scores['rouge3'].fmeasure, 4),
            "ROUGE-4": round(scores['rouge4'].fmeasure, 4)
        })

    return rouge_scores

# Example usage:
reference_texts = ["Your reference sentences here"]
model_texts = ["Your model-generated sentences here"]

rouge_results = calculate_rouge_scores(reference_texts, model_texts)
for result in rouge_results:
    print(result)
