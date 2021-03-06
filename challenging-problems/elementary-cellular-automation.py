# THREE GOLD STARS
# Question 3-star: Elementary Cellular Automaton

# Please see the video for additional explanation.

# A one-dimensional cellular automata takes in a string, which in our 
# case, consists of the characters '.' and 'x', and changes it according 
# to some predetermined rules. The rules consider three characters, which 
# are a character at position k and its two neighbours, and determine 
# what the character at the corresponding position k will be in the new 
# string.

# For example, if the character at position k in the string  is '.' and 
# its neighbours are '.' and 'x', then the pattern is '..x'. We look up 
# '..x' in the table below. In the table, '..x' corresponds to 'x' which 
# means that in the new string, 'x' will be at position k.

# Rules:
#          pattern in         position k in        contribution to
# Value    current string     new string           pattern number
#                                                  is 0 if replaced by '.'
#                                                  and value if replaced
#                                                  by 'x'
#   1       '...'               '.'                        1 * 0
#   2       '..x'               'x'                        2 * 1
#   4       '.x.'               'x'                        4 * 1
#   8       '.xx'               'x'                        8 * 1
#  16       'x..'               '.'                       16 * 0
#  32       'x.x'               '.'                       32 * 0
#  64       'xx.'               '.'                       64 * 0
# 128       'xxx'               'x'                      128 * 1
#                                                      ----------
#                                                           142

# To calculate the patterns which will have the central character x, work 
# out the values required to sum to the pattern number. For example,
# 32 = 32 so only pattern 32 which is x.x changes the central position to
# an x. All the others have a . in the next line.

# 23 = 16 + 4 + 2 + 1 which means that 'x..', '.x.', '..x' and '...' all 
# lead to an 'x' in the next line and the rest have a '.'

# For pattern 142, and starting string
# ...........x...........
# the new strings created will be
# ..........xx...........  (generations = 1)
# .........xx............  (generations = 2)
# ........xx.............  (generations = 3)
# .......xx..............  (generations = 4)
# ......xx...............  (generations = 5)
# .....xx................  (generations = 6)
# ....xx.................  (generations = 7)
# ...xx..................  (generations = 8)
# ..xx...................  (generations = 9)
# .xx....................  (generations = 10)

# Note that the first position of the string is next to the last position 
# in the string.

# Define a procedure, cellular_automaton, that takes three inputs: 
#     a non-empty string, 
#     a pattern number which is an integer between 0 and 255 that
# represents a set of rules, and 
#     a positive integer, n, which is the number of generations. 
# The procedure should return a string which is the result of
# applying the rules generated by the pattern to the string n times.

def pattern_rules(pn):
    pn_binary = format(pn, '8b')
    patterns = ['...', '..x', '.x.', '.xx',
                'x..', 'x.x', 'xx.', 'xxx']
    rules = {}
    for i in range(0, 8):
        if pn_binary[7-i]=='1':
            rules[patterns[i]] = 'x'
        else:
            rules[patterns[i]] = '.'
    return rules

def cellular_automaton(string, pattern_num, generations):
    n = len(string)
    rules = pattern_rules(pattern_num)
    for unused in range(0, generations):
        temp = string[-1:] + string + string[:1]
        string = ""
        for i in range(0, n):
            string += rules[temp[i:i+3]]
    return string

test_param = [[['.x.x.x.x.', 17, 2],
"xxxxxxx.."],
[['.x.x.x.x.', 249, 3],
".x..x.x.x"],
[['...x....', 125, 1],
"xx.xxxxx"],
[['...x....', 125, 2],
".xxx...."],
[['...x....', 125, 3],
".x.xxxxx"],
[['...x....', 125, 4],
"xxxx...x"],
[['...x....', 125, 5],
"...xxx.x"],
[['...x....', 125, 6],
"xx.x.xxx"],
[['...x....', 125, 7],
".xxxxx.."],
[['...x....', 125, 8],
".x...xxx"],
[['...x....', 125, 9],
"xxxx.x.x"],
[['...x....', 125, 10],
"...xxxxx"]]

correct =0
for p in test_param:
    res = cellular_automaton(p[0][0],p[0][1],p[0][2])
    if res != p[1]:
        print res," should be ",p[1]," for input: ",p[0]
    else:
        correct +=1
print "Passed ",correct," out of ",len(test_param)
