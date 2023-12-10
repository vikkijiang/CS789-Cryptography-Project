from functions_new import*
first30 = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]

def RSA_encrypt(m,e,n):
    out = fast_exp(m,e,n)
    print("---------------------------------------------------")
    print("Encrypted message:", out)
    print("---------------------------------------------------")
def RSA_est():
    # the number of bits for p,q lower than 32
    n = 32

    p = find_random_prime(blum_blum_shub(n),n)
    q = find_random_prime(blum_blum_shub(n),n)
    while q == p:
        q = find_random_prime(blum_blum_shub(n),n)
    n_out = p*q

    e = find_random_prime(blum_blum_shub(n),n)%n_out
    phi = (p-1)*(q-1)
    one, inverse = exp_euclidean(phi,e)
    if inverse < 0:
        inverse += phi

    print("---------------------------------------------------")
    print("**KEEP SECRET**  private key (d) =", inverse)
    print("Post: n =",n_out, "public key (e) =", e)
    print("---------------------------------------------------")

def RSA_decrypt(x,d,n):
    out = fast_exp(x,d,n)

    print("---------------------------------------------------")
    print("Message from sender:", out)
    print("---------------------------------------------------")

def RSA_intercept(x,n,e):
    pq = pollards_rho(n)
    phi = (pq[0]-1)*(pq[1]-1)
    one, inverse = exp_euclidean(phi,e)
    if inverse < 0:
        inverse += phi
    out = fast_exp(x,inverse,n)

    print("---------------------------------------------------")
    print("Original message:", out)
    print("---------------------------------------------------")

def dh_est():
    n = 32
    p = find_random_prime(blum_blum_shub(n),n)
    b = 0
    for i in range (0,len(first30)):
        if primitive_root(first30[i],p):
            b = first30[i]
            break

    r = int(input("Pick a number as your secret (r) -> "))
    br = fast_exp(b,r,p)

    print("---------------------------------------------------")
    print("p =",p, "  b =", b, "  b_r =", br)
    print("---------------------------------------------------")

def dh_est_d(p,b):
    l = int(input("Pick a number as your secret (l) -> "))
    bl = fast_exp(b,l,p)

    print("---------------------------------------------------")
    print("b_l =", bl)
    print("---------------------------------------------------")

def dh_encrypt(p,r,bl,msg):
    shared_secret = fast_exp(bl,r,p)
    msg_e = (msg*shared_secret)%p

    print("---------------------------------------------------")
    # print(shared_secret)
    print("Encrypted message = ", msg_e)
    print("---------------------------------------------------")

def dh_decrypt(p,bl,msg_e):
    r = int(input("What was your secret number (l) -> "))
    shared_secret = fast_exp(bl,r,p)
    inverse = fast_exp(shared_secret,p-2,p)
    msg = (msg_e*inverse)%p

    print("---------------------------------------------------")
    print("The original message is: ", msg)
    print("---------------------------------------------------")

def dh_intercept(p,b,br,bl,msg_e):
    r = babygiant(br,b,p)
    l = babygiant(bl,b,p)
    shared_secret = fast_exp(bl,r,p)
    inverse = fast_exp(shared_secret,p-2,p)
    msg = (msg_e*inverse)%p

    print("---------------------------------------------------")
    print("The original message is: ", msg)
    print("---------------------------------------------------")

def error():
    print("Invalid Selection, please select again")

def ui():
    while True:
        select = input("Select encryption method: [D] Diffie Hellman [R] RSA or select [Q] anytime to quit -> ")
        if select== "Q":
            break
        elif select =="R":
            sr = input("Select the following: [e] Encrypt [d] Decrypt [i] Intercept -> ")
            if sr== "Q":
                break
            elif sr == "e":
                me = int(input("Enter your message -> "))
                ee = int(input("Enter public key (e) -> "))
                ne = int(input("Enter n -> "))
                RSA_encrypt(me,ee,ne)
            elif sr == "d":
                dyn = input("Have you posted n and e? [y] Yes [n] No -> ")
                if dyn== "Q":
                    break
                elif dyn == "y":
                    xd = int(input("Enter the encrypted message -> "))
                    dd = int(input("Enter private key (d) -> "))
                    nd = int(input("Enter n -> "))
                    RSA_decrypt(xd,dd,nd)
                elif dyn == "n":
                    RSA_est()
                else:
                    error()
                    continue
            elif sr == "i":
                xi = int(input("Enter the encrypted message -> "))
                ni = int(input("Enter n -> "))
                ei = int(input("Enter the public key (e) -> "))
                RSA_intercept(xi,ni,ei)

            else:
                    error()
                    continue
        elif select == "D" :
            ed = input("Select the following: [e] Encrypt [d] Decrypt [i] Intercept -> ")
            if ed == "Q":
                break
            elif ed == "e":
                est = input("Have you posted p and b? [y] Yes [n] No -> ")
                if est== "Q":
                    break
                elif est == "n":
                    dh_est()
                elif est == "y":
                    pe = int(input("Enter p -> "))
                    r = int(input("Enter r (your secret number) -> "))
                    bl = int(input("Enter b_l (other person) -> "))
                    msg = int(input("Enter your message -> "))
                    while True:
                        if msg > pe:
                            msg = input("Message cannot be greater than p, enter again-> ")
                        else:
                            break
                    dh_encrypt(pe,r,bl, msg)
                else:
                    error()
                    continue 
            elif ed == "d":
                est_d = input("Have you established your key? [y] Yes [n] No -> ")
                if est_d== "Q":
                    break
                elif est_d == "n":
                    pn = int(input("Enter p -> "))
                    bn = int(input("Enter b -> "))
                    dh_est_d(pn,bn)
                elif est_d == "y":
                    pd = int(input("Enter p -> "))
                    bl = int(input("Enter b_r (other person) -> "))
                    msg_e = int(input("Enter the encrypted message -> "))
                    dh_decrypt(pd,bl,msg_e)
                else:
                    error()
                    continue 
            elif ed == "i":
                pi = int(input("Enter p -> "))
                bi = int(input("Enter b -> "))
                br_i = int(input("Enter b_r -> "))
                bl_i = int(input("Enter b_l -> "))
                msg_i = int(input("Enter the encrypted message -> "))
                dh_intercept(pi,bi,br_i,bl_i,msg_i)

            else:
                error()
                continue           

                      

        else:
            error()
            continue

ui()