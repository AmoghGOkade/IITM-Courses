#medium level

'''A subsequence is a sequence that can be derived from another sequence by deleting some elements without changing the order of the remaining elements.

Write a function countSebseq(S) that accepts a string S which only contains digit characters. The function returns the number of non-empty subsequences that can be obtained from S such
that every digit in the subsequence is strictly greater than all previous digits (if exist).

Example:-
If S = '7598' then there are 8 subsequences which follow the above constraint. These are '7', '5', '9', '8', '79', '78', '59', '58'. Notice that '7598' is not a valid required subsequence
because 7 > 5 and 9 > 8.'''

def countSubseq(S):
    n = len(S)
    dp=[]
    for i in range(n):
        dp.append(0)
    
    #base case
    dp[0] = 1   #S[0] is a valid subsequence
    ans = 1     #because of dp[0]
    
    for i in range(1, n):
        dp[i] = 1   #because the letter is itself a valid subsequence
        for j in range(0,i):
            if S[j] < S[i]:
                dp[i] += dp[j]
                
        ans += dp[i]
    #print(dp)
    return ans
        
S = input()
print(countSubseq(S))
