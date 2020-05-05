# -*- coding: utf-8 -*-
# Copyright (c) 2020 Benjamin Yao
import os
import platform
import time
import math
from decimal import *
from decimal import Decimal as dec
getcontext().prec = 32768
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
	return ans
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
	return run_string
def getcalc():
	clear()
	calc_str = str(input(":"))
	tstart = time.perf_counter()
	calc_str = Eq_fix(calc_str)
	clear()
	print("Calculating...")
	try:
		final_ans = eval(calc_str)
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
getcalc()
wait()
