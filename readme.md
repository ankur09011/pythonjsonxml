## Instructions 

####About PythonJSONXML:
(Currently under development)
A Simple Python package to convert JSON data to configurable XML format.

### How to use as package 

Clone the repo {repo_link} here, run following command (current compatibility for Python3) 

```
pip3 install . 
```

### Usage

### Command Line

##### Usage With Positional Argument

After cloning the project

```
python3 src/cli_interface.py "examples/example.json" "examples/example.xml"
```

##### Usage With Named Argument

```
python -m src.cli_interface --jsonfile="examples/example.json --xmlfile="examples/example.xml"
```

### Inline in Code

#### from JSON file 

```python

# import xmljsonconvertor module
from src import xmljsonconverter

# initialise class
convertor = xmljsonconverter.XMLJSONConverter()

# the file will be saved to desired path
convertor.convertJSONtoXML(json_file='examples/example.json', xml_file='xamples/example.xml')

```

### Bugs, Features Improvements

#####New Features:
1. Add support to configure names of XML data-type
2. Add server mode to use as internal service
3. ...

Please suggest more features by opening
