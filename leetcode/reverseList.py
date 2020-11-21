class ListNode:
     def __init__(self, x):
         self.val = x
         self.next = None

class Solution:
    #迭代方法
    def reverseList1(self, head):
        prev = None
        while head:
            nxt = head.next
            head.next = prev
            prev = head
            head = nxt
        return prev

    #递归方法
    def reverseList(self, head):
        new_tail = self.revrese(head)
        new_head = new_tail.next 
        new_tail.next = None
        return new_head

    def revrese(self, head):
        if head is None or head.next is None: return head
        
        tails = head.next
        head.next = None
        
        left = head
        right = self.revrese(tails)
        
        temp = right.next
        right.next = left
        left.next = right if temp is None else temp

        return  left    

node1 = ListNode(1)
node2 = ListNode(2)
node3 = ListNode(3)
node4 = ListNode(4)
node5 = ListNode(5)

node1.next = node2
node2.next = node3
node3.next = node4
node4.next = node5


s = Solution()
n = s.reverseList(node1)
print(n)



