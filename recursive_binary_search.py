def recursive_binary_search(list, target):
    if len(list) == 0:
        return print(f"The list is empty")
    else:
        midpoint = (len(list)) // 2
        if list[midpoint] == target:
            return True
        else:
            if list[midpoint] < target:
                return recursive_binary_search(list[midpoint + 1 :], target)
            else:
                if list[midpoint] > target:
                    return recursive_binary_search(list[:midpoint], target)


def verify(result):
    print(f"Target found: {result}")


nums = [1, 2, 3, 4, 5, 6, 7, 8]
result = recursive_binary_search(nums, 12)
verify(result)
result = recursive_binary_search(nums, 3)
verify(result)

# Recursive Depth is the no. of times a function calls itself, recursive algorithms
# Tail optimization
# Algorithmic thinking
