class Solution:
    def trap(self, height: list[int]) -> int:
        n=len(height)
        
        left_max=[]
        right_max=[]
        water=0
        
        for i in range(n):
            left_max.append(0)
            right_max.append(0)

        left_max[0]=height[0]

        for i in range(1,n):
            left_max[i]=max(left_max[i-1],height[i])


        right_max[n-1]=height[n-1]

        for i in range(n-2,-1,-1):
            right_max[i]=max(height[i],right_max[i+1])

        for i in range(0,n):
            water+=min(left_max[i],right_max[i])-height[i]

        return water                   