import numpy as np

# Parametri del segnale
sample_rate = 200000  # Frequenza di campionamento in Hz
duration = 2  # Durata del segnale in secondi
sequence = "1000100010001000100010111000100111000101110011011100010001000100010001000100110110001000000000000000000000000000000000000000000000000000100010001000100010001011100010011100010111001101110001000100010001000100010011011000100000000000000000000000000000000000000000000000000000000000000000000001000100010001000100010111000100111000101110011011100010001000100010001000100110110001000000000000000000000000000000000000000000000000000000000000000000000000000000001000100010001000100010111000100111000101110011011100010001000100010001000100110110001000000000000000000000000000000000000000000000000000000000000000000000000000000010001000100010001000101110001001110001011100110111000100010001000100010001001101100010000000000000000000000000000000000000000000000000000000000000000000000000000000"

# Genera il segnale BPSK
samples_per_bit = int(sample_rate * duration / len(sequence))
I = np.zeros(samples_per_bit * len(sequence))

for i, bit in enumerate(sequence):
    phase = 0 if bit == '0' else np.pi  # 0 o π in base al bit
    t = np.linspace(i * samples_per_bit / sample_rate, (i + 1) * samples_per_bit / sample_rate, samples_per_bit, endpoint=False)
    I[i * samples_per_bit:(i + 1) * samples_per_bit] = np.sin(2 * np.pi * 1000 * t + phase)  # Usiamo una frequenza di portante di 1000 Hz

# Normalizza e converti in formato uint8
I_u8 = np.uint8((I / np.max(np.abs(I)) + 1) * 127.5)

# Intercala I e Q (Q non usato in BPSK puro, quindi è zero)
Q_u8 = np.zeros_like(I_u8)

iq_samples = np.empty(2 * len(I), dtype=np.uint8)
iq_samples[0::2] = I_u8
iq_samples[1::2] = Q_u8

# Salva il segnale I/Q in un file
with open('bpsk_signal.iq', 'wb') as f:
    f.write(iq_samples.tobytes())

print("File .iq creato con successo per il segnale BPSK.")
