#冒泡排序
def bubble_sort(A):
    length = len(A)
    for i in range(length):
        orded_count = i #已完成排序的个数  位于数组的末尾
        for j in range(length - orded_count - 1):
            if A[j] > A[j+1]: #大的数据向后排
                A[j+1], A[j] = A[j], A[j+1]

def main():
    A = [2,8,7,1,3,5,6,4]
    bubble_sort(A)
    print(A)


if __name__ == '__main__':
    main()