def stemming_ays(word):
    prefixes = [
        'meng', 'meny', 'men', 'mem', 'me',
        'peng', 'pen', 'pem', 'pe',
        'ber', 'per', 'di', 'ke', 'se', 'ter'
    ]


    suffixes = ['kan', 'an', 'i', 'lah', 'kah', 'nya']

    for p in prefixes:
        if word.startswith(p):
            word = word[len(p):]
            break

    for s in suffixes:
        if word.endswith(s):
            word = word[:-len(s)]
            break

    return word

def stemming_process(tokens):
    return [stemming_ays(t) for t in tokens]
