from lxml import etree
import re

def has_numbers(string):
    pattern = r'\d+'  # Regular expression pattern to match any digit
    return bool(re.search(pattern, string))
def test(xml_data, stringValues):

    # Parse XML using lxml
    root = etree.fromstring(xml_data)

    modified_paragraph = stringValues

    # Iterate over the elements in the XML
    for element in root.iter():
        if element.text is not None and element.text in modified_paragraph:
            modified_paragraph = replace_values(modified_paragraph, element)

    # returns modified paragraphs
    return modified_paragraph

def replace_values(brief, element):
    parent_tag = element.getparent().tag
    tag = element.tag
    text = element.text

    brief = brief.replace(text, f"<{parent_tag}><{tag}>")

    return brief
def replaceStringValues(element, stringValues):

    modified_paragraph = stringValues

    if element.text is not None and element.text in modified_paragraph:
        modified_paragraph = replace_values(modified_paragraph, element)

    # returns modified paragraphs
    return modified_paragraph

# Function to replace values
def replaceNumberValues(element, word):
    parent = element.getparent()
    if parent is not None:
        parent_tag = parent.tag
        tag = element.tag
        text = element.text

        # Skip whitespace values in the XML
        if text and text.strip():
            # Check if the text is a valid float
            try:
                float_value = float(text.replace("'", "").replace(",", ""))
            except ValueError:
                float_value = None

            # Try converting the word to a float
            try:
                wordTemp = word.replace("'", "").replace(",", "")
                word_float = float(wordTemp)
            except ValueError:
                word_float = None

            # Replace the word with XML element if it matches the XML float
            if float_value is not None and word_float is not None and float_value == word_float:
                return f"<{parent_tag}><{tag}>"

    return word


# Returns the same string but replaced with tags found in the XML file
def replaceValues(xml_data, stringValues):
    # Parse XML using lxml
    root = etree.fromstring(xml_data)

    modified_words = []

    lines = stringValues.split("-/-")
    for strings in lines:
        # checks if table part contains numbers of each by / separeted items
        if has_numbers(strings):
            # Split the stringValues into individual words/numbers
            words = strings.split()

            # Iterate over each word and search in the XML
            for word in words:
                found = False

                # Iterate over the elements in the XML
                for element in root.iter():
                    if element.text is not None:
                        #checks if number
                        try:
                            wordTemp = word.replace("'", "").replace(",", "").replace(")", "").replace(":", "")
                            word_float = float(wordTemp)
                            replaced_word = replaceNumberValues(element, word)
                        except:
                            # Try replacing the word with XML element if it matches the XML float
                            replaced_word = replaceStringValues(element, word)

                        if replaced_word != word:
                            modified_words.append(replaced_word)
                            found = True
                            break

                if not found:
                    modified_words.append(word)

        else:
            modified_words.append(test(xml_data,strings))

    modified_paragraph = ' '.join(modified_words)
    return modified_paragraph


