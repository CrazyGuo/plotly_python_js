"""基数排序"""
def radix_sort(A):
    i = 0 # 记录当前正在排哪一位，最低位为1
    max_num = max(A)  # 最大值
    j = len(str(max_num))  # 记录最大值的位数
    for i in range(j):
        bucket_list =[[] for _ in range(10)] #初始化桶数组
        for x in A:
            #x值的i位所在桶的编号
            x_index = int( x / (10**i) ) % 10
            bucket_list[x_index].append(x) # 找到位置放入桶数组
        print(bucket_list)
        A.clear()
        for bucket in bucket_list:   # 放回原序列
            for val in bucket:
                A.append(val)

def main():
    A = [334,5,67,345,7,345345,99,4,23,78,45,1,3453,23424]
    radix_sort(A)
    print(A)

if __name__ == '__main__':
    main()