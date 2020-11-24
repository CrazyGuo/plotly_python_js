
#计数排序
def count_sort(A):
    # 找到最大最小值
    min_num = min(A)
    max_num = max(A)
    # 计数列表
    count_list = [0]* (max_num - min_num + 1)
    # 计数
    for i in A:
        count_list[ i - min_num ] += 1
    A.clear()
    # 填回
    for idx, count in enumerate(count_list):
        while count != 0:
            A.append( idx + min_num)
            count -= 1

def main():
    A = [3,6,8,4,2,6,7,3]
    count_sort(A)
    print(A)

if __name__ == '__main__':
    main()
