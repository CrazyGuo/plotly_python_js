
#谢尔插入排序
def shell_insert_sort(A, end_index, gap):
    for i in range(gap, end_index+1):
        key = A[i]
        #当前i处的值 与前面每隔gap值进行插入排序
        pre_index = i - gap
        while pre_index >= 0 and A[pre_index] > key:
            A[pre_index + gap] = A[pre_index]
            pre_index -=  gap
        #将key值插入此处
        A[pre_index + gap] = key

#谢尔排序
def shell_sort(A):
    length = len(A)
    gap = length // 2 #谢尔增量
    while gap >= 1:
        shell_insert_sort(A, length - 1, gap)

        gap //= 2

def main():
    A = [2,8,7,1,3,5,6,4]
    shell_sort(A)
    print(A)


if __name__ == '__main__':
    main()