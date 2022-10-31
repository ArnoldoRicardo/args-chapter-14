from typing import Dict, Iterator, List, Set, Union


class ArgumentMarshaler:
    value: Union[bool, str, int, float, List[str]]

    def set(self, current_argument: str):
        pass


class BooleanArgumentMarshaler(ArgumentMarshaler):
    value: bool

    def set(self, value: bool):
        self.value = True

    def getValue(self) -> bool:
        return bool(self.value)


class StringArgumentMarshaler(ArgumentMarshaler):
    value: str

    def set(self, value: bool):
        self.value = value

    def getValue(self) -> bool:
        if not self.value:
            return ''
        return self.value


class Args:
    schema: str
    args: List[str]
    valid: bool = True
    unexpectedArguments: Set[str] = set()
    booleanArgs: Dict[str, bool] = dict()
    stringArgs: Dict[str, str] = dict()
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
        elif self.isStringSchemaElement(elementTail):
            self.parseStringSchemaElement(elementId)
        else:
            raise Exception(f"Argument: {elementId} has invalid format: {elementTail}.")

    def validateSchemaElementId(self, elementId: str):
        if not elementId.isalpha():
            raise Exception("Bad character:" + elementId + "in Args format: " + self.schema)

    def parseBooleanSchemaElement(self, elementId: str):
        self.booleanArgs[elementId] = BooleanArgumentMarshaler()

    def isBooleanSchemaElement(self, elementTail: str) -> bool:
        return len(elementTail) == 0

    def parseStringSchemaElement(self, elementId: str):
        self.stringArgs[elementId] = StringArgumentMarshaler()

    def isStringSchemaElement(self, elementTail: str) -> bool:
        return elementTail == "*"

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

        if self.isBooleanArg(argChar):
            self.setBooleanArg(argChar, True)
        elif self.isStringArg(argChar):
            self.setStringArg(argChar)
        else:
            return False

        return True

    def setBooleanArg(self, argChar: str, value: bool):
        self.booleanArgs[argChar].set(value)

    def isBooleanArg(self, argChar: str) -> bool:
        return argChar in self.booleanArgs

    def isStringArg(self, argChar: str) -> bool:
        return argChar in self.stringArgs

    def setStringArg(self, argChar: str):
        self.currentArgument += 1
        try:
            self.stringArgs[argChar].set(self.args[self.currentArgument])
        except Exception as e:
            self.valid = False
            self.errorArgumentId = argChar
            raise e

    def cardinality(self) -> int:
        return len(self.argsFound)

    def usage(self) -> str:
        if len(self.schema) > 0:
            return "-[" + self.schema + "]"
        else:
            return ""

    def getBoolean(self, arg: str) -> bool:
        am = self.booleanArgs.get(arg, None)
        if am:
            return am.getValue()
        else:
            return False

    def getString(self, arg: str) -> str:
        am = self.stringArgs.get(arg, None)
        if am:
            return am.getValue()
        else:
            return ''

    def has(self, arg: str) -> bool:
        return arg in self.argsFound

    def isValid(self) -> bool:
        return self.valid
