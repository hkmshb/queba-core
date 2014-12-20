# -*- coding: utf-8 -*-
"""
Defines core functions and classes for QuEBA.
"""

__author__  = 'Hazeltek Solutions'
__version__ = '0.1'


from abc import ABCMeta, abstractmethod



class QuEBAError(Exception):
    """Base error class for QuEBA related errors."""
    pass


#+=============================================================================+
#| Validator Classes
#+=============================================================================+
class Validator(object):
    """Represents the base validator for Validator objects."""
    __metaclass__ = ABCMeta
    
    def __init__(self, error_message='validation failed'):
        self.error_message = error_message
    
    @abstractmethod
    def __call__(self, value):
        pass

    def format(self, value):
        """Returns a formatted version of the validated value."""
        return value


class BookNumberValidator(Validator):
    """Validates an Accounts book number."""
    
    def __init__(self, error_message='Invalid book number', format=True):
        super(BookNumberValidator, self).__init__(error_message)
        self._format = format

    def __call__(self, value):
        if value is None:
            return (value, self.error_message)

        book = value.replace('\\', '').replace('/','').replace('-', '')
        if (len(book) != 6 or not self._isnumeric(book) or
            book[:2] in ('30', '31', '39')):
            return (value, self.error_message)
        
        if self._format:
            return (self.format(book), None)
        return (value, None)
    
    def _isnumeric(self, value):
        try: l = long(value); return True
        except: False

    def format(self, value):
        return "%s/%s/%s" % (value[:2], value[2:4:], value[4:])

