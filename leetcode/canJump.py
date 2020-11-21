
class Solution:
    
    def canJump(self, nums):   
        self.length = len(nums)
        if self.length <=0: return True
        self.nums = nums
        return self.dfs(0)
          
    def dfs(self, index):
        val = self.nums[index] 
        if index + val >= self.length - 1: return True
        max_val = -1
        idx = 0
        for step, val_n in enumerate( self.nums[index+1:index+val+1]):
            if val_n >= max_val and step + val_n >= val:
                max_val = val_n
                idx = step
        if max_val != -1:
            return self.dfs(index + idx + 1)
        else:
            return False
s = Solution()
a = s.canJump([1,1,2,2,0,1,1])
print(a)




