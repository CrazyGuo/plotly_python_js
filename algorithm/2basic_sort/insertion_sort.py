#插入排序算法
def insertion_sort(A):
    length = len(A)
    for i in range(1, length):
        key = A[i]
        j = i - 1
        #在i之前寻找比key小的值
        while j >= 0 and A[j] > key:
            A[j], A[j+1] = A[j+1], A[j]
            j -= 1
        #将key值填入到j+1处
        A[j+1] = key
    return A

def main():
    A = [2,8,7,1,3,5,6,4]
    insertion_sort(A)
    print(A)


if __name__ == '__main__':
    main()
