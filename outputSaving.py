import re

def save_list_to_file(lst, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        for item in lst:
            file.write(item + '\n')


def saveOutput(clusterObjects, filePath):

    paragraphStrings = []
    ruleCounter = 1
    loopCounter = 1

    for cluster in clusterObjects:

        if len(cluster.clusterRule) > 0:
            paragraph = cluster.paragraphs[0]
            rules = ""
            for rule in cluster.clusterRule[0][0]:
                rules += rule.replace("/", " == ") + " / "
            #paragraphStrings.append(f"#Start Rule {ruleCounter}: "+ str(cluster.clusterRule[0][0]))
            paragraphStrings.append(f"#Start Rule {ruleCounter}: " + rules)
            paragraphStrings.append(str(paragraph.modContent))
            paragraphStrings.append(f"#End Rule {ruleCounter}: ")
            ruleCounter += 1

        elif len(cluster.loop) > 0:
            for paragraph in cluster.paragraphs:
                if paragraph.isLoop:
                    paragraphStrings.append(f"#Start Loop {loopCounter}: " + str(cluster.loop[0][0]) + " / " + str(cluster.loop[1]))
                    paragraphStringOutput = find_words(str(paragraph.modContent),cluster.loop[1] )
                    paragraphStrings.append(str(paragraphStringOutput))
                    paragraphStrings.append(f"#End Loop {loopCounter}: ")
                    ruleCounter += 1
                    break
        else:
            try:
                paragraphStrings.append(cluster.paragraphs[0].modContent)
            except:
                continue

        paragraphStrings.append(" ")

    save_list_to_file(paragraphStrings, filePath)

# Finds the loop output
def find_words(text, words_list):
    words_found = set()
    words_checked = []

    words = text.split()

    for word in words:
        words_checked.append(word)
        wordsNew = re.findall(r'<[^>]+>|[\w]+', word)
        for w in wordsNew:
            w = w.strip('<>')
            if w in words_list:
                words_found.add(word)
        if len(words_found) == len(words_list):
            break

    return ' '.join(words_checked)