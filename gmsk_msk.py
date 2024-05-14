import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import gausspulse

# Parametri del segnale
sample_rate = 250000  # Frequenza di campionamento in Hz
bit_duration = 0.001  # Durata di ogni bit in secondi
sequence = "00000000001111111111000000000011111111110000000000111111001100000000001111111111000000000011111111110000000000"
#sequence = "111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111"
#sequence = "00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"
# Calcolo del numero di campioni per bit
samples_per_bit = int(sample_rate * bit_duration)

# Funzione per la modulazione MSK
def msk_modulation(sequence, sample_rate, bit_duration):
    samples_per_bit = int(sample_rate * bit_duration)
    t = np.arange(0, len(sequence) * bit_duration, 1 / sample_rate)

    I = np.zeros_like(t)
    Q = np.zeros_like(t)

    for i, bit in enumerate(sequence):
        phase_shift = np.pi * (int(bit) - 0.5)  # π/2 per '1' e -π/2 per '0'
        t_bit = np.linspace(i * bit_duration, (i + 1) * bit_duration, samples_per_bit, endpoint=False)
        I[i * samples_per_bit:(i + 1) * samples_per_bit] = np.cos(2 * np.pi * 1000 * t_bit + phase_shift)
        Q[i * samples_per_bit:(i + 1) * samples_per_bit] = np.sin(2 * np.pi * 1000 * t_bit + phase_shift)

    return I, Q

# Funzione per la modulazione GMSK
def gmsk_modulation(sequence, sample_rate, bit_duration, bt=0.3):
    samples_per_bit = int(sample_rate * bit_duration)
    t = np.arange(0, len(sequence) * bit_duration, 1 / sample_rate)

    I = np.zeros_like(t)
    Q = np.zeros_like(t)

    # Genera la forma d'onda MSK di base
    I, Q = msk_modulation(sequence, sample_rate, bit_duration)

    # Applicazione del filtro gaussiano
    pulse = gausspulse(t, fc=1 / bit_duration, bw=bt, retquad=False)
    I_filtered = np.convolve(I, pulse, mode='same')
    Q_filtered = np.convolve(Q, pulse, mode='same')

    return I_filtered, Q_filtered

# Modulazione MSK
I_msk, Q_msk = msk_modulation(sequence, sample_rate, bit_duration)

# Modulazione GMSK
I_gmsk, Q_gmsk = gmsk_modulation(sequence, sample_rate, bit_duration)

# Normalizza e converte in formato uint8
def normalize_and_convert(I, Q):
    I_u8 = np.uint8((I / np.max(np.abs(I)) + 1) * 127.5)
    Q_u8 = np.uint8((Q / np.max(np.abs(Q)) + 1) * 127.5)
    iq_samples = np.empty(2 * len(I), dtype=np.uint8)
    iq_samples[0::2] = I_u8
    iq_samples[1::2] = Q_u8
    return iq_samples


iq_samples_msk = normalize_and_convert(I_msk, Q_msk)
iq_samples_gmsk = normalize_and_convert(I_gmsk, Q_gmsk)

# Salva i segnali I/Q in file
with open('msk_signal.iq', 'wb') as f:
    f.write(iq_samples_msk.tobytes())

with open('gmsk_signal.iq', 'wb') as f:
    f.write(iq_samples_gmsk.tobytes())

print("File .iq creati con successo per i segnali MSK e GMSK")
