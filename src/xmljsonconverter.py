"""
.. module:: xmljsonconverter

   This module provides a conversion tool for converting from JSON to XML.

"""
import json
from helper import convert


class XMLJSONConverter():

  """
  .. class:: XMLJSONConverter()

     This class provides a conversion tool for converting from JSON
     files to XML.
  """
  def __init__(self, root_object=True, root_object_name='object'):
    """
    Initialise class:
    :TODO: initialisation/configuration logic can be add here

    :param root_object: add root object to output, default=True
    :param root_object_name: root object name, default="Object"

    """
    self.status = 'init'
    self.root_object = root_object
    self.root_object_name = root_object_name



  def convertJSONtoXML(self, json_file, xml_file="output.xml"):
    """
    .. method:: convertJSONtoXML(json_file, xml_file)

       This method converts the JSON in the given file to the XML and
       outputs to the given file.

       The implementer of this method is responsible for opening both
       files, reading from the JSON file and writing to the XML
       file. He must ensure that all the proper error handling is
       performed.

       :param str json_file: A string representing a file path to a
                             JSON file.
       :param str xml_file: A string representing a file path to
                            output XML after converting it from the
                            given JSON file
       :returns: True if success, else False
       :rtype: Boolean
    """

    json_data = open(json_file)
    data = json.load(json_data)
    json_data.close()

    output = []

    add_output_line = output.append

    if type(data) in [dict, list]:

        if self.root_object == True:

          add_output_line('<%s>%s</%s>' % (
            self.root_object_name,
            convert(data),
            self.root_object_name,
          )
                  )
        else:

          add_output_line('%s' % (convert(data)))

    else:
        add_output_line('%s' % convert(data, add_name=False))

    output_file = open(xml_file, "wb")

    output_file.write(''.join(output).encode('utf-8'))

    output_file.close()

    print("XML output is successfully saved to : {}".format(xml_file))

    return True
