#medium level

'''Given a rod of length n and a list of prices that contains prices of all pieces of size smaller than or equal to n.

Determine the maximum value obtainable by cutting up the rod and selling the pieces.

Write a function cutRod(n, price) that returns the maximum value obtainable by cutting up the rod and selling the pieces.

Sample input:
8 #n
[1, 5, 8, 9, 10, 17, 17, 20] #price
Output:
22 #maximum value
Explanation:
The maximum value obtainable is 22 by cutting in two pieces of length 2 and 6, i.e., 5+17=22'''

def cutRod(n, price):
    dp=[]
    for i in range(n+1):
        dp.append(0)
    
    #base cases
    dp[0] = 0   #price of no rod is 0
    dp[1] = price[0]    #price of len 1 is the 1st index
    
    for i in range(2, n+1):
        l=[]
        for j in range(0, i):
            l.append(dp[j]+price[i-j-1])    #len n + dp(0 len), len n-1 + dp(1 len), len n-2 + dp(2 len), ...
        dp[i] = max(l)
    return dp[n]
    
N = int(input())
price= eval(input())
print(cutRod(N,price))
