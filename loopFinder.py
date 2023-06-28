import xml.etree.ElementTree as ET
import io

# Gets XML tag and returns word inside <>
def extract_word_from_list(word_list):
    # Check if the list has exactly one element
    if len(word_list) == 1:
        # Extract the word by removing the angle brackets
        word = word_list[0].strip('<>')
        return word
    else:
        return None

# Finds children tags
def find_children_tags(xml_string, parent_tag):
    root = ET.fromstring(xml_string)
    children_tags = set()

    for parent in root.iter(parent_tag):
        for child in parent:
            children_tags.add(child.tag)

    return list(children_tags)

# Find loop in XML
def loopXML(xml_data):
    xml_data = xml_data.strip()  # Remove leading and trailing whitespaces
    file_obj = io.StringIO(xml_data)  # Create a file-like object from the XML data
    last_closing = ""
    matching_tags = set()  # Use a set to store unique matching tags

    for event, elem in ET.iterparse(file_obj, events=("start", "end")):
        if event == "start":
            cleaned_last_closing = last_closing.replace("<", "").replace("/", "").replace(">", "")
            if elem.tag == cleaned_last_closing:
                matching_tags.add(elem.tag)

        elif event == "end":
            closing_tag = f"</{elem.tag}>"
            last_closing = closing_tag

    return list(matching_tags)  # Convert the set back to a list

# Checks XML for loops
def findLoopXML(xmlList):
    xmlLoops = set()
    for xml in xmlList:
        loops = loopXML(xml)
        for loop in loops:
            xmlLoops.add(loop)
    xmlLoops = list(xmlLoops)
    return xmlLoops

# Find loop in Paragrpahs
def loopParagraph(word_list, text):
    word_count = []

    for word in word_list:
        word = word.replace(" ", "")
        formatted_word = f"<{word}>"
        count = text.lower().count(formatted_word.lower())
        word_count.append([formatted_word, count])

    loopParagraph = []
    for word in word_count:
        if word[1] > 1:
            loopParagraph.append(word)
    return loopParagraph

# Checks if loop in paragraph
def findLoopParagraph(clusterList, wordList):

    for cluster in clusterList:
        foundLoop = set()
        foundCildren = set()
        for paragraph in cluster.paragraphs:
            loops = loopParagraph(wordList ,paragraph.modContent)
            # If loop detected
            if len(loops) > 0:
                for loop in loops:
                    paragraph.isLoop = True
                    paragraph.loop.append(loop[0])
                    foundLoop.add(loop[0])
                xmlWord = extract_word_from_list(list(foundLoop))
                childrenTags = find_children_tags(paragraph.xml, xmlWord)
                for child in childrenTags:
                    foundCildren.add(child)

        foundLoop = list(foundLoop)
        foundCildren = list(foundCildren)
        if len(foundLoop) > 0:
            cluster.loop.append(foundLoop)
            cluster.loop.append(foundCildren)