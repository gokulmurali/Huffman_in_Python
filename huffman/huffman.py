#Huffman 

class codeTree: pass

class Fork(codeTree):
    def __init__(self, left, right, chars, weight):
        self.left = left
        self.right = right
        self.chars = chars
        self.weight = weight

class Leaf(codeTree):
    def __init__(self, char, weight):
        self.left = None
        self.right = None
        self.char = char
        self.chars = list(char)
        self.weight = weight


def weight(tree):
     return tree.weight

def chars(tree):
    if (tree.left and tree.right) == None:
        return list(tree.char)
    else:
        return tree.left.chars + tree.right.chars
      
def makeCodeTree(left, right):
    return Fork(left, right, chars(left) + chars(right), weight(left) + weight(right))
 
def string2Chars(str):return list(str)

def times(chars):
    dict ={}
    def times0(chars, dict):
        if chars == []:return dict
        else:
            dict.update({chars[0]:chars.count(chars[0])})
            return times0(filter(lambda f: f != chars[0], chars), dict)

    return times0(chars, dict)

def makeOrderedLeafList(dict):
    list=[]
    def helper(dict, list):
        if dict == {}:return list
        else:
            lis = dict.keys()
            char = lis[0]
            weigh = dict[lis[0]]
            del(dict[lis[0]])
            list.append(Leaf(char,weigh))
            return helper(dict,list)
    return sorted(helper(dict,list), key=weight)

def singleton(trees):
    if len(trees) ==1: return True
    else: return False

def combine(trees):
    if (trees == []) or (len(trees) == 1): return trees
    #elif len(trees) == 1: trees
    else:
        t = trees[2:]
        c = makeCodeTree(trees[0],trees[1])
        t.append(c)
        return sorted(t, key=weight)

def until(cond, act, trees):
    if cond(trees): return trees
    else:
        return until(cond,act,act(trees))
    
def createCodeTree(chars):
    m=makeOrderedLeafList(times(chars))
    return until(singleton, combine, m)

frenchCode= Fork(Fork(Fork(Leaf('s',121895),Fork(Leaf('d',56269),Fork(Fork(Fork(Leaf('x',5928),Leaf('j',8351),['x','j'],14279),Leaf('f',16351),['x','j','f'],30630),Fork(Fork(Fork(Fork(Leaf('z',2093),Fork(Leaf('k',745),Leaf('w',1747),['k','w'],2492),['z','k','w'],4585),Leaf('y',4725),['z','k','w','y'],9310),Leaf('h',11298),['z','k','w','y','h'],20608),Leaf('q',20889),['z','k','w','y','h','q'],41497),['x','j','f','z','k','w','y','h','q'],72127),['d','x','j','f','z','k','w','y','h','q'],128396),['s','d','x','j','f','z','k','w','y','h','q'],250291),Fork(Fork(Leaf('o',82762),Leaf('l',83668),['o','l'],166430),Fork(Fork(Leaf('m',45521),Leaf('p',46335),['m','p'],91856),Leaf('u',96785),['m','p','u'],188641),['o','l','m','p','u'],355071),['s','d','x','j','f','z','k','w','y','h','q','o','l','m','p','u'],605362),Fork(Fork(Fork(Leaf('r',100500),Fork(Leaf('c',50003),Fork(Leaf('v',24975),Fork(Leaf('g',13288),Leaf('b',13822),['g','b'],27110),['v','g','b'],52085),['c','v','g','b'],102088),['r','c','v','g','b'],202588),Fork(Leaf('n',108812),Leaf('t',111103),['n','t'],219915),['r','c','v','g','b','n','t'],422503),Fork(Leaf('e',225947),Fork(Leaf('i',115465),Leaf('a',117110),['i','a'],232575),['e','i','a'],458522),['r','c','v','g','b','n','t','e','i','a'],881025),['s','d','x','j','f','z','k','w','y','h','q','o','l','m','p','u','r','c','v','g','b','n','t','e','i','a'],1486387)

secret = [0,0,1,1,1,0,1,0,1,1,1,0,0,1,1,0,1,0,0,1,1,0,1,0,1,1,0,0,1,1,1,1,1,0,1,0,1,1,0,0,0,0,1,0,1,1,1,0,0,1,0,0,1,0,0,0,1,0,0,0,1,0,1]

def decode(tree, bits):
    list = []
    def decode0(tree0,bits0,list):
        if bits0 == []:
            if isinstance(tree0,Leaf):
                list.append(tree0.char)
                return list
            else: return []
        else:
            if isinstance(tree0, Leaf):
                list.append(tree0.char)
                return decode0(tree,bits0,list)
            else:
                if bits0[0] == 0:
                    t = tree0.left
                else:
                    t = tree0.right
                    
                return decode0(t, bits0[1:],list)
    return decode0(tree,bits,list)

decodedSecret = decode(frenchCode,secret)
print decodedSecret

def encode(tree, text):
    list = []
    def encode0(tree0,text0,list):
        if text0 == []:
            print list
            return list
        else:
            if isinstance(tree0, Leaf):
                return encode0(tree, text0[1:], list)
            else:
                if text0[0] in chars(tree0.left):
                    t = tree0.left
                    b = 0
                else:
                    t = tree0.right
                    b = 1
                list.append(b)    
                return encode0(t, text0, list)
    return encode0(tree, text, list)

def codeBits(table, char):
    if table == []:return []
    elif (table[0][0] == char):return table[0][1]
    else:return codeBits(table[1:],char)

def mergeCodeTables(a, b):
    return a + b

def convert(tree):
    list = []
    def convert0(tree, acc1, acc2):
        if isinstance(tree, Leaf):
            return acc1+[(tree.char,acc2)]
        else:
            return mergeCodeTables(convert0(tree.left, acc1, acc2+[0]), convert0(tree.right, acc1,acc2+[1]))

    return convert0(tree,list,list)

def quickEncode(tree, text):
    list = []
    def quickEncode0(tree0, text0, list):
        if text0 == []: return list
        else:
            return quickEncode0(tree0, text0[1:], list+codeBits(tree0,text0[0]))
      
    return quickEncode0(convert(tree), text, list)

#print convert(frenchCode)
#print codeBits(convert(frenchCode),"g")
c=quickEncode(frenchCode, list("gokulrahul"))
print c
d=decode(frenchCode,c)
print d
