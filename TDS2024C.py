# The following program acquires the signal from the specified channel of a Tektronix TDS 2024C Oscilloscope,
# and then takes the FFT of the acquired signal. The program can work for other Tektronix scopes, as well as
# oscilloscopes from other manufacturers, as SCPI commands are used. Please refer to the programmer manual of
# the oscilloscope you are using.

# Citations:
# https://www.ritchievink.com/blog/2017/04/23/understanding-the-fourier-transform-by-example/
# https://www.tek.com/support/faqs/programing-how-get-and-plot-waveform-dpo-mso-mdo4000-series-scope-python

import pyvisa
import numpy as np
from struct import unpack
import matplotlib.pyplot as plt

rm = pyvisa.ResourceManager()
print(rm.list_resources())

# The address passed to the open_resource function will depend on the port the oscilloscope is connected to (for
# a USB connection). For a GPIB or TCP/IP connection, you can also pass the address to the open_resource function.
# Please refer to the programmer manual of the oscilloscope you are using.

scope = rm.open_resource('USB0::0x0699::0x03A6::C047156::INSTR')
print(scope.query('*IDN?'))

#The data obtained from the oscilloscope will be digitzed values, that will have to be converted to Volts & Time
ymult = float(scope.query('WFMPRE:YMULT?'))
yzero = float(scope.query('WFMPRE:YZERO?'))
yoff = float(scope.query('WFMPRE:YOFF?'))
xincr = float(scope.query('WFMPRE:XINCR?'))

scope.write('CH1:SCAle 0.05')
scope.write('DATa:SOUrce CH1')
scope.write('DATa:ENCdg RPBinary')
scope.write('DATa:WIDth 1')
scope.write('DATa:STARt 1')
scope.write('DATa:STOP 2500')

scope.write('CURVE?')
data = scope.read_raw()
headerlen = 2 + int(data[1])
header = data[:headerlen]
ADC_wave = data[headerlen:-1]

ADC_wave = np.array(unpack('%sB' % len(ADC_wave),ADC_wave))
Volts = (ADC_wave - yoff) * ymult  + yzero
Time = np.arange(0, xincr * len(Volts), xincr)

plt.figure(1)
plt.plot(Time,Volts)

# Taking the FFT of the signal acquired from the oscilloscope
plt.figure(2)
fft = np.fft.fft(Volts)
T = Time[1] - Time[0]
N = Volts.size
f = np.linspace(0, 1 / T, N)

plt.ylabel("Amplitude")
plt.xlabel("Frequency [Hz]")
plt.plot(f[:N // 2], np.abs(fft)[:N // 2] * 1 / N)  # 1 / N is a normalization factor
plt.show()

#print(scope.query('CH1:SCAle?'))
#print(scope.query('DATa:SOUrce?'))
#print(scope.query('DATa:STARt?'))
#print(scope.query('DATa:STOP?'))
#print(scope.query('DATa:WIDth?'))
#print(scope.query('DATa:ENCdg?'))
