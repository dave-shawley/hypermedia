from tests.compat import mock, unittest

from flask.ext.hypermedia import exceptions


class CannotDetermineMethodTests(unittest.TestCase):
    def setUp(self):
        self.exc = exceptions.CannotDetermineMethod(mock.sentinel.rule)

    def test_that_failed_rule_attribute_is_retained(self):
        self.assertIs(self.exc.failed_rule, mock.sentinel.rule)

    def test_that_failed_rule_is_included_in_str(self):
        self.assertIn(str(mock.sentinel.rule), str(self.exc))


class MethodDoesNotExistTests(unittest.TestCase):
    def setUp(self):
        self.exc = exceptions.MethodDoesNotExist(
            mock.sentinel.rule, mock.sentinel.method)

    def test_that_failed_rule_attribute_is_retained(self):
        self.assertIs(self.exc.failed_rule, mock.sentinel.rule)

    def test_that_specified_method_attribute_is_retained(self):
        self.assertIs(self.exc.specified_method, mock.sentinel.method)

    def test_that_failed_rule_is_included_in_str(self):
        self.assertIn(str(mock.sentinel.rule), str(self.exc))

    def test_that_specified_method_is_included_in_str(self):
        self.assertIn(str(mock.sentinel.method), str(self.exc))


class AlreadyAdvertisedTests(unittest.TestCase):
    def setUp(self):
        self.exc = exceptions.AlreadyAdvertised(
            mock.sentinel.failed_rule,
            mock.sentinel.existing_rule,
            mock.sentinel.link_name,
        )

    def test_that_failed_rule_attribute_is_retained(self):
        self.assertIs(self.exc.failed_rule, mock.sentinel.failed_rule)

    def test_that_existing_rule_attribute_is_retained(self):
        self.assertIs(self.exc.existing_rule, mock.sentinel.existing_rule)

    def test_that_link_name_attribute_is_retained(self):
        self.assertIs(self.exc.link_name, mock.sentinel.link_name)

    def test_that_existing_rule_is_included_in_str(self):
        self.assertIn(str(mock.sentinel.existing_rule), str(self.exc))

    def test_that_link_name_is_included_in_str(self):
        self.assertIn(str(mock.sentinel.link_name), str(self.exc))
