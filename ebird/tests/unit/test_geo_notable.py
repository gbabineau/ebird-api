# -*- coding: utf-8 -*-

from unittest import TestCase

try:
    import mock
except ImportError:
    import unittest.mock as mock

from ebird.data import GEO_NOTABLE_URL, geo_notable


# noinspection PyUnusedLocal
def get_content(url, params):
    return '[]'


class GeoNotableTests(TestCase):

    parameters = [
        (  # Only the format is added when default arguments are used
            {'lat': 1.0, 'lng': 0.0},
            {'lat': '1.00', 'lng': '0.00', 'fmt': 'json'}),
        (  # Default dist is filtered out
            {'lat': 1.0, 'lng': 0.0, 'dist': 25},
            {'lat': '1.00', 'lng': '0.00', 'fmt': 'json'}),
        (  # Value for dist is included
            {'lat': 1.0, 'lng': 0.0, 'dist': 10},
            {'lat': '1.00', 'lng': '0.00', 'dist': 10, 'fmt': 'json'}),
        (  # Default back is filtered out
            {'lat': 1.0, 'lng': 0.0, 'back': 14},
            {'lat': '1.00', 'lng': '0.00', 'fmt': 'json'}),
        (  # Value for back is filtered out
            {'lat': 1.0, 'lng': 0.0, 'back': 10},
            {'lat': '1.00', 'lng': '0.00', 'back': 10, 'fmt': 'json'}),
        (  # Default max_results is filtered out
            {'lat': 1.0, 'lng': 0.0, 'max_results': None},
            {'lat': '1.00', 'lng': '0.00', 'fmt': 'json'}),
        (  # Value for max_results is included
            {'lat': 1.0, 'lng': 0.0, 'max_results': 10},
            {'lat': '1.00', 'lng': '0.00', 'maxResults': 10, 'fmt': 'json'}),
        (  # Default locale is filtered out
            {'lat': 1.0, 'lng': 0.0, 'locale': 'en_US'},
            {'lat': '1.00', 'lng': '0.00', 'fmt': 'json'}),
        (  # Value for locale is included
            {'lat': 1.0, 'lng': 0.0, 'locale': 'de_DE'},
            {'lat': '1.00', 'lng': '0.00', 'locale': 'de_DE', 'fmt': 'json'}),
        (  # Default hotspot is filtered out
            {'lat': 1.0, 'lng': 0.0, 'hotspot': False},
            {'lat': '1.00', 'lng': '0.00', 'fmt': 'json'}),
        (  # Value for hotspot is included
            {'lat': 1.0, 'lng': 0.0, 'hotspot': True},
            {'lat': '1.00', 'lng': '0.00', 'hotspot': 'true', 'fmt': 'json'}),
        (  # Default hotspot is filtered out
            {'lat': 1.0, 'lng': 0.0, 'detail': 'simple'},
            {'lat': '1.00', 'lng': '0.00', 'fmt': 'json'}),
        (  # Value for hotspot is included
            {'lat': 1.0, 'lng': 0.0, 'detail': 'full'},
            {'lat': '1.00', 'lng': '0.00', 'detail': 'full', 'fmt': 'json'}),
    ]

    validation = [
        {'lat': 91, 'lng': 0.0},  # lat is more than 90
        {'lat': -91, 'lng': 0.0},  # lat is less than 90
        {'lat': 'str', 'lng': 0.0},  # lat cannot be converted to a float
        {'lat': 0.0, 'lng': 181},  # lat is more than 90
        {'lat': 0.0, 'lng': -181},  # lat is less than 90
        {'lat': 0.0, 'lng': 'str'},  # lat cannot be converted to a float
        {'lat': 0.0, 'lng': 0.0, 'dist': 51},  # dist is more than 50
        {'lat': 0.0, 'lng': 0.0, 'dist': -1},  # dist is less than 0
        {'lat': 0.0, 'lng': 0.0, 'dist': 'str'},  # dist cannot be converted to an integer
        {'lat': 0.0, 'lng': 0.0, 'back': 31},  # back is more than 30
        {'lat': 0.0, 'lng': 0.0, 'back': 0},  # back is less than 1
        {'lat': 0.0, 'lng': 0.0, 'back': 'str'},  # back cannot be converted to an integer
        {'lat': 0.0, 'lng': 0.0, 'max_results': 10001},  # max_results is more than 10000
        {'lat': 0.0, 'lng': 0.0, 'max_results': 0},  # max_results is less than 1
        {'lat': 0.0, 'lng': 0.0, 'max_results': 'str'},  # max_results is not an integer
        {'lat': 0.0, 'lng': 0.0, 'locale': 'enUS'},  # locale is not valid
        {'lat': 0.0, 'lng': 0.0, 'locale': ''},  # locale is blank
        # TODO Currently do not have validation tests for hotspot
        {'lat': 0.0, 'lng': 0.0, 'detail': 'complex'},  # detail is not a recognised value
        {'lat': 0.0, 'lng': 0.0, 'detail': ''},  # detail is blank
    ]

    @mock.patch('ebird.data.get_content', side_effect=get_content)
    def test_url(self, mocked_function):
        """Verify the correct URL is used to fetch the records."""
        geo_notable(0.0, 0.0)
        actual = mocked_function.call_args[0][0]
        self.assertEqual(GEO_NOTABLE_URL, actual)

    @mock.patch('ebird.data.get_content', side_effect=get_content)
    def test_parameters(self, mocked_function):
        """Verify only non-default values for query string parameters are sent."""
        for idx, (pattern, expected) in enumerate(self.parameters):
            geo_notable(**pattern)
            actual = mocked_function.call_args[0][1]
            self.assertDictEqual(expected, actual, msg="Pattern %d failed" % idx)

    # noinspection PyUnusedLocal
    @mock.patch('ebird.data.get_content', side_effect=get_content)
    def test_validation(self, mocked_function):
        """Verify the function arguments are validated."""
        for idx, pattern in enumerate(self.validation):
            with self.assertRaises(ValueError, msg='Pattern %d failed' % idx):
                geo_notable(**pattern)
