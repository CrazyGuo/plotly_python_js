
#对数组A,[low, mid], [mid+1, high]进行合并排序
def merge(A, low, mid, high):
    #将数据分成2个数据
    left_count = mid - low + 1
    right_count = high - (mid + 1) + 1
    left_arr = [None] * (left_count + 1)
    right_arr = [None] * (right_count + 1)

    for l in range(0, left_count):
        left_arr[l] = A[low + l]

    for r in range(0, right_count):
        right_arr[r] = A[mid + 1 + r]
    
    #最后都加入哨兵到末尾 目的简化代码
    left_arr[left_count] = float("inf")
    right_arr[right_count] = float("inf")

    l, r, k = 0, 0, low
    #将l,r中值小的放入到k位置
    for k in range(low, high+1):
        if left_arr[l] <= right_arr[r]:
            A[k] = left_arr[l]
            l += 1
        else:
            A[k] = right_arr[r]
            r += 1

#归并算法
def merge_sort(A, low, high):
    if low < high:
        mid = low + ((high - low) >> 1)

        merge_sort(A, low, mid)
        merge_sort(A, mid+1, high)

        merge(A, low, mid, high)

def main():
    A = [2,8,7,1,3,5,6,4]
    merge_sort(A, 0, len(A)-1)
    print(A)


if __name__ == '__main__':
    main()
