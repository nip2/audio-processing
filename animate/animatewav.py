import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
import scipy as sp
from scipy.io import wavfile
import scienceplots
from playsound import playsound
import multiprocessing as mp
import time

# set plot style using scienceplots module
plt.style.use(['science','notebook','grid'])

#=============================================================
# This program takes an audio file and plots its frequency
# response animated while playing the audio

#=============================================================
# User defined variables:

# audio file to use:
filename = "animate/500-1000Hz.wav"
#filename = "sigproc/500Hz.wav"
# start plot delay to keep in sync with audio:
start_delay = .35   # seconds
# set size of each chunk of audio (in samples)
chunksize = 4096

#=============================================================

# class that stores frequency spectrum of each chunk
# f and Xreal arrays are 1:1 x,y axes
class Chunkf:
    def __init__(self, fs: int, data: np.ndarray, index: int):
        self.fs = fs
        self.data = data
        self.index = index
        self.N = len(self.data)
        # zero-padded length
        self.Nf = 8192
        # log magnitude
        self.X = 20 * np.log10(sp.fft.fft(self.data, n=self.Nf))
        # absolute magnitude
        #self.X = sp.fft.fft(self.data, n=self.Nf)
        self.Xreal = self.X[:self.Nf//2]
        # define x axis frequency range
        self.f = np.linspace(0,self.fs//2,self.Nf//2)

# animate plots of each chunk
def animateFunc():
    # x limit in Hz
    xlimit = (10,3000)
    # y limit in dB
    ylimit = (20,160)
    # y limit in normalized absolute
    #ylimit = (0,2)
    fig = plt.figure(figsize=(12, 6))
    axis = plt.axes(xlim = xlimit, ylim = ylimit)
    line, = axis.plot([], [], lw = 1)
    axis.set_title('Audio spectrum')
    axis.set_xlabel('Frequency (Hz)')
    axis.set_ylabel('Magnitude (dB)')
    # use set_xticks for logarithmic plot (which doesn't work great)
    #axis.set_xticks([10,100,1000,5000])

    def init():
        line.set_data([], [])
        return line,

    def animate(i):
        x = chunks[i].f
        y = chunks[i].Xreal
        line.set_data(x,y)
        # logarithmic plot doesn't work great
        #axis.set_xscale('log')
        return line,

    anim = FuncAnimation(fig, animate, init_func = init, 
                        frames = numchunks - 1, interval = delay, blit = True)
    plt.show()


#=============================================================

if __name__ == "__main__":

    fs, data = wavfile.read(filename)
    N = len(data)
    # break apart into left and right channels
    dataL = data[:,0]
    dataR = data[:,1]
    # sum channels elementwise to mono
    dataC = np.add(dataL,dataR)

    # chop up signal into chunks
    numchunks = int(np.ceil(N/chunksize))
    # delay (in ms) sets frame interval for animation playback
    delay = chunksize / fs * 1000
    # split left channel data into chunks
    chunks = []
    for i in range(numchunks):
        istart = i * chunksize
        if i == numchunks - 1:
            iend = N
        else:
            iend = istart + chunksize
        chunks.append(Chunkf(fs,dataC[istart:iend],i))
    
    # multiprocessing to play audio while animation plots
    p = mp.Process(target=playsound, args=(filename,))
    p.start()
    # delay to start plot in sync with sound
    time.sleep(start_delay)
    animateFunc()
    # audio stops when plot is closed
    p.terminate()
