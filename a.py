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

NVARIANTS = ["1st", "2nd", "3rd"]

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
    "matio",
    "mruby",
    "ntp",
    "php",
    "wavpack",
    "zlib"]

class Record:

    def __init__(self, name, base):

        self.name = name
        self.base = base
        self.evals = dict() 


def parse_csv(feature, mode):
    
    path = "a.csv" #% (feature, mode)
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
    
    #feature = sys.argv[1]
    feature = 1
    #mode = sys.argv[2]
    mode = 1

    records = parse_csv(feature, mode)
    bars = dict()

    for n in NVARIANTS:
        if n == '1st':
            bars[n] = [0.073, 0.215, 0.008, 0.338, 0.324, 0.006, 0.062, 0.014, 0.326, 0.314, 0.021, 0.041, 0.006, 0.016, 0.003, 0.371, 0.116, 0.100, 0.017, 0.268, 0.255, 0.015, 0.267, 0.183, 0.022, 0.002]
        if n == '2nd':
            bars[n] = [0.066, 0.147, 0.004, 0.056, 0.186, 0.002, 0.054, 0.012, 0.054, 0.098, 0.003, 0.040, 0.004, 0.010, 0.002, 0.056, 0.009, 0.036, 0.008, 0.238, 0.081, 0.002, 0.064, 0.029, 0.001, 0.001]
        if n == '3rd':
            bars[n] = [0.059, 0.133, 0.001, 0.018, 0.146, 0.001, 0.030, 0.010, 0.034, 0.028, 0.001, 0.032, 0.001, 0.001, 0.001, 0.022, 0.005, 0.028, 0.004, 0.173, 0.070, 0.001, 0.056, 0.003, 0.001, 0.001]

    N = len(PROGRAMS)
    ind = np.arange(N)
    width = 0.15

    labels = PROGRAMS

    fig, ax = plt.subplots()

    rects = dict()
    for i, k in enumerate(NVARIANTS):
        color = (1 - 1.0 / (len(NVARIANTS)) * i)/1.4
        print(color)
        rects[k] = ax.bar(ind + i * width, bars[k], width, color="%f" % color)

    ax.set_ylabel("Three highest duplicating hash rate in 1M executions")
    ax.set_ylim(0,0.40)
    ax.set_xticks(ind + width * (len(NVARIANTS) / 2))
    ax.set_xticklabels(PROGRAMS, rotation="-0")

    ax.yaxis.set_major_formatter(FuncFormatter(to_percent))
    ax.yaxis.grid(True, which='major')

    ax.axhline(0, color="black")

    ax.legend((rects[n] for n in NVARIANTS),
    ("%s high duplication ratio" % n for n in NVARIANTS),
    loc="upper right", ncol=len(NVARIANTS), fontsize=12)
    plt.xticks(rotation=45)
    plt.subplots_adjust(left=0.05, right=0.99, top=0.9, bottom=0.1)
    fig.set_size_inches(13, 8)

    fig.savefig("a.pdf" , format="pdf")

    plt.close()



