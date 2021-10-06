#!/usr/bin/env python

import sys
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from matplotlib.backends.backend_pdf import PdfPages

matplotlib.rc('font', family='serif') 
matplotlib.rc('font', serif='Times') 
matplotlib.rcParams.update({'font.size': 12})
matplotlib.rc('text', usetex=True)

NVARIANTS = ["2", "4", "6", "8"]

PROGRAMS = ["perlbench", "bzip2", "gcc", "mcf", "milc", "namd", "gobmk",
        "dealII", "soplex", "povray", "hmmer", "sjeng", "libquantum", "h264ref",
        "lbm", "omnetpp", "astar", "sphinx3", "xalancbmk", "Average"]

class Record:

	def __init__(self, name, base):

		self.name = name
		self.base = base
		self.evals = dict() 


def parse_csv(feature, mode):
	
	path = "spec-%s-%s.csv" % (feature, mode)
	records = dict() 

	with open(path) as f:
		content = f.readlines()

		for line in content[1:]:
			tokens = line.split(",")
			record = Record(tokens[1], float(tokens[2]))

			for i, k in enumerate(NVARIANTS):
				record.evals[k] = float(tokens[3 + i]) 

			records[record.name] = record

	return records


def autolabel(rects):
	for rect in rects:
		height = rect.get_height()
		ax.text(rect.get_x() + rect.get_width()/2.0, 1.05*height,
				'%d' % int(height),
				ha='center', va='bottom',
				fontsize=12)


def to_percent(y, position):
	s = str(int(100 * y))
	return s + r'$\%$'


if __name__ == "__main__":
	
	feature = sys.argv[1]
	mode = sys.argv[2]

	records = parse_csv(feature, mode)
	bars = dict()

	for n in NVARIANTS:
		bar = []
		for prog in PROGRAMS:
			record = records[prog]
			bar.append((record.evals[n] - record.base) / record.base)

		bars[n] = bar 

	N = len(PROGRAMS)
	ind = np.arange(N)
	width = 0.15

	labels = PROGRAMS

	fig, ax = plt.subplots()

	rects = dict()
	for i, k in enumerate(NVARIANTS):
		color = 1 - 1.0 / (len(NVARIANTS)) * i
		rects[k] = ax.bar(ind + i * width, bars[k], width, color="%f" % color)

	ax.set_ylabel("Overhead relative to baseline")
	ax.set_ylim(0,0.45)
	ax.set_xticks(ind + width * (len(NVARIANTS) / 2))
	ax.set_xticklabels(PROGRAMS, rotation="-0")

	ax.yaxis.set_major_formatter(FuncFormatter(to_percent))
	ax.yaxis.grid(True, which='major')

	ax.axhline(0, color="black")

	ax.legend((rects[n] for n in NVARIANTS),
	("%s variants" % n for n in NVARIANTS),
	loc="upper right", ncol=len(NVARIANTS), fontsize=12)

	plt.subplots_adjust(left=0.05, right=0.99, top=0.9, bottom=0.1)
	fig.set_size_inches(15, 2)

	fig.savefig("a.pdf" % (feature, mode), format="pdf")

	plt.close()

