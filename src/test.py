import yake
from rake import rake
import pprint
import os
import time
from typing import TypedDict

## Setup
pp = pprint.PrettyPrinter(indent=4)
script_dir = os.path.dirname(__file__)


class Document(TypedDict):
    source: str
    lang: str
    topics: list[str]


documents: list[Document] = [
    {
        "source": "sole_24_ore_chatgpt",
        "lang": "it",
        "topics": [
            "garante per la privacy",
            "italia",
            "openai",
            "privacy",
            "chatgpt",
        ],
    },
    {
        "source": "guardian_cracked_tiles_wonky_gutters_leaning_walls",
        "lang": "en",
        "topics": [
            "homes",
            "construction industry",
            "property",
            "house prices",
            "features",
        ],
    },
    {
        "source": "focus_virgin_galactic",
        "lang": "it",
        "topics": [
            "spazio",
            "virgin galactic",
            "turismo spaziale",
            "walter villadei",
            "aeronautica militare",
            "missioni spaziali",
        ],
    }
    # "micromega",
    #          "valore_tempo"
]


def get_doc_path(input: str):
    return os.path.join(script_dir, "documents/" + input + ".txt")


def get_keyword_extractor(type: str, lang: str, stop: str):
    if type == "rake":
        r = rake.Rake(stop, 5, 3, 4)
        return r.run
    elif type == "yake":
        y = yake.KeywordExtractor(lan=lang)
        # y = yake.KeywordExtractor(stop_file=stop)
        return y.extract_keywords
    else:
        raise Exception("Invalid type")


# rake_object = rake.Rake(stoppath, 5, 3, 4)
# kwe = yake.KeywordExtractor(stop_file=stoppath)


def average(lst):
    return sum(lst) / len(lst)


def test(type, printer):
    for document in documents:
        path = get_doc_path(document["source"])
        stop = os.path.join(script_dir, "stoplist/" + document["lang"] + ".txt")

        sample_file = open(path, "r", encoding="utf-8")
        text = sample_file.read().lower()
        times = []
        start_time = time.time()
        keywords = []
        for _ in range(1, 21):
            ke = get_keyword_extractor(type=type, lang=document["lang"], stop=stop)
            keywords = ke(text)
            times.append(round(time.time() - start_time, 3))
        # times.sort()
        print("###")
        print("Document", os.path.basename(path))
        print("Worst: ", times[-1])
        print("Best: ", times[0])
        print("Times: ", times)
        print("Average: ", average(times))
        print("Keywords: ")
        nk = keywords[:5]

        # foreach element of nk test if it is present in topics
        t_p = 0
        t_n = 0
        f_n = 0
        for kw in nk:
            # print('key:', kw[0])
            if kw[0] in document["topics"]:
                t_p += 1
            else:
                t_n += 1
        for t in document["topics"]:
            if t not in nk:
                f_n += 1
        print("t_p:", t_p)
        print("t_n:", t_n)
        print("f_n:", f_n)
        precision = t_p / (t_p + t_n)
        recall = t_p / (t_p + f_n) if t_p + f_n > 0 else 0
        f1 = (
            (2 * (precision * recall) / (precision + recall))
            if precision + recall > 0
            else 0
        )
        print("Precision: ", precision)
        print("Recall: ", recall)
        print("F1: ", f1)
        printer(nk)


def print_k(keywords):
    for kw in keywords:
        print(kw)


if __name__ == "__main__":
    print("-----")
    print("RAKE")
    print("-----")
    test(type="rake", printer=print_k)
    print("-----")
    print("YAKE")
    print("-----")
    test(type="yake", printer=print_k)
