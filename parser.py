import re


def build_tree(tokens, acc):
    while len(tokens) != 0:
        token = tokens[0]
        tokens = tokens[1:]
        if token == '(':
            a, tokens = build_tree(tokens, [])
            acc.append(a)
        else:
            if token == ')':
                return acc, tokens
            acc.append(token)
    return acc, tokens


def tokenise(string):
    # tokenizáló reguláris kifejezés
    return re.findall(r"[^ \t\n\r\f\v()\"]+|\(|\)|\".*\"", string)


def is_number(s):
    if type(s) is str and re.match(r'\d+\Z',s):
        return True
    else:
        return False


def is_string(s):
    if type(s) is str and re.match(r"\".*\"",s):
        return True
    else:
        return False


def str2py_str(s):
    return s[1:-1]

# TODO: exception handling!
def plus(env):
    val = 0
    for item in env.values():
        val += item
    return val

# TODO: exception handling!
def minus(env):
    val = 0
    for item in env.values():
        val -= item
    return val


environment = {'+': plus, '-': minus}
def funcall(func):
    try:
        fun = environment[func[0]]
    except:
        pass


def eval_tree(tree, env):
    if type(tree[0]) is list:
        result = None
        for t in tree:
            result = eval_tree(t, env)
        return result
    if is_string(tree):
        return str2py_str(tree)
    if tree == 'True':
        return True
    if tree == 'False':
        return False
    if tree[0] == 'and':
        return eval_tree(tree[1], env) and eval_tree(tree[2], env)
    if is_number(tree):
        return int(tree)
    if tree[0] == '+':
        return eval_tree(tree[1], env) + eval_tree(tree[2], env)
    if tree[0] == 'print':
        print(eval_tree(tree[1], env))
        return None
    if tree[0] == 'let':
        environment[tree[1]] = eval_tree(tree[2], env)
    else:
        return environment[tree]


def main():
    tokens = tokenise("(+ 12 13) (+ 1 2)")
    print("tokens "+str(tokens))
    a, _ = build_tree(tokens, [])
    print(a)

    inp = input("write some code:")
    a,_ = build_tree(tokenise(inp),[])
    print(a)
    print(inp + " = " + str(eval_tree(a, {})))

if __name__ == "__main__":
    main()
