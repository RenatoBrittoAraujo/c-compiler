UNDETERMINED_VALUE = ""
DEBUG = False

#=====================================================================

# Not Leaf Type
class Node:
    type: str

    def __init__(self, type: str):
        self.type = type
        if DEBUG: print("<NEW_"+type+">", end="")

# Not Leaf Type
class ProcedureNode(Node):

    def __init__(self, type: str):
        super().__init__(type)

# Not Leaf Type
class ExpressionNode(ProcedureNode):
    value: str

    def __init__(self, type: str, value: str):
        super().__init__(type)
        self.value = value

# Not Leaf Type
class Type(ExpressionNode):
    nested_pointer_level: int

    def __init__(self, type: str, value: str, nested_pointer_level: int):
        if is_base_type(type):
            return BaseType(type, value, nested_pointer_level)

        super().__init__(type, value)
        self.nested_pointer_level = nested_pointer_level

class BaseType(Type):
    def __init__(self, type: str, value: str, nested_pointer_level: int):
        super().__init__(type, value, nested_pointer_level)
        self.type = type

class Expression(ExpressionNode):
    operands: list[ExpressionNode]
    __calculated: str

    def __init__(self, operands: list[ExpressionNode]):
        self.operands = operands
        self.__calculated = None

        value = self.get_value()

        super().__init__("EXPRESSION", value)
        self.operands = operands
    
    def get_value(self):
        if self.__calculated != None:
            return self.__calculated

        self.__calculated = UNDETERMINED_VALUE

        # [TODO] Implement
        if self.operands != []:
            pass

        return self.__calculated

class VariableDefinition(ProcedureNode):
    variable_type: str
    variable_name: str

    def __init__(self, variable_type: str, variable_name: str):
        super().__init__("VARIABLE_DEFINITION")
        self.variable_type = variable_type
        self.variable_name = variable_name

class VariableDeclaration(VariableDefinition):
    value: BaseType
    expression: Expression

    def __init__(self, variable_type: str, variable_name: str, expression: Expression):
        super().__init__(variable_type, variable_name)
        self.type = "VARIABLE_DEFINITION"
        self.expression = expression
        self.value = expression.get_value()


class VariableAssignment(ExpressionNode):
    variable_name: str
    value: str
    expression: Expression

    def __init__(self, variable_name: str, expression: Expression):
        super().__init__("VARIABLE_ASSIGNMENT", expression.get_value())
        self.variable_name = variable_name
        self.expression = expression
        self.value = expression.get_value()

class ProcedureCall(ExpressionNode):
    procedure_name: str
    operands: list[ExpressionNode | Expression]

    def __init__(self, procedure_name: str, operands: list[ExpressionNode | Expression]):
        super().__init__("PROCEDURE_CALL", UNDETERMINED_VALUE)
        self.procedure_name = procedure_name
        self.operands = operands

class Procedure(Node):
    procedure_name: str
    return_type: str
    declared: bool
    declared_variables: dict[str, VariableDefinition]
    operands: list[ExpressionNode]
    procedure_operations: list[ProcedureNode]

    def __init__(self, type: str, procedure_name: str, operands: list[ExpressionNode | Expression], procedure_operations: list[ProcedureNode]=[]):
        super().__init__("PROCEDURE")
        self.declared = False
        self.procedure_name = procedure_name
        self.return_type = type
        self.operands = operands
        self.declared_variables = {}
        self.procedure_operations = []

        if procedure_operations != []:
            self.procedure_operations = procedure_operations
            self.declared = True

    def add_procedure_operation(self, procedure_operation: ProcedureNode):
        self.declared = True

        # handle procedure definition
        if procedure_operation.type == "PROCEDURE":
            error("procedure has been defined inside procedure")

        # handle variable definition and declaration
        if procedure_operation.type == "VARIABLE_DECLARATION" or procedure_operation.type == "VARIABLE_DEFINITION":
            if self.declared_variables.has(procedure_operation.variable_name):
                error("redeclared or redefined variable '" + procedure_operation.variable_name + "'")
            else:
                self.declared_variables.set(VariableAssignment(procedure_operation.variable_name, procedure_operation))
            
        # [TODO] what else are the rules of a procedure?

        self.procedure_operations.append(procedure_operation)

class Root(Node):
    procedures: dict[str, Procedure]

    def __init__(self, procedures: list[Procedure]):
        super().__init__("root")
        self.procedures = {}

        for procedure in procedures:
            self.procedures[procedure.procedure_name] = procedure

class Stdin():
    txt: str

    def __init__(self, txt: str="") -> None:
        self.txt = txt

    # Skips all spaces and new lines
    def seek_next_char(self):
        while True:
            c = self.next_noop()
            if is_end(c):
                self.next()
            else:
                break

    # Removes and returns next char
    def next(self):
        c = self.next_noop()
        self.txt = self.txt[1:]
        if DEBUG: print(c + "<pop>", end="")
        return c

    # Removes and returns next char, skipping all spaces and new lines
    def next_skip_end(self):
        self.seek_next_char()
        return self.next()
    
    # Echoes next char, skipping all spaces and new lines
    def next_skip_end_noop(self):
        self.seek_next_char()
        return self.next_noop()

    # Echoes next char
    def next_noop(self):
        if len(self.txt) == 0:
            error("unexpected end of file", EOFError)
        if DEBUG: print(self.txt[0], end="")
        return self.txt[0]

#=====================================================================

def error(msg, exception=None):
    if exception is not None:
        raise exception(msg)
    else:
        print("ERROR: ", msg)
        print("ABORTED!")
        exit(1)

def is_numeric(x: str):
    return x.isnumeric()

def is_alpha(x: str):
    return x.isalpha()

def is_alphanumeric(x: str):
    return x.isalnum()

def is_end(x: str):
    return x == ' ' or x == '\n' or x == '\0'

def is_special(x: str):
    return not is_numeric(x) and not is_alpha(x)

def is_not_operands_end(x: str):
    return x != ')' and x != ','

def is_not_string_end(x: str):
    return x != '"'

def is_not_char_end(x: str):
    return x != "'"

def is_not_expression_end(x: str):
    return x != ';'

def compile_to(type, root):
    if type == "json":
        compile_to_json(root)
    else:
        error("invalid compilation target")

def tab(s: int):
    for i in range(0, s):
        print("  ", end="")

def compile_to_json(node: Node, tab_size=0):
    if node == None:
        return

    p = 0
    node = node.__dict__
    mp = len(node.keys())

    def pr(x):
        print(x, end="")
    
    pr("{\n")

    for key, cnode in node.items():
        p = p + 1

        if key[0] == '_':
            continue
        tab(tab_size+1)
        pr('"' + key + "\": ")

        if type(cnode) == str:
            pr('"' + cnode + '"')
        
        elif isinstance(cnode, Node) and type(cnode) != dict:
            compile_to_json(cnode, tab_size+2)
        
        elif type(cnode) == bool:
            v = "true"
            if not cnode:
                v = "false"
            pr('"' + v + '"')

        elif type(cnode) == int:
            pr('"' + str(cnode) + '"')

        elif type(cnode) == list:
            pr("[\n")
            s = len(cnode)
            for item in cnode:
                tab(tab_size+2)
                compile_to_json(item, tab_size+2)
                s = s - 1
                if s > 0:
                    pr(",")
                pr("\n")
            tab(tab_size+1)
            pr("]")

        elif type(cnode) == dict:
            pr("{\n")
            s = len(cnode.keys())
            for key, val in cnode.items():
                tab(tab_size+2)
                pr('"' + key + "\": ")
                compile_to_json(val, tab_size+2)
                s = s - 1
                if s > 0:
                    pr(",")
                pr("\n")
            tab(tab_size+1)
            pr("}")

        else:
            error("failed to compile to json, invalid type: " + str(type(cnode)) + " for key: " + key)

        if p < mp:
            pr(",\n")
        else:
            pr("\n")
 
    tab(tab_size)
    pr("}")

def is_base_type(buff):
    if buff == "int" or \
       buff == "char" or \
       buff == "string":
        return True
    return False

def get_operands(stdin):
    operands = []

    while True:
        operand = lookahead(stdin, read_only=True, is_intake_char=is_not_operands_end)

        if operand != None:
            operands.append(parse_expression(operand))

        c = stdin.next_skip_end()
        if c == ')':
            break
        elif c != ',':
            error("invalid arguments for procedure call")
    
    return operands
                
# This procedure gets a buffer and decides if it is one of:
# - variable definition
# - procedure definition
# - variable assignment
# - procedure call
# - string, int, sum, subtraction, division, multiplication, modulus, char
def interpret(stdin: Stdin, buff: str) -> Node:

    # this is the definition of a variable or a procedure
    if is_base_type(buff):
        c = stdin.next_skip_end_noop()
        if not is_alpha(c):
            error("invalid definition starting with number")

        typeb = buff
        name = lookahead(stdin, read_only=True)

        c = stdin.next_skip_end()

        # is definition of new variable
        if c == ';' or c == '=':
            value = ""

            # var declaration
            if c == '=':
                next()
                value = lookahead(stdin)
                return VariableDeclaration(typeb, name, value)
            
            return VariableDefinition(typeb, name)


        # is definition of procedure
        if c == '(':
            operands = get_operands(stdin)

            new_procedure = Procedure(typeb, name, operands)

            c = stdin.next_skip_end()

            # try to get the procedure implementation
            if c == ';':
                # procedure definiton without implementation 
                return new_procedure
            elif c == '{':
                # procedure defined with implementation (may already be defined)

                while True:
                    prcd_do = lookahead(stdin)

                    if prcd_do is not None:                    
                        new_procedure.add_procedure_operation(prcd_do)

                    if not has_char_stdin(stdin):
                        break

                    if c == '}':
                        break
                    
            else:
                error("invalid procedure definition")

            return new_procedure
        
        error("invalid definition")        

    # this is a procedure call or a variable assignment
    if is_alpha(buff[0]) and is_alphanumeric(buff):
        c = stdin.next_skip_end()
        name = buff

        # procedure call
        if c == '(':
            operands = get_operands(stdin)
            return ProcedureCall(name, operands)
        

        # variable assignment
        if c == '=':
            name = buff
            
            expression_txt = lookahead(stdin, read_only=True, is_intake_char=is_not_expression_end)

            expression = parse_expression(expression_txt)

            if expression == None:
                error("invalid assignment, no value provided")
            
            return VariableAssignment(name, expression)

    # this is a number
    if is_numeric(buff) or (buff[0] == '-' and is_numeric(buff[1:])):
        return BaseType("INT", buff, 0)

    if len(buff) == 1:
        stdin.next()
        c = buff[0]

        # this is a string
        if c == '\"':
            str = lookahead(stdin, read_only=True, is_intake_char=is_not_string_end)
            stdin.next()
            return BaseType("STRING", str, 0)

        # this is a char
        if c == '\'':
            chr = lookahead(stdin, read_only=True, is_intake_char=is_not_char_end)
            stdin.next()
            return BaseType("CHAR", chr, 0)

        # this is sum
        if c == '+':
            return BaseType("SUM", buff, 0)

        # this is subtraction
        if c == '-':
            return BaseType("SUBTRACTION", buff, 0)

        # this is multiplication
        if c == '*':
            return BaseType("MULTIPLICATION", buff, 0)

        # this is division
        if c == '/':
            return BaseType("DIVISION", buff, 0)

        # this is modulus
        if c == '%':
            return BaseType("MODULUS", buff, 0)

        # this is not up for our interpretation
        if c == ')' or c == '}' or c == ',' or c == ';' or c == '{' or c == '(':
            return None
    
        # this is not up for our interpretation, but we want to let parent know
        if c == ';':
            return c

    error("Undefined token '" + buff + "'")

def lookahead(stdin: Stdin, read_only=False, is_intake_char=is_alphanumeric):
    stdin.seek_next_char()
    c = stdin.next_noop()
    buff = c
    first = True

    while is_intake_char(c):
        if not first:
            buff += c
        first = False
        stdin.next()
        c = stdin.next_noop()

    if len(buff) == 1 and is_end(buff[0]):
        return buff
    
    if read_only:
        return buff
    
    return interpret(stdin, buff)

# this is not a clear soltion, but it is a solution
# bcs we need a dumb second pass to parse the expression
# maybe this is how its done because interpret() still runs once per char?
def parse_expression(buff) -> Expression | ExpressionNode:
    buff = buff + ';' # the last token gets fully interpreted
    exp_buff = Stdin(buff)
    expression_items = []

    while True:
        try:
            item = lookahead(exp_buff)
            if not isinstance(item, ExpressionNode):
                error("found invalid expression item: " + item.type)
            expression_items.append(item)
        except Exception as e:
            if e != "unexpected end of file":
                # Failed to find more stdin to parse, so we are done
                break
            else:
                raise e

    # this is not just an expression node like just '1'
    # instead its an expression like "1 + 1"
    if len(expression_items) > 1:
        return Expression(expression_items)

    if expression_items == []:
        return None

    return expression_items[0]

def has_char_stdin(stdin):
    try:
        stdin.seek_next_char()
    except Exception as e:
        if e != "unexpected end of file":
            # Failed to find more stdin to parse, so we are done
            return False
        else:
            raise e
    return True



def main():
    f = open('target.c')
    code = f.read()
    stdin = Stdin(code)
    f.close()

    procedures = []

    while True:
        if not has_char_stdin(stdin):
            break

        procedure = lookahead(stdin)

        if procedure == None:
            error("failed to read procedure (possible compiler error)")

        if procedure.type != "PROCEDURE":
            error("expression outside procedure scope")
        
        procedures.append(procedure)
    
    root = Root(procedures)

    print("\n")

    compile_to("json", root)

    print("\n")

if __name__ == "__main__":
    main()
