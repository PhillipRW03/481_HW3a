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

class MyVisitor(ast.NodeTransformer):
    """Notes all Numbers and all Strings. Replaces all numbers with 481 and
    strings with 'SE'."""

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
        return ast.Num(value=481, kind=None)

    def visit_Str(self, node):
        print("Visitor sees a string: ", ast.dump(node), " aka ", astor.to_source(node))
        # Note: some students may want: return ast.Str(s=481)
        return ast.Str(value="SE", kind=None)

# Instead of reading from a file, the starter code always processes in 
# a small Python expression literally written in this string below: 
code = """print(111 + len("hello") + 222 + len("goodbye"))"""

# As a sanity check, we'll make sure we're reading the code
# correctly before we do any processing. 
print("Before any AST transformation")
print("Code is: ", code)
print("Code's output is:") 
exec(code)      # not needed for HW3
print()

# Now we will apply our transformation. 
print("Applying AST transformation")
tree = ast.parse(code)
tree = MyVisitor().visit(tree)
# Add lineno & col_offset to the nodes we created
ast.fix_missing_locations(tree)
print("Transformed code is: ", astor.to_source(tree))
co = compile(tree, "", "exec")
print("Transformed code's output is:") 
exec(co)        # not needed for HW3