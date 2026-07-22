class Solution:
    def myAtoi(self, s: str) -> int:
        s=s.strip()
        if not s:
            return 0
        i=0    
        sign=1
        num=0
        n=len(s)

        if s[i]=='-' or s[i]=='+':
            if s[i]=='-':
                sign=-1
            i=i+1

        while i<n and s[i].isdigit():
            digit=int(s[i])

            #Check overflow before adding the digit
            if num>(2**31-1 -digit)//10:
                if sign==1:
                    return 2**31-1
                else:
                    return -2**31
            num=num*10+digit
            i=i+1
        return sign*num                         
        