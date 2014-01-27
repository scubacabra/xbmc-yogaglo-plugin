from pkgutil import extend_path, get_data

__path__ = extend_path(__path__, "resources")

def readTestInput(filename):
    inputdata = get_data("test.resources", filename)
    return inputdata 
