from farasa.pos import FarasaPOSTagger
from farasa.ner import FarasaNamedEntityRecognizer
from farasa.diacratizer import FarasaDiacritizer
from farasa.segmenter import FarasaSegmenter
from farasa.stemmer import FarasaStemmer


def tokenize_posttag(text):
    pos_tagger = FarasaPOSTagger()
    pos_tagged_text = pos_tagger.tag(text)
    for txt in pos_tagged_text.split('\n'):
        row_pos_tags = txt.split('/')
        pos_tags = list()
        for i, e in enumerate(row_pos_tags):

            if i == 0:
                token = e
            else:
                pos_tag = e.split()[0]
                tokens, poss = token.split('+'), pos_tag.split('+')
                tokens = [t for t in tokens if t]
                poss = [p for p in poss if p]
                if len(tokens) == len(poss):
                    for ii in range(len(tokens)):
                        pos_tags.append((tokens[ii], poss[ii]))
                else:
                    print('error:', tokens, poss)
                token = ' '.join(e.split()[1:])
        print(pos_tags)