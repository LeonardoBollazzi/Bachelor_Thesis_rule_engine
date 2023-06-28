import xml.etree.ElementTree as ET
from collections import defaultdict
from xml.etree.ElementTree import ParseError
def read_xml_files(file_paths):
    xml_data_list = []

    for file_path in file_paths:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                xml_data = file.read()
                xml_data_list.append(xml_data)
        except FileNotFoundError:
            print(f"XML file not found: {file_path}")

    return xml_data_list

# Transform XML files to group them by same tags
def group_tags(xml_strings):
    grouped_tags = defaultdict(list)

    for xml_string in xml_strings:
        try:
            root = ET.fromstring(xml_string)
            for element in root.iter():
                if element.text is not None:
                    tag_name = element.tag
                    grouped_tags[tag_name].append(element.text)
        except ParseError:
            print(f"Invalid XML format: {xml_string}")

    result = []
    max_entries = max(len(entries) for entries in grouped_tags.values())

    for tag_name, entries in grouped_tags.items():
        xml_structure = f'<{tag_name}>'
        for i in range(max_entries):
            if i < len(entries):
                value = entries[i].strip()  # Remove leading and trailing whitespace
                value = value.replace('\n', '').replace('\t', '')  # Remove newline and tab characters
                value = value.replace('&', '&amp;')  # Replace '&' with '&amp;'
                xml_structure += f'<value>{value}</value>'
        xml_structure += f'</{tag_name}>'
        result.append(xml_structure)

    return result


