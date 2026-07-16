class Solution:
    def lengthOfLastWord(self, s: str) -> int:
        i=len(s)-1

        while i>=0 and s[i]==" ":
            i=i-1

        #Count the character of the last word
        length=0
        while i>=0 and s[i]!=" ":
            length=length+1
            i=i-1
        return length        
