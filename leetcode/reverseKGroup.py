class ListNode:
     def __init__(self, x):
         self.val = x
         self.next = None
    
def reverse(head, tail):
    new_tail = head
    new_head = tail
    stop_node = tail.next

    previous = tail.next
    while head:
        if head == stop_node:
            break
        #逆向改动
        next_node = head.next
        head.next = previous
        #向前移动
        previous = head
        head = next_node
    return new_head, new_tail

def reverseKGroup(head, k):
    dummy = ListNode(None)
    dummy.next = head

    #检查当前组是否小于k
    def check_k_number(tail_node):
        has_k = True
        for _ in range(k):
            tail_node = tail_node.next
            if not tail_node:
                return None
        return tail_node

    previous = dummy
    tail = dummy
    while True:
        tail = check_k_number(tail)
        if not tail:
            break
        rverse_head, reverse_tail = reverse(head, tail)
        previous.next = rverse_head

        previous = reverse_tail
        head = reverse_tail.next
        tail = reverse_tail

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

n = reverseKGroup(node1,3)
print(n)



