"""
Merge function for 2048 game.
"""

def merge(line):
    """
    Function that merges a single row or column in 2048.
    """
    new_list = []
    result_list = []
    
    for elem in range(len(line)):
        
        if line[elem] != 0:
            
            new_list.append(line[elem])
    
    if len(new_list) < len(line):
        
        for elem in range(len(line) - len(new_list)):
            
            new_list.append(0)
    
    count = 0
    
    while count < len(new_list):
        
        if new_list[count] != 0:

            if count == (len(new_list) - 1):
                
                result_list.append(new_list[count])
                
                count += 1
            
            elif new_list[count] == new_list[count + 1]:
            
                new_element = new_list[count] + new_list[count + 1]
                
                result_list.append(new_element)
                
                count += 2
                
            else:
                
                new_element = new_list[count]
                
                result_list.append(new_element)
                
                count += 1
                
        else:
            
            count += 1

    if len(result_list) < len(line):
        
        for elem in range(len(line) - len(result_list)):
            
            result_list.append(0)

    return result_list