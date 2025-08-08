import re
line = "@@4000161 Section : Life and Letters <p> I do n't remember hearing the phrase \" white guilt \" very much before the mid-1960s. Growing up black in the 1950s , I never had the impression that whites were much disturbed by guilt when it came to blacks . "
line = re.sub(r'^@@\d+\s*', '', line).rstrip()
SENT_SPLIT_PATTERN = re.compile(r'(?<=[。．！？!?\.])\s+')
sentences = SENT_SPLIT_PATTERN.split(line)
print(sentences)