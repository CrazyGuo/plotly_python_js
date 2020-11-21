class ListNode:
     def __init__(self, x):
         self.val = x
         self.next = None

def addTwoNumbers(l1: ListNode, l2: ListNode) -> ListNode:
    #链表合并函数
    def merge(node):
        result = []
        while node:
            result.append(str(node.val))
            node = node.next
        return ''.join(result)
    #翻转并求和
    fisrt_val = merge(l1)
    ft = fisrt_val[-1::-1]
    sum_val = int(merge(l1)[-1::-1]) + int(merge(l2)[-1::-1])
    #倒序拆分
    result = [ListNode(int(val)) for val in str(sum_val)[-1::-1]]
    #合并链表
    previous_node = None
    for node in result:
        if previous_node is None:
            previous_node = node
        else:
            previous_node.next = node
            previous_node = node
    return result[0]


def addTwoNumbers2(l1: ListNode, l2: ListNode) -> ListNode:
    result_head_node = ListNode(0)
    result_next_node = result_head_node
    l1_next = l1
    l2_next = l2
    flag_val = 0
    while l1_next or l2_next:
        #1.按位数相加求和
        l1_val = l1_next.val if l1_next else 0
        l2_val = l2_next.val if l2_next else 0
        sum_val = l1_val + l2_val + flag_val #注意进位
        #2.进位值情况处理
        flag_val = sum_val // 10
        sum_val = sum_val % 10
        #3. 保存到链表结果
        result_next_node.next = ListNode(sum_val)
        
        #3. 指向下一位计算的值
        l1_next = l1_next.next if l1 else None
        l2_next = l2_next.next if l2 else None
        result_next_node = result_next_node.next
    else:
        #4.最后一位计算进位情况检查
        if flag_val > 0:
            result_next_node.next = ListNode(flag_val)
    return result_head_node.next

def addTwoNumbers(self, l1: ListNode, l2: ListNode) -> ListNode:
    carry = 0
    head = ListNode(0)
    node = head
    while (l1 or l2):
        x = l1.val if l1 else 0
        y = l2.val if l2 else 0
        s = x + y + carry
        carry = s // 10
        node.next = ListNode(s % 10)
        node = node.next
        if l1:
            l1 = l1.next
        if l2:
            l2 = l2.next
    if carry > 0:
        node.next = ListNode(1)
    return head.next  

node1 = ListNode(2)
node2 = ListNode(4)
node3 = ListNode(3)
node1.next = node2
node2.next = node3

node4 = ListNode(5)
node5 = ListNode(6)
node6 = ListNode(4)
node4.next = node5
node5.next = node6

n = addTwoNumbers2(node1,node4)
print(n)



