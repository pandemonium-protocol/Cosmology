import mpmath as mp
mp.mp.dps = 50

alpha = mp.mpf('7.2973525693e-3')
euler_e = mp.exp(1)
G = mp.mpf('6.67430e-11')
m_p = mp.mpf('1.67262192369e-27')
hbar = mp.mpf('1.054571817e-34')
c = mp.mpf('299792458')

alpha_G = (G * m_p**2) / (hbar * c)
Lambda2 = alpha_G / (alpha ** 18)

term = 1 - 4*alpha/3 + (alpha**2) / mp.sqrt(euler_e)
Lambda1 = mp.sqrt(3) * term

print("Lambda1:", Lambda1)
print("Lambda2:", Lambda2)
print("Relative diff:", abs(Lambda1 - Lambda2) / Lambda2)
