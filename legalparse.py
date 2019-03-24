#!/usr/bin/env python

import textract
import re

text = textract.process('Commercial-Law-Exam-Notep.pdf')
versus = 'v'

class CaseReferences(object):

    reference_re = re.compile(r'((?:[A-Z]{0,}[a-z]{0,}\s)+v[s\.]?\.?\s(?:[A-Z]{0,}[a-z]{0,}\s)+(?:[\[\(]\d+[\]\)])\s(?:[A-Z]+\s\d+))')

    # Each case reference object stores the origin filename by default.
    def __init__(self, filename):
        self.filename = filename
    
    # GetText method will extract the text from the given filename and returns True
    # if something was successfully loaded.
    def GetText(self):

        # TODO(sewid): Support PPTX text extractor.
        if self.filename.endswith('.pdf'):
            self.content = textract.process(self.filename)
        elif self.filename.endswith('.txt'):
            self.content = open(self.filename).read()
  

        if len(self.content) == 0:
            raise("error")
    
    # Parse will attempt to find legal references in text blocks.
    def Parse(self):
        oneline = self.content.replace("\n", " ")
        matches = self.reference_re.findall(oneline)
        references = []

        for m in matches:
            words = m.strip().split()


            # Start in the middle where " v " is
            vs = words.index(versus)

            # Parse backwards looking for either the beginning of the list of an uncapitalized words
            for i in range(vs-1, 0, -1):
                print words[i], words[i][0], words[i][0].islower()
                if words[i][0].islower():
                    references.append(" ".join(words[i+1:]))
                    break
            else:
                # It was fine as it was, inner loop was not broken.
                references.append(m.strip())

 
        return references
            


if __name__ == "__main__":
    c  = CaseReferences('Commercial-Law-Exam-Notep.pdf')
    c.GetText()
    p = c.Parse()

    print p

            

