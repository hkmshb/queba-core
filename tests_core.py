# -*- coding: utf-8 -*-
"""
Defines unit tests for queba-core.
"""
import unittest

from ddt import ddt, data, unpack
from queba import core



class CoreAttrTest(unittest.TestCase):
    ""
    def test_author_isdefined(self):
        self.assertEqual('Hazeltek Solutions', core.__author__)

    def test_version_isdefined(self):
        self.assertTrue(
            core.__version__ != None and
            core.__version__.strip() != ''
        )


class QuEBAErrorTest(unittest.TestCase):
    ""
    def test_QuEBAError_object_is_exception_instance(self):
        ex = core.QuEBAError()
        self.assertIsInstance(ex, core.QuEBAError)

    def test_QuEBAError_can_have_message(self):
        ex = core.QuEBAError('Error message')
        self.assertEqual('Error message', str(ex))


class FakeValidator(core.Validator):
    ""
    def __call__(self, condition):
        if condition == True:
            return (condition, None)
        return (condition, self.error_message)


class ValidatorTest(unittest.TestCase):
    ""
    def test_cannot_create_abstract_validator(self):
        self.assertRaises(TypeError, core.Validator)

    def test_result_is_sequence_object(self):
        rtn = FakeValidator()(1 > 2)
        self.assertEqual(2, len(rtn))
        self.assertIn(type(rtn), [list, tuple])
    
    def test_failed_result_contains_value_and_default_error(self):
        rtn = FakeValidator()(1 > 2)
        self.assertTrue(
            rtn[0] == (1 > 2),
            rtn[1] == 'validation failed'
        )

    def test_default_error_can_be_overridden_for_validator(self):
        MESSAGE = 'Condition not met'
        rtn = FakeValidator(error_message=MESSAGE)(1 > 2)
        self.assertTrue(
            rtn[0] == (1 > 2),
            rtn[1] == MESSAGE
        )

    def test_passed_result_contains_value_and_None(self):
        rtn = FakeValidator()(1 < 2)
        self.assertTrue(
            rtn[0] == (1 < 2),
            rtn[1] == None
        )


@ddt
class BookNumberValidatorTest(unittest.TestCase):
    ""
    
    @unpack
    @data(['32/06/01'], ['32-06-01'], ['32/06-01'], ['32-06/01'],
          ['3206-01'],  ['3206/01'],  ['32/0601'],  ['32-0601'], 
          ['320601'],)
    def test_validate_for_valid_book_number_in_diff_format(self, value):
        r = core.BookNumberValidator()(value)
        self.assertIsNone(r[1])     # passing validation

    @unpack
    @data(['32/06/01/32'], ['32060132'],    # too many
          ['31/06/01'],    ['310601'],      # first-two-digits < 32
          ['39/06/01'],    ['390601'],      # first-two-digits > 38
          ['32/06/AB'],    ['3206AB'],)     # contains xters besides separator=/
    def test_validate_fails_for_invalid_book_number_in_diff_format(self, value):
        r = core.BookNumberValidator()(value)
        self.assertEqual(value, r[0])   # returns value in r
        self.assertIsNotNone(r[1])      # failing validation

    @unpack
    @data(['32/06/01', '32/06/01'], ['32-06-01', '32/06/01'],
          ['3206/01', '32/06/01'], ['32-0601', '32/06/01'],
          ['320601', '32/06/01'])
    def test_reformats_valid_book_number(self, value, expected):
        r = core.BookNumberValidator()(value)
        self.assertEqual(expected, r[0])
        self.assertIsNone(r[1])             # passing validation

    @unpack
    @data(['32/06/01'], ['32-06-01'], ['3206/01'], ['32-0601'], ['320601'])
    def test_no_reformat_of_valid_book_number_if_format_is_false(self, value):
        r = core.BookNumberValidator(format=False)(value)
        self.assertEqual(value, r[0])
        self.assertIsNone(r[1])

    @unpack
    @data(['310601'], ['390601'], ['470601'], ['520601'], ['990601'])
    def test_fails_for_book_number_with_bad_first_two_digits(self, value):
        # first two digits MUST be: x where {31 < x < 39}
        r = core.BookNumberValidator()(value)
        self.assertEqual(value, r[0])   # returns value in r
        self.assertIsNotNone(r[1])      # failing validation


@ddt
class AccountNumberValidatorTest(unittest.TestCase):
    
    @unpack
    @data(['32/06/01/5726-01'], ['32-06-01-5726-01'], ['32-06/01/5726-01'],
          ['32/06-01-5726-01'], ['3206015726-01'],    ['3206015726'],
          ['32/06/01/5726'],    ['32-06-01-5726'],    ['32-06/01/5726'],
          ['32/06-01-5726'],)
    def test_validate_for_valid_acct_number_in_diff_format(self, value):
        r = core.AccountNumberValidator()(value)
        self.assertIsNone(r[1])     # passing validation
    
    @unpack
    @data(['32/06/01/57263-01'], ['32060157263-01'],    # too many digits
          ['31/06/01-5726-01'],  ['49-06/01/5726-01'],  # invalid first two digits
          ['32:06/01/5726'],     ['32/06/01/X726'],     # invalid sep and xter
          ['32/06/01/5721-01'],  ['3206015727'],)       # invalid acct-no validator digit
    def test_validate_fails_for_invalid_account_number_in_diff_format(self, value):
        r = core.AccountNumberValidator()(value)
        self.assertEqual(value, r[0])   # returns value in r
        self.assertIsNotNone(r[1])      # failing validation

    @unpack
    @data(['32/06/01/5726-01', '32/06/01/5726-01'], 
          ['32-06-01-5726-01', '32/06/01/5726-01'], 
          ['32-06/01/5726-01', '32/06/01/5726-01'],
          ['3206015726-01',    '32/06/01/5726-01'],    
          ['3206015726',       '32/06/01/5726'],
          ['32-06-01-5726',    '32/06/01/5726'],
          ['32-06/01/5726',    '32/06/01/5726'],)
    def test_reformats_valid_acct_number_in_diff_format(self, value, expected):
        r = core.AccountNumberValidator()(value)
        self.assertEqual(expected, r[0])
        self.assertIsNone(r[1])             # passing validation

    @unpack
    @data(['32/06/01/5726-01'], ['32-06-01-5726-01'], ['32-06/01/5726-01'],
          ['32/06-01-5726-01'], ['3206015726-01'],    ['3206015726'],
          ['32/06/01/5726'],    ['32-06-01-5726'],    ['32-06/01/5726'],
          ['32/06-01-5726'],)    
    def test_no_reformat_of_valid_account_number_if_format_is_false(self, value):
        r = core.AccountNumberValidator(format=False)(value)
        self.assertEqual(value, r[0])
        self.assertIsNone(r[1])             



if __name__ == '__main__':
    unittest.main()
