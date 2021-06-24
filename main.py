# Copyright 2021 UCLouvain
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH
# REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY
# AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT,
# INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM
# LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR
# OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
# PERFORMANCE OF THIS SOFTWARE


import h5py
import pickle
import numpy as np
from methods import DataloadNPY,DataloadNPZ,DataloadMemmap,DataloadNPYmmap,DataloadH5
import argparse
import os
from time import time
from tqdm import tqdm
parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument(
    "--database",
    type=str,
    default="atmega8515-raw-traces.h5",
    help="Location of the 'raw traces' ASCAD database file (default: ./atmega8515-raw-traces.h5)",
)
parser.add_argument(
    "-n",
    "--ntraces",
    type=int,
    default=10000,
    help="Number of traces benchmark with" 
)
parser.add_argument(
    "-a",
    "--average",
    type=int,
    default=10,
    help="Number of averaged loads"
)
args = parser.parse_args()

DATA_DIR = "data/"
os.makedirs(DATA_DIR,exist_ok=True)

NTRACES = args.ntraces
f_database = h5py.File(args.database, "r")

traces = f_database["traces"][:NTRACES].astype(np.int8).copy()
npy = DataloadNPY(DATA_DIR+"traces.npy")
npym = DataloadNPYmmap(DATA_DIR+"traces.npy")
npz = DataloadNPZ(DATA_DIR+"traces.npz")
h5 = DataloadH5(DATA_DIR+"traces.h5")
memmap = DataloadMemmap(DATA_DIR+"traces.mem")

methods = [{"method":"npy","loader":npy},
        {"method":"npym","loader":npym},
        {"method":"npz","loader":npz},
        {"method":"h5","loader":h5},
        {"method":"memmap","loader":memmap}]

start = time()
ref = np.sum(traces)
stime = time() - start
stime = 0
print("\nlinear access:")
for m in methods:
    m["loader"].write(traces)
    times = []
    for _ in range(args.average):
        start = time()
        t = m["loader"].load() 
        assert(ref==np.sum(t))

        times.append(time()-start-stime)

        del t
    print(f"> {m['method']}: {np.mean(times):.4f}[s]")

for npoi in range(1,10000,500):
    print(f"\naccess {npoi} POIs:")
    for m in methods:
        times = []
        for _ in range(args.average):
            pois = np.sort(np.random.randint(0,len(traces[0,:]),npoi))
            start = time()
            ref = np.sum(traces[:,pois])
            stime = time() - start
            stime = 0

            start = time()
            t = m["loader"].load() 
            assert(ref==np.sum(t[:,pois]))
            times.append(time()-start-stime)

            del t
        print(f"> {m['method']}: {np.mean(times):4f}[s]")
