def collatz(n)
    if n == 1:
        return 1
    if n % 2 == 0:
        return collatz(n // 2)
    else:
        return collatz(3 * n + 1)