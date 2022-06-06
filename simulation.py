from re import A
import numpy as np
from scipy.stats import poisson, uniform

### parameters
total_time = 3*(10**4) # time slot
W = 10*(10**6) # system bandwidth
f =2.35*(10**9) # center frequency
v = 100 # moving speed (m/s)
L = 500 # packet length (bits)
R = 1.5 # cell radius (km)
Ts = 1*10**(-3) # slot duration (ms)
d0 = 50 # distance between BS and rail (m)
K = 4 # number of service
N0 = 10**(-17.4) * 10**-3 # noise power spectral density (dB m/Hz)

### arrive packets number is a truncated poisson distribution with Amax and lambda(mu)
def truncated_Poisson(mu, max_value, sample_size):
    cutoff = poisson.cdf(max_value, mu)
    # generate uniform distribution [0,cutoff):
    u = uniform.rvs(scale=cutoff, size= sample_size)
    # convert to Poisson:
    truncated_poisson = poisson.ppf(u, mu)
    return truncated_poisson

### initial state information
class sysQueue():
    def __init__(self, K):
        self.Q = np.zeros(K) # real queue, number of packets at slot t in the buffer k. Denote Qk(t)
        self.D = np.zeros(K) # virtual queue
    def getQ(self):
        return self.Q
    def getD(self):
        return self.D
    def update_D(self, Dkt, rk, qk, lambdak, K):
        for k in range(K):
            self.D[k] = max(Dkt[k]-rk[k], 0) + qk[k]*lambdak[k]
        return self.D
    def update_Q(self, Qkt, mukt, rkt, K):
        for k in range(K):
            self.Q[k] = Qkt[k] - mukt[k] + rkt[k]
        return self.Q
    def setQ(self, K):
        self.Q = np.zeros(K)
        return self.Q
    def setD(self, K):
        self.D = np.zeros(K)
        return self.D

## fully distributed admission control scheme
def calRk(Qk, Dk, Ak, K):
    rk = np.zeros(K)
    for k in range(K):
        if Qk[k] > Dk[k]:
            rk[k] = 0 
        else:
            rk[k] = Ak[k]
    return rk

def calRk_heu(qk, Ak, K):
    rk = np.zeros(K)
    for k in range(K):
        if np.random.rand() < qk:
            rk[k] = Ak[k]
    return rk

def calM(C, Q, N, K, V, eta):
    g1 = 0
    re = C 
    if re == 0: # M(0) = 0 
        return 0 
    for i in range(K):
        if re > Q[i]:
            g1 += Q[i] * Q[i]
            re -= Q[i]
        else:
            g1 += Q[i] * re
            re = 0
    g2 = N*K*V*(2**(eta*C) - 1)
    # print("g2: ", g2)
    return g1 - g2


## cooperative distributed resource allocation scheme
def calmuP(Q, N, K, V, eta):
    mu = np.zeros(K)
    C = 0
    tQ = Q
    indices = np.argsort(Q)[::-1]
    tQ[::-1].sort() ## sort by descending order
    for idx in indices: #### not considering Q order  range(Q.size)
        for i in range(int(Q[idx])):
            mu[idx] +=1
            if calM(C+1, tQ, N, K, V, eta) < calM(C, tQ, N, K, V, eta):
                mu[idx] -=1
                break
            C +=1
    P = N*(2**(eta*C) - 1)
    return mu, P, C

def calmuP_heu(Q, N, K, eta):
    mu = np.zeros(K)
    C = 0
    for k in range(K):
        C += Q[k]
        mu[k] = Q[k]
    P = N*(2**(eta*C) - 1)
    return mu, P, C

ddrm = sysQueue(K)
eta = L/(Ts*W) # eta
# lambdak = [100, 80, 60, 40]
# qk = [0.95, 0.90, 0.85, 0.80]
# Ak = None
# ### for four service, Ak with respect to kth service packet arrival distribution
# max_value = 200
# for i in range(K):
#     if Ak is None:
#         Ak = truncated_Poisson(lambdak[i], max_value, total_time)
#     else:
#         Ak = np.vstack((Ak, truncated_Poisson(lambdak[i], max_value, total_time)))

# # experiment (3)
# n_q = np.array([0])
# c_q = np.array([0])
# b_q = np.array([0])
# p_q = np.array([0])

# Q = ddrm.setQ(K)
# D = ddrm.setD(K)
# V = 100
# for t in range(total_time): 
#     d = 0.1 * t
#     if d > 1500:
#         d = 3000 - d
#     h = (10**(-1.24))/((d+0.1)**3.03) #### for not divide by 0
#     N = W*N0/h # definition of N(t) channel condition
#     rk = calRk(Q, D, Ak.T[t], K)
#     muk, Pt, C = calmuP(Q, N, K, V, eta)
#     D = ddrm.update_D(D, rk, qk, lambdak, K)
#     Q = ddrm.update_Q(Q, muk, rk, K)
#     # print("Q:",Q)
#     # print("D:",D)
#     n_q = np.append(n_q, N)
#     b_q = np.append(b_q, Q[0])
#     p_q = np.append(p_q, Pt)
#     c_q = np.append(c_q, C)


# np.save("3a.npy",n_q)
# np.save("3b.npy",p_q)
# np.save("3c.npy",c_q)
# np.save("3d.npy",b_q)


# # experiment (4)
# dr_q = np.zeros(4)
# backlog_q = np.zeros(4)
# p_q = np.array([0])
# for V in range(0, 501, 50):
#     backlog = np.zeros(K)
#     A = np.zeros(K)
#     r = np.zeros(K)
#     pC = 0
#     Q = ddrm.setQ(K)
#     D = ddrm.setD(K)
    
#     for t in range(total_time): 
#         d = 0.1 * t
#         if d > 1500:
#             d = 3000 -d
#         h = (10**(-1.24))/((d+0.1)**3.03) #### for not divide by 0
#         N = W*N0/h # definition of N(t) channel condition
#         rk = calRk(Q, D, Ak.T[t], K)
#         r += rk
#         A += Ak.T[t]
#         muk, Pt, C = calmuP(Q, N, K, V, eta)
#         D = ddrm.update_D(D, rk, qk, lambdak, K)
#         Q = ddrm.update_Q(Q, muk, rk, K)
#         # print("Q:",Q)
#         # print("D:",D)
#         backlog += Q
#         pC += Pt

#     # # plot avgBacklog        
#     avgBacklog = backlog/total_time
#     print(avgBacklog)
#     # # plot power consumption
#     avgpC = pC/total_time
#     print(avgpC)
#     ## plot achieved delivery ratio
#     avgdr = r/ A
#     print(avgdr)

#     backlog_q = np.vstack((backlog_q, avgBacklog))
#     p_q = np.append(p_q, avgpC)
#     dr_q = np.vstack((dr_q, avgdr))
   
# np.save("backlog.npy",backlog_q)
# np.save("power.npy",p_q)
# np.save("delivery.npy",dr_q)

# experiment (6)
# V = 50 #### change from 0, 10, 30, 50
# backlog_q = np.array([0])
# p_q = np.array([0])
# for ar in range(60, 81, 5):
#     lamdbat = ar/0.8
#     lambdak = [lamdbat, lamdbat, lamdbat, lamdbat]
#     qk = [0.8, 0.8, 0.8, 0.8]
#     Ak = None
#     ### for four service, Ak with respect to kth service packet arrival distribution
#     max_value = 200
#     for i in range(K):
#         if Ak is None:
#             Ak = truncated_Poisson(lambdak[i], max_value, total_time)
#         else:
#             Ak = np.vstack((Ak, truncated_Poisson(lambdak[i], max_value, total_time)))

#     backlog = 0
#     pC = 0
#     Q = ddrm.setQ(K)
#     D = ddrm.setD(K)
#     for t in range(total_time): 
#         d = 0.1 * t
#         if d > 1500:
#             d = 3000 -d
#         h = (10**(-1.24))/((d+0.1)**3.03) #### for not divide by 0
#         N = W*N0/h # definition of N(t) channel condition
#         rk = calRk(Q, D, Ak.T[t], K)
#         muk, Pt, C = calmuP(Q, N, K, V, eta)
#         D = ddrm.update_D(D, rk, qk, lambdak, K)
#         Q = ddrm.update_Q(Q, muk, rk, K)
#         backlog += np.average(Q)
#         pC += Pt

#     # # plot avgBacklog        
#     avgBacklog = backlog/total_time
#     print(avgBacklog)
#     # # plot power consumption
#     avgpC = pC/total_time
#     print(avgpC)

#     backlog_q = np.append(backlog_q, avgBacklog)
#     p_q = np.append(p_q, avgpC)

   
# np.save("6bv50.npy",backlog_q)
# np.save("6pv50.npy",p_q)



## heuristic
backlog_q = np.array([0])
p_q = np.array([0])
for ar in range(60, 81, 5):
    lamdbat = ar/0.8
    lambdak = [lamdbat, lamdbat, lamdbat, lamdbat]
    qk = [0.8, 0.8, 0.8, 0.8]
    Ak = None
    ### for four service, Ak with respect to kth service packet arrival distribution
    max_value = 200
    for i in range(K):
        if Ak is None:
            Ak = truncated_Poisson(lambdak[i], max_value, total_time)
        else:
            Ak = np.vstack((Ak, truncated_Poisson(lambdak[i], max_value, total_time)))

    backlog = 0
    pC = 0
    Q = ddrm.setQ(K)
    D = ddrm.setD(K)
    for t in range(total_time): 
        d = 0.1 * t
        if d > 1500:
            d = 3000 -d
        h = (10**(-1.24))/((d+0.1)**3.03) #### for not divide by 0
        N = W*N0/h # definition of N(t) channel condition
        rk = calRk_heu(qk[0], Ak.T[t], K)
        muk, Pt, C = calmuP_heu(Q, N, K, eta)
        D = ddrm.update_D(D, rk, qk, lambdak, K)
        Q = ddrm.update_Q(Q, muk, rk, K)
        backlog += np.average(Q)
        pC += Pt

    # # plot avgBacklog        
    avgBacklog = backlog/total_time
    print(avgBacklog)
    # # plot power consumption
    avgpC = pC/total_time
    print(avgpC)

    backlog_q = np.append(backlog_q, avgBacklog)
    p_q = np.append(p_q, avgpC)

   
np.save("6bheu.npy",backlog_q)
np.save("6pheu.npy",p_q)
