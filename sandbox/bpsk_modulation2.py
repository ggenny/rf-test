import numpy as np

# Parametri del segnale
sample_rate = 200000  # Frequenza di campionamento in Hz
bit_duration = 0.005  # Durata di ogni bit in secondi (ad esempio, 5 ms per bit)
sequence = "10001000100010001000101110001001110001011100110111000100010001000100010001001101100010000000000000000000000000000000000000000000000000000000000000111111111111111111111111111111111111111111111111111111111111111111111111111110000000000000000000000000000000000000000000000000000000000000000010001000100010001000101110001001110001011100110111000100010001000100010001001101100010000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"  # Sequenza binaria di esempio

# Calcolo del numero di campioni per bit
samples_per_bit = int(sample_rate * bit_duration)

# Inizializza il segnale I (in fase)
I = np.zeros(samples_per_bit * len(sequence))

# Genera il segnale BPSK
for i, bit in enumerate(sequence):
    phase = 0 if bit == '1' else np.pi  # Fase 0 per '0' e π per '1'
    t = np.linspace(i * samples_per_bit / sample_rate, (i + 1) * samples_per_bit / sample_rate, samples_per_bit, endpoint=False)
    I[i * samples_per_bit:(i + 1) * samples_per_bit] = np.cos(2 * np.pi * 10000 * t + phase)  # Frequenza di portante a 1000 Hz

# Normalizza e converti in formato uint8
I_u8 = np.uint8((I + 1) * 127.5)  # Mappatura da -1->1 a 0->255

# Salva il segnale I/Q in un file (Q non è usato in BPSK puro, quindi rimane a zero)
with open('bpsk_signal.iq', 'wb') as f:
    iq_samples = np.zeros(2 * len(I), dtype=np.uint8)
    iq_samples[0::2] = I_u8  # Solo componente I, Q è zero
    f.write(iq_samples)

print("File .iq creato con successo per il segnale BPSK.")
