
def my_sum(nums, target):
    my_nums = {}
    if 2 <= len(nums) <= 104:
        if -109 <= target <= 109:
            for i, num in enumerate(nums):
                chazhi = target - num
                if chazhi in my_nums:
                    return [my_nums[chazhi], i]
                my_nums[num] = i
            return []


print(my_sum((1, 103, 2, 109, 101), 103))