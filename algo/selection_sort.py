# Sorting function 
def selection_sort(l):
   
    for start in range(len(l)):        
        min_pos = start

        for i in range(start, len(l)):
            if l[i] < l[min_pos]:
                min_pos = i
        # swap values
        (l[start], l[min_pos]) = (l[min_pos], l[start])
        
# Test input  
l = [54, 26, 93, 17, 77, 31, 44, 55, 20]
selection_sort(l)
print(l)

