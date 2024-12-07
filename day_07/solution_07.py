lines = open('input.txt').read().strip().split('\n')

def valid(value, nums):
    if len(nums) == 1:
        return nums[0]==value
    return (valid(value, [nums[0] + nums[1]] + nums[2:])
        or valid(value, [nums[0] * nums[1]] + nums[2:]))

def valid2(value, nums):
    if len(nums) == 1:
        return nums[0] == value
    return (valid2(value, [nums[0] + nums[1]] + nums[2:])
        or valid2(value, [nums[0] * nums[1]] + nums[2:])
        or valid2(value, [int(str(nums[0]) + str(nums[1]))] + nums[2:])
        )


x = 0
for line in lines:
    value, nums = line.split(':')
    value = int(value)
    nums = [int(x) for x in nums.split()]
    if valid(value, nums):
        x += value

print(x)

x = 0
for line in lines:
    value, nums = line.split(':')
    value = int(value)
    nums = [int(x) for x in nums.split()]
    if valid2(value, nums):
        x += value

print(x)
