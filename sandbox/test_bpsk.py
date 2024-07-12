import numpy as np
import matplotlib.pyplot as plt

# Parametri del segnale
sample_rate = 250000  # Frequenza di campionamento in Hz
bit_duration = 0.001  # Durata di ogni bit in secondi
sequence = "00000000001111111111000000000011111111110000000000111111001100000000001111111111000000000011111111110000000000"

# Calcolo del numero di campioni per bit
samples_per_bit = int(sample_rate * bit_duration)

# Inizializza il segnale I (in fase) e Q (in quadratura)
I = np.zeros(samples_per_bit * len(sequence))
Q = np.zeros_like(I)

for i, bit in enumerate(sequence):
    phase = 0 if bit == '1' else np.pi  # Fase 0 per '1' e π per '0'
    t = np.linspace(i * samples_per_bit / sample_rate, (i + 1) * samples_per_bit / sample_rate, samples_per_bit, endpoint=False)
    I[i * samples_per_bit:(i + 1) * samples_per_bit] = np.cos(2 * np.pi * 1000 * t + phase)
    Q[i * samples_per_bit:(i + 1) * samples_per_bit] = np.zeros_like(t)  # Q rimane zero per BPSK

# Calcolo FFT per analisi dello spettro
fft_I = np.fft.fft(I)
fft_Q = np.fft.fft(Q)
freqs = np.fft.fftfreq(len(fft_I), 1/sample_rate)

# Visualizza lo spettro del segnale
plt.figure(figsize=(12, 6))
plt.plot(freqs, np.abs(fft_I), label='I component')
plt.plot(freqs, np.abs(fft_Q), label='Q component')
plt.xlim(-5000, 5000)
plt.xlabel('Frequency (Hz)')
plt.ylabel('Magnitude')
plt.title('Spectrum of BPSK Signal')
plt.legend()
plt.grid()
plt.show()

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
