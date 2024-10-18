import re

# https://github.com/kristopolous/Porter-Stemmer/blob/master/PorterStemmer1980.js
# Improvals are made
def porter_stemmer(word, debug=False):
    step2list = {
        "ational": "ate",
        "tional": "tion",
        "enci": "ence",
        "anci": "ance",
        "izer": "ize",
        "bli": "ble",
        "alli": "al",
        "entli": "ent",
        "eli": "e",
        "ousli": "ous",
        "ization": "ize",
        "ation": "ate",
        "ator": "ate",
        "alism": "al",
        "iveness": "ive",
        "fulness": "ful",
        "ousness": "ous",
        "aliti": "al",
        "iviti": "ive",
        "biliti": "ble",
        "logi": "log",
        "est": "e",  # [IMPROVEMENT] HANDLE cheapest case
    }

    step3list = {
        "icate": "ic",
        "ative": "",
        "alize": "al",
        "iciti": "ic",
        "ical": "ic",
        "ful": "",
        "ness": ""
    }

    c = "[^aeiou]"  # consonant
    v = "[aeiouy]"  # vowel
    C = c + "[^aeiouy]*"  # consonant sequence
    V = v + "[aeiou]*"  # vowel sequence

    mgr0 = re.compile("^(" + C + ")?" + V + C)  # [C]VC... is m>0
    meq1 = re.compile("^(" + C + ")?" + V + C + "(" + V + ")?$")  # [C]VC[V] is m=1
    mgr1 = re.compile("^(" + C + ")?" + V + C + V + C)  # [C]VCVC... is m>1
    s_v = re.compile("^(" + C + ")?" + v)  # vowel in stem

    def dummy_debug(*args):
        pass

    def real_debug(*args):
        print(' '.join(map(str, args)))

    debug_function = real_debug if debug else dummy_debug

    if len(word) < 3:
        return word

    firstch = word[0]
    if firstch == "y":
        word = firstch.upper() + word[1:]

    # Step 1a
    word = re.sub(r'^(.+?)(ss|i)es$', r'\1\2', word)
    word = re.sub(r'^(.+?)([^s])s$', r'\1\2', word)

    # Step 1b
    if re.search(r'^(.+?)eed$', word):
        fp = re.findall(r'^(.+?)eed$', word)[0]
        if mgr0.search(fp):
            word = re.sub(r'eed$', 'ee', word)
    elif re.search(r'^(.+?)(ed|ing)$', word):
        fp = re.findall(r'^(.+?)(ed|ing)$', word)[0]
        stem = fp[0]
        if s_v.search(stem) and not re.search(r'thing$', word):  # [IMPROVEMENT]
            word = stem
            if re.search(r'(at|bl|iz)$', word):
                word += "e"
            elif re.search(r'([^aeiouylsz])\1$', word):
                word = re.sub(r'.$', '', word)
            elif re.search(r'^' + C + v + r'[^aeiouwxy]$', word):
                word += "e"

    # Step 1c
    if re.search(r'^(.*' + v + r'.*)y$', word) and not re.search(r'sy$', word):
        word = re.sub(r'y$', 'i', word)

    # Step 2
    if re.search(r'^(.+?)(ational|tional|enci|anci|izer|bli|alli|entli|eli|ousli|ization|ation|ator|alism|iveness|fulness|ousness|aliti|iviti|biliti|logi|est)$', word):
        fp = re.findall(r'^(.+?)(ational|tional|enci|anci|izer|bli|alli|entli|eli|ousli|ization|ation|ator|alism|iveness|fulness|ousness|aliti|iviti|biliti|logi|est)$', word)[0]
        stem = fp[0]
        suffix = fp[1]
        if mgr0.search(stem):
            word = stem + step2list[suffix]

    # Step 3
    if re.search(r'^(.+?)(icate|ative|alize|iciti|ical|ful|ness)$', word):
        fp = re.findall(r'^(.+?)(icate|ative|alize|iciti|ical|ful|ness)$', word)[0]
        stem = fp[0]
        suffix = fp[1]
        if mgr0.search(stem):
            word = stem + step3list[suffix]

    # Step 4
    if re.search(r'^(.+?)(al|ance|ence|er|ic|able|ible|ant|ement|ment|ent|ou|ism|ate|iti|ous|ive|ize)$', word):
        fp = re.findall(r'^(.+?)(al|ance|ence|er|ic|able|ible|ant|ement|ment|ent|ou|ism|ate|iti|ous|ive|ize)$', word)[0]
        stem = fp[0]
        if mgr1.search(stem):
            word = stem
    elif re.search(r'^(.+?)(s|t)(ion)$', word):
        fp = re.findall(r'^(.+?)(s|t)(ion)$', word)[0]
        stem = fp[0] + fp[1]
        if mgr1.search(stem):
            word = stem

    # Step 5
    if re.search(r'^(.+?)e$', word):
        fp = re.findall(r'^(.+?)e$', word)[0]
        stem = fp
        if (mgr1.search(stem) or meq1.search(stem) and not re.search(r'^' + C + v + r'[^aeiouwxy]$', stem)) and (not re.search(r'^(.+?)(ce|ge|ke|le|se|ve)$', word)):  # [IMPROVEMENT]
            print ("word = stem")
            word = stem

    if re.search(r'll$', word) and mgr1.search(word):
        word = re.sub(r'll$', 'l', word)

    if firstch == "y":
        word = firstch.lower() + word[1:]

    return word