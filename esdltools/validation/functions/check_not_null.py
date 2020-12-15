from numbers import Number

from esdltools.validation.functions import utils
from esdltools.validation.functions.function import FunctionFactory, FunctionCheck, FunctionDefinition, ArgDefinition, FunctionType, CheckResult


@FunctionFactory.register(FunctionType.CHECK, "not_null")
class ContainsNotNull(FunctionCheck):

    def get_function_definition(self):
        return FunctionDefinition(
            "not_null",
            "Check if a value is set",
            [
                ArgDefinition("property", "The name of the propery containing the value to check, leave propery out to check directly on input value", False),
                ArgDefinition("counts_as_null", "Array of values which are seen as null values such as 0.0 for a double, 0 for int, 'NULL' for a string", False)
            ]
        )

    def before_execute(self):
        pass

    def execute(self):
        prop, propertySet = utils.get_args_property(self.args, "property")
        include, includeSet = utils.get_args_property(self.args, "counts_as_null")

        value = self.value

        if propertySet:
            if not hasattr(value, prop):
                return CheckResult(False, "property {0} not found".format(prop))
            
            value = getattr(value, prop)
        
        if value is None:
            return CheckResult(False)
        
        if includeSet:
            return self.check_includes(include, value)

        return CheckResult(True)

    def check_includes(self, include, value):
        for includeValue in include:
            if str(includeValue) == str(value):
                return CheckResult(False)

        return CheckResult(True)
