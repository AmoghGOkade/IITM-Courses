#hard level

'''You are given weights and values of N items. Put these items in a knapsack of capacity w to get the maximum total value in the knapsack.
You can either pick an item or not pick it, you are not allowed to break an item.

Sample input:-
3 #n
4 #w
[4, 5, 1] #weight
[1, 20, 3] #value

Output:- 3'''

def knapSack(W, weight, values, n):
    dp = []
    for i in range(n+1):
        dp.append([0]*(W+1))
    
    #base case
    for w in range(W+1):
        dp[0][w] = 0    #if no item is available, max value is 0 irrespective of allowed weight

    for i in range(1, n+1):     #dp[i] is if only i elements are available
        for w in range(1, W+1):
            if weight[i-1]>w:
                dp[i][w] = dp[i-1][w]   #if you can't include for the given w, dp will be same as the previous one's
            else:
                val1 = dp[i-1][w]       #exclude the item, same as the previous one's for the same weight w
                val2 = dp[i-1][w-weight[i-1]]+values[i-1]   #include the item, (maximum value you can get with i-1 items and (w - weight of item)) + value of item
                dp[i][w] = max(val1, val2)
                
    return dp[n][W]
