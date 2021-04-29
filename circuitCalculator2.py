from settings import Settings
import sympy as sp
from sympy import diff, dsolve, symbols, Eq

S = Settings()


def getExpression(mode, submode):
	'''一阶电路示例'''
	if (mode == 1):
		if (submode == 1):
			Vc = symbols('Vc', cls=sp.Function)
			t = symbols('t')
			if (S.mode == 0):
				eq = Eq(diff(Vc(t), t, 1), -Vc(t) / (S.R * S.C) + S.Vs / (S.R * S.C))
				sp.pprint(dsolve(eq, Vc(t), ics={Vc(0): S.V0}))
			elif (S.mode == 1):
				eq = Eq(diff(Vc(t), t, 1), -Vc(t) / (S.R * S.C) + S.Vs * sp.sin(2 * sp.pi * t / S.T0) / (S.R * S.C))
				sp.pprint(dsolve(eq, Vc(t), ics={Vc(0): S.V0}))


		elif (submode == 2):
			iL = symbols('iL', cls=sp.Function)
			t = symbols('t')
			if (S.mode == 0):
				eq = Eq(diff(iL(t), t, 1), -iL(t) * S.R / S.L + S.iS * S.R / S.L)
				sp.pprint(dsolve(eq, iL(t), ics={iL(0): S.I0}))
			elif (S.mode == 1):
				eq = Eq(diff(iL(t), t, 1), -iL(t) * S.R / S.L + S.iS * sp.sin(2 * sp.pi * t / S.T0) * S.R / S.L)
				sp.pprint(dsolve(eq, iL(t), ics={iL(0): S.I0}))

		'''二阶电路示例'''
	elif (mode == 2):
		if (submode == 1):
			Vc, iL = symbols('Vc,iL', cls=sp.Function)
			t = symbols('t')
			if (S.mode == 0):
				eq1 = Eq(
					diff(Vc(t), t, 2) + S.R * diff(Vc(t), t, 1) / S.L + Vc(t) / (S.L * S.C),
					S.Vs / (S.L * S.C))
				sp.pprint(dsolve(eq1, Vc(t), ics={Vc(0): S.V0, diff(Vc(t), t).subs(t, 0): S.I0 / S.C}))
			elif (S.mode == 1):
				eq1 = Eq(
					diff(Vc(t), t, 2) + S.R * diff(Vc(t), t, 1) / S.L + Vc(t) / (S.L * S.C),
					S.Vs * sp.sin(2 * sp.pi * t / S.T0) / (S.L * S.C))
				sp.pprint(dsolve(eq1, Vc(t), ics={Vc(0): S.V0, diff(Vc(t), t).subs(t, 0): S.I0 / S.C}))
