class ListNode:
     def __init__(self, x):
         self.val = x
         self.next = None
    
def revrese(head, tail):
    new_tail = head
    prev = tail.next
    stop_node = tail.next;
    while head :
        if head == stop_node:
            break
        temp = head.next
        #指向前一个节点
        head.next = prev
        prev = head
        #下一个待处理节点
        head = temp
    return tail, new_tail

def reverseBetween( head, m, n):
    dummy = ListNode(None)
    dummy.next = head
    next_node = dummy
    
    left_prev = None
    for _ in range(m):
        left_prev = next_node
        next_node = next_node.next
    left = next_node
    for _ in range(n-m):
        next_node = next_node.next
    right = next_node

    new_head, new_tail = revrese(left, right)
    left_prev.next = new_head
    return dummy.next

node1 = ListNode(0)
node2 = ListNode(1)
node3 = ListNode(2)
node4 = ListNode(3)
node5 = ListNode(4)

node1.next = node2
node2.next = node3
node3.next = node4
node4.next = node5

n = reverseBetween(node1,2,4)
print(n)



