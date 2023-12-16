from tokenize import Token
from ParseTree import *

KEYWORDS = {'class', 'constructor', 'function', 'method', 'field', 'static', 'var', 'int', 'char', 'boolean', 'void', 'true', 'false', 'null', 'this', 'let', 'do', 'if', 'else', 'while', 'return', 'skip'}
SYMBOLS = {'{', '}', '(', ')', '[', ']', '.', ',', ';', '+', '-', '*', '/', '&', '|', '<', '>', '=', '~'}
OPERATORS = {'+', '-', '*', '/', '&', '|', '<', '>', '='}
UNARY_OPERATORS = {'~', '-'}
KEYWORD_CONSTANTS = {'true', 'false', 'null', 'this'}

def CheckInteger(token):
    token = token.value if isinstance(token, Token) else token
    return token.isinteger() and int(token) < 32768

def Symbol(token, symbols):
    token = token.value if isinstance(token, Token) else token
    for s in symbols:
        if s in token:
            return s
    return False

def isIdentifier(token):
    token = token.value if isinstance(token, Token) else token
    return token.isidentifier()

class CompilerParser :
    
    type = {'void','int','char','boolean'}
    
    className = []
    
    varName = []
    
    subroutineName = []
    
    def __init__(self,tokens):
        """
        Constructor for the CompilerParser
        @param tokens A list of tokens to be parsed
        """
        self.current_tokens = tokens
        self.token_index = 0
        

    def isMatch(self, token:Token, tokenType:str=None,tokenValue:str=None):
        if tokenType is not None and token.node_type != tokenType:
            return False
        if tokenValue is not None and token.value != tokenValue:
            return False
        return True

    def tokenMatch(self, container:ParseTree, tokenType:str=None, tokenValue:str=None):
        if self.current is not None and self.isMatch(self.current, tokenType, tokenValue):
            container.addChild(self.current)
            self.next()
            return True
        raise ParseException
    
    def typeMatch(self, container:ParseTree):
        if (self.current.value in self.type) or (self.current.node_type == "identifier"):
            self.tokenMatch(container) 
        else:
            raise ParseException
        
    def statementMatch(self, container:ParseTree, statement:ParseTree|Token, statement_type:str=None):
        if self.isMatch(statement, statement_type):   
            container.addChild(statement)
            return True
        else:
            raise ParseException
        
    def add_className(self):
        if self.isMatch(self.current, tokenType="identifier"):
            self.className.append(self.current)
        else:
            raise ParseException(f"Invalid syntax: {self.current}")
        
    def add_subroutineName(self):
        if self.current is not None and isIdentifier(self.current):
            self.subroutineName.append(self.current)
        else:
            raise ParseException("Invalid syntax" + (f": {self.current}" if self.current else ""))
        
    def add_varName(self):
        if self.current is not None and isIdentifier(self.current):
            self.subroutineName.append(self.current)
        else:
            raise ParseException("Invalid syntax" + (f": {self.current}" if self.current else ""))
                    
    def compileProgram(self):
        """
        Generates a parse tree for a single program
        @return a ParseTree that represents the program
        """
        return self.compileClass()
    
    
    def compileClass(self):
        """
        Generates a parse tree for a single class
        @return a ParseTree that represents a class
        """
        root = ParseTree("class", "")

        self.tokenMatch(root, 'keyword', 'class')
        self.tokenMatch(root, 'identifier')
        self.tokenMatch(root, 'symbol', '{')

        while self.current is not None:
            try:
                statement = self.compileClassVarDec()  # Try to parse classVarDec
            except ParseException:
                try:
                    statement = self.compileSubroutine()  # Try to parse subroutine
                except ParseException:
                    break

            self.statementMatch(root, statement, statement.node_type)

        self.tokenMatch(root, 'symbol', '}')
        return root
    

    def compileClassVarDec(self):
        """
        Generates a parse tree for a static variable declaration or field declaration
        @return a ParseTree that represents a static variable declaration or field declaration
        """
        root = ParseTree("classVarDec", "")

        if self.current.value in ["static", "field"]:
            self.tokenMatch(root, "keyword")
        else:
            raise ParseException

        self.typeMatch(root)
        
        while True:
            self.add_varName()
            self.tokenMatch(root, 'identifier')
            
            if self.current.value == ',':
                self.tokenMatch(root, 'symbol', ',')
            else:
                break

        self.tokenMatch(root, 'symbol', ';')
        return root
    
    def compileSubroutine(self):
        """
        Generates a parse tree for a method, function, or constructor
        @return a ParseTree that represents the method, function, or constructor
        """
        root = ParseTree("subroutine","")
        
        if self.current.value in ['constructor','function','method']:
            self.tokenMatch(root, "keyword")
        else:
            raise ParseException

        self.typeMatch(root)
            
        self.add_subroutineName()
        self.tokenMatch(root,"identifier")
        self.tokenMatch(root,'symbol','(')
        
        parameter_statement = self.compileParameterList()
        self.statementMatch(root,parameter_statement,'parameterList')
        self.tokenMatch(root,'symbol',')')
        
        subroutine_statement = self.compileSubroutineBody()
        self.statementMatch(root, subroutine_statement, 'subroutineBody')
        return root
    
    
    def compileParameterList(self):
        """
        Generates a parse tree for a subroutine's parameters
        @return a ParseTree that represents a subroutine's parameters
        """
        root = ParseTree("parameterList","")

        try:
            self.typeMatch(root)
        except: 
            return root
        self.tokenMatch(root,'identifier')
        while self.current is not None:
            try:
                self.tokenMatch(root,'symbol',',')
                self.typeMatch(root)
                self.tokenMatch(root,'identifier')
            except:
                break
        return root
    
    
    def compileSubroutineBody(self):
        """
        Generates a parse tree for a subroutine's body
        @return a ParseTree that represents a subroutine's body
        """
        root = ParseTree("subroutineBody", "")
        self.tokenMatch(root, "symbol", "{")

        while self.current is not None and self.current.value == 'var':
            varDecStatement = self.compileVarDec()
            self.statementMatch(root, varDecStatement, 'varDec')

        statements = self.compileStatements()
        self.statementMatch(root, statements, "statements")
        self.tokenMatch(root, "symbol", "}")

        return root
    
    
    def compileVarDec(self):
        """
        Generates a parse tree for a variable declaration
        @return a ParseTree that represents a var declaration
        """
        root = ParseTree("varDec", "")
        self.tokenMatch(root, "keyword", "var")

        self.typeMatch(root)

        self.add_varName()
        self.tokenMatch(root, "identifier")

        while self.current is not None and self.current.value == ',':
            self.tokenMatch(root, 'symbol', ',')
            self.add_varName()
            self.tokenMatch(root, "identifier")

        self.tokenMatch(root, 'symbol', ';')

        return root
        

    def compileStatements(self):
        """
        Generates a parse tree for a series of statements
        @return a ParseTree that represents the series of statements
        """
        root = ParseTree("statements", "")
        statement_parsers = {
            'letStatement': self.compileLet,
            'ifStatement': self.compileIf,
            'whileStatement': self.compileWhile,
            'doStatement': self.compileDo,
            'returnStatement': self.compileReturn
        }

        while self.current is not None:
            statement_type = None
            for key, parser in statement_parsers.items():
                try:
                    statement = parser()
                    statement_type = key
                    break
                except ParseException:
                    pass

            if statement_type is not None:
                self.statementMatch(root, statement, statement_type)
            else:
                break

        return root
    
    
    def compileLet(self):
        """
        Generates a parse tree for a let statement
        @return a ParseTree that represents the statement
        """
        root = ParseTree("letStatement", "")

        self.tokenMatch(root, 'keyword', 'let')
        self.tokenMatch(root, 'identifier')

        if self.current.value == "[":
            self.tokenMatch(root, "symbol", "[")
            expression_statement = self.compileExpression()
            self.statementMatch(root, expression_statement, 'expression')
            self.tokenMatch(root, "symbol", "]")

        self.tokenMatch(root, 'symbol', '=')
        expression_statement = self.compileExpression()
        self.statementMatch(root, expression_statement, 'expression')
        self.tokenMatch(root, 'symbol', ';')

        return root
    

    def compileIf(self):
        """
        Generates a parse tree for an if statement
        @return a ParseTree that represents the statement
        """
        root = ParseTree("ifStatement","")
        self.tokenMatch(root,'keyword','if')
        
        self.tokenMatch(root,'symbol',"(")
        expression_statement = self.compileExpression()
        self.statementMatch(root,expression_statement,'expression')
        self.tokenMatch(root,'symbol',")")
        
        self.tokenMatch(root,'symbol',"{")
        statements = self.compileStatements()
        self.statementMatch(root,statements,'statements')
        self.tokenMatch(root,'symbol',"}")
        
        try:
            self.tokenMatch(root, 'keyword','else')
            self.tokenMatch(root,'symbol',"{")
            statements = self.compileStatements()
            self.statementMatch(root,statements,'statements')
            self.tokenMatch(root,'symbol',"}")         
        except:
            pass
                
        return root
    
    
    def compileWhile(self):
        """
        Generates a parse tree for a while statement
        @return a ParseTree that represents the statement
        """
        root = ParseTree("whileStatement","")
        self.tokenMatch(root,"keyword","while")
        self.tokenMatch(root,"symbol","(")
        expression_statement = self.compileExpression()
        self.statementMatch(root,expression_statement,"expression")
        self.tokenMatch(root,"symbol",")")
        self.tokenMatch(root,"symbol","{")
        statements = self.compileStatements()
        self.statementMatch(root,statements,"statements")
        self.tokenMatch(root, "symbol","}")
        return root 

    def compileDo(self):
        """
        Generates a parse tree for a do statement
        @return a ParseTree that represents the statement
        """
        root = ParseTree("doStatement","")
        self.tokenMatch(root,'keyword','do')
        expression_statement = self.compileExpression()
        self.statementMatch(root,expression_statement,'expression')
        self.tokenMatch(root,'symbol',';')      
        return root
    

    def compileReturn(self):
        """
        Generates a parse tree for a return statement
        @return a ParseTree that represents the statement
        """
        root = ParseTree("returnStatement","")
        self.tokenMatch(root,'keyword','return')
        try:
            expression_statement = self.compileExpression()
            self.statementMatch(root, expression_statement, 'expression')            
        except:
            pass
        self.tokenMatch(root,'symbol',';')        
        return root
    

    def compileExpression(self):
        """
        Generates a parse tree for an expression
        @return a ParseTree that represents the expression
        """
        root = ParseTree("expression", "")

        if self.current.value == "skip":
            self.tokenMatch(root, "keyword", "skip")
        else:
            term_statement = self.compileTerm()
            self.statementMatch(root, term_statement, 'term')

            while self.current is not None and self.current.value in OPERATORS:
                self.tokenMatch(root, "symbol")
                term_statement = self.compileTerm()
                self.statementMatch(root, term_statement, 'term')

        return root
    

    def compileTerm(self):
        """
        Generates a parse tree for an expression term
        @return a ParseTree that represents the expression term
        """
        root = ParseTree("term","")
        if self.current.node_type == "integerConstant" or \
                self.current.node_type == "stringConstant" or \
                (self.current.node_type == "keyword" and self.current.value in KEYWORD_CONSTANTS):
            self.tokenMatch(root, self.current.node_type)
        elif self.current.node_type == "identifier":                                     
            self.tokenMatch(root, "identifier")                                                       
            if self.current is not None:
                if self.current.value == "[":                                                        
                    self.tokenMatch(root,"symbol","[")
                    expression_statement = self.compileExpression()
                    self.statementMatch(root, expression_statement,"expression")
                    self.tokenMatch(root,"symbol","]")
                if self.current.value == "(":                                                        
                    self.tokenMatch(root,"symbol","(")
                    expressionList_statement = self.compileExpressionList()
                    self.statementMatch(root, expressionList_statement,"expressionList")
                    self.tokenMatch(root,"symbol",")")
                if self.current.value == ".":                                                       
                    self.tokenMatch(root,"symbol",".")
                    self.tokenMatch(root, "identifier")
                    self.tokenMatch(root,"symbol","(")
                    expressionList_statement = self.compileExpressionList()
                    self.statementMatch(root, expressionList_statement,"expressionList")
                    self.tokenMatch(root,"symbol",")")
        elif self.current.value == "(":                                                   
            self.tokenMatch(root,"symbol","(")
            expression_statement = self.compileExpression()
            self.statementMatch(root, expression_statement,"expression")
            self.tokenMatch(root,"symbol",")")
        elif self.current.value in UNARY_OPERATORS:                                            
            self.tokenMatch(root,"symbol")
            term_statement = self.compileTerm()
            self.statementMatch(root, term_statement,"term")
        else:
            raise ParseException
        return root
    

    def compileExpressionList(self):
        """
        Generates a parse tree for an expression list
        @return a ParseTree that represents the expression list
        """
        root = ParseTree("expressionList", "")

        try:
            expression_statement = self.compileExpression()
            self.statementMatch(root, expression_statement, 'expression')

            while self.current is not None and self.current.value == ",":
                self.tokenMatch(root, 'symbol', ',')
                expression_statement = self.compileExpression()
                self.statementMatch(root, expression_statement, 'expression')

        except ParseException:
            pass

        return root


    def next(self):
        """
        Advance to the next token
        """
        self.token_index += 1

    @property
    def current(self):
        """
        Return the current token
        @return the token
        """
        if self.token_index < len(self.current_tokens):
            return self.current_tokens[self.token_index]
        return None 


    def have(self,expectedType,expectedValue):
        """
        Check if the current token matches the expected type and value.
        @return True if a match, False otherwise
        """
        if self.current is not None:
            if (expectedType is None or self.current.node_type == expectedType) and (expectedValue is None or self.current.value == expectedValue):
                return True
        return False


    def mustBe(self,expectedType,expectedValue):
        """
        Check if the current token matches the expected type and value.
        If so, advance to the next token, returning the current token, otherwise throw/raise a ParseException.
        @return token that was current prior to advancing.
        """
        if self.have(expectedType, expectedValue):
            current_token = self.current
            self.next()
            return current_token
        raise ParseException
    

if __name__ == "__main__":


    """ 
    Tokens for:
        class MyClass {
        
        }
    """
    tokens = []
    tokens.append(Token("keyword","class"))
    tokens.append(Token("identifier","MyClass"))
    tokens.append(Token("symbol","{"))
    tokens.append(Token("symbol","}"))

    parser = CompilerParser(tokens)
    try:
        result = parser.compileProgram()
        print(result)
    except ParseException:
        print("Error Parsing!")

