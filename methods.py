import numpy as np
import h5py
class Dataload():
    def __init__(self,filename):
        self.filename = filename
    def load(self):
        pass
        return None
    def write(self,traces):
        pass

class DataloadNPZ(Dataload):
    def load(self):
        return np.load(self.filename)["t"]
        
    def write(self,traces):
        np.savez(self.filename,t=traces)

class DataloadNPY(Dataload):
    def load(self):
        return np.load(self.filename)
        
    def write(self,traces):
        np.save(self.filename,traces)

class DataloadNPYmmap(Dataload):
    def load(self):
        return np.load(self.filename,mmap_mode="r")
        
    def write(self,traces):
        np.save(self.filename,traces)
class DataloadH5(Dataload):
    def load(self):
        h5f = h5py.File(self.filename,"r")
        t = h5f["traces"][:]
        h5f.close()
        return t
        pass
    def write(self,traces):
        h5f = h5py.File(self.filename, 'w')
        h5f.create_dataset('traces', data=traces)
        h5f.close()

class DataloadMemmap(Dataload):
    def load(self):
        return np.memmap(self.filename,
                dtype=self.dtype,mode='r',shape=self.shape)
        
    def write(self,traces):
        self.dtype = traces.dtype
        self.shape = traces.shape

        fp = np.memmap(self.filename, 
                        dtype=self.dtype, mode='w+', shape=self.shape)

        fp[:] = traces[:]
        fp.flush()
