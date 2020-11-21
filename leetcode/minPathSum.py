
class Solution:
    def minPathSum(self, grid):
        rows = len(grid)
        if rows == 0: return 0
        cols = len(grid[0])
        dp = [[0] * cols] * rows
        dp[0][0] = grid[0][0]
        for idx in range(1, cols):
            dp[0][idx] = dp[0][idx-1] + grid[0][idx]
        print(dp[0])
        for idx2 in range(1, rows):
            temp_val = dp[idx2-1][0]
            gval = grid[idx2][0]
            dp[idx2][0] = temp_val + gval
        print(dp)
        for i in range(1,rows):
            for j in range(1,cols):
                    dp[i][j] = min(dp[i][j-1], dp[i-1][j]) + grid[i][j]
        print(dp)
        return dp[rows-1][cols-1]
s = Solution()
a = s.minPathSum(
[[7,4,8,7,9,3,7,5,0],[1,8,2,2,7,1,4,5,7],[4,6,4,7,7,4,8,2,1],[1,9,6,9,8,2,9,7,2],[5,5,7,5,8,7,9,1,4],[0,7,9,9,1,5,3,9,4]])
print(a)