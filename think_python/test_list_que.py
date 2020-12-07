import collections

A = [1,2,3,4,5]

for a in A:
    if a < 4:
        A.remove(a)
        A.append(a)
        print(A)

#合并2个字典
dict1 = {'staff_id': 1, 'sex': 'M'}
dict2 = collections.defaultdict(dict)
dict2['1'].update(dict1)
print(dict2)

#改变合并后的字典 不会改变原始字典
dict2['1']['sex'] = 'F'
print(dict2)
print(dict1)


