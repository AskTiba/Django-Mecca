def linear_search(list,target):
    # Returns the index position of the target if found,else returns None
    for i in range(0,len(list)): 
        # i being the index
        if list[i] == target:
            return i

    return None


def verify(index):
    if index is not None:
        # print (`Target found at index: ${index}`)
        print('Target found at index:', index)
    else:
        print ('Target not found in list')
        

nums=[1,2,3,4,5,6,7,8,9,10]

result = linear_search(nums,7)
verify(result)