from math import sqrt,ceil,floor,log
from random import randint
# Euclidian Algorithm
def euclidean (m,n):
    if m-n > 0:
        n0  = n
        m0 = m
    else:
        n0 = m
        m0 = n

    #search for multiple
    x = 1
    mod = 2
    while n0 > 1:
        tmp = m0 #temporary variable that stores the biggest number 
        while x*n0 < m0:
            mod = m0-(x*n0)
            x+=1

        #update m0 and n0
        m0 = n0
        n0 = mod

        print(tmp," = ",x-1,"*",m0,"+",n0)

        if x-1 == 0:
            break

        x = 1
    

# Expanded Euclidean Algorithm
def exp_euclidean(m, n):
    # Base Case
    if m == 0:
        return 0, 1
    
    # x and y is some formula with x1 and/or y1
    x1, y1 = exp_euclidean(n % m, m)
 
    x = y1 - (n//m) * x1
    y = x1
 
    # print("m = ",m," x = ",x, " n = ", n," y = ",y)
    return x, y
 

# Fast Exponentation Algorithm
def fast_exp(x,e,m):
    Y = 1
    # print("{:<30} {:<30} {:<30}".format('x:','e:','Y:'))
    # print("{:<30} {:<30} {:<30}".format(x,e, Y))

    while e>0:
        if e%2 == 0:
            x = (x**2)%m
            e = e//2
        else:
            e = e-1
            Y = (x*Y)%m

        # print("{:<30} {:<30} {:<30} ".format(x,e, Y))

    return Y


def gcd(m, n):
 
    if (m == 0):
        return n
    return gcd(n % m, m)

def primitive_root(b,p):
    # find all prime divisors (q) of p-1
    ref = pollards_rho(p-1)
    # print("p-1 divisors:",ref)

    for i in range (0, len(ref)):
        # k = p-1/q
        k = (p-1)/ref[i]
        # print("q = ",ref[i], "p-1/q = ", k)
        if fast_exp(b,k,p) == 1:
            # print(b,"^",k,"mod",p," = 1, try another b")
            return False

        
    return True

def babygiant(a,b,p):
    # find log(base b)a in mod p
    m = ceil(sqrt(p-1))
    # print("a =",a," b =",b, " m(ceiling of Sqrt(p)) = ",m)

    # BABY STEP
    elements = {}
    for j in range (0,m):
        # compute b^j%p
        elements[fast_exp(b,j,p)]=j
    # print(elements)
    
    # compute b inverse for c = (b^-1)^m
    b_inv = fast_exp(b,p-2,p)
    # print("b inverse =",b_inv)
    # use fast exponential compute c because b_inv^len(elements)%p = c
    c = fast_exp(b_inv,m,p)
    # print("c =", c)

    # compute a*c^i for some i will have the same value as b^j
    # GIANT STEP
    # elements1 = {}
    answers = []
    for i in range (0,m):
        findmatch = (a*fast_exp(c,i,p))%p
        # print(fast_exp(a,1,p),"*",fast_exp(c,i,p),"=",findmatch)
        # elements1[findmatch]=i
        if findmatch in elements:
            l = (i*m+elements[findmatch])%(p-1)
            answers.append(l)
            # print("l=",i,"*",m,"+",elements[findmatch],"=",l)

    # print(answers)

    answers.sort()

    return answers[0]

def miller_rabin(n):
    if n==1 or n==2:
        return True
    elif n%2 == 0:
        return False
    
    # find m
    m = n-1
    r = 0
    while m%2 == 0:
        m = m//2
        r += 1
    # print("m = ",m,"r = ",r)


    k = 10
    while k > 0:
        go_up = False
        # print("k = ", k)
        b0 = randint(2,n-1)
        # print("base = ", b0)
        b0 = fast_exp(b0,m,n)
        # print("b0 = ",b0)
        if b0%n == 1 or b0%n == n-1:
            # print(b0," mod ",n, " = ", b0%n, " -> maybe prime, next round")
            k -= 1
            continue
        else:
            for s in range (0,r):
                bs = fast_exp(b0,2,n)
                # print("bs = ", bs)
                if bs%n == n-1:
                    # print("Maybe prime, break")
                    go_up = True
                    break
                elif bs%n != n-1:
                    # print(bs," mod ",n, " = ", bs%n)
                    b0 = bs
            
            if go_up == True:
                k-=1
                continue

            # print("all bs not congruent to -1, composite")
            return False
    
    # print(n,"is probably prime")
    return True


def find_random_prime (pq,n):
    if miller_rabin(pq):
        return pq
    return find_random_prime(blum_blum_shub(n),n)

def blum_blum_shub(len):
    bit = 6
    p = find_3mod4(randint(2**(bit-1)+1, 2**bit-1),bit)
    q = find_3mod4(randint(2**(bit-1)+1, 2**bit-1),bit)
    while q == p:
        q = find_3mod4(randint(2**(bit-1)+1, 2**bit-1),bit)

    n = p*q
    # print("p =",p, ",q =",q, ",n =",n)

    s0 = randint(1,n)
    while True:
        if s0 % p != 0 and s0 % q != 0:
            break
        else:
            s0 = randint(1,n)
    s = [(s0**2)%n]
    for i in range (0,n-1):
        s.append((s[i]**2)%n)
    
    b = ""
    for j in range (0,n):
        b += str(s[j]%2)
    b = binary_decimal(int(b[:len]))
    # bf = int(b[:len])

    return b

def find_3mod4 (pq,n):
    if miller_rabin(pq) and pq%4 == 3:
        return pq
    return find_3mod4(randint(2**(n-1)+1, 2**n-1),n)

def binary_decimal(n):
    decimal = 0
    power = 1
    while n>0:
        rem = n%10
        n = n//10
        decimal += rem*power
        power = power*2
        
    return decimal

def pollards_rho(n):
    out = []
    x = 2
    y = (x**2)+1
    ct = 0
    while True:
        g = gcd(abs(x-y),n)
        if n%2 == 0:
            if 2 not in out:
                out.append(2)
            n = n//2
            x = 2
            y = (x**2)+1
        elif 1<g<n:
            if g not in out and miller_rabin(g):
                out.append(g)
            n = n//g
            x = 2
            y = (x**2)+1
        elif g == 1:
            x = ((x**2)+1)%n
            y = ((((y**2)+1)**2)+1)%n
        elif g == n:
            if miller_rabin(n):
                out.append(n)
                break
            else:
                x = 2+ct
                y = (x**2)+1
                ct += 1
        
    return out
