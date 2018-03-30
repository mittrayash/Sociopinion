import re
from textblob import TextBlob
sentence = """
My 7 yr old daughter, as we discussed the family tree: “Dada, we are NOT related to Donald Trump.
"""
# sentence = sentence.replace('"', "\"")
sentence = sentence.replace("'", "")
sentence = sentence.replace('"', "")
sentence = sentence.replace(':', "")
print(sentence)
test = TextBlob(sentence)
pol = test.sentiment.polarity
print(pol)
