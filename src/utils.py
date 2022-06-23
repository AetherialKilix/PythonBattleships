def add_all(values):
    out = 0
    for i in values:
        out += i
    return out


def create_2d_list(size, fill=None):
    out = []
    for i in range(size):
        this = []
        if fill is not None:
            for j in range(size):
                this.append(fill)
        out.append(this)
    return out


def to_string_list(data):
    out = []
    for entry in data:
        out.append(str(entry))
    return out


def list_operator(a, b, operator=lambda a, b: a + b):
    out = []
    if len(a) != len(b):
        raise ValueError
    for i in range(len(a)):
        out = operator(a[i], b[i])
    return out


def create_and_fill_list(size, fill):
    out = []
    for i in range(size):
        out.append(fill)
    return out