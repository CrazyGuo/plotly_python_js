#选择排序
def selected_sort(A):
    length = len(A)
    for i in range(length):
        min_index = i #i之前是排序好的 i处是要在之后找到对应的最小值
        for j in range(i+1, length):
            if A[j] < A[min_index]:
                A[min_index], A[j] = A[j], A[min_index]

def main():
    A = [2,8,7,1,3,5,6,4]
    selected_sort(A)
    print(A)


if __name__ == '__main__':
    main()