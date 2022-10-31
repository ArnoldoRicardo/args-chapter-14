from typing import Dict, List, Set


class Args:
    schema: str
    args: List[str]
    valid: bool = True
    unexpectedArguments: Set[str] = set()
    booleanArgs: Dict[str, bool] = dict()
    argsFound: Set[str] = set()
    currentArgument: int

    def __init__(self, schema: str, args: List[str]):
        self.schema = schema
        self.args = args
        self.currentArgument = 0
        self.valid = self.parse()

    def parse(self) -> bool:
        if len(self.schema) == 0 and len(self.args) == 0:
            return True
        self.parseSchema()

        try:
            self.parseArguments()
        except Exception as e:
            print(e)
            pass

        return self.valid

    def parseSchema(self) -> bool:
        for element in self.schema.split(","):
            if len(element) > 0:
                trimmedElement = element.strip()
                self.parseSchemaElement(trimmedElement)
        return True

    def parseSchemaElement(self, element: str):
        elementId: str = element[0]
        elementTail: str = element[1:]
        self.validateSchemaElementId(elementId)

        if self.isBooleanSchemaElement(elementTail):
            self.parseBooleanSchemaElement(elementId)
        else:
            raise Exception(f"Argument: {elementId} has invalid format: {elementTail}.")

    def validateSchemaElementId(self, elementId: str):
        if not elementId.isalpha():
            raise Exception("Bad character:" + elementId + "in Args format: " + self.schema)

    def parseBooleanSchemaElement(self, elementId: str):
        self.booleanArgs[elementId] = False

    def isBooleanSchemaElement(self, elementTail: str) -> bool:
        return len(elementTail) == 0

    def parseArguments(self) -> bool:
        for arg in self.args:
            self.parseArgument(arg)
        return True

    def parseArgument(self, arg: str):
        if (arg.startswith("-")):
            self.parseElements(arg)

    def parseElements(self, arg: str):
        for chart in arg[1:]:
            self.parseElement(chart)

    def parseElement(self, argChar: str):
        if self.setArgument(argChar):
            self.argsFound.add(argChar)
        else:
            self.unexpectedArguments.add(argChar)
            self.valid = False

    def setArgument(self, argChar: str) -> bool:

        # TODO: a new par o methods for doouble
        if self.isBooleanArg(argChar):
            self.setBooleanArg(argChar, True)
        else:
            return False

        return True

    def setBooleanArg(self, argChar: str, value: bool):
        self.booleanArgs[argChar] = value

    def isBooleanArg(self, argChar: str) -> bool:
        return argChar in self.booleanArgs

    def cardinality(self) -> int:
        return len(self.argsFound)

    def usage(self) -> str:
        if len(self.schema) > 0:
            return "-[" + self.schema + "]"
        else:
            return ""

    def falseIfNull(self, b: bool) -> bool:
        if b is None:
            return False
        else:
            return b

    def getBoolean(self, arg: str) -> bool:
        return self.falseIfNull(self.booleanArgs[arg])

    def has(self, arg: str) -> bool:
        return arg in self.argsFound

    def isValid(self) -> bool:
        return self.valid
