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

    def __init__(self):
        self.num_count = 0
        self.str_count = 0
        self.compare_count = 0
        self.binOp_count = 0
        self.boolOp_count = 0
        self.total_mutations = 0

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
        self.num_count += 1
        if self.total_mutations >= 2:
            return node
        num = random.randint(1,10)
        if num == 1:
            if self.num_count % 4 == 1:
                self.total_mutations += 1
                return ast.Num(n=0)
            elif self.num_count % 4 == 2:
                self.total_mutations += 1
                return ast.Num(n=-1)
            elif self.num_count % 4 == 3:
                self.total_mutations += 1
                return ast.Num(n=1)
            else:
                return node
        else:
            return node
        

    def visit_Str(self, node):
        print("Visitor sees a string: ", ast.dump(node), " aka ", astor.to_source(node))
        # Note: some students may want: return ast.Str(s=481)
        
        self.str_count += 1
        num = random.randint(1,10)
        if num == 1:
            if self.str_count % 3 == 1:
                self.total_mutations += 1
                return ast.Str(s="")
            elif self.str_count % 3 == 2:
                self.total_mutations += 1
                return ast.Str(s=node.s[1:])
            else:
                return node
        else: 
            return node
        # Same, "" or 
    
    def visit_Compare(self, node):
        print("Visitor sees a comparison operator: ", ast.dump(node), " aka ", astor.to_source(node))
        # >, >=, ==, <=, <
        # 50% chance of negating comparison operator
        self.compare_count += 1
        if self.total_mutations >= 2:
            return node
        num = random.randint(1,10)
        if num == 1:
            self.total_mutations += 1
            if isinstance(node.ops[0], ast.Lt()):
                return ast.Compare(left=node.left, ops=[ast.GtE()], comparators=node.comparators)
            elif isinstance(node.ops[0], ast.LtE()):
                return ast.Compare(left=node.left, ops=[ast.Gt()], comparators=node.comparators)
            elif isinstance(node.ops[0], ast.Gt()):
                return ast.Compare(left=node.left, ops=[ast.LtE()], comparators=node.comparators)
            elif isinstance(node.ops[0], ast.GtE()):
                return ast.Compare(left=node.left, ops=[ast.Lt()], comparators=node.comparators)
            elif isinstance(node.ops[0], ast.Eq()):
                return ast.Compare(left=node.left, ops=[ast.NotEq()], comparators=node.comparators)
            elif isinstance(node.ops[0], ast.NotEq()):
                return ast.Compare(left=node.left, ops=[ast.Eq()], comparators=node.comparators)
        else:
            return node

    
    def visit_BinOp(self, node):
        print("Visitor sees a binary operator: ", ast.dump(node), " aka ", astor.to_source(node))
        # + to -, * to //, + to *, - to //, leave the same 
        
        self.binOp_count += 1
        if self.total_mutations >= 2:
            return node
        
        num = random.randint(1,10)
        if num == 1:
            if isinstance(node.op, ast.Add):
                choices = [ast.Sub(), ast.Mult()]
            elif isinstance(node.op, ast.Sub):
                choices = [ast.Add(), ast.FloorDiv()]
            elif isinstance(node.op, ast.Mult):
                choices = [ast.FloorDiv(), ast.Add()]
            elif isinstance(node.op, ast.FloorDiv):
                choices = [ast.Sub(), ast.Mult()]
            else:
                return node  # If not one of the above, return unchanged
            newOp = random.choice(choices)
            self.total_mutations += 1
            return ast.BinOp(left=node.left, op=newOp, right=node.right)
        else:
            return node
    
    def visit_BoolOp(self, node):
        print("Visitor sees a boolean operator: ", ast.dump(node), " aka ", astor.to_source(node))
        # 50% chance of negating boolean statement, 50% chance of leaving statement alone
        self.boolOp_count += 1
        num = random.randint(1, 10)
        if num == 1:
            self.total_mutations += 1
            if isinstance(node.op, ast.And):
                return ast.BoolOp(op=ast.Or(), values=node.values)
            elif isinstance(node.op, ast.Or):
                return ast.BoolOp(op=ast.And(), values=node.values)
        return node
    
    # def visit_Expr(self, node):
    # # implement 25% chance of deleting, 75% lea
    #     num = random.randint(1,4)
    #     if isinstance(node.value, ast.Call) and num == 1:
    #         print("Visitor sees a function call: ", ast.dump(node), " aka ", astor.to_source(node))
    #         return None  # Deleting function call
    #     return node

parser = argparse.ArgumentParser()

parser.add_argument('file_name', type=str, help='The name of the file to process')
parser.add_argument('num_mutants', type=int, help='The number of mutants to generate')

args = parser.parse_args()
file_name = args.file_name
num_mutants = args.num_mutants

with open(file_name, 'r') as file:
   file_contents = file.read()
   code = file_contents
# code = "a = 10; b = 20; c = 'Hello'; d = 'World'; is_equal = a > b; "
print("Before any AST transformation")
print("Code is: ", code)
print("Code's output is:") 
print()
print("Applying AST transformation")
for i in range(num_mutants):
    random.seed(i)
    tree = ast.parse(code)
    output_name = str(i) + ".py"
    tree = MyVisitor().visit(tree)
    # Add lineno & col_offset to the nodes we created
    ast.fix_missing_locations(tree)
    print(ast.dump(tree))
    print("Transformed code is: ", astor.to_source(tree))
    with open(output_name, 'w') as outputFile:
        outputFile.write(astor.to_source(tree))
