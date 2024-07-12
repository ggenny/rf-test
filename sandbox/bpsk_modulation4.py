import numpy as np
import matplotlib.pyplot as plt

# Parametri del segnale
sample_rate = 250000  # Frequenza di campionamento in Hz
bit_duration = 0.001  # Durata di ogni bit in secondi
sequence = "00000000001111111111000000000011111111110000000000111111001100000000001111111111000000000011111111110000000000"

# Calcolo del numero di campioni per bit
samples_per_bit = int(sample_rate * bit_duration)

# Inizializza il segnale I (in fase)
I = np.zeros(samples_per_bit * len(sequence))
Q = np.zeros_like(I)

for i, bit in enumerate(sequence):
    phase = 0 if bit == '1' else np.pi  # Fase 0 per '1' e π per '0'
    t = np.linspace(i * samples_per_bit / sample_rate, (i + 1) * samples_per_bit / sample_rate, samples_per_bit, endpoint=False)
    I[i * samples_per_bit:(i + 1) * samples_per_bit] = np.cos(2 * np.pi * 1000 * t + phase)
    Q[i * samples_per_bit:(i + 1) * samples_per_bit] = np.cos(2 * np.pi * 1000 * t + phase)

# Normalizza e converti in formato uint8
I_u8 = np.uint8((I / np.max(np.abs(I)) + 1) * 127.5)
Q_u8 = np.uint8((Q / np.max(np.abs(Q)) + 1) * 127.5)

# Intercala I e Q
iq_samples = np.empty(2 * len(I), dtype=np.uint8)
iq_samples[0::2] = I_u8
iq_samples[1::2] = Q_u8

# Salva il segnale I/Q in un file (Q non è usato in BPSK puro, quindi rimane a zero)
with open('bpsk_signal.iq', 'wb') as f:
    f.write(iq_samples.tobytes())

print("File .iq creato con successo per il segnale BPSK")

# # Calcolo della FFT per analizzare lo spettro del segnale
# fft_signal = np.fft.fft(I)
# freqs = np.fft.fftfreq(len(I), 1/sample_rate)
#
# # Plot dello spettro del segnale BPSK
# plt.figure()
# plt.plot(freqs, np.abs(fft_signal))
# plt.title('Spectrum of BPSK Signal')
# plt.xlabel('Frequency (Hz)')
# plt.ylabel('Magnitude')
# plt.grid(True)
# plt.show()
#
# plt.figure()
# plt.plot(I[:5*samples_per_bit])  # Visualizza i primi 5 bit del segnale
# plt.title('Time Domain Signal for First 5 Bits')
# plt.xlabel('Sample Number')
# plt.ylabel('Amplitude')
# plt.grid(True)
# plt.show()
#
# # Genera una componente Q fittizia per simulare la costellazione BPSK
# Q = np.zeros_like(I)
# plt.figure()
# plt.scatter(I[::samples_per_bit], Q[::samples_per_bit], color='red')
# plt.title('BPSK Constellation Diagram')
# plt.xlabel('In-phase (I)')
# plt.ylabel('Quadrature (Q)')
# plt.grid(True)
# plt.axis('equal')
# plt.show()
#
# autocorr = np.correlate(I, I, mode='full')
# plt.figure()
# plt.plot(autocorr[len(I)-100:len(I)+100])  # Visualizza un segmento dell'autocorrelazione
# plt.title('Autocorrelation of BPSK Signal')
# plt.xlabel('Lag')
# plt.ylabel('Correlation')
# plt.grid(True)
# plt.show()
#
# # Calcola la fase del segnale
# phases = np.arctan2(Q, I)
# plt.figure()
# plt.plot(phases[:10 * samples_per_bit])  # Visualizza le fasi dei primi 10 bit
# plt.title('Phase Transitions in BPSK Signal')
# plt.xlabel('Sample Number')
# plt.ylabel('Phase (radians)')
# plt.grid(True)
# plt.show()
#
# # Usa una finestra di Blackman per una migliore risoluzione spettrale
# windowed_signal = I * np.blackman(len(I))
# fft_windowed = np.fft.fft(windowed_signal)
# plt.figure()
# plt.plot(freqs, np.abs(fft_windowed))
# plt.title('Spectrum with Blackman Window')
# plt.xlabel('Frequency (Hz)')
# plt.ylabel('Magnitude')
# plt.grid(True)
# plt.show()
