class ListNode:
     def __init__(self, x):
         self.val = x
         self.next = None

def detectCycle( head):
    if head is None or head.next is None:
        return None
    slow = head
    fast = head
    #第一次相遇得到k值 并确定有环
    k = 0
    while fast is not None and fast.next is not None:     
        fast = fast.next.next
        slow = slow.next
        k += 1
        if fast == slow:
            break
    if fast is None:
        return None
        
    #第二次相遇得到m值
    m = 0
    slow = head
    while fast != slow:
        fast = fast.next
        slow = slow.next
        m += 1
    print('k is %d' % k)
    print('m is %d' % m)
    return slow.val

node1 = ListNode(1)
node2 = ListNode(2)
node3 = ListNode(3)
node4 = ListNode(4)
node5 = ListNode(5)

node1.next = node2
node2.next = node3
node3.next = node4
node4.next = node5
node5.next = node2


n = detectCycle(node1)
print(n)



