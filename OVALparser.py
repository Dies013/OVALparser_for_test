import xml.etree.ElementTree as ET
import pandas as pd


path = 'D:/interviews/R-vision/rhel-8.oval.xml'


tree = ET.parse(path)
root = tree.getroot()

ns = {'oval': 'http://oval.mitre.org/XMLSchema/oval-definitions-5'}


# Использовал для исследования файла
# def extract_tags(obj):
#     tags = list()
#     for elem in obj.iter():
#         tags.append(elem.tag)
#     return tags

# tags = parser_functions.extract_tags(root)
# print(tags)
# tags_df = pd.DataFrame(data=tags, columns=['Tag',])
# tags_df.to_excel('tags_df.xlsx')

# tags = parser_functions.extract_tags(root.findall('oval:tests', ns)[0])
# tags_df = pd.DataFrame(data=tags, columns=['Tag',])
# tags_df.to_excel('tags_df.xlsx')


def parse_criteria(element):
    conditions = []
    for child in element:
        if child.tag.endswith('criterion'):
            conditions.append(child.get('comment'))
        elif child.tag.endswith('criteria'):
            conditions.append(parse_criteria(child))
    return conditions


data = []
namespace = {'oval': 'http://oval.mitre.org/XMLSchema/oval-definitions-5'}

for definition in root.findall('oval:definitions/oval:definition', namespace):
    title = definition.find('oval:metadata/oval:title', namespace).text
    description = definition.find('oval:metadata/oval:description', namespace).text
    severity = definition.find('oval:metadata/oval:advisory/oval:severity', namespace).text
    cves = ', '.join([cve.text for cve in definition.findall('oval:metadata/oval:advisory/oval:cve', namespace)])

    criteria = definition.find('oval:criteria', namespace)
    parsed_criteria = parse_criteria(criteria)

    data.append({'Title': title, 'Severity': severity, 'Description': description, 'CVEs': cves, 'Criteria': parsed_criteria})

df = pd.DataFrame(data)
df.to_excel('vulnerabilities.xlsx', index=False)
