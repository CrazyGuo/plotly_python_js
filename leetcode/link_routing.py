class ListNode:
     def __init__(self, x):
         self.val = x
         self.next = None

def rotateRight(head: ListNode, k: int) -> ListNode:
    if k <= 0:
        return head
    while True:
        slow = fast = head
        fast_prev = slow_prev = None
        length = 0
        for x in range(k):
            if fast:
                fast = fast.next
                length += 1
            else:
                break

        while fast:
            slow_prev = slow
            slow = slow.next
            fast_prev = fast
            fast = fast.next

            length += 1

        if length == 1:
            return head
            
        if k < length:
            slow_prev.next = None
            fast_prev.next = head
            return slow
        elif k == length:
            return head
        else:
            while k > length:
                k -= length

node1 = ListNode(0)
node2 = ListNode(1)
node3 = ListNode(2)
node1.next = node2
node2.next = node3

n = rotateRight(node1,4)
print(n)



