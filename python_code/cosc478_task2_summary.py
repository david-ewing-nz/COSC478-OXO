from collections import Counter
import math

passage = """
The Olympic Games, a global sporting spectacle, trace their roots back to ancient Greece. Originating as a religious festival honouring Zeus, the god of sky and thunder, the ancient Olympics were held in Olympia every four years from approximately 776 BC to 393 AD. Initially, the games consisted of a single footrace, but over time expanded to include various athletic contests and cultural events. The Olympics served as a unifying force among Greek city-states, even during periods of war, fostering a spirit of competition and camaraderie.
However, with the decline of the Roman Empire, the Olympic Games fell into obscurity. It wasn't until the late 19th century that the idea of reviving the Games emerged. Inspired by the ideals of Olympism, which emphasized physical and moral education, Baron Pierre de Coubertin, a French educator, founded the International Olympic Committee (IOC) in 1894. His vision was to create a global sporting event that would promote peace and understanding among nations.
The first modern Olympic Games were held in Athens, Greece, in 1896, featuring a modest program of sports. Over the years, the Games grew in scale and scope, with the inclusion of new sports and the participation of athletes from an increasing number of countries. The Winter Olympic Games were added in 1924 to accommodate winter sports.
The Olympics have faced challenges and controversies throughout their history. The Games were cancelled during both World Wars, and issues such as amateurism, doping, and political interference have marred their reputation at times. Nevertheless, the Olympic spirit has endured, and the Games continue to be a powerful symbol of international unity and competition.
Today, the Olympics are a mega-event, with thousands of athletes from around the world competing in a wide range of sports. The Games have evolved into a global cultural phenomenon, with billions of people tuning in to watch the world's best athletes compete. While the original ideals of Olympism may have been diluted, the spirit of competition, excellence, and friendship remains at the heart of the Games.
The Olympics have come a long way since their humble beginnings in ancient Greece. From a local religious festival to a global spectacle, the Games have shaped the course of history and continue to inspire athletes and spectators alike.
"""

# Summarize the passage in 40 words
summary_copilot  = """ The Olympic Games, a global sporting spectacle, trace their roots back to ancient Greece. Originating as a religious festival honouring Zeus, the god of sky and thunder, the ancient Olympics were held in Olympia every four years from approximately 776 BC to 393 AD. Initially, the games consisted of a single footrace, but over time expanded to include various athletic contests and cultural events. The Olympics served as a unifying force among Greek city-states, even during periods of war, fostering a spirit of competition and camaraderie. """
summary_chatgpt  = """The Olympic Games began in ancient Greece as a religious festival, later revived in 1896 by Baron de Coubertin. They have grown into a global event with athletes competing, despite challenges such as wars and controversies."""
summary_bard     = """The Olympics began in ancient Greece as a festival honoring Zeus. After a long hiatus, they were revived in 1896 and have evolved into a global event, promoting competition and unity despite facing various challenges."""
summary_claude   = """The Olympic Games originated in ancient Greece and were revived in 1896 by Pierre de Coubertin. Today, they are a major global event that promote international unity, despite challenges like wars and controversies over time."""

# calculate n-grams
def get_ngrams(text, n):
    tokens = text.split()
    return [tuple(tokens[i:i+n]) for i in range(len(tokens)-n+1)]

# calculate ROGUE-N precision
def calculate_rogue_n(reference, hypothesis, n):
    ref_ngrams = get_ngrams(reference, n)
    hyp_ngrams = get_ngrams(hypothesis, n)
    
    ref_counts = Counter(ref_ngrams)
    hyp_counts = Counter(hyp_ngrams)
    
    # calculate matches
    matches = sum(min(ref_counts[ngram], hyp_counts[ngram]) for ngram in hyp_counts)
    total_hyp_ngrams = len(hyp_ngrams)
    
    # Precision = number of matches / total number of n-grams in hypothesis
    precision = matches / total_hyp_ngrams if total_hyp_ngrams > 0 else 0
    return precision

# Fcalculate ROGUE-N score (geometric mean of ROGUE-1 to ROGUE-4)
def calculate_rogue_n_score(reference, hypothesis):
    precisions = []
    for n in range(1, 5):  # ROGUE-1 to ROGUE-4
        precision = calculate_rogue_n(reference, hypothesis, n)
        precisions.append(precision)
    
    # calculate geometric mean of the precisions
    if all(p > 0 for p in precisions):
        score = math.exp(sum(math.log(p) for p in precisions) / 4)
    else:
        score = 0
    return precisions, score

# structured summaries
summaries = {
 #  "CoPilot" : summary_copilot,
    "ChatGPT": summary_chatgpt,
   "Bard"    : summary_bard #,
 #  "Claude"  : summary_claude
}

# generate table for report. 
for model_name, summary in summaries.items():
    precisions, rogue_n_score = calculate_rogue_n_score(summary_claude, summary)
    print(f"{model_name} Summary:")
    print(f" ROGUE-1: {precisions[0]:.4f},\n ROGUE-2: {precisions[1]:.4f},\n ROGUE-3: {precisions[2]:.4f},\n ROGUE-4: {precisions[3]:.4f}")
    print(f"Overall ROGUE-N Score: {rogue_n_score:.4f}\n")


#if __name__ == "__main__":
#    main()
#