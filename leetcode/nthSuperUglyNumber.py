class Solution:
    def nthSuperUglyNumber1(self, n, primes):
        prime_length = len(primes)
        prime_target_indexs = [0] * prime_length

        dp = [0] * n
        dp[0] = 1
        i = 1
        while i < n:
            #找到最小值
            min_val = float("inf")
            for j, prime_val in enumerate(primes):
                val = primes[j] * dp[prime_target_indexs[j]]
                min_val = min(val, min_val)
            #放入数组
            dp[i] = min_val
            #更新prime_target_indexs,注意有相同公约数的情况都要向前 否则会造成重复
            #[3,5,7,11,19,23,29,41,43,47]
            for m,_ in  enumerate(primes):
                if primes[m] * dp[ prime_target_indexs[m] ] == min_val:
                    prime_target_indexs[m] += 1

            i += 1
        return dp[-1]

    
    def nthSuperUglyNumber(self, n, primes):
        prime_length = len(primes)
        L = [0 for i in range(len(primes))]
        result = [0 for i in range(n)]
        result[0] = 1
        for i in range(1, len(result)):
            min_u = min([result[L[j]]*primes[j] for j in range(len(L))])
            result[i] = min_u
            for k in range(len(L)):
                if result[L[k]]*primes[k] == min_u:
                    L[k] += 1
        return result[n-1]
    
s = Solution()
s.nthSuperUglyNumber1(15,[3,5,7,11,19,23,29,41,43,47])