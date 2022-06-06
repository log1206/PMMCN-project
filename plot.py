import numpy as np
import matplotlib.pyplot as plt

### figure 3
# x = [i for i in range(0, 30000, 100)]
# a3 =np.load("3a.npy")[1:]
# b3 =np.load("3b.npy")[1:]
# c3 =np.load("3c.npy")[1:]
# d3 =np.load("3d.npy")[1:]
# b3 = [b3[i] for i in range(0, 30000, 100)]
# c3 = [c3[i] for i in range(0, 30000, 100)]
# d3 = [d3[i] for i in range(0, 30000, 100)]

# N(t)
# plt.plot(x, a3)#, label = "power consumption"
# plt.xlabel("t")
# plt.ylabel("N (t)")
# plt.xlim(0,30000)
# plt.ylim(0,0.008)
# # plt.legend()
# plt.show()

# P(t)
# plt.plot(x, b3)#, label = "power consumption"
# plt.xlabel("t")
# plt.ylabel("P (t)")
# plt.xlim(0,30000)
# plt.ylim(0,25)
# # plt.legend()
# plt.show()
# # C(t)
# plt.plot(x, c3)#, label = "power consumption"
# plt.xlabel("t")
# plt.ylabel("C (t)")
# plt.xlim(0,30000)
# plt.ylim(0,400)
# # plt.legend()
# plt.show()
# # Q1(t)
# plt.plot(x, d3)#, label = "power consumption"
# plt.xlabel("t")
# plt.ylabel("Q1 (t)")
# plt.xlim(0,30000)
# plt.ylim(0,300)
# # plt.legend()
# plt.show()

# figure 4
# x = [0,50,100,150,200,250,300,350,400,450,500]
# a =np.load("backlog.npy")
# b =np.load("power.npy")
# c =np.load("delivery.npy")

# a = a[1:]
# b = b[1:]
# c = c[4:]
# c=c.reshape(-1,4)
# print(a)
# print(b)
# print(c)

# ## power
# plt.plot(x, b)#, label = "power consumption"
# plt.xlabel("V")
# plt.ylabel("Average power consumption (W)")
# plt.xlim(0,500)
# plt.ylim(2,12)
# plt.legend()
# plt.show()

# ## backlog
# q1 = a.T[0]
# q2 = a.T[1]
# q3 = a.T[2]
# q4 = a.T[3]
# plt.plot(x, q1, label = "Q1")
# plt.plot(x, q2, label = "Q2")
# plt.plot(x, q3, label = "Q3")
# plt.plot(x, q4, label = "Q4")
# plt.xlabel("V")
# plt.ylabel("Average queue backlog (packets)")
# plt.xlim(0,500)
# plt.ylim(0,300)
# plt.legend()
# plt.show()

# ## delivery
# q1 = c.T[0]
# q2 = c.T[1]
# q3 = c.T[2]
# q4 = c.T[3]
# plt.plot(x, q1, label = "service 1, lambda1=100, q1=0.95")
# plt.plot(x, q2, label = "service 2, lambda2=80, q1=0.90")
# plt.plot(x, q3, label = "service 3, lambda3=60, q1=0.85")
# plt.plot(x, q4, label = "service 4, lambda4=40, q1=0.80")
# plt.xlabel("V")
# plt.ylabel("Average queue backlog (packets)")
# plt.xlim(0,500)
# plt.ylim(0.6,1)
# plt.legend()
# plt.show()


### figure 6
x = [i for i in range(60, 81, 5)]
b6v0 =np.load("6bv0.npy")[1:]
p6v0 =np.load("6pv0.npy")[1:]
b6v10 =np.load("6bv10.npy")[1:]
p6v10 =np.load("6pv10.npy")[1:]
b6v30 =np.load("6bv30.npy")[1:]
p6v30 =np.load("6pv30.npy")[1:]
b6v50 =np.load("6bv50.npy")[1:]
p6v50 =np.load("6pv50.npy")[1:]
b6heu =np.load("6bheu.npy")[1:]
p6heu =np.load("6pheu.npy")[1:]
# queue backlog
plt.plot(x, b6heu, label = "Heuristic algorithm")
plt.plot(x, b6v0, label = "Proposed algorithm, V = 0")
plt.plot(x, b6v10, label = "Proposed algorithm, V = 10")
plt.plot(x, b6v30, label = "Proposed algorithm, V = 30")
plt.plot(x, b6v50, label = "Proposed algorithm, V = 50")
plt.xlabel("Average arrival rate")
plt.ylabel("Average queue backlog (packets)")
plt.xlim(60,80)
plt.ylim(45,150)
plt.legend()
plt.show()

# power consumption
# plt.plot(x, p6heu, label = "Heuristic algorithm")
# plt.plot(x, p6v0, label = "Proposed algorithm, V = 0")
# plt.plot(x, p6v10, label = "Proposed algorithm, V = 10")
# plt.plot(x, p6v30, label = "Proposed algorithm, V = 30")
# plt.plot(x, p6v50, label = "Proposed algorithm, V = 50")
# plt.xlabel("Average arrival rate")
# plt.ylabel("Average power consumption (W)")
# plt.xlim(60,80)
# plt.ylim(0,150)
# plt.legend()
# plt.show()
