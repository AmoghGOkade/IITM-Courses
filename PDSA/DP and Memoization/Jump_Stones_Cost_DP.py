#very easy

'''There are N stones, numbered 0, 1, 2, …, N-1. For each i (0 ≤ i ≤ N-1), the height of stone 'i' is hi.

If a frog is currently on Stone i, he can jump to Stone i+1 or Stone i+2. Here, a cost of |hi - hj| is incurred, where j is the stone to land on.

The frog is initially on Stone 0. Find the minimum possible total cost to reach at last stone.

Write a function minCost(H), where H is a list of heights for N stones. The function returns the minimum possible total cost to reach at last stone.

Sample Input = [10, 30, 40, 20]
Output = 30
Explanation:- If we follow the path 0 → 1 → 3, the total cost incurred would be
∣10−30∣+∣30−20∣=30.
'''

def minCost(H):
    n = len(H)
    dp = []
    for i in range(n):
        dp.append(0)
    
    #base cases
    dp[0] = 0   #we start on the 1st stone, so no cost
    dp[1] = abs(H[1] - H[0])    #can only get to the 2nd stone from the 1st stone
    
    for i in range(2, n):
        c1 = dp[i-2] + abs(H[i] - H[i-2])
        c2 = dp[i-1] + abs(H[i] - H[i-1])
        dp[i] = min(c1, c2)
    
    return dp[n-1]
    
H = eval(input())
print(minCost(H))
