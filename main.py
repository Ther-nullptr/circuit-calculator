from circuitCalculator1 import plot
from circuitCalculator2 import getExpression


def main():
	mode = int(input('choose the order of the circuit (1 or 2):'))
	if (mode == 1):
		submode = int(input('choose the circuit type (1--RC 2--RL):'))
		getExpression(mode, submode)
		plot(mode, submode)
	elif (mode == 2):
		submode = int(input('choose the circuit type (1--RLC(in series)):'))
		getExpression(mode, submode)
		plot(mode, submode)


if __name__ == '__main__':
	main()
