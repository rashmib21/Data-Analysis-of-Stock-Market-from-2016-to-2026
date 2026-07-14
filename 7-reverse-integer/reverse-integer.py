class Solution:
    def reverse(self, x: int) -> int:
        y=str(x)
        z=y[::-1]
        check=""

        if z[-1]=='-':
            check=check+z[-1]
            z=z[:len(y)-1]
            check=check+z

        else:
            check=check+z

        result=int(check)
        if result <-2**31 or result >2**31-1:
            check=0

        return int(check)        