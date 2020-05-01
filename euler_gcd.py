# Recurtion way
def gcd_rec(m,n):
    if m< n: 
        (m,n) = (n,m)
    if(m%n) == 0:
        return n 
    else:
        return (gcd_rec(n, m % n)) # recursion taking place

# calling function with parameters and printing it out        
print(gcd_rec(8,12))

# Iteration way
def gcd_while(m,n):
    if m< n: 
        (m,n) = (n,m)
    while (m % n != 0):
        (m, n) = (n, m % n)
    return n

# calling function with parameters and printing it out        
print(gcd_while(8,12))

