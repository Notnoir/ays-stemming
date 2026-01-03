def jaccard_similarity(tokens1, tokens2):
    """
    Calculate Jaccard similarity between two lists of tokens.
    Tokens can be tuples (original, stemmed) or strings.
    """
    # Extract stemmed words if tuples, otherwise use as-is
    if tokens1 and isinstance(tokens1[0], tuple):
        set1 = set([stem for _, stem in tokens1])
    else:
        set1 = set(tokens1)
    
    if tokens2 and isinstance(tokens2[0], tuple):
        set2 = set([stem for _, stem in tokens2])
    else:
        set2 = set(tokens2)
    
    intersection = set1.intersection(set2)
    union = set1.union(set2)

    if not union:
        return 0.0

    return len(intersection) / len(union)
