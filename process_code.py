#!/usr/bin/env python

import os
import sys
import subprocess
import visionAPI as vAPI
import iCompileServer as server

def get_text_from_files(vision, input_filenames):
    """Call the Vision API on a file and index the results."""
    texts = vision.detect_text(input_filenames)
    print texts
    for filename, text in texts.items():
        extract_descriptions(filename, text)

def extract_descriptions(input_filename, texts):
    """Gets and indexes the text that was detected in the image."""
    if texts:
        document = extract_description(texts)
        runCode(document)
    else:
        if texts == []:
            print('%s had no discernible text.' % input_filename)

def extract_description(texts):
    document = ''
    for word in texts[0]['description']:
        document += word
    return document

def runCode(codeString):
    """Wraps code in main and adds include statements."""
    header = "#include <stdlib.h>\n#include <stdio.h>\n"
    main_declaration = "int main(int argc, char* argv[]){\n"
    main_close = "}\n"
    wrapped_code = header + main_declaration + codeString + main_close
    print wrapped_code
    with open("program.c", "w+") as program:
        program.write(wrapped_code)
    subprocess.call(["gcc", "program.c", "-o",  "program"])
    subprocess.call(["./program"])
    os.remove("program")

def main(argv):
    """Walk through all the not-yet-processed image files in the given
    directory, extracting any text from them and adding that text to an
    inverted index.
    """
    # Create a client object for the Vision API
    vision = vAPI.VisionApi()
    input_filenames = argv[1:]
    document = get_text_from_files(vision, input_filenames)

if __name__ == "__main__":
    main(sys.argv)
