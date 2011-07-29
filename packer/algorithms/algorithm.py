
class Algorithm(object):
    """Abstract baseclass for all the packing algorithms"""
    pass

    def __init__(self):
        self.error = None 

    def pack(self, settings, sprites):
        """
        To create an algorithm, check naive.py for an example
        """
        self.error = "Can't use base class as algorithm"
        return False

# Registry of all algorithms
ALGORITHMS = {}

class register(object):
    def __init__(self, name):
        self.name = name    

    def __call__(self, cls):
        global ALGORITHMS
        ALGORITHMS[self.name] = cls

