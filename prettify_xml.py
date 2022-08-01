import lxml.etree as ET
from utils.files import choose_file

xml_file = choose_file('./', '.urdf', filetype_name='URDF file')

parser = ET.XMLParser(remove_blank_text=True)
tree = ET.parse(xml_file, parser)
tree.write(xml_file.name, pretty_print=True)
