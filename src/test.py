from yake import yake
from rake import rake
import pprint
import os
import time

## Setup
pp = pprint.PrettyPrinter(indent=4)
script_dir = os.path.dirname(__file__)
stoppath = os.path.join(script_dir, "stoplist/it.txt")

documents = ["micromega", "valore_tempo"]
documents_paths = [
    os.path.join(script_dir, "documents/" + doc + ".txt") for doc in documents
]


rake_object = rake.Rake(stoppath, 5, 3, 4)
kwe = yake.KeywordExtractor(stop_file=stoppath)


def average(lst):
    return sum(lst) / len(lst)


def test(ke, printer):
    for document in documents_paths:
        sample_file = open(document, "r", encoding="utf-8")
        text = sample_file.read()
        times = []
        start_time = time.time()
        keywords = []
        for _ in range(1, 21):
            keywords = ke(text)
            times.append(time.time() - start_time)
        times.sort()
        print("###")
        print("Document", os.path.basename(document))
        print("Worst: ", times[-1])
        print("Best: ", times[0])
        print("Average: ", average(times[1:-1]))
        # print('Keywords: ')
        # printer(keywords)

def print_k(keywords):
    for kw in keywords:
        print(kw)

if __name__ == "__main__":
    print("-----")
    print("RAKE")
    print("-----")
    test(ke=rake_object.run, printer=print_k)
    print("-----")
    print("YAKE")
    print("-----")
    test(ke=kwe.extract_keywords, printer=print_k)
