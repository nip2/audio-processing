import numpy as np
import matplotlib.pyplot as plt
import scipy as sp
import glob

# get list of data files in dir
myFiles = sorted(glob.glob('*.txt'))

# load most recent file
filename = myFiles[-1]
x = np.loadtxt(filename)

# dimension variables
fs = 10000
ts = 1/fs
N = len(x)
T = N * ts
t = np.linspace(0,N*ts,N)

# define filter
numtaps = 128
fc1 = 400
fc2 = fs//2 - fs//20
fc = [fc1,fc2]
#fc = 70
filter = sp.signal.firwin(numtaps, fc, pass_zero=False, fs=fs)

# filter operation
y = np.convolve(filter,x,'same')
# fundamental frequency
Y = 20 * np.log10(abs(sp.fft.fft(y)))
f = np.linspace(0,fs,N)
fund = f[np.argmax(Y[:N//2])]

# plot frequency data
fig = plt.figure(figsize=(12,6))
plt.plot(f[:N//2],Y[:N//2])
plt.vlines(fund,0,max(Y),color='red',label=f'fundamental {fund:.0f}Hz')
plt.title('frequency response of piezo on tone bowl')
plt.xlabel('frequency (Hz)')
plt.ylabel('amplitude (dB)')
plt.legend()
plt.show()
