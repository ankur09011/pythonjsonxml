"""
Helper Functions/Classes:
This module contains generic helper functions/classes which are needed throughout for consistency.
"""


from __future__ import unicode_literals

import collections
import logging
import numbers


from random import randint




CONVERTOR_LOG = logging.getLogger("convert_data_to_xml")
# initialize list of unique ids
ids = []


class XMLJSONConverterException(Exception):
    """
    :TODO: Implement Custom Exception Class
    """
    pass


def sanity_check(value):
    """
    Check if provided JSON file is present valid and existing

    :TODO: implement more sanity check functions here

    :param value: Object
    :return: sanity as Boolean, True or False
    """
    pass


def unicode_me(something):
    """
    Converts strings with non-ASCII characters to unicode logging
    and other purpose.

    """
    try:
        return str(something, 'utf-8')
    except:
        return str(something)


def make_id(element, start=100000, end=999999):
    """Returns a random integer"""
    return '%s_%s' % (element, randint(start, end))


def get_unique_id(element):
    """Returns a unique id for a given element"""
    this_id = make_id(element)
    dup = True
    while dup:
        if this_id not in ids:
            dup = False
            ids.append(this_id)
        else:
            this_id = make_id(element)
    return ids[-1]


def change_xml_type_name(val):
    """

    Returns the data type for the xml type attribute

    :param val: object
    :return: xml type name as String
    """

    if type(val).__name__ in ('str', 'unicode'):
        return 'string'
    if type(val).__name__ in ('int', 'long'):
        return 'number'
    if type(val).__name__ == 'float':
        return 'float'
    if type(val).__name__ == 'bool':
        return 'boolean'
    if type(val).__name__ == 'NoneType':
        return 'null'
    if isinstance(val, dict):
        return 'object'
    if isinstance(val, collections.Iterable):
        return 'array'

    return type(val).__name__


def replace_escape_xml(s):
    """
    escape strings for unicode errors 
    :param s: string
    """
    if type(s) in [str]:
        
        s = unicode_me(s) #handle unicode 
        s = s.replace('\'', '&apos;')
        s = s.replace('<', '&lt;')
        s = s.replace('>', '&gt;')
        s = s.replace('&', '&amp;')
        s = s.replace('"', '&quot;')
        
    return s


def make_attrstring(attr):
    """Returns an attribute string in the form key="val" """
    attrstring = ' '.join(['%s="%s"' % (k, v) for k, v in attr.items()])
    return '%s%s' % (' ' if attrstring != '' else '', attrstring)


def key_is_valid_xml(key):

    try:
        # :TODO: implement key validity function
        return True
    except Exception:

        return False


def make_valid_xml_name(key, attr):
    """Tests an XML name and fixes it if invalid"""
    key = replace_escape_xml(key)
    attr = replace_escape_xml(attr)

    # pass through if key is already valid
    if key_is_valid_xml(key):
        return key, attr

    # prepend a lowercase n if the key is numeric
    if key.isdigit():
        return 'n%s' % (key), attr

    # replace spaces with underscores if that fixes the problem
    if key_is_valid_xml(key.replace(' ', '_')):
        return key.replace(' ', '_'), attr

    # key is still invalid - move it into a name attribute
    attr['name'] = key
    key = 'key'

    return key, attr


def convert(obj, add_name=True, parent='root'):

    """
    Logical routing call to convert function based on data type.
    Treat as interface for custom routing logic for data type
    """


    ids = False
    item_name = 'item'

    if type(obj) in [str, int, float]:
        return convert_int_str_to_xml(item_name, obj, add_name=add_name)

    if hasattr(obj, 'isoformat'):
        return convert_int_str_to_xml(item_name, obj.isoformat())

    if type(obj) == bool:
        print("boolean")
        return convert_bool_to_xml(item_name, obj, add_name=add_name)

    if obj is None:
        return convert_none_to_xml(item_name, '', add_name=add_name)

    if isinstance(obj, dict):
        print("dict")
        return convert_dict_to_xml(obj, ids, parent)

    if isinstance(obj, collections.Iterable):
        return convert_list_to_xml(obj, ids, parent)

    raise TypeError('Unsupported data type: %s (%s)' % (obj, type(obj).__name__))


def convert_dict_to_xml(obj, ids, parent):
    """
    Converts python dict into XML elements.
    """
    attr_type = True
    output = []
    add_output_line = output.append


    for key, val in obj.items():

        attr = {}

        key, attr = make_valid_xml_name(key, attr)


        if type(val) in [str, int, float]:
            add_output_line(convert_int_str_to_xml(key, val))

        elif hasattr(val, 'isoformat'): # datetime
            add_output_line(convert_int_str_to_xml(key, val.isoformat()))

        elif type(val) == bool:
            add_output_line(convert_bool_to_xml(key, val))

        elif isinstance(val, dict):
            if attr_type:
                attr['type'] = change_xml_type_name(val)
            types = change_xml_type_name(val)
            add_output_line('<%s name="%s">%s</%s>' % (
                types, key,
                convert_dict_to_xml(val, ids, key),
                types
            )
                    )

        elif isinstance(val, collections.Iterable):
            if attr_type:
                attr['type'] = change_xml_type_name(val)
            types = change_xml_type_name(val)
            add_output_line('<%s name="%s">%s</%s>' % (
                types,
                key,
                convert_list_to_xml(val, ids, key),
                types
            )
                    )

        elif val is None:
            add_output_line(convert_none_to_xml(key, val))

        else:
            raise TypeError('Unsupported data type: %s (%s)' % (
                val, type(val).__name__)
                            )

    return ''.join(output)


def convert_list_to_xml(items, unique_ids, parent):
    """
    Converts python list into an XML elements.
    """

    output = []
    add_output_line = output.append

    item_name = 'item'
    attr_type = True

    if unique_ids:
        this_id = get_unique_id(parent)


    for i, item in enumerate(items):

        attr = {} if not ids else { 'id': '%s_%s' % (this_id, i+ 1)}

        if type(item) in [str, int]:
            add_output_line(convert_int_str_to_xml(item_name, item, add_name=False))

        elif hasattr(item, 'isoformat'):
            add_output_line(convert_int_str_to_xml(item_name, item.isoformat()))

        elif type(item) == bool:
            add_output_line(convert_bool_to_xml(item_name, item, add_name=False))

        elif isinstance(item, dict):
            add_output_line('<object>%s </object>' % (convert(item),))

        elif isinstance(item, collections.Iterable):
            if not attr_type:
                add_output_line('<%s %s>%s</%s>' % (
                    item_name, make_attrstring(attr),
                    convert_list_to_xml(item, ids, item_name),
                    item_name,))
            else:
                add_output_line('<%s type="list"%s>%s</%s>' % (
                    item_name, make_attrstring(attr),
                    convert_list_to_xml(item, ids, item_name,),
                    item_name,
                )
                        )

        elif item is None:
            add_output_line(convert_none_to_xml(item_name, None,))

        else:
            raise TypeError('Unsupported data type: %s (%s)' % (
                item, type(item).__name__)
                            )
    return ''.join(output)


def convert_int_str_to_xml(key, val, add_name=True):
    """
    Converts a number or string into an XML element
    """
    attr = {}


    key, attr = make_valid_xml_name(key, attr)


    type = change_xml_type_name(val)

    if add_name:
        return '<%s name="%s">%s</%s>' % (
            type, key,
            replace_escape_xml(val),
            type
        )
    else:
        return '<%s>%s</%s>' % (
            type,
            replace_escape_xml(val),
            type
        )


def convert_bool_to_xml(key, val, add_name=True):
    """
    Converts a boolean into an XML element
    """
    attr_type = True
    attr = {}
    key, attr = make_valid_xml_name(key, attr)

    if attr_type:
        attr['type'] = change_xml_type_name(val)

    type = change_xml_type_name(val)

    if add_name:
        return '<%s name="%s">%s</%s>' % (type, key, str(val).lower(), type)
    else:
        return '<%s>%s</%s>' % (type, str(val).lower(), type)


def convert_none_to_xml(key, val, add_name=True):
    """
    Converts a null value into an XML element.
    """
    attr = {}
    attr_type = True

    key, attr = make_valid_xml_name(key, attr)

    if attr_type:
        attr['type'] = change_xml_type_name(val)


    type = change_xml_type_name(val)

    if add_name:
        return '<%s name="%s" />' % (type, key)
    else:
        return '<%s />' % (type)

def wrap_escape_string(s):
    """
    Wraps a string into extra section if required, currently disabled

    """
    s = unicode_me(s).replace(']]>', ']]]]><![CDATA[>')
    return '<![CDATA[' + s + ']]>'