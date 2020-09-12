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
precision = 2048
core_count = os.cpu_count()

getcontext().prec = precision

base10 = list(range(10))

class cache:
	def __init__(self):
		self.ans_cache = dict()
	def add_result(self, func, param, result):
		self.ans_cache.update({result:{func:param}})
	def lookup(self, func, param):
		for results in self.ans_cache:
			try:
				if self.ans_cache[results][func] == param:
					return results
			except KeyError:
				pass
		return None

cache = cache()
def npfactorial(x):
	ans = 1
	for mul in range(1,x+1):
		ans *= mul
	return ans

def multi_pi(start_var, var, pi_ans):
	pi = 0
	for x in range(start_var - 1, precision, var):
		pi += dec(1) / dec(16) ** dec(x) * (dec(4) / (dec(8) * x + dec(1)) - dec(2) / (dec(8) * x + dec(4)) - dec(1) / (dec(8) * x + dec(5)) - dec(1) / (dec(8) * x + dec(6)))
	pi_ans.put(pi)
def calc_pi():
	ans = 0
	pi_manager = Manager()
	pi_ans = pi_manager.Queue()
	for num in range(1,core_count+1):
		pi_worker = Process(target=multi_pi, args=(num, core_count, pi_ans))
		pi_worker.start()
	while not core_count <= pi_ans.qsize():
		time.sleep(0.001)
	for num in range(core_count):
		pi_worker.terminate()
		pi_worker.join(timeout=0.01)
		ans += pi_ans.get_nowait()
	finish.put_nowait(0)
	return ans

def multi_e(start_var, var, e_ans):
	e = 0
	for x in range(start_var - 1, precision, var):
		e += dec(1) / dec(npfactorial(x))
	e_ans.put(e)
def calc_e():
	ans = 0
	e_manager = Manager()
	e_ans = e_manager.Queue()
	for num in range(1,core_count+1):
		e_worker = Process(target=multi_e, args=(num, core_count, e_ans))
		e_worker.start()
	while not core_count <= e_ans.qsize():
		time.sleep(0.001)
	for num in range(core_count):
		e_worker.terminate()
		e_worker.join(timeout=0.01)
		ans += e_ans.get_nowait()
	finish.put_nowait(0)
	return ans


def multi_sin(x, start_var, var, sin_ans, progress):
	ans = 0
	for k in range(start_var - 1, precision + 1, var):
		progress.put_nowait(0)
		ans += (dec(-1)**k)*(x**(dec(1)+dec(2)*k))/npfactorial(1+2*k)
	sin_ans.put_nowait(ans)
def sin(x):
	if not cache.lookup('sin', x) == None:
		return cache.lookup('sin', x)
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
	finish.put_nowait(0)
	cache.add_result('sin',x,ans)
	return ans

def multi_cos(x, start_var, var, cos_ans, progress):
	ans = 0
	for k in range(start_var - 1, precision + 1, var):
		progress.put_nowait(0)
		ans += (dec(-1)**k)*(x**(dec(2)*k))/npfactorial(2*k)
	cos_ans.put_nowait(ans)
def cos(x):
	if not cache.lookup('cos', x) == None:
		return cache.lookup('cos', x)
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
	finish.put_nowait(0)
	cache.add_result('cos',x,ans)
	return ans

def tan(x):
	if not cache.lookup('tan', x) == None:
		return cache.lookup('tan', x)
	ans = sin(x)/cos(x)
	cache.add_result('tan',x,ans)
	return ans

def multi_factorial(x, start_var, var, factorial_ans, progress):
	ans = 1
	for k in range(start_var, x + 1, var):
		ans *= k
		progress.put_nowait(0)
	factorial_ans.put_nowait(ans)
def factorial(x):
	if not cache.lookup('factorial', x) == None:
		return cache.lookup('factorial', x)
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
	finish.put_nowait(0)
	cache.add_result('factorial',x,ans)
	return ans

def progress_bar(opsq, progress, start_time, bar_size, finished, action, remain, finish):
	ops = 1
	cur_act = ""
	while finished.empty():
		try:
			while not action.empty():
				cur_act = action.get_nowait()
			while not opsq.empty():
				ops += int(opsq.get_nowait())
		except:
			pass
		try:
			complete = progress.qsize() // (ops // bar_size)
		except ZeroDivisionError:
			return
		print(f"|\033[107m{'█'*complete if complete <= bar_size else '█'*bar_size}\033[0m{'='*(bar_size - complete)}| "+'%.2f'%(progress.qsize()/ops*100 if progress.qsize()/ops*100 <= 100 else 100) +f"%  [Current: {cur_act}, Remaining: {remain-finish.qsize()-1}] Elapsed: "+'%.1f'%(time.time() - start_time)+"s"+" "*bar_size, end="\r")
	print(' '*(bar_size+255),end="\r\033[A")
	while not finished.empty():
		finished.get_nowait()
	while not progress.empty():
		progress.get_nowait()
	del ops


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
	global opsq
	global action
	global finish
	opsq = Queue()
	finished = Queue()
	action = Queue()
	finish = Queue()
	run = True
	bar_size = 32
	pi = calc_pi()
	e = calc_e()
	while run:
		try:
			global progress
			progress = Queue()
			equation_str = checkstr(str(input(r">>> ")))
			todo_q = equation_str.count("sin")+equation_str.count("cos")+equation_str.count("tan")*2+equation_str.count("factorial")
			if equation_str == "":
				continue
			elif equation_str == "exit":
				sys.exit(0)
			else:
				start_time = time.time()
				prog_bar = Process(target=progress_bar, args=(opsq, progress, start_time, bar_size, finished, action, todo_q, finish))
				prog_bar.start()
				ans = eval(equation_str)
				finished.put_nowait(0)
				time.sleep(0.05)
				print(ans)
				prog_bar.join(timeout=0.01)
				del progress
				while not finish.empty():
					finish.get_nowait()
		except Exception as ex:
			print(str(ex))
			continue
		except KeyboardInterrupt:
			sys.exit(0)

if __name__ == "__main__":
	main()


