#!/usr/bin/env python

import sys
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from matplotlib.backends.backend_pdf import PdfPages

matplotlib.rc('font', family='serif') 
matplotlib.rc('font', serif='Times') 
matplotlib.rcParams.update({'font.size': 10})
matplotlib.rc('text', usetex=True)

NVARIANTS = range(2, 4, 1)

PROGRAMS = ["arrow",
"binutils",
"capstone",
"c-ares",
"eigen",
"ffmpeg",
"flac",
"freeimage",
"gfwx",
"giflib",
"htslib",
"jansson",
"kcodec",
"lame",
"libmpeg2",
"libpcap",
"libpng-proto",
"libtiff",
"libzip",
"lodepng",
"lz4",
"matio",
"mruby",
"ntp",
"php",
"wavpack",
"zlib"
]

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

            for i in NVARIANTS:
                record.evals[i] = float(tokens[3 + (i - 2) * 2])

            records[record.name] = record

    return records


def autolabel(rects):
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width()/2.0, 1.05*height,
                '%d' % int(height),
                ha='center', va='bottom',
                fontsize=8)


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
            val = (record.evals[n] - record.base) / record.base
            bar.append(val)

        bars[n] = bar

    N = len(PROGRAMS) 
    ind = np.arange(N)
    width = 0.25

    labels = []
    labels.extend(PROGRAMS)

    fig, ax = plt.subplots()

    rects = dict()
    for n in NVARIANTS:
        rects[n] = ax.bar(ind + (n-2) * width, bars[n], width, color="%f" % (1 - 1.0/(len(NVARIANTS)-0.5) * (n-2)))

    ax.set_ylabel("Overhead relative to baseline")
    ax.set_xticks(ind + width)
    ax.set_xticklabels(labels, rotation="-90")

    ax.yaxis.set_major_formatter(FuncFormatter(to_percent))
    ax.yaxis.grid(True, which='major')

    ax.axhline(0, color="black")

    ax.legend((rects[n] for n in NVARIANTS), ("Strict", "Selective"), loc="upper center", ncol=len(NVARIANTS), fontsize=9)

    plt.xticks(rotation=45)

    plt.subplots_adjust(left=0.1, right=0.99, top=0.9, bottom=0.30)
    fig.set_size_inches(8, 5)

    fig.savefig("a.pdf", format="pdf")

    plt.close()

