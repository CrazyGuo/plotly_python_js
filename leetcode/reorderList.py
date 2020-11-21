class ListNode:
     def __init__(self, x):
         self.val = x
         self.next = None

class Solution:
    
    def reverse(self, head):
        prev = None
        while head:
            temp = head.next
            head.next = prev
            prev = head

            head = temp
        return prev

    def merge(self, head1, head2):
        h1 = head1
        h2 = head2
        while h1 and h2:
            temp1 = h1.next
            h1.next = h2
            temp2 = h2.next
            h2.next = temp1

            h1 = temp1
            h2 = temp2
        return head1
        
    def reorderList(self, head):
        """
        Do not return anything, modify head in-place instead.
        """
        if head is None or head.next is None:
            return head
        #1.找到中间节点
        fast = head
        slow = head
        while fast is not None and fast.next is not None:
            fast = fast.next.next
            slow = slow.next
        middle_point = slow
        #2. 对后半段进行逆向排序
        second_head = middle_point.next
        middle_point.next = None
        new_head = self.reverse(second_head)
        # 合并2个链表
        return self.merge(head, new_head)

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
n = s.reorderList(node1)
print(n)



