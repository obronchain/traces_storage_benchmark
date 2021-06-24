This repository attempts to benchmark different fileformats to store the ASCAD
traces both with a linear access on the traces and with a random POI access. 

The tested methods are:
    - `.npy` with an without `mmap_mode`.
    - `.npz`
    - `memmap` 
