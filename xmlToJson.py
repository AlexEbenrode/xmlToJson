# -*- coding: utf-8 -*-
import os
import sys
import getopt
import json
from lxml import etree


def showHelp():
    print("XML to json converter.")
    print("Search and convert all xml files include inner folders to json format.\n")
    print("usage: python3 xmlToJson.py [-i path] [-o path]")
    print("Options and arguments:")
    print("-i --input\t: Input folder absolute path.")
    print(
        "-o --output\t: Output folder absolute path. Default: output directory in script folder;"
    )
    return


def xmlToJson(xml):
    dictionary = {}
    if xml.tag is etree.Comment:
        dictionary["tag"] = "__comment"
    else:
        dictionary["tag"] = xml.tag
    dictionary["text"] = xml.text or ""
    dictionary["attributes"] = {}
    for item in xml.items():
        dictionary["attributes"][item[0]] = item[1]
    dictionary["items"] = []
    for element in xml:
        dictionary["items"].append(xmlToJson(element))

    return dictionary


def search(path, relative_path):
    if not os.path.exists(relative_path):
        os.mkdir(relative_path)
    for name in os.listdir(path):
        new_path = path + "/" + name
        if os.path.isdir(new_path):
            search(new_path, relative_path + "/" + name)

        elif os.path.isfile(new_path):
            if os.path.splitext(new_path)[1] == ".xml":
                with open(new_path, "r", encoding="utf-8") as file:
                    xml_string = file.read()
                    xml = etree.fromstring(bytes(xml_string, encoding="utf-8"))
                    dictionary = xmlToJson(xml)
                    with open(relative_path + "/" + name + ".json", "w") as json_file:
                        json_file.write(json.dumps(dictionary))


def main(argv):
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hi:o:", ["help", "input=", "output="])
    except getopt.GetoptError as err:
        print(err)
        sys.exit(2)

    input_path = None
    output_path = None

    for o, a in opts:
        if o in ("-h", "--help"):
            showHelp()
            sys.exit(0)
        elif o in ("-i", "--input"):
            input_path = a
        elif o in ("-o", "--output"):
            output_path = a
        else:
            assert False, "unhandled option"
    if input_path is None:
        input_path = input("Enter input folder absolute path: ")

    if output_path is None:
        output_path = (
            input("Enter output folder absolute path. Default: CWD/output: ")
            or "output"
        )

    if output_path == "output" and not os.path.exists("output"):
        os.mkdir("output")

    relative_path = output_path + "/" + os.path.basename(input_path)

    search(input_path, relative_path)


if __name__ == "__main__":
    main(sys.argv[1:])
