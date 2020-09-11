# -*- coding: utf-8 -*-
# Copyright (c) 2020 Benjamin Yao
import os
import sys
import platform
import time
import multiprocessing
from multiprocessing import Queue, Process, Manager
from decimal import *
from decimal import Decimal as dec

# Precision of Calculator
# Increasing will reult in longer wait times
precision = 2560
core_count = os.cpu_count()

getcontext().prec = precision

base10 = list(range(10))

def npfactorial(x):
	ans = 1
	for mul in range(1,x+1):
		ans *= mul
	return ans

def multi_sin(x, start_var, var, sin_ans, progress):
	ans = 0
	for k in range(start_var - 1, precision + 1, var):
		progress.put_nowait(0)
		ans += (dec(-1)**k)*(x**(dec(1)+dec(2)*k))/npfactorial(1+2*k)
	sin_ans.put_nowait(ans)
def sin(x):
	action.put("Sin")
	opsq.put_nowait(precision)
	ans = 0
	sin_manager = Manager()
	sin_ans = sin_manager.Queue()
	for num in range(1,core_count+1):
		progress.put_nowait(0)
		sin_worker = Process(target=multi_sin, args=(x, num, core_count, sin_ans, progress))
		sin_worker.start()
	while not core_count <= sin_ans.qsize():
		time.sleep(0.001)
	for num in range(core_count):
		sin_worker.terminate()
		sin_worker.join(timeout=0.01)
		ans += sin_ans.get_nowait()
	return ans

def multi_cos(x, start_var, var, cos_ans, progress):
	ans = 0
	for k in range(start_var - 1, precision + 1, var):
		progress.put_nowait(0)
		ans += (dec(-1)**k)*(x**(dec(2)*k))/npfactorial(2*k)
	cos_ans.put_nowait(ans)
def cos(x):
	action.put("Cos")
	opsq.put_nowait(precision)
	ans = 0
	cos_manager = Manager()
	cos_ans = cos_manager.Queue()
	for num in range(1,core_count+1):
		cos_worker = Process(target=multi_cos, args=(x, num, core_count, cos_ans, progress))
		cos_worker.start()
	while not core_count <= cos_ans.qsize():
		time.sleep(0.001)
	for num in range(core_count):
		cos_worker.terminate()
		cos_worker.join(timeout=0.01)
		ans += cos_ans.get_nowait()
	return ans

def tan(x):
	return sin(x)/cos(x)

def multi_factorial(x, start_var, var, factorial_ans, progress):
	ans = 1
	for k in range(start_var, x + 1, var):
		ans *= k
		progress.put_nowait(0)
	factorial_ans.put_nowait(ans)
def factorial(x):
	action.put("Factorial")
	opsq.put_nowait(int(x))
	ans = 1
	factorial_manager = Manager()
	factorial_ans = factorial_manager.Queue()
	for num in range(1,core_count+1):
		factorial_worker = Process(target=multi_factorial, args=(x, num, core_count, factorial_ans, progress))
		factorial_worker.start()
	while not core_count <= factorial_ans.qsize():
		time.sleep(0.001)
	action.put("Factorial Multiplication")	
	for num in range(core_count):
		factorial_worker.terminate()
		factorial_worker.join(timeout=0.01)
		ans *= factorial_ans.get_nowait()
	return ans

def progress_bar(opsq, progress, start_time, bar_size, finished, action):
	ops = 1
	cur_act = ""
	while finished.empty():
		try:
			while not action.empty():
				cur_act = action.get_nowait()
		except:
			pass
		try:
			while not opsq.empty():
				ops += int(opsq.get_nowait())
		except:
			pass
		inc = ops // bar_size
		complete = progress.qsize() // inc
		print(f"|{'█'*complete if complete <= bar_size else '█'*bar_size}{'='*(bar_size - complete)}| "+'%.2f'%(progress.qsize()/ops*100 if progress.qsize()/ops*100 <= 100 else 100) +f"%  Current: {cur_act} in "+'%.1f'%(time.time() - start_time)+"s"+" "*bar_size, end="\r\r")
	while not finished.empty():
		finished.get_nowait()
	while not progress.empty():
		progress.get_nowait()
	ops = 1


def checkstr(chckstr):
	checkfor = ["sys", "os.", "system", "multiprocessing", "platform", "imort", "exec", "eval", ";"]
	for _ in chckstr:
		chckstr = chckstr.replace("^","**")
		chckstr = chckstr.replace("xx", "x*x")
		chckstr = chckstr.replace("0(", "0*(")
		chckstr = chckstr.replace("1(", "1*(")
		chckstr = chckstr.replace("2(", "2*(")
		chckstr = chckstr.replace("3(", "3*(")
		chckstr = chckstr.replace("4(", "4*(")
		chckstr = chckstr.replace("5(", "5*(")
		chckstr = chckstr.replace("6(", "6*(")
		chckstr = chckstr.replace("7(", "7*(")
		chckstr = chckstr.replace("8(", "8*(")
		chckstr = chckstr.replace("9(", "9*(")
		chckstr = chckstr.replace(")0", ")*0")
		chckstr = chckstr.replace(")1", ")*1")
		chckstr = chckstr.replace(")2", ")*2")
		chckstr = chckstr.replace(")3", ")*3")
		chckstr = chckstr.replace(")4", ")*4")
		chckstr = chckstr.replace(")5", ")*5")
		chckstr = chckstr.replace(")6", ")*6")
		chckstr = chckstr.replace(")7", ")*7")
		chckstr = chckstr.replace(")8", ")*8")
		chckstr = chckstr.replace(")9", ")*9")
		chckstr = chckstr.replace("Factorial", "factorial")
		chckstr = chckstr.replace("Pi", "pi")
		chckstr = chckstr.replace("PI", "pi")
		chckstr = chckstr.replace("E", "e")
		chckstr = chckstr.replace("Euler", "e")
		chckstr = chckstr.replace("euler", "e")
	if any([x in chckstr for x in checkfor]):
		raise Exception("Illegal")
	return chckstr

def main():
	os.system('')
	global progress
	global opsq
	global action
	progress = Queue()
	opsq = Queue()
	finished = Queue()
	action = Queue()
	run = True
	bar_size = 75
	while run:
		try:
			print(">>> "+" "*(bar_size+255), end="\r")
			equation_str = checkstr(str(input("\033[A>>> ")))
			if equation_str == "":
				continue
			start_time = time.time()
			prog_bar = Process(target=progress_bar, args=(opsq, progress, start_time, bar_size, finished, action))
			prog_bar.start()
			ans = eval(equation_str)
			finished.put_nowait(0)
			time.sleep(0.05)
			print(ans)
			prog_bar.join(timeout=0.01)
		except Exception as ex:
			print(ex)
			continue
		except KeyboardInterrupt:
			sys.exit(0)

if __name__ == "__main__":
	main()


