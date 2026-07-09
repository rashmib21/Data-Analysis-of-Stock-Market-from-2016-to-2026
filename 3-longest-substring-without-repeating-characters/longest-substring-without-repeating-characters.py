# class Solution:
#     def lengthOfLongestSubstring(self, s: str) -> int:
#         max_length=0
#         for i in range(len(s)):
#             for j in range(i+1,len(s)+1):
#                 if s[i]==s[i+1]:
#                     continue
#                 else:    

# class Solution:
#     def lengthOfLongestSubstring(self, s: str) -> int:
#         max_length = 0
        
#         for i in range(len(s)):
#             for j in range(i + 1, len(s) + 1):
#                 substring = s[i:j]
#                 if len(substring) == len(set(substring)):  
#                     max_length = max(max_length, len(substring))
        
#         return max_length


class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        last_seen = {}
        left = 0
        max_length = 0

        for right, ch in enumerate(s):
            if ch in last_seen and last_seen[ch] >= left:
                left = last_seen[ch] + 1

            last_seen[ch] = right
            max_length = max(max_length, right - left + 1)

        return max_length