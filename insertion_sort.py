def instertion_sort(seq):

    for slice_end in range(len(seq)):
        pos = slice_end
        # inserting elements at correct position
        while pos > 0 and seq[pos] < seq[pos - 1]:
            (seq[pos], seq[pos - 1]) = (seq[pos - 1], seq[pos])
            pos = pos - 1


# test input
l = [54, 26, 93, 17, 77, 31, 44, 55, 20]
instertion_sort(l)
print(l)

