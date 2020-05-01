#работает за О(n), занимает O(1) памяти.



fib1 = fib2 = 1
 
n = int(input("Номер элемента ряда Фибоначчи: ")) - 2
 
while n > 0:
    fib1, fib2 = fib2, fib1 + fib2
    n -= 1
 
print(fib2)
