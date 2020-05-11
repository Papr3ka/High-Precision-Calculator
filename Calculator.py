# -*- coding: utf-8 -*-
# Copyright (c) 2020 Benjamin Yao
import os
import platform
import time
import math
from decimal import *
from decimal import Decimal as dec
precision = 768
getcontext().prec = precision
def clear():
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')
def wait():
	wait = str(input("Press enter to exit..."))
def factorial(x):
    ans = 1
    for fac in range(x,1,-1):
        ans *= fac
    x = ans
    return x
def sqrt(x):
	ans = dec(x)**dec((dec(1))/dec(2))
	ans = dec(int(ans * dec(10 ** precision)) / dec(10 ** precision))
	return ans
def abs(x):
	if x < 0:
		ans = x * -1
	else:
		ans = x
	return ans
def ceil(x):
	ans = int(int(x) + 1)
	return ans
def floor(x):
	ans = int(x)
	return ans
def constant(precision):
	print("Loading Constants...")
	global pi
	global e
	pi = 0
	e = 0
	for x in range(0,precision): 
		pi += dec((dec(1) / dec(16) ** dec(x)) * (dec(4) / (dec(8) * x + dec(1)) - dec(2) / (dec(8) * x + dec(4)) - dec(1) / (dec(8) * x + dec(5)) - dec(1) / (dec(8) * x + dec(6))))
	pi = dec(int(pi * dec(10 ** precision)) / dec(10 ** precision))
	for x in range(0,precision + 64):
		e += dec(dec(1) / dec(factorial(int(x))))
	e = dec(int(e * dec(10 ** precision)) / dec(10 ** precision))
def bernoulli(n):
    A = [0] * (n+1)
    for m in range(n+1):
        A[m] = dec(1)/(m+dec(1))
        for j in range(m, 0, -1):
          A[j-1] = j*(A[j-1] - A[j])
    return A[0]
# Taylor series Expansion of Trigonomic functions
def sin(x):
	ans = 0
	for n in range(0,int(precision)+int(abs(x))):
	 	ans += dec((dec(-1)**n)*x**(dec(2)*n+dec(1)))/dec(factorial(2*n+1))
	ans = dec(int(ans * dec(10 ** precision)) / dec(10 ** precision))
	return ans
def cos(x):
	ans = 0
	for n in range(0,int(precision)+int(abs(x))):
	 	ans += dec((dec(-1)**n)*x**(dec(2)*n))/dec(factorial(2*n))
	ans = dec(int(ans * dec(10 ** precision)) / dec(10 ** precision))
	return ans
def tan(x):
	ans = sin(x)/cos(x)
	ans = dec(int(ans * dec(10 ** precision)) / dec(10 ** precision))
	return ans
def arcsin(x):
	ans = 0
	for n in range(0,int(precision)+int(x)):
		ans += dec(factorial(2*n))*x**dec(dec(2)*n+dec(1))/dec(4)**n*dec(factorial(n))**dec(2)*dec(dec(2)*n+dec(1))
	ans = dec(int(ans * dec(10 ** precision)) / dec(10 ** precision))
	return ans
def arccos(x):
	pass
def arctan(x):
	pass
def sinh(x):
	ans = (e**x-e**(-x))/dec(2)
	return ans
def cosh(x):
	ans = (e**x+e**(-x))/dec(2)
	return ans
def tanh(x):
	ans = (e**x-e**(-x))/((e**x)+e**(-x))
	return ans
def coth(x):
	ans = (e**x+e**-x)/(e**x-e**-x)
	return ans
def sech(x):
	ans = dec(2)/(e**x+e**-x)
	return ans
def csch(x):
	ans = dec(2)/(e**x-e**-x)
	return ans
def arcsinh(x):
	pass
def arccosh(x):
	pass
def arctanh(x):
	pass
def sec(x):
	ans = dec(1)/cos(x)
	ans = dec(int(ans * dec(10 ** precision)) / dec(10 ** precision))
	return ans
def csc(x):
	ans = dec(1)/sin(x)
	ans = dec(int(ans * dec(10 ** precision)) / dec(10 ** precision))
	return ans
def cot(x):
	ans = dec(1)/tan(x)
	ans = dec(int(ans * dec(10 ** precision)) / dec(10 ** precision))
	return ans
def arcsec(x):
	pass
def arccsc(x):
	pass
def arccot(x):
	pass
def arcsech(x):
	pass
def arccsch(x):
	pass
def arccoth(x):
	pass
# Incomplete WIP
# Error Function
def erf(z):
#	ans = 0
#	for n in range(0,precision+int(z)+1000):
#		ans += dec((dec(-1)**n)*z**dec(2)*n+dec(1))/dec(factorial(n))*(dec(2)*n+dec(1))
#	ans = ans*(dec(2)/sqrt(pi))
#	ans = dec(int(ans * dec(10 ** precision)) / dec(10 ** precision))
#	return ans
	pass
def exp(x):
	ans = e**x
	return ans
# Gamma Function
pass
# Finite Integral
def fnint(var,eq,min,max):
	pass
def Eq_fix(run_string):
	for x in range(1, len(run_string)):
		run_string = run_string.replace("^","**")
		run_string = run_string.replace("xx", "x*x")
		run_string = run_string.replace("0(", "0*(")
		run_string = run_string.replace("1(", "1*(")
		run_string = run_string.replace("2(", "2*(")
		run_string = run_string.replace("3(", "3*(")
		run_string = run_string.replace("4(", "4*(")
		run_string = run_string.replace("5(", "5*(")
		run_string = run_string.replace("6(", "6*(")
		run_string = run_string.replace("7(", "7*(")
		run_string = run_string.replace("8(", "8*(")
		run_string = run_string.replace("9(", "9*(")
		run_string = run_string.replace(")0", ")*0")
		run_string = run_string.replace(")1", ")*1")
		run_string = run_string.replace(")2", ")*2")
		run_string = run_string.replace(")3", ")*3")
		run_string = run_string.replace(")4", ")*4")
		run_string = run_string.replace(")5", ")*5")
		run_string = run_string.replace(")6", ")*6")
		run_string = run_string.replace(")7", ")*7")
		run_string = run_string.replace(")8", ")*8")
		run_string = run_string.replace(")9", ")*9")
		run_string = run_string.replace("Factorial", "factorial")
		run_string = run_string.replace("Pi", "pi")
		run_string = run_string.replace("PI", "pi")
		run_string = run_string.replace("E", "e")
		run_string = run_string.replace("Euler", "e")
		run_string = run_string.replace("euler", "e")
# Section for future string corrections
	return run_string
def getcalc():
	clear()
	calc_str = str(input(":"))
	tstart = time.perf_counter()
	calc_str = Eq_fix(calc_str)
	clear()
	print("Calculating...")
	try:
		final_ans = dec(eval(calc_str))
		clear()
	except FloatingPointError:
		print("ERROR:FloatingPointError")
	except MemoryError:
		print("ERROR:MemoryError")
	except OverflowError:
		print("ERROR:OverflowError")
	except ZeroDivisionError:
		print("ERROR:ZeroDivisionError")
	except all:
		print("ERROR")
	else:
		tend = time.perf_counter()
		print("Result")
		tstart_copy = time.perf_counter()
		print(final_ans)
		tend_copy = time.perf_counter()
		print("\n")
		print(calc_str)
		print("\n")
		print("Compute time:",'%.4f'%(tend - tstart),"Seconds")
		print("I/O time:",'%.4f'%(tend_copy - tstart_copy),"Seconds")
		print("Total time:",'%.4f'%(tend - tstart + tend_copy - tstart_copy),"Seconds")
constant(precision)
getcalc()
wait()
