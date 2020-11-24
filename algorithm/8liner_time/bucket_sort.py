"""桶排序"""

def bucket_sort(A):
    min_num, max_num, length = min(A), max(A), len(A)
    #桶数组
    bucket_list = [ [] for i in range(length)]
    #每个桶的大小,至少有1个元素
    bucket_range = max((max_num - min_num) // length, 1)
    # 向桶数组填数
    for val in A:
        #val元素对应所在桶的编号
        bucket_index =  ( val - min_num ) // bucket_range
        bucket_list[int(bucket_index)].append(val)
    A.clear()
    # 回填，这里桶内部排序直接调用了sorted
    for bucket in bucket_list:
        for val in sorted(bucket):
            A.append(val)

def main():
    A = [3.2,6,8,4,2,6,7,3]
    bucket_sort(A)
    print(A)

if __name__ == '__main__':
    main()
