import unittest

from esdlvalidator.validation.tests import get_test_schema_data, get_test_schema_id, get_test_dataset_ameland, get_test_dataset_hybrid
from esdlvalidator.validation.validator import EsdlValidator


class TestValidator(unittest.TestCase):
    """Tests for the validator"""

    @classmethod
    def setUpClass(cls):
        super(TestValidator, cls).setUpClass()
        cls.schemaOne = get_test_schema_id(get_test_schema_data("testdata/schema_test_1.json"))
        cls.schemaTwo = get_test_schema_id(get_test_schema_data("testdata/schema_test_2.json"))
        cls.esdlAmeland = get_test_dataset_ameland()
        cls.esdlHybrid = get_test_dataset_hybrid()

    def test_validate_schema_1(self):
        """test running the validator"""

        # prepare
        validator = EsdlValidator()

        # execute, validate against 1 schema
        result = validator.validate(self.esdlAmeland, [self.schemaOne])
        validation = result.schemas[0].validations[0]

        self.assertEqual(validation.checked, 8, "there should be 8 checked")
        self.assertEqual(len(validation.warnings), 1, "there should be 1 warning")
        self.assertEqual(validation.warnings[0], "Area does not have a scope: value equals undefined for entity BU00600007", "Warning should say: Area does not have a scope: value equals undefined for entity BU00600007")

    def test_validate_schema_2(self):
        """test running the validator on test schema 2 with and, or defined"""

        # prepare
        validator = EsdlValidator()

        # execute, validate against 1 schema
        result = validator.validate(self.esdlHybrid, [self.schemaTwo])
        validation = result.schemas[0].validations[0]

        # assert
        self.assertEqual(validation.checked, 3, "there should be 3 checked since there are only 3 producers")
        self.assertEqual(len(validation.errors), 2, "there should be 2 errors since 1 producer validates ok")
        self.assertEqual(validation.errors[0], "Consumer missing power and marginal costs or no energy profile connected: None", "Warning should say: Consumer missing power and marginal costs or no energy profile connected: None")

    def test_validate_multiple_schemas(self):
        """Test if the validator works with checking multiple schemas"""

        # prepare
        validator = EsdlValidator()

        # execute, validate against 2 schemas
        result = validator.validate(self.esdlHybrid, [self.schemaOne, self.schemaTwo])

        # assert
        self.assertEqual(len(result.schemas), 2, "there should be 2 schemas in the result")
