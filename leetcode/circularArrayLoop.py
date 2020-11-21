class Solution:
    def circularArrayLoop(self, nums):
        length = len(nums)
        if length <= 1: return False
        for i in range(length):
            print(i)
            #确定快慢指针的起点
            slow, fast = i, self.getNext(nums, i)
            #保证快慢指针方向一致
            while nums[i] * nums[slow] > 0  and nums[i] * nums[fast] >0 and nums[i] * nums[self.getNext(nums,fast)] > 0:
                a = (i,slow, fast)
                print(a)
                if slow == fast: #快慢指针相遇
                    if slow == self.getNext(nums, slow):
                        break
                    return True
                #慢指针向前移动 相当于slow=slow.next
                slow = self.getNext(nums, slow)
                #快指针向前移动 相当于fast=fast.next.next
                fast = self.getNext(nums, self.getNext(nums,fast))
        return False

    def getNext(self, nums, index):
        res = None
        next_idx = index + nums[index]
        if next_idx >= 0:
            res = next_idx % len(nums)
        else: #相当于倒数第next_idx个位置
            res = len(nums) - (abs(next_idx) % len(nums))
        return res

s = Solution()
s.circularArrayLoop([1,1,1,1,1,1,1,1,1,-5])