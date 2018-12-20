import argparse
import json
import sys

from helper import XMLJSONConverterException
from xmljsonconverter import XMLJSONConverter



def main(arguments=None):

    parser = argparse.ArgumentParser(description='Utility to convert json to valid xml.')

    parser.add_argument('--jsonfile', dest='jsonfile', action='store')
    parser.add_argument('--xmlfile', dest='xmlfile', action='store')

    output_filename = 'xml_out.xml'
    input_filename = None


    try:

        # check for known or positional argument
        args = parser.parse_known_args()


        named_arguments = args[0]
        positional_argumets = args[1]

        if positional_argumets:
            # set positional argument

            input_filename = positional_argumets[0]
            if len(args[1]) > 1:
                output_filename = positional_argumets[1]

        if named_arguments.jsonfile:
            # set named arguments, given priority over positional arguments

            input_filename = named_arguments.jsonfile
            if named_arguments.xmlfile:
                output_filename = named_arguments.xmlfile

    except Exception as e:

        raise XMLJSONConverterException("Some error while initialising check parameters again")


    if input_filename:

        try:

            xml_json = XMLJSONConverter()
            xml_json.convertJSONtoXML(input_filename, output_filename)

        except IOError as e:

            raise XMLJSONConverterException("File parsing or I/O error encounteres ({0}): {1}".
                                            format(e.errno, e.strerror))

    else:

        raise XMLJSONConverterException("Input File is required")



if __name__ == "__main__":
    main(sys.argv)
