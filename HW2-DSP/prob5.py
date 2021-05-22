import matplotlib.pyplot as plt
import numpy as np
import csv
import math

def FFT_plot(filename, X):
    t = [] # column 0
    data = [] # column 1

    with open(filename) as f:
        # open the csv file
        reader = csv.reader(f)
        for row in reader:
            # read the rows 1 one by one
            t.append(float(row[0])) # leftmost column
            data.append(float(row[1])) # second column

    sample_rate = len(t) / t[-1]
    print("Sample rate for " + filename + " is " + str(sample_rate))
    averages = []

    for q in range(0, X):
        averages.append(0)

    for i in range(0, len(t)-X):
        samples = []
        for j in range(i, i+X):
            samples.append(data[j])
        
        ave = sum(samples) / X
        averages.append(ave)

    ## For unfiltered and filtered data
    t = np.array(t)
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
    s_f = averages

    ts_f = np.arange(0,t[-1],Ts) # time vector
    y_f = s_f # the data to make the fft from
    n_f = len(y_f) # length of the signal
    k_f = np.arange(n_f)
    T_f = n_f/Fs
    frq_f = k_f/T_f # two sides frequency range
    frq_f = frq_f[range(int(n_f/2))] # one side frequency range
    Y_f = np.fft.fft(y_f)/n_f # fft computing and normalization
    Y_f = Y_f[range(int(n_f/2))]

    fig, (ax1, ax2) = plt.subplots(2, 1)
    fig.suptitle('MAF Over Average of ' + str(X) + ' Datapoints', fontsize=14, fontweight='bold')
    ax1.plot(t,y,'black') # Unfiltered data
    ax1.plot(t,y_f,'r') # Filtered data
    ax1.set_xlabel('Time')
    ax1.set_ylabel('Amplitude')
    ax2.loglog(frq,abs(Y),'black') # plotting the fft for unfiltered data
    ax2.loglog(frq_f,abs(Y_f),'r') # plotting the fft for filtered data
    ax2.set_xlabel('Freq (Hz)')
    ax2.set_ylabel('|Y(freq)|')

FFT_plot('sigA.csv', 500) # No less then 400
FFT_plot('sigB.csv', 300)
FFT_plot('sigC.csv', 700) #Lets do 700 cause the samples are so low. No less then 500
FFT_plot('sigD.csv', 100)
plt.show()