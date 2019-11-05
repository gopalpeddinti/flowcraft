#!/usr/bin/env python3

import os
import json
from xml.etree import cElementTree as ElementTree

from flowcraft_utils.flowcraft_base import get_logger, MainWrapper

"""
Purpose
-------

This module is intended to process the xml files generated by
 pneumocat proces to generate a report.


Expected input
--------------


Generated output
----------------
- ``.report.jason``: Data structure for the report
- ``{$sample_id}_pneumocat.tsv``: Tsv with the results

Code documentation
------------------

"""

__version__ = "1.0.0"
__build__ = "05.11.2019"
__template__ = "pneumocat-nf"

logger = get_logger(__file__)

if __file__.endswith(".command.sh"):
    XML_RESULT = '$res'
    SAMPLE_ID = '$sample_id'
    logger.debug("Running {} with parameters:".format(
        os.path.basename(__file__)))
    logger.debug("SAMPLE_ID: {}".format(SAMPLE_ID))
    logger.debug("XML_RESULT: {}".format(XML_RESULT))


class XmlListConfig(list):
    def __init__(self, aList):
        for element in aList:
            if element:
                # treat like dict
                if len(element) == 1 or element[0].tag != element[1].tag:
                    self.append(XmlDictConfig(element))
                # treat like list
                elif element[0].tag == element[1].tag:
                    self.append(XmlListConfig(element))
            elif element.text:
                text = element.text.strip()
                if text:
                    self.append(text)


class XmlDictConfig(dict):
    """
    Example usage:

    >>> tree = ElementTree.parse('your_file.xml')
    >>> root = tree.getroot()
    >>> xmldict = XmlDictConfig(root)

    Or, if you want to use an XML string:

    >>> root = ElementTree.XML(xml_string)
    >>> xmldict = XmlDictConfig(root)

    And then use xmldict for what it is... a dict.
    """
    def __init__(self, parent_element):
        if parent_element.items():
            self.update(dict(parent_element.items()))
        for element in parent_element:
            if element:
                # treat like dict - we assume that if the first two tags
                # in a series are different, then they are all different.
                if len(element) == 1 or element[0].tag != element[1].tag:
                    aDict = XmlDictConfig(element)
                # treat like list - we assume that if the first two tags
                # in a series are the same, then the rest are the same.
                else:
                    # here, we put the list in dictionary; the key is the
                    # tag name the list elements all share in common, and
                    # the value is the list itself
                    aDict = {element[0].tag: XmlListConfig(element)}
                # if the tag has attributes, add those to the dict
                if element.items():
                    aDict.update(dict(element.items()))
                self.update({element.tag: aDict})
            # this assumes that if you've got an attribute in a tag,
            # you won't be having any text. This may or may not be a
            # good idea -- time will tell. It works for the way we are
            # currently doing XML configuration files...
            elif element.items():
                self.update({element.tag: dict(element.items())})
            # finally, if there are no child tags and no attributes, extract
            # the text
            else:
                self.update({element.tag: element.text})

@MainWrapper
def main(xml_file, sample_id):
    """Main executor of the process_newick template.

    Parameters
    ----------
    xml_file : str
        path to the xml file.

    sample_id: str
        sample name

    """

    logger.info("Starting {} xml file processing".format(sample_id))

    # Open XML document using minidom parser
    tree = ElementTree.parse(xml_file)
    root = tree.getroot()
    xmldict = XmlDictConfig(root)
    logger.info("Serotype found: {}".format(xmldict['results']['result']['value']))

    # write report in json format
    with open(".report.json", "w") as json_report:
        json_dic = {
            "tableRow": [{
                "sample": sample_id,
                "data": [
                    {"header": "Serotype",
                     "value": xmldict['results']['result']['value'],
                     "table": "typing",
                     "columnBar": False}
                ]
        }]}

        json_report.write(json.dumps(json_dic, separators=(",", ":")))

    with open(".status", "w") as status_fh:
        status_fh.write("pass")


if __name__ == '__main__':
    main(XML_RESULT, SAMPLE_ID)
