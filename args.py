from typing import Dict, Iterator, List, Set, Union


class ArgumentMarshaler:
    value: Union[bool, str, int, float, List[str]]

    def set(self, current_argument: str):
        pass


class BooleanArgumentMarshaler(ArgumentMarshaler):
    value: bool

    def set(self, currentArgument: Iterator[str]):
        self.value = True

    @staticmethod
    def getValue(am: ArgumentMarshaler) -> bool:
        if (am is not None and isinstance(am, ArgumentMarshaler)):
            return am.value
        else:
            return False


class StringArgumentMarshaler(ArgumentMarshaler):
    value: str

    def set(self, currentArgument: Iterator[str]):
        try:
            self.value = next(currentArgument)
        except Exception as e:
            raise e

    @staticmethod
    def getValue(am: ArgumentMarshaler) -> str:
        if (am is not None and isinstance(am, ArgumentMarshaler)):
            return am.value
        else:
            return ""


class Args:
    schema: str
    args: List[str]
    valid: bool = True
    unexpectedArguments: Set[str] = set()
    marshalers: Dict[str, ArgumentMarshaler]
    argsFound: Set[str]
    currentArgument: Iterator[str]

    def __init__(self, schema: str, args: List[str]):
        self.marshalers = dict()
        self.schema = schema
        self.args = args
        self.argsFound = set()
        self.valid = self.parse()

    def parse(self) -> bool:
        if len(self.schema) == 0 and len(self.args) == 0:
            return True
        self.parseSchema()

        try:
            self.parseArguments(self.args)
        except Exception as e:
            print(e)

        return self.valid

    def parseSchema(self) -> bool:
        for element in self.schema.split(","):
            if len(element):
                trimmedElement = element.strip()
                self.parseSchemaElement(trimmedElement)
        return True

    def parseSchemaElement(self, element: str):
        elementId: str = element[0]
        elementTail: str = element[1:]
        self.validateSchemaElementId(elementId)

        if len(elementTail) == 0:
            self.marshalers[elementId] = BooleanArgumentMarshaler()
        elif elementTail == "*":
            self.marshalers[elementId] = StringArgumentMarshaler()
        else:
            raise Exception(f"Argument: {elementId} has invalid format: {elementTail}.")

    def validateSchemaElementId(self, elementId: str):
        if not elementId.isalpha():
            raise Exception("Bad character:" + elementId + "in Args format: " + self.schema)

    def parseArguments(self, args_list: List[str]) -> bool:
        self.currentArgument = iter(args_list)
        arg_string = next(self.currentArgument, '')
        if (arg_string.startswith("-")):
            self.parseElements(arg_string[1:])

    def parseElements(self, arg: str):
        for chart in arg:
            self.parseElement(chart)

    def parseElement(self, argChar: str):
        if self.setArgument(argChar):
            self.argsFound.add(argChar)
        else:
            self.unexpectedArguments.add(argChar)
            self.valid = False

    def setArgument(self, argChar: str) -> bool:
        m = self.marshalers.get(argChar, None)

        if not m:
            raise Exception
            return False
        else:
            self.argsFound.add(argChar)
            try:
                m.set(self.currentArgument)
            except Exception as e:
                self.valid = False
                self.errorArgumentId = argChar
                raise e
        return True

    def cardinality(self) -> int:
        return len(self.argsFound)

    def usage(self) -> str:
        if len(self.schema) > 0:
            return "-[" + self.schema + "]"
        else:
            return ""

    def getBoolean(self, arg: str) -> bool:
        return BooleanArgumentMarshaler.getValue(am=self.marshalers[arg])

    def getString(self, arg: str) -> str:
        return StringArgumentMarshaler.getValue(am=self.marshalers[arg])

    def has(self, arg: str) -> bool:
        return arg in self.argsFound

    def isValid(self) -> bool:
        return self.valid
