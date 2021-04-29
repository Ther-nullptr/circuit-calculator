from scipy.integrate import odeint
import matplotlib.pyplot as plt
import numpy as np
from settings import Settings

S = Settings()  # 引入电路参量

dots1 = 200  # 一阶电路采样点数
dots2 = 1000  # 二阶电路采样点数


def pulse(t):  # 成一个低值为0,高值为1的方波,周期为T0的方波
	pulse = 1
	for k in range(1, 100, 1):
		pulse = pulse + 4 * np.sin(
			(2 * k - 1) * 2 * np.pi * t / S.T0) / ((2 * k - 1) * np.pi)
	return 0.5 * pulse


# 一阶RC电路,返回电容电压
def RC_diff(Vc, t):
	if S.mode == 0:
		return np.array(-Vc / (S.R * S.C) + S.Vs / (S.R * S.C))
	elif S.mode == 1:
		return np.array(-Vc / (S.R * S.C) + S.Vs * np.sin(2 * np.pi * t / S.T0) /
		                (S.R * S.C))
	elif S.mode == 2:
		return np.array(-Vc / (S.R * S.C) + S.Vs * pulse(t) / (S.R * S.C))


# 一阶RL电路,返回电感电流
def RL_diff(iL, t):
	if S.mode == 0:
		return np.array(-iL * S.R / S.L + S.R * S.iS / S.L)
	elif S.mode == 1:
		return np.array(-iL * S.R / S.L + S.R * S.iS * np.sin(2 * np.pi * t / S.T0) / S.L)
	elif S.mode == 2:
		return np.array(-iL * S.R / S.L + S.iS * pulse(t) * S.R / S.L)


# 二阶RLC电路
def RLC_diff(state_vector, t):
	Vc, iL = state_vector
	if S.mode == 0:
		return np.array([iL / S.C, -S.R * iL / S.L - Vc / S.L + S.Vs / S.L])
	elif S.mode == 1:
		return np.array([
			iL / S.C, -S.R * iL / S.L - Vc / S.L + S.Vs * np.sin(2 * np.pi * t / S.T0) / S.L
		])
	elif S.mode == 2:
		return np.array([iL / S.C, -S.R * iL / S.L - Vc / S.L + S.Vs * pulse(t) / S.L])


def plot(mode, submode):
	if (mode == 1):
		if (submode == 1):
			tau = S.R * S.C
			t = np.linspace(0, 5 * tau, dots1)
			result = odeint(RC_diff, S.V0, t)
			plt.xlabel('t')
			plt.ylabel('Vc')
			plt.xlim(0, 5 * tau)
			if S.mode == 0:
				plt.ylim(0, max(S.Vs, S.V0))
			else:
				plt.ylim(min(-S.Vs, -S.V0), max(S.Vs, S.V0))
			plt.plot(t, result, label='Vc')
			plt.legend()
			plt.show()

		elif (submode == 2):
			tau = S.L / S.R
			t = np.linspace(0, 5 * tau, dots1)
			result = odeint(RL_diff, S.I0, t)
			plt.xlabel('t')
			plt.ylabel('iL')
			plt.xlim(0, 5 * tau)
			if S.mode == 0:
				plt.ylim(0, max(S.iS, S.I0))
			else:
				plt.ylim(min(-S.iS, -S.I0), max(S.iS, S.I0))
			plt.plot(t, result, label='iL')
			plt.legend()
			plt.show()

	elif (mode == 2):
		damping_factor = S.R * np.sqrt(S.C / S.L) / 2  # 阻尼系数ξ
		omega = 1 / np.sqrt(S.L * S.C)  # 自由振荡频率

		if (submode == 1):
			'''
		LC谐振腔的品质因数Q = 1/(2*ξ)
		经过Q个周期，振铃幅度衰减为4.3%以下
		经过1.5Q个周期，振铃幅度衰减为1%以下
		经过2.2Q个周期，振铃幅度衰减为0.1%以下
			'''
			if (damping_factor < 1 and damping_factor > 0):  # 欠阻尼
				T = 2 * np.pi / (omega * np.sqrt(1 - damping_factor ** 2)
				                 )  # RLC电路的周期
				Q = 1 / (2 * damping_factor)
				t = np.linspace(0, 1.5 * Q * T, dots2)
				result = odeint(RLC_diff, [S.V0, S.I0], t)
				plt.xlabel('t')
				plt.ylabel('Vc/iL')
				plt.xlim(0, 1.5 * Q * T)
				plt.ylim(min(-S.V0,-S.Vs), max(2*S.V0,2 * S.Vs))
				plt.plot(t, result)
				plt.show()
				'''
		过阻尼下的时间常数τ1=(ξ+sqrt(ξ^2-1))/ω(长寿命项),τ2=(ξ-sqrt(ξ^2-1))/ω(短寿命项)
		短期行为看短寿命项,长期寿命看长寿命项
				'''
			elif (damping_factor > 1):  # 过阻尼
				tau = (damping_factor +
				       np.sqrt(damping_factor ** 2 - 1)) / omega
				t = np.linspace(0, 5 * tau, dots2)
				result = odeint(RLC_diff, [0, 0], t)
				plt.xlabel('t')
				plt.ylabel('Vc/iL')
				plt.xlim(0, 5 * tau)
				plt.ylim(min(-S.V0, -S.Vs), max(2 * S.V0, 2 * S.Vs))
				plt.plot(t, result)
				plt.show()
				'''
		临界阻尼中有一项是e^(-ωt),有一项是t*e^(-ωt),这里定义其时间常数τ=1/ω
				'''
			elif (damping_factor == 1):  # 临界阻尼
				tau = 1 / omega
				t = np.linspace(0, 5 * tau, dots2)
				result = odeint(RLC_diff, [0, 0], t)
				plt.xlabel('t')
				plt.ylabel('Vc/iL')
				plt.xlim(0, 5 * tau)
				plt.ylim(min(-S.V0, -S.Vs), max(2 * S.V0, 2 * S.Vs))
				plt.plot(t, result)
				plt.show()

			else:  # 无阻尼
				T = 2 * np.pi / omega
				t = np.linspace(0, 5 * T, dots2)
				result = odeint(RLC_diff, [0, 0], t)
				plt.xlabel('t')
				plt.ylabel('Vc/iL')
				plt.xlim(0, 5 * T)
				plt.ylim(-2 * S.Vs, 2 * S.Vs)
				plt.plot(t, result)
				plt.show()
