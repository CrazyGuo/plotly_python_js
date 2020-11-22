
import random


#数组A的两个元素互换
def swap(A, i, j):
    A[i], A[j] = A[j], A[i]

#对数组A进行分治 返回i下标 [0, i-1]比i处的值小或等于, [i+1, end_index]比i处的大或等于
def partition(A, begin_index, end_index):
    pivot = A[end_index]
    #i指向比pivot小的最后一个元素
    i = begin_index - 1
    for j in range(begin_index, end_index, 1):
        if A[j] <= pivot:
            i += 1
            swap(A, i, j)
    #与pivot交换
    i += 1
    swap(A, i, end_index)
    return i

#对数组A进行随机化处理
def randomized_partition(A, begin_index, end_index):
    #随机获取区间[begin_index, end_index]中的任何一个数
    random_index = random.randint(begin_index, end_index)
    swap(A, random_index, end_index)
    return partition(A, begin_index, end_index )

#对数组A进行快排序
def quick_sort(A, begin_index, end_index):
    if begin_index < end_index:
        pivot_index = randomized_partition(A, begin_index, end_index ) 

        quick_sort(A, 0, pivot_index - 1)
        quick_sort(A, pivot_index + 1, end_index)


def main():
    A = [2,8,7,1,3,5,6,4]
    quick_sort(A, 0, len(A)-1)
    print(A)


if __name__ == '__main__':
    main()
