const = ('[', ']', '{', '}', ',', ':')
flags = ('function', 'class', 'object')


def doc_to_tokens(doc) -> []:
    tokens = []
    i = 0
    to_tokens_funcs = [str_to_token, bool_to_token, num_to_token, null_to_token]

    while i < len(doc):
        for func in to_tokens_funcs:
            flg, token, i = func(doc, i)
            if flg:
                tokens.append(token)
                break

        def append_token_and_name(flag, i):
            if len(doc) >= len(flag):
                if doc[i:i + len(flag)] == flag:
                    tokens.append(flag)
                    i += len(flag) + 1
                    name = ''

                    while i < len(doc):
                        if doc[i] == ')':
                            i += 2
                            break
                        else:
                            if doc[i] != '"':
                                name += doc[i]
                        i += 1

                    tokens.append(name)
            return i

        for flag in flags:
            i = append_token_and_name(flag, i)

        if i >= len(doc):
            break
        if doc[i] in (' ', '"'):
            i += 1
        elif doc[i] in const:
            tokens.append(doc[i])
            i += 1
        else:
            raise Exception()

    return tokens


def str_to_token(doc, i):
    token = ''
    if doc[i] != '"':
        return False, None, i
    i += 1

    while i < len(doc):
        if doc[i] == '"' and doc[i-1] != '\\':
            token = token.replace('\\"', '"').replace("\\'", "'")
            return True, token, i
        else:
            token += doc[i]
        i += 1

    raise Exception()


def bool_to_token(doc, i):
    bool_const = {'false': False, 'true': True}

    for key, val in bool_const.items():
        if len(doc) >= len(key):
            if doc[i:i + len(key)] == key:
                token = val
                i += len(key)
                return True, token, i

    return False, None, i


def num_to_token(doc, i):
    token = ''
    num_ch = [str(k) for k in range(0, 10)] + ['-', 'e', '.']

    float_const = {'NaN': float('nan'), 'Infinity': float('inf'), '-Infinity': -float('inf')}

    for key, val in float_const.items():
        if len(doc) >= len(key):
            if doc[i:i + len(key)] == key:
                token = val
                i += len(key)
                return True, token, i

    for j in range(i, len(doc)):
        if doc[j] in num_ch:
            token += doc[j]
        else:
            break

    if len(token) == 0:
        return False, None, i

    i += len(token)

    if '.' or 'e' in token:
        token = float(token)
    else:
        token = int(token)

    return True, token, i


def null_to_token(doc, i):
    null = 'null'
    if len(doc) >= len(null):
        if doc[i:i + len(null)] == null:
            token = None
            i += len(null)
            return True, token, i

    return False, None, i

