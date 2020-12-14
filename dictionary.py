from bs4 import BeautifulSoup
import requests
import json
from colorama import init
from termcolor import colored
import csv
import re

init()

tr_definitions = []
en_definition = ""
collocations = []
synonyms = []
word_forms = {
    "Noun": [],
    "Verb": [],
    "Adjective": [],
    "Adverb": []
}
sentences = []

pattern = '(\w+)\s*(-t|-d|-c|-syn|-sen|-wf)?\s*(-n|-v|-adj|-adv)?'

star_colors = ["red", "green", "yellow", "blue", "magenta", "white"]


def get_turk(word):
    source = requests.get(f"https://tureng.com/en/turkish-english/{word}").text
    soup = BeautifulSoup(source, "lxml")
    turk_table = soup.find("table").find_all("td", class_="tr ts")

    global tr_definitions
    tr_definitions.append(turk_table[0].find("a").text)
    try:
        tr_definitions.append(turk_table[1].find("a").text)
        tr_definitions.append(turk_table[2].find("a").text)
    except:
        pass

    return ", ".join(tr_definitions)


def get_sentences(word):
    source = requests.get(f"https://sentence.yourdictionary.com/{word}").text
    soup = BeautifulSoup(source, "lxml")
    sentences_table = soup.find_all("div", class_="sentence component")

    global sentences
    sentences.append(sentences_table[0].find("p").text)
    try:
        sentences.append(sentences_table[1].find("p").text)
        sentences.append(sentences_table[2].find("p").text)
    except:
        pass

    return " || ".join(sentences)


def get_en(word):
    source = requests.get(f"https://www.yourdictionary.com/{word}").text
    soup = BeautifulSoup(source, "lxml")
    def_en = soup.find("div", class_="definition").find("div").text

    if ("The definition of" in def_en):
        def_en = (def_en[18]).upper() + def_en[19:]
        return def_en
    else:
        return def_en


def get_synonyms(word):
    source = requests.get(
        f"http://www.synonymy.com/synonym.php?word={word}").text
    soup = BeautifulSoup(source, "lxml")
    sy_table = soup.find_all("div", class_="defbox")[
        1].find("ol").find("li").find_all("a")

    for sy in sy_table:
        global synonyms
        synonyms.append(sy.text)

    return ", ".join(synonyms)


def get_forms(word, form):
    if (form == "noun"):
        source = requests.get(
            f"https://www.wordhippo.com/what-is/the-noun-for/{word}.html").text
        soup = BeautifulSoup(source, "lxml")
        noun_table = soup.find_all("div", class_="defv2wordtype")
        for i in range(0, 4):
            try:
                word_forms["Noun"].append(noun_table[i].text)
            except:
                pass
        return ", ".join(word_forms["Noun"])
    elif (form == "verb"):
        source = requests.get(
            f"https://www.wordhippo.com/what-is/the-verb-for/{word}.html").text
        soup = BeautifulSoup(source, "lxml")
        verb_table = soup.find_all("div", class_="defv2wordtype")
        for i in range(0, 4):
            try:
                word_forms["Verb"].append(verb_table[i].text)
            except:
                pass
        return ", ".join(word_forms["Verb"])
    elif (form == "adjective"):
        source = requests.get(
            f"https://www.wordhippo.com/what-is/the-adjective-for/{word}.html").text
        soup = BeautifulSoup(source, "lxml")
        adj_table = soup.find_all("div", class_="defv2wordtype")
        for i in range(0, 4):
            try:
                word_forms["Adjective"].append(adj_table[i].text)
            except:
                pass
        return ", ".join(word_forms["Adjective"])
    elif (form == "adverb"):
        source = requests.get(
            f"https://www.wordhippo.com/what-is/the-adverb-for/{word}.html").text
        soup = BeautifulSoup(source, "lxml")
        adv_table = soup.find_all("div", class_="defv2wordtype")
        for i in range(0, 4):
            try:
                word_forms["Adverb"].append(adv_table[i].text)
            except:
                pass
        return ", ".join(word_forms["Adverb"])


def get_collocations(word):
    try:
        response = requests.get(
            f"http://www.just-the-word.com/api/combinations?word={word}").text
        data = json.loads(response)
    except:
        pass

    i = 0
    try:
        for item in data["combinations"][1]["list"]:
            if (not i == 5):
                global collocations
                collocations.append(item[2])
                i += 1
    except:
        for item in data["combinations"][0]["list"]:
            if (not i == 5):
                collocations.append(item[2])
                i += 1

    return ", ".join(collocations)


def search(word):
    try:
        print(colored("Turkish:", "cyan", "on_grey", ["bold"]), get_turk(word))
    except:
        print(colored("Turkish:", "cyan", "on_grey", ["bold"]), None)

    try:
        print(colored("Definition:", "cyan",
                      "on_grey", ["bold"]), get_en(word))
    except:
        print(colored("Definition:", "cyan", "on_grey", ["bold"]), colored(
            "ERROR", "red", "on_grey", ["bold"]))

    try:
        print(colored("Collocations:", "cyan", "on_grey",
                      ["bold"]), get_collocations(word))
    except:
        print(colored("Collocations:", "cyan", "on_grey",
                      ["bold"]), colored("100 words/day limit reached.", "white", "on_grey", ["reverse"]))

    try:
        print(colored("Synonyms:", "cyan", "on_grey",
                      ["bold"]), get_synonyms(word))
    except:
        print(colored("Synonyms:", "cyan", "on_grey", ["bold"]), None)

    try:
        print(colored("Sentences:", "cyan", "on_grey",
                      ["bold"]), get_sentences(word))
    except:
        print(colored("Sentences:", "cyan", "on_grey", ["bold"]), None)

    print(colored("Word formations:", "cyan", "on_grey", ["bold"]))
    try:
        print(colored("\tNoun:", "cyan", "on_grey",
                      ["bold"]), get_forms(word, "noun"))
    except:
        print(colored("\tNoun:", "cyan", "on_grey", ["bold"]), None)

    try:
        print(colored("\tVerb:", "cyan", "on_grey",
                      ["bold"]), get_forms(word, "verb"))
    except:
        print(colored("\tVerb:", "cyan", "on_grey", ["bold"]), None)

    try:
        print(colored("\tAdjective:", "cyan", "on_grey",
                      ["bold"]), get_forms(word, "adjective"))
    except:
        print(colored("\tAdjective:", "cyan", "on_grey", ["bold"]), None)

    try:
        print(colored("\tAdverb:", "cyan", "on_grey",
                      ["bold"]), get_forms(word, "adverb"))
    except:
        print(colored("\tAdverb:", "cyan", "on_grey", ["bold"]), None)


def store(word):
    with open("words.csv", "a") as csv_file:
        csv_writer = csv.writer(csv_file)
        try:
            csv_writer.writerow(["", "", "", "", "", "", "", "", "", ""])
            csv_writer.writerow(["Word", "Turkish", "Definition", "Collocations", "Synonyms",
                                 "Sentences", "Noun F.", "Verb F.", "Adjective F.", "Adverb F."])
            csv_writer.writerow([word, get_turk(word), get_en(word), get_collocations(word), get_synonyms(word), get_sentences(
                word), get_forms(word, "noun"), get_forms(word, "verb"), get_forms(word, "adjective"), get_forms(word, "adverb")])
        except:
            try:
                csv_writer.writerow([word, get_turk(word), get_en(word), "100 words/day limit reached.", get_synonyms(word), get_sentences(
                    word), get_forms(word, "noun"), get_forms(word, "verb"), get_forms(word, "adjective"), get_forms(word, "adverb")])
            except:
                pass


print(colored("\nFLAGS", "white", "on_grey", ["bold", "underline"]))
print("")


print(colored("-t:", "white", "on_grey", ["bold"]),
      colored("turkish", "white", "on_grey"))

print(colored("-d:", "white", "on_grey", ["bold"]),
      colored("definition", "white", "on_grey"))

print(colored("-c:", "white", "on_grey", ["bold"]),
      colored("collocations", "white", "on_grey"))

print(colored("-syn:", "white", "on_grey", ["bold"]),
      colored("synonyms", "white", "on_grey"))

print(colored("-sen:", "white", "on_grey", ["bold"]),
      colored("sentences", "white", "on_grey"))

print(colored("-wf:", "white", "on_grey", ["bold"]),
      colored("word formations", "white", "on_grey"))

print(colored("  -wf -n:", "white", "on_grey", ["bold"]),
      colored("noun form", "white", "on_grey"))

print(colored("  -wf -v:", "white", "on_grey", ["bold"]),
      colored("verb form", "white", "on_grey"))
print(colored("  -wf -adj:", "white", "on_grey", ["bold"]),
      colored("adjective form", "white", "on_grey"))
print(colored("  -wf -adv:", "white", "on_grey", ["bold"]),
      colored("adverb form", "white", "on_grey"))


print("\n", colored("Type 'berke' to exit.",
                    "red", "on_grey", ["bold"]), "\n")

while True:
    print(colored("*" * 50, "blue", "on_grey", ["bold"]))
    _word_ = input(colored("$Word: ", "yellow", "on_grey", ["bold"]))
    if (not _word_ == "berke"):
        tr_definitions = []
        en_definition = ""
        collocations = []
        synonyms = []
        word_forms = {
            "Noun": [],
            "Verb": [],
            "Adjective": [],
            "Adverb": []
        }
        sentences = []

        match = re.search(pattern, _word_)

        if (match):
            _word_ = match.group(1)
            if (match.group(2) == None):
                search(_word_)
                store(_word_)
            elif (match.group(2) == "-t"):
                try:
                    print(colored("Turkish:", "cyan",
                                  "on_grey", ["bold"]), get_turk(_word_))
                except:
                    print(colored("Turkish:", "cyan",
                                  "on_grey", ["bold"]), None)
            elif (match.group(2) == "-d"):
                try:
                    print(colored("Definition:", "cyan",
                                  "on_grey", ["bold"]), get_en(_word_))
                except:
                    print(colored("Definition:", "cyan", "on_grey", ["bold"]), colored(
                        "ERROR", "red", "on_grey", ["bold"]))
            elif (match.group(2) == "-c"):
                try:
                    print(colored("Collocations:", "cyan", "on_grey",
                                  ["bold"]), get_collocations(_word_))
                except:
                    print(colored("Collocations:", "cyan",
                                  "on_grey", ["bold"]), colored("100 words/day limit reached.", "white", "on_grey", ["reverse"]))
            elif (match.group(2) == "-syn"):
                try:
                    print(colored("Synonyms:", "cyan", "on_grey",
                                  ["bold"]), get_synonyms(_word_))
                except:
                    print(colored("Synonyms:", "cyan",
                                  "on_grey", ["bold"]), None)
            elif (match.group(2) == "-sen"):
                try:
                    print(colored("Sentences:", "cyan", "on_grey",
                                  ["bold"]), get_sentences(_word_))
                except:
                    print(colored("Sentences:", "cyan",
                                  "on_grey", ["bold"]), None)
            elif (match.group(2) == "-wf"):
                if (match.group(3) == None):
                    print(colored("Word formations:",
                                  "cyan", "on_grey", ["bold"]))
                    try:
                        print(colored("\tNoun:", "cyan", "on_grey",
                                      ["bold"]), get_forms(_word_, "noun"))
                    except:
                        print(colored("\tNoun:", "cyan",
                                      "on_grey", ["bold"]), None)

                    try:
                        print(colored("\tVerb:", "cyan", "on_grey",
                                      ["bold"]), get_forms(_word_, "verb"))
                    except:
                        print(colored("\tVerb:", "cyan",
                                      "on_grey", ["bold"]), None)

                    try:
                        print(colored("\tAdjective:", "cyan", "on_grey",
                                      ["bold"]), get_forms(_word_, "adjective"))
                    except:
                        print(colored("\tAdjective:", "cyan",
                                      "on_grey", ["bold"]), None)

                    try:
                        print(colored("\tAdverb:", "cyan", "on_grey",
                                      ["bold"]), get_forms(_word_, "adverb"))
                    except:
                        print(colored("\tAdverb:", "cyan",
                                      "on_grey", ["bold"]), None)
                elif(match.group(3) == "-n"):
                    try:
                        print(colored("Noun:", "cyan", "on_grey",
                                      ["bold"]), get_forms(_word_, "noun"))
                    except:
                        print(colored("Noun:", "cyan",
                                      "on_grey", ["bold"]), None)
                elif(match.group(3) == "-v"):
                    try:
                        print(colored("Verb:", "cyan", "on_grey",
                                      ["bold"]), get_forms(_word_, "verb"))
                    except:
                        print(colored("Verb:", "cyan",
                                      "on_grey", ["bold"]), None)
                elif(match.group(3) == "-adj"):
                    try:
                        print(colored("Adjective:", "cyan", "on_grey",
                                      ["bold"]), get_forms(_word_, "adjective"))
                    except:
                        print(colored("Adjective:", "cyan",
                                      "on_grey", ["bold"]), None)
                elif(match.group(3) == "-n"):
                    try:
                        print(colored("Adverb:", "cyan", "on_grey",
                                      ["bold"]), get_forms(_word_, "adverb"))
                    except:
                        print(colored("Adverb:", "cyan",
                                      "on_grey", ["bold"]), None)
                else:
                    pass
            else:
                pass
        else:
            print("pattern not found")
    else:
        print(colored("*" * 50, "blue", "on_grey", ["bold"]))
        print("\n", colored("Bye!",
                            "white", "on_grey", ["bold"]), "\n")
        break
