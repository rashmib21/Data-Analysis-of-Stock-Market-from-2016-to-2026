class Solution:
    def searchRange(self, nums: List[int], target: int) -> List[int]:
        result=[-1,-1]

        for i in range(len(nums)):
            if nums[i]==target:
                if result[0]==-1:
                    result[0]=i
                result[1]=i
        return result        