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
        if len(book) != 6 or not self._isnumeric(book):
            return (value, self.error_message)
        
        buCode = int(book[:2])
        if buCode < 32 or buCode > 38:
            return (value, self.error_message)
        
        if self._format:
            return (self.format(book), None)
        return (value, None)
    
    def _isnumeric(self, value):
        try: l = long(value); return True
        except: False

    def format(self, value):
        return "%s/%s/%s" % (value[:2], value[2:4:], value[4:])


class AccountNumberValidator(BookNumberValidator):
    """Validates an Accounts customer account number."""
    
    def __init__(self, error_message='Invalid account number', format=True):
        super(AccountNumberValidator, self).__init__(error_message, format)

    def __call__(self, value):
        if value is None:
            return (value, self.error_message)
        
        acctno = value.replace('\\', '').replace('/', '').replace('-', '')
        if len(acctno) < 10 or len(acctno) > 12 or not self._isnumeric(acctno):
           return (value, self.error_message)
        
        buCode = int(acctno[:2])
        if buCode < 32 or buCode > 38:
            return (value, self.error_message)

        acct = acctno[:10]
        acct_digit_pos_weights = [
            int(acct[i]) * (i+1) 
                for i in range(len(acct) - 1)
        ]

        acct_vld_digit = sum(acct_digit_pos_weights) % 10
        if acct[-1] != str(acct_vld_digit):
            return (value, self.error_message)
        
        if self._format:
            return (self.format(acctno), None)
        return (value, None)
    
    def format(self, value):
        return "%s/%s/%s/%s%s" % (
            value[:2], value[2:4], value[4:6], value[6:10],
            ('' if len(value) == 10 else '-%s' % value[10:])
        )

    