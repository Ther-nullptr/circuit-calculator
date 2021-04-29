class Settings:
	def __init__(self):
		self.Vs = 1  # 电压源电压(恒压源值,方波峰值,交流源峰值)
		self.iS = 1  # 电流源电流(同上)
		self.T0 = 0.5  # 电源周期
		self.V0 = 0.5  # 电容电压初值
		self.I0 = 1  # 电感电流初值
		self.R = 0.1  # 电阻值
		self.C = 1  # 电容值
		self.L = 1  # 电感值
		self.mode = 1  # 电源类型(0:v(i)dc 1:v(i)sin 2:v(i)pulse)
