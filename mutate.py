# This "Starter Code" for EECS 481 HW3 shows how to use a visitor
# pattern to replace nodes in an abstract syntax tree. 
# 
# Note well:
# (1) It does not show you how to read input from a file. 
# (2) It does not show you how to write your resulting source
#       code to a file.
# (3) It does not show you how to "count up" how many of 
#       instances of various node types exist.
# (4) It does not show you how to use random numbers. 
# (5) It does not show you how to only apply a transformation
#       "once" or "some of the time" based on a condition.
# (6) It does not show you how to copy the AST so that each
#       mutant starts from scratch. 
# (7) It does show you how to execute modified code, which is
#       not relevant for this assignment.
#
# ... and so on. It's starter code, not finished code. :-) 
# 
# But it does highlight how to "check" if a node has a particular type, 
# and how to "change" a node to be different. 

import ast
import astor
import random
import argparse


class MyVisitor(ast.NodeTransformer):
    """Notes all Numbers and all Strings. Replaces all numbers with 481 and
    strings with 'SE'."""
    # each function has a random chance of 
    # Note how we never say "if node.type == Number" or anything like that.
    # The Visitor Pattern hides that information from us. Instead, we use
    # these visit_Num() functions and the like, which are called
    # automatically for us by the library. 
    def visit_Num(self, node):
        print("Visitor sees a number: ", ast.dump(node), " aka ", astor.to_source(node))
        # Note how we never say "node.contents = 481" or anything like
        # that. We do not directly assign to nodes. Intead, the Visitor
        # Pattern hides that information from us. We use the return value
        # of this function and the new node we return is put in place by
        # the library. 
        # Note: some students may want: return ast.Num(n=481) 
        
        # 0, -1, 1, or same
        num = random.randint(1,4)
        if num == 1:
            return ast.Num(value=0, kind=None)
        elif num == 2:
            return ast.Num(value=-1, kind=None)
        elif num == 3:
            return ast.Num(value=1, kind=None)
        else:
            return node

    def visit_Str(self, node):
        print("Visitor sees a string: ", ast.dump(node), " aka ", astor.to_source(node))
        # Note: some students may want: return ast.Str(s=481)
        
        num = random.randint(1,3)
        if num == 1:
            return ast.Num(value="", kind=None)
        elif num == 2:
            return ast.Num(value=node.value[1:], kind=None)
        else:
            return node
        # Same, "" or 
    
    def visit_Compare(self, node):
        # >, >=, ==, <=, <
        # 50% chance of negating comparison operator
        num = random.randint(1, 2)
        if num == 1:
            if isinstance(node.ops[0], ast.Lt):
                return ast.Compare(left=node.left, ops=[ast.GtE()], comparators=node.comparators)
            elif isinstance(node.ops[0], ast.LtE):
                return ast.Compare(left=node.left, ops=[ast.Gt()], comparators=node.comparators)
            elif isinstance(node.ops[0], ast.Gt):
                return ast.Compare(left=node.left, ops=[ast.LtE()], comparators=node.comparators)
            elif isinstance(node.ops[0], ast.GtE):
                return ast.Compare(left=node.left, ops=[ast.Lt()], comparators=node.comparators)
            elif isinstance(node.ops[0], ast.Eq):
                return ast.Compare(left=node.left, ops=[ast.NotEq()], comparators=node.comparators)
            elif isinstance(node.ops[0], ast.NotEq):
                return ast.Compare(left=node.left, ops=[ast.Eq()], comparators=node.comparators)
        else:
            return node
        return node
    
    def visit_BinOp(self, node):
        # + to -, * to //, + to *, - to //, leave the same 
        if isinstance(node.op, ast.Add):  # If the operation is "+"
            choices = [ast.Sub(), ast.Mult(), ast.Add()]  # -, *, +
        elif isinstance(node.op, ast.Sub):  # If the operation is "-"
            choices = [ast.Add(), ast.FloorDiv(), ast.Sub()]  # +, //, -
        elif isinstance(node.op, ast.Mult):  # If the operation is "*"
            choices = [ast.FloorDiv(), ast.Add(), ast.Mult()]  # //, +, *
        elif isinstance(node.op, ast.FloorDiv):  # If the operation is "//"
            choices = [ast.Sub(), ast.Mult(), ast.FloorDiv()]  # -, *, //
        else:
            return node  # If it's not one of the above, return the node unchanged
        
        # Randomly select one of the choices with equal probability
        newOp = random.choice(choices)
        
        return ast.BinOp(left=node.left, op=newOp, right=node.right)
    
    def visit_BoolOp(self, node):
        # 50% chance of negating boolean statement, 50% chance of leaving statement alone
        num = random.randint(1, 2)
        if num == 1:
            if isinstance(node.op, ast.And):
                return ast.BoolOp(op=ast.Or(), values=node.values)
            elif isinstance(node.op, ast.Or):
                return ast.BoolOp(op=ast.And(), values=node.values)
        else:
            return node
        return node
    
    def visit_Expr(self, node):
    # implement 25% chance of deleting, 75% lea
        num = random.randint(1,4)
        if isinstance(node.value, ast.Call) and num == 1:
            print("Visitor sees a function call: ", ast.dump(node), " aka ", astor.to_source(node))
            return None  # Deleting function call
        return node

parser = argparse.ArgumentParser()

parser.add_argument('file_name', type=str, help='The name of the file to process')
parser.add_argument('num_mutants', type=int, help='The number of mutants to generate')

args = parser.parse_args()
file_name = args.file_name
num_mutants = args.num_mutants

try:
    with open(file_name, 'r') as file:
        file_contents = file.read()
        code = file_contents
        print("Before any AST transformation")
        print("Code is: ", code)
        print("Code's output is:") 
        print()
        print("Applying AST transformation")
        ast.parse(code)
        for i in range(num_mutants):
            random.seed = i
            output_name = str(i) + ".py"
            tree = MyVisitor().visit(tree)
            # Add lineno & col_offset to the nodes we created
            ast.fix_missing_locations(tree)
            print("Transformed code is: ", astor.to_source(tree))
            with open(output_name, 'w') as outputFile:
                outputFile.write(astor.to_source(tree))
            
except FileNotFoundError:
    print(f"Error: The file '{file_name}' does not exist.")
except Exception as e:
    print(f"An error occurred: {e}")
