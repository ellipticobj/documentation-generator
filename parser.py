from typing import Optional, List, Tuple
from ast import dump, parse, AST, Module
import zlib
import base64

def outputlen(func):
    '''returns the length of the output of a function'''
    def wrapper(*args, **kwargs):
        out = func(*args, **kwargs)
        try:
            outputlen = len(out)
        except TypeError:
            outputlen = 0
        return f"output of {func.__name__} is {outputlen} characters long", out
    return wrapper
    
class Parser:
    def __init__(self, filename: str = "") -> None:
        self.filename: str = filename
        self.tree: Optional[AST] = None
    
    def parsefile(self) -> Module:
        '''parses the file and returns the ast'''
        with open(self.filename, "r") as f:
            source: str = f.read()
        
        module: Module = parse(source)
        self.tree = module
        return self.tree
    
    @staticmethod
    def replacek(s: str) -> str:
        '''
        replaces keywords with shorterned characters
        '''
        replacements = {
            "FormattedValue": "FV",
            "FunctionDef": "FD",
            "ExceptHandler": "EX",
            "ImportFrom": "IF",
            "AnnAssign": "AA",
            "Attribute": "ATT",
            "arguments": "ARG",
            "Subscript": "SS",
            "Constant": "CO",
            "ClassDef": "CD",
            "UnaryOp": "UO",
            "keyword": "K",
            "Starred": "ST",
            "Return": "R",
            "Assign": "AS",
            "Import": "I",
            "Module": "M",
            "alias": "AL",
            "Store": "S",
            "value": "val",
            "Call": "C",
            "Expr": "E",
            "Name": "N",
            "Load": "L"
        }
    
        # Perform all replacements from the dictionary
        for long, short in replacements.items():
            s = s.replace(long, short)
            
        return s
    
    @staticmethod
    def unreplacek(s: str) -> str:
        '''
        replaces keywords with shorterned characters
        '''
        replacements = {
            "FormattedValue": "FV",
            "FunctionDef": "FD",
            "ExceptHandler": "EX",
            "ImportFrom": "IF",
            "AnnAssign": "AA",
            "Attribute": "ATT",
            "arguments": "ARG",
            "Subscript": "SS",
            "Constant": "CO",
            "ClassDef": "CD",
            "UnaryOp": "UO",
            "keyword": "K",
            "Starred": "ST",
            "Return": "R",
            "Assign": "AS",
            "Import": "I",
            "Module": "M",
            "alias": "AL",
            "Store": "S",
            "value": "val",
            "Call": "C",
            "Expr": "E",
            "Name": "N",
            "Load": "L"
        }
        
        revreplacements = {v: k for k, v in replacements.items()}
    
        # Perform all replacements from the dictionary
        for long, short in revreplacements.items():
            s = s.replace(long, short)
            
        return s
    
    @outputlen
    def getuncompressed(self) -> str:
        '''prints the ast in an uncompressed format'''
        if not self.tree:
            raise RuntimeError("ast is empty. have you run parsefile() yet?") # \nreport this to https://github.com/ellipticobj/documentation-generator/issues/new
        
        ast: str = dump(self.tree, indent=4)
        print(ast)
        return ast
    
    @outputlen
    def getcompressed(self) -> str:
        '''
        compresses the ast as much as possible without zlib
        can be passed into gemini 2.0 flash
        '''
        if not self.tree:
            raise RuntimeError("ast is empty. have you run parsefile() yet?")
        
        # ballpark figures lol
        # removes unnecessary whitespace and attributes (decreases length of output by ~71%)
        compast: str = dump(self.tree, annotate_fields=False, include_attributes=False, indent=0, show_empty=False)
        
        # remove newlines + whitespace (decreases length by ~7%)
        compast = "".join(compast.split())
        
        # replace keywords with shorter wersions (decreases length by ~40%)
        compast = self.replacek(compast)
            
        print(compast)
        return compast
    
    @outputlen
    def zlibcomp(self) -> str:
        """
        compresses the ast, then compresses it again using zlib
        can be passed into gemini 2.0 pro
        https://aistudio.google.com/prompts/1RVQLvTAJqwBIctnmLxReYX-N07lOwL0X
        """
        if not self.tree:
            raise RuntimeError("AST is empty. Have you run parsefile() yet?")
        
        # minimal formatting
        ast = dump(
            self.tree,
            annotate_fields=False,
            include_attributes=False,
            indent=0,
            show_empty=False
        )
        # no whitespace
        ast = "".join(ast.split())
        
        # replace keywords with shorter wersions (decreases length by ~40%)
        ast = self.replacek(ast)
        
        # base64 compressed bytes
        compbytes = zlib.compress(ast.encode('utf-8'))
        encstr = base64.b64encode(compbytes).decode('utf-8')
        
        return encstr

if __name__ == "__main__":
    parser = Parser("parser.py") # parses itself lol funny haha
    parser.parsefile()
    outs: List[Tuple[str, str]] = []
    outs.append(parser.getuncompressed())
    outs.append(parser.getcompressed())
    outs.append(parser.zlibcomp())
    
    for i in outs:
        print(i[1])
    print()
    for i in outs:
        print(i[0])