#!/usr/bin/env python

import subprocess
import argparse

calldb = {}


def cscope(index, sym):
	p = subprocess.Popen('cscope -L' + index + ' ' + sym, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

	ret = []

	for line in p.stdout.readlines():
			ret.append(line.split()[1])
			retval = p.wait()
	return set(ret)


def callers(sym):
	clist = cscope('3', sym)

	for c in clist:
		if c not in calldb:
			calldb[c] = []
		calldb[c].append(sym)
		callers(c)


def callees(sym):
	if sym in calldb:
		return

	callee = cscope('2', sym)

	if callee:
		calldb[sym] = callee

	for c in callee:
		callees(c)

def allcallers():
	funcs = cscope('0', '.\*')

	for f in funcs:
		callees(f)


def gendot():
	f = open('csgraph.dot', 'w')

	f.write('digraph {\n')

	for func in calldb:
		for call in calldb[func]:
			f.write(func + ' -> ' + call + '\n')

	f.write('}\n')


def main():
	parser = argparse.ArgumentParser()
	group = parser.add_mutually_exclusive_group()
	group.add_argument("--callers", nargs='+')
	group.add_argument("--callees", nargs='+')
	args = parser.parse_args()

	if args.callers:
		for c in args.callers:
			callers(c)
	elif args.callees:
		for c in args.callees:
			callees(c)
	else:
		allcallers()

	gendot()

if __name__ == "__main__":
	    main()
