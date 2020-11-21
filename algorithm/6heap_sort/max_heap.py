#该函数递归方式维护最大二叉堆的性质
def max_heapify(A, i, arr_len):
    """
    基本思路是从一个元素开始，如果这个元素不符合最大堆的规定，那么就把其子节点的元素，提升到父节点上面。
    注意这是一个递归的过程，只有在满足最大堆的条件或者到达堆的叶节点的时候才会退出.
    注意：heapify方法的条件是他的子节点都是最大堆，使用的时候要注意这一点。
    """
    largest = i
    left = i * 2 + 1
    right = i * 2 + 2
    # 这个地方使用left和right比较，是为了防止到了叶节点的时候会出现数组越界。
    if left < arr_len and A[largest] < A[left]:
        largest = left

    if right < arr_len and A[largest] < A[right]:
        largest = right

    # 保证在父元素就是最大值的时候不要移动元素
    if largest != i:
        A[largest], A[i] = A[i], A[largest]
        max_heapify(A, largest, arr_len)

#该函数迭代方式维护最大二叉堆的性质
def loop_max_heapify(A, i, arr_len):
    """
    基本思路是从一个元素开始，如果这个元素不符合最大堆的规定，那么就把其子节点的元素，提升到父节点上面。
    注意这是一个递归的过程，只有在满足最大堆的条件或者到达堆的叶节点的时候才会退出.
    注意：heapify方法的条件是他的子节点都是最大堆，使用的时候要注意这一点。
    """
    while True:
        largest = i
        left = i * 2 + 1
        right = i * 2 + 2
        # 这个地方使用left和right比较，是为了防止到了叶节点的时候会出现数组越界。
        if left < arr_len and A[largest] < A[left]:
            largest = left

        if right < arr_len and A[largest] < A[right]:
            largest = right

        # 保证在父元素就是最大值的时候不要移动元素
        if largest != i:
            A[largest], A[i] = A[i], A[largest]
            i = largest
        else:
            break

#把数组A转换为最大堆
def build_max_heap(A):
    arr_len = len(A)
    mid = arr_len // 2
    #从中间的元素开始建堆
    for i in range(mid, -1, -1):
        max_heapify(A, i, arr_len)

#堆排序
def heap_sort(A):
    arr_len = len(A)
    build_max_heap(A)
    for i in range(arr_len-1, 0, -1):
        #将数组首尾元素值交换 也即最大值放到最后 
        A[0], A[i] = A[i], A[0]
        arr_len = i
        max_heapify(A, 0, arr_len)


#使用堆实现的优先队列

#1.返回优先队列中的首个任务
def heap_maximun(A):
    return A[0]

#2.返回首个任务 并从中删除
def heap_extract_max(A):
    if len(A) <= 0:
        return None
    max = A[0]
    A[0] = A[-1]
    A.pop()
    max_heapify(A,0, len(A))
    return max

#3.将第i处的值 提高到key
def heap_increase_key(A, i, key):
    def parent(index): #注意index对应parent节点下标的计算 考虑 奇偶情况
        if index % 2 == 0:
            return index // 2 - 1
        else:
            return index  // 2
    if key > A[i]:
        A[i] = key
        while i > 0 and A[parent(i)] < A[i]:
            A[parent(i)], A[i] = A[i], A[parent(i)]
            i = parent(i)

#4.插入优先级为key的新任务
def max_heap_insert(A, key):
    A.append(float("-inf"))
    arr_len = len(A)
    heap_increase_key(A, arr_len-1, key)


def main():
    A = [16, 14, 10, 8, 7, 9, 3, 2, 4, 1 ]
    #1.建立大根堆
    #build_max_heap(A)
    #print(A)

    #2.堆排序
    #heap_sort(A)
    #print(A)

    #3.优先队列测试
    build_max_heap(A)
    #r = heap_extract_max(A)
    #print(r)
    print(A)
    heap_increase_key(A, 8, 15)
    print(A)
    max_heap_insert(A, 17)
    print(A)


if __name__ == '__main__':
    main()