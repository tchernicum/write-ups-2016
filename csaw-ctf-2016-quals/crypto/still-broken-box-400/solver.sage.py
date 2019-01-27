# This file was *autogenerated* from the file solver.sage
from sage.all_cmdline import *   # import sage library
_sage_const_3 = Integer(3); _sage_const_2 = Integer(2); _sage_const_1 = Integer(1); _sage_const_0 = Integer(0); _sage_const_0x10001 = Integer(0x10001);  _sage_const_1025 = Integer(1025); _sage_const_97 = Integer(97); _sage_const_300 = Integer(300)
from sparrowCTF import *
from z3 import *

def pos(g, orig_s, err_s, N):
    r = list(range(_sage_const_1025 ))
    for x in r:
        if (err_s * pow(g, _sage_const_2 **x, N)) % N == orig_s:
            r.remove(x)
            return x, _sage_const_1 
        elif (orig_s * pow(g, _sage_const_2 **x, N)) % N == err_s:
            r.remove(x)
            return x, _sage_const_0 

def rotate(req):
    req.recv_until(":")
    req.sendline("yes")
    req.recv_until(":")

def NnS():
    r = Remote("192.241.234.35", 31337 , debug=False)
    r.sendline("3")
    #get N
    N = r.recvline()[:-_sage_const_1 ].split(':')[-_sage_const_1 ]
    rotate(r)
    r.sendline("3")
    #get orig_s
    ss = list()
    while len(ss) == len(set(ss)):
        rotate(r)
        r.sendline("3")
        orig_s = r.recvline().split(',')[_sage_const_0 ].split(':')[-_sage_const_1 ]
        ss.append(orig_s)

    return int(N), int(orig_s)

def solve():
    N, orig_s = NnS()
    e = _sage_const_0x10001 
    g = _sage_const_3 
    r = Remote("192.241.234.35", 31337 , debug=False)
    res = _sage_const_0 
    bits = _sage_const_300 
    while bits > _sage_const_0 :
        r.sendline("3")
        sig = int(r.recvline().split(',')[_sage_const_0 ].split(':')[-_sage_const_1 ])
        rotate(r)

        if sig == orig_s:
            continue
        p, b = pos(g, orig_s, sig, N)
        res += (_sage_const_2 **p) * b
        bits -= _sage_const_1 
        print "[+] {0} bits left to map...\n[+] current d:{1}".format(bits, res)

    return res, N

def recover(partial_d, N, e):
    # ed' = 1 + k(N - s + 1) mod n'
    # (k*(qq**2) + (e*d - k*(N+1) - 1)*qq + k*N) % 2**300 == 0
    dd = partial_d
    k = _sage_const_0 

    while k < e:
        print "[+]Testing %d" % k
        print solve_mod([(k*(x**_sage_const_2 ) + (e*dd - k*(N+_sage_const_1 ) - _sage_const_1 )*x + k*N) == _sage_const_0 ], _sage_const_2 **_sage_const_300 )
        k += _sage_const_1 

    #when k == 57 got the correct p' which can to be used to factor N by coppersmith.
    #too lazy to implement it here :P
    
def main():
    res, N = solve()
    e = _sage_const_97 
    recover(res, N, e)

if __name__ == "__main__":
    main()