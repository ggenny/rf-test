import numpy as np

# Parametri del segnale
sample_rate = 200000  # Frequenza di campionamento in Hz
duration = 1  # Durata del segnale in secondi
delta_f = 10e3  # Differenza di frequenza per FSK, 10kHz
center_frequency = 433.94e6  # Frequenza centrale in Hz

# Frequenze relative
f0 = -delta_f  # Frequenza per il bit '0'
f1 = delta_f   # Frequenza per il bit '1'
sequence = "1000100010001000100010111000100111000101110011011100010001000100010001000100110110001000000000000000000000000000000000000000000000000000100010001000100010001011100010011100010111001101110001000100010001000100010011011000100000000000000000000000000000000000000000000000000000000000000000000000001000100010001000100010111000100111000101110011011100010001000100010001000100110110001000000000000000000000000000000000000000000000000000000000000000000000000000001000100010001000100010111000100111000101110011011100010001000100010001000100110110001000000000000000000000000000000000000000000000000000000000000000000000000000000010001000100010001000101110001001110001011100110111000100010001000100010001001101100010000000000000000000000000000000000000000000000000000000000000000000000000000000000000010001000100010001000101110001001110001011100110111000100010001000100010001001101100010000000000000000000000000000000000000000000000000000000000000000000000000000000"

# Genera il segnale FSK
samples_per_bit = int(sample_rate * duration / len(sequence))
I = np.zeros(samples_per_bit * len(sequence))
Q = np.zeros_like(I)

for i, bit in enumerate(sequence):
    f = f0 if bit == '0' else f1
    t = np.linspace(i * samples_per_bit / sample_rate, (i + 1) * samples_per_bit / sample_rate, samples_per_bit, endpoint=False)
    I[i * samples_per_bit:(i + 1) * samples_per_bit] = np.sin(2 * np.pi * f * t)
    Q[i * samples_per_bit:(i + 1) * samples_per_bit] = np.cos(2 * np.pi * f * t)

# Normalizza e converti in formato uint8
I_u8 = np.uint8((I / np.max(np.abs(I)) + 1) * 127.5)
Q_u8 = np.uint8((Q / np.max(np.abs(Q)) + 1) * 127.5)

# Intercala I e Q
iq_samples = np.empty(2 * len(I), dtype=np.uint8)
iq_samples[0::2] = I_u8
iq_samples[1::2] = Q_u8

# Salva il segnale I/Q in un file
with open('fsk_signal.iq', 'wb') as f:
    f.write(iq_samples.tobytes())

print("File .iq creato con successo per il segnale FSK.")
