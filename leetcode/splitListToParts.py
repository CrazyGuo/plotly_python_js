class ListNode:
     def __init__(self, x):
         self.val = x
         self.next = None

class Solution:
    def splitListToParts(self, root, k):
        if root is None or root.next is None: return [root]
        length = 0
        current = root
        while current:
            current = current.next
            length += 1
        if length > k:
            group_member_count = length // k
            lefted = length % k
        else:
            group_member_count = 1
            lefted = 0
        result = []
        for x in range(k):
            el = []
            ll = 0
            if lefted > 0 :
                length -= 1
                ll = 1
            num = group_member_count + ll
            new_head = self.put(el, root, num)
            root = new_head
            
            result.append(el)
        return result

    def put(self, containter, head, remove_num):
        dummy = ListNode(None)
        prev = dummy
        i = 0
        while head:
            temp = head
            head = head.next
            temp.next = None

            prev.next = temp
            prev = prev.next
            i += 1
            if i == remove_num:
                containter.append(dummy.next.val)
                break
        return head  

node1 = ListNode(1)
node2 = ListNode(2)
node3 = ListNode(3)
node4 = ListNode(4)
node5 = ListNode(5)

node1.next = node2
node2.next = node3
node3.next = node4
node4.next = node5

x,y = divmod(12, 5)

s = Solution()
n = s.splitListToParts(node1,5)
print(n)



