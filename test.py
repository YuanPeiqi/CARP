if __name__ == '__main__':
    a = [[1, 2], [3, 4]]
    print(a[3])
    c = None
    for item in a:
        if item is not None:
            c = item
    c.remove(3)
    print(a)

