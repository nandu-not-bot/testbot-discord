import inspect

def dec(f):
    def wrapper(*key):
        ints = [int(e) for e in key]
        f(key=ints)
    return wrapper

@dec
def add(id, key):
    print(id)
    print(key)

add(69, '1', '2')
