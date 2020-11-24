
#计数排序 其中k为数组A中的最大值
def counter_sort(A, k):
    B, C = [0] * len(A), [0] * (k+1)
    #统计数组A元素的个数 并放到C中：key为元素值 val为个数
    for val in A:
        C[val] += 1
    #统计C[i]对应的前缀和 也即在[0,i]之间<=i 的元素个数
    for i in range(1, k+1):
        C[i] = C[i] + C[i-1]

    for val in A[::-1]:#A中的元素值 注意是从后向前遍历
        count = C[val] # <= val的个数
        val_index = count - 1 #对应下标位置
        B[val_index] = val #值在B中的位置

        C[val] -= 1 # <= val的个数减少1个

    return B

def main():
    A = [2, 5, 3,0,2,3,0,3]
    #A = [1,2,4,3,5]
    B = counter_sort(A, 5)
    print(B)

if __name__ == '__main__':
    main()
