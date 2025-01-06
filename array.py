new_list = [13,"Jade",False,12.45,"Emily"]
result = new_list[2]
print(result)

# Search a list
if 'Emily' in new_list:
    print(True)
    # break
    
# Or use a for loop
for name in new_list:
    if name == "Emily":
        print('heyy girl,you decided to hide from me')
        break
    

# Insert a value or values in a list
girls = ["Nuulu", "Private Jet", "Yunia"]
new_list.append('Janny')
new_list.extend(girls)
new_list.insert(0, "Giraffe")
new_list[0] = "Hellen"
print(new_list)
