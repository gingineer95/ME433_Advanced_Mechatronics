import matplotlib.pyplot as plt
import numpy as np
import csv
import math
import prob7_weights as FIIR

def FFT_plot(filename, sample_rate, h, fL, bL):
    t = [] # column 0
    data = [] # column 1

    with open(filename) as f:
        # open the csv file
        reader = csv.reader(f)
        for row in reader:
            # read the rows 1 one by one
            t.append(float(row[0])) # leftmost column
            data.append(float(row[1])) # second column

    # sample_rate = 
    print("Sample rate for " + filename + " is " + str(sample_rate))

    new_data = []
    data_len = len(data)
    h_len = len(h)
    diff_len = data_len  - h_len

    for i in range(diff_len):
        buffer = []
        for j in range(h_len):
            buffer.append(data[i + j])

        new_data.append(np.average(buffer, weights=h))

    ## For unfiltered and filtered data
    t = np.array(t)
    new_t = t[0 : diff_len]
    s = data

    Fs = sample_rate
    Ts = 1.0/Fs; # sampling interval
    ts = np.arange(0,t[-1],Ts) # time vector
    y = s # the data to make the fft from
    # y = data
    n = len(y) # length of the signal
    k = np.arange(n)
    T = n/Fs
    frq = k/T # two sides frequency range
    frq = frq[range(int(n/2))] # one side frequency range
    Y = np.fft.fft(y)/n # fft computing and normalization
    Y = Y[range(int(n/2))]

    ## For filtered data
    # s_f = output

    ts_f = np.arange(0,new_t[-1],Ts) # time vector
    y_f = new_data # the data to make the fft from
    n_f = len(y_f) # length of the signal
    k_f = np.arange(n_f)
    T_f = n_f/Fs
    frq_f = k_f/T_f # two sides frequency range
    frq_f = frq_f[range(int(n_f/2))] # one side frequency range
    Y_f = np.fft.fft(y_f)/n_f # fft computing and normalization
    Y_f = Y_f[range(int(n_f/2))]

    fig, (ax1, ax2) = plt.subplots(2, 1)
    fig.suptitle(f'FIIR Hamming Window with {h_len} weights, cutoff freq = {fL} and bandwidth = {bL}', fontsize=14, fontweight='bold')
    ax1.plot(t,y,'black') # Unfiltered data
    ax1.plot(new_t,y_f,'r') # Filtered data
    ax1.set_xlabel('Time')
    ax1.set_ylabel('Amplitude')
    ax2.loglog(frq,abs(Y),'black') # plotting the fft for unfiltered data
    ax2.loglog(frq_f,abs(Y_f),'r') # plotting the fft for filtered data
    ax2.set_xlabel('Freq (Hz)')
    ax2.set_ylabel('|Y(freq)|')

FFT_plot('sigA.csv', FIIR.sample_rate_A, FIIR.h_A, FIIR.fL_A, FIIR.bL_A)
FFT_plot('sigB.csv', FIIR.sample_rate_B, FIIR.h_B, FIIR.fL_B, FIIR.bL_B)
FFT_plot('sigC.csv', FIIR.sample_rate_C, FIIR.h_C, FIIR.fL_C, FIIR.bL_C)
FFT_plot('sigD.csv', FIIR.sample_rate_D, FIIR.h_D, FIIR.fL_D, FIIR.bL_D)
plt.show()