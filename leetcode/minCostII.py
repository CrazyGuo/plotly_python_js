class Solution:
    def minCostII(self, costs):
        #房子数量
        cols = len(costs)
        if cols == 0 : return 0
        if cols == 1: return min(costs[0])
        ##优化地方1： 记录某列最小值 与 次最小值
        min1, min2 = float("inf"), float("inf")
        #颜色数量
        rows = len(costs[0])
        #定义dp: rows行 * cols列
        dp = [ [ 0 for _ in range(cols)] for _ in range(rows) ]
        #初始化第一列
        for r in range(rows):
            dp[r][0] = costs[0][r]
            #优化地方2
            if dp[r][0] < min1:
                min2 = min1
                min1 = dp[r][0]
            elif dp[r][0] >= min1 and dp[r][0] < min2:
                min2 = dp[r][0]
        print(min1,min2)
        #递推公式
        result = float("inf")
        for j in range(1, cols):
            #优化地方2
            temp_min1, temp_min2 = float("inf"), float("inf")
            for i in range(0,rows):
                min_val = float("inf")
                #优化地方4
                if dp[i][j-1] != min1:
                    min_val = min1
                else:
                    min_val = min2
                dp[i][j] = costs[j][i] + min_val
                #优化地方5
                if dp[i][j] < temp_min1:
                    temp_min2 = temp_min1
                    temp_min1 = dp[i][j]
                elif dp[i][j] >= temp_min1 and dp[i][j] < temp_min2:
                    temp_min2 = dp[i][j]
                
                #最后一列中 保存了最小值
                if j == cols-1:
                    result = min(result, dp[i][j])
            print(temp_min1,temp_min2)
            min1, min2 = temp_min1, temp_min2
        print(dp)
        return result
s = Solution()
l = [[3,20,7,7,16,8,7,12,11,19,1],[10,14,3,3,9,13,4,12,14,13,1],[10,1,14,11,1,16,2,7,16,7,19],[13,20,17,15,3,13,8,10,7,8,9],[4,14,18,15,11,9,19,3,15,12,15],[14,12,16,19,2,12,13,3,11,10,9],[18,12,10,16,19,9,18,4,14,2,4]]
res = s.minCostII(l)    
print(res)