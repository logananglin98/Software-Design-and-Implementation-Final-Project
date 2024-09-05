import unittest
from inspect import getframeinfo, stack
from FinalProjectLoganSara import *

def unittest(did_pass):
    caller = getframeinfo(stack()[1][0])
    linenum = caller.lineno
    if did_pass:
        msg = "Line {0} ok".format(linenum)
    else:
        msg = "Line {0} bad".format(linenum)
    print(msg)


unittest(test(22) == False)
unittest(test(1) == True)
