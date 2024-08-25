def sliding_window(li, length=2, step=1):
    i, j = 0, length
    while j<=len(li):
        yield li[i:j]
        i+= step
        j+= step