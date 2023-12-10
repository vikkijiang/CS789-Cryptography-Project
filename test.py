import pytest
from functions_new import *

@pytest.mark.parametrize("m,n,x,y", [(614,513,-193,231),
                                    (556265469809196112, 951351593, 262322527, -153382792226207511),
                                    (380326201357833120, 347229989, 95254631, -104333822301195571),
                                    (571152, 677, -284, 239597),
                                    (11872,3,1,-3957) ])
def test_expanded_euclid(m,n,x,y):
    assert exp_euclidean(m,n) == (x,y)

@pytest.mark.parametrize("x,e,m,r", [(3981,3,12091,12039),
                                    (234,1732803997, 583036978241036573,161895904251733444),
                                    (161895904251733444, 344302545430182373, 583036978241036573, 234),
                                    (9812,7915,12091,142),
                                    (127086110514210358,163035183806575847,172154898922723459,384)])
def test_fast_exp(x,e,m,r):
    assert fast_exp(x,e,m) == r

@pytest.mark.parametrize("m,n,g", [(2423393857,15,1),
                                    (4043235727, 4061260703, 1),
                                    (120, 135, 15),
                                    (1913616227,1787128521,1)])
def test_gcd(m,n,g):
    assert gcd(m,n) == g


@pytest.mark.parametrize("b,p", [(2,1913616227),
                                 (11, 839),
                                 (3,15649041275014254103),
                                 (7,50374586549039)])
def test_primitive_root(b,p):
    assert primitive_root(b,p)
    assert not primitive_root(2,9511)

@pytest.mark.parametrize("a,b,p,e", [(634617746,2,2726153531,45),
                                     (35292112,2,2726153531,279),
                                     (1673869378,7,2423393857,25),
                                     (1257251040,7,2423393857,590)])
def test_babygiant(a,b,p,e):
    assert babygiant(a,b,p) == e

def test_miller_rabin():

    assert not miller_rabin(15)
    assert miller_rabin(53)
    assert miller_rabin(19441)
    assert miller_rabin(2)
    assert miller_rabin(3)
    assert not miller_rabin(4)

@pytest.mark.parametrize("n,l", [(9510,[2,3,5,317]),
                                 (102,[2, 3, 17]),
                                 (16420634371030736081,[4043235727,4061260703]),
                                 (583036978241036573,[136945987, 4257422879])])
def test_pollards_rho(n,l):
    assert pollards_rho(n) == l
