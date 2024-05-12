import numpy as np

# Parametri del segnale
sample_rate = 200000  # Frequenza di campionamento in Hz
bit_duration = 0.0001  # Durata di ogni bit in secondi (5 ms per bit)
sequence = "00000000000000000000000000000000000000000000000000000000000000010001000100010001000101110001001110001011100110111000100010001000100010001001101100010000000000000000000000000000000000000000000011111111111111111111111111111111111111111111111111000000000000000000000000000000000000000000000000111111111111111111111111111111111111111111111111111111111"  # Sequenza binaria di esempio
sequence = "000000000000000000000000000000000000000000111111111111110001111111111110000000000000000000000000000000000000000001111111111111110001111111111100000000000000000000000000000000000000000011111111111111100011111111111"
# Calcolo del numero di campioni per bit
samples_per_bit = int(sample_rate * bit_duration)

# Inizializza il segnale I (in fase)
I = np.zeros(samples_per_bit * len(sequence))

# Genera il segnale BPSK con ampiezza ridotta
amp_factor = 1.0  # Riduci l'ampiezza del 50%

for i, bit in enumerate(sequence):
    phase = 0 if bit == '1' else np.pi  # Fase 0 per '0' e π per '1'
    t = np.linspace(i * samples_per_bit / sample_rate, (i + 1) * samples_per_bit / sample_rate, samples_per_bit, endpoint=False)
    I[i * samples_per_bit:(i + 1) * samples_per_bit] = amp_factor * np.cos(2 * np.pi * 10000 * t + phase)  # Usiamo una frequenza di portante di 1000 Hz

# Normalizza e converti in formato uint8
I_u8 = np.uint8((I + 1) * 127.5)  # Mappatura da -1->1 a 0->255

# Salva il segnale I/Q in un file (Q non è usato in BPSK puro, quindi rimane a zero)
with open('bpsk_signal.iq', 'wb') as f:
    iq_samples = np.zeros(2 * len(I), dtype=np.uint8)
    iq_samples[0::2] = I_u8  # Solo componente I, Q è zero
    f.write(iq_samples)

print("File .iq creato con successo per il segnale BPSK con ampiezza ridotta.")
