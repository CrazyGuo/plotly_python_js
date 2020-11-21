class ListNode:
     def __init__(self, x):
         self.val = x
         self.next = None
    
def partition(head, x):
    if head is None or head.next is None:
        return head
    dumy_max = ListNode(None)
    dumy_max.next = head
    max_prev = dumy_max

    dumy_min = ListNode(None)
    min_prev = dumy_min

    next_node = head

    while next_node:
        if next_node.val < x:
            #从当前队列移除
            temp = next_node.next
            next_node.next = None
            max_prev.next = temp
            #小的插入队列
            min_prev.next = next_node
            min_prev = next_node
            #指向下一个
            next_node = temp
        else:
            max_prev = next_node
            next_node = next_node.next
    #min_prev.next = dumy_max.next
    return dumy_max.next

node1 = ListNode(1)
node2 = ListNode(4)
node3 = ListNode(3)
node4 = ListNode(2)
node5 = ListNode(5)

node1.next = node2
node2.next = node3
node3.next = node4
node4.next = node5

n = partition(node1,3)
print(n)



