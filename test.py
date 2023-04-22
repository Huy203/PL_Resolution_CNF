tuple1 = ([1,2], [2,3], 3, 4, 5)
tuple2 = ([1,2], [2,3], 3)

if set(tuple2) <= set(tuple1):
    print("tuple2 is a subset of tuple1")
else:
    print("tuple2 is not a subset of tuple1")
