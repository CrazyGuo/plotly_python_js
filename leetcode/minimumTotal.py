class Solution:
    tri = None
    length = 0
    def minimumTotal(self, triangle):
        self.tri = triangle
        self.length = len(self.tri)
        return self.dps()

    def dps(self):
        dp = {}
        for i in range(self.length-1)[-1::-1]:
            for j in range(i+1):
                if i == self.length - 2:
                    dp[(i,j)] = min(self.tri[i+1][j], self.tri[i+1][j+1]) + self.tri[i][j]
                else:
                    dp[(i,j)] = min(dp[(i+1, j)], dp[(i+1, j+1)]) + self.tri[i][j]
        return dp[(0,0)]

test_data = [
     [2],
    [3,4],
   [6,5,7],
  [4,1,8,3]
]

so = Solution()
so.minimumTotal(test_data)