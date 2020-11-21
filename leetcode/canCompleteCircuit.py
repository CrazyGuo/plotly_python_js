
class Solution:
    def canCompleteCircuit(self, gas, cost):
        length = len(gas)
        
        for i in range(length):
            start = i
            remain = 0
            while True:
                index = start % length
                if start > i and index == i:
                        return i
                x = gas[index]
                y = cost[index]
                remain += x
                if remain >= y:
                    remain -= y
                    start += 1
                else:
                    break
        return -1
s = Solution()
a = s.canCompleteCircuit([1,2,3,4,5],[3,4,5,1,2])
print(a)




