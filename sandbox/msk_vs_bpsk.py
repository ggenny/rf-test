import numpy as np
import matplotlib.pyplot as plt

# Parametri del segnale
sample_rate = 250000  # Frequenza di campionamento in Hz
bit_duration = 0.001  # Durata di ogni bit in secondi
sequence = "1011001110001111"

# Calcolo del numero di campioni per bit
samples_per_bit = int(sample_rate * bit_duration)

# BPSK
def bpsk_modulation(sequence, sample_rate, bit_duration):
    samples_per_bit = int(sample_rate * bit_duration)
    I = np.zeros(samples_per_bit * len(sequence))
    Q = np.zeros_like(I)

    for i, bit in enumerate(sequence):
        phase = 0 if bit == '1' else np.pi  # Fase 0 per '1' e π per '0'
        t = np.linspace(i * bit_duration, (i + 1) * bit_duration, samples_per_bit, endpoint=False)
        I[i * samples_per_bit:(i + 1) * samples_per_bit] = np.cos(2 * np.pi * 1000 * t + phase)
        Q[i * samples_per_bit:(i + 1) * samples_per_bit] = np.cos(2 * np.pi * 1000 * t + phase)
    return I, Q

# MSK
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

# Modulazione BPSK
I_bpsk, Q_bpsk = bpsk_modulation(sequence, sample_rate, bit_duration)

# Modulazione MSK
I_msk, Q_msk = msk_modulation(sequence, sample_rate, bit_duration)

# Plot dei segnali
plt.figure(figsize=(12, 6))

plt.subplot(2, 1, 1)
plt.plot(I_bpsk[:5*samples_per_bit], label="I (BPSK)")
plt.title("Segnale BPSK")
plt.xlabel("Campioni")
plt.ylabel("Ampiezza")
plt.grid(True)
plt.legend()

plt.subplot(2, 1, 2)
plt.plot(I_msk[:5*samples_per_bit], label="I (MSK)")
plt.plot(Q_msk[:5*samples_per_bit], label="Q (MSK)")
plt.title("Segnale MSK")
plt.xlabel("Campioni")
plt.ylabel("Ampiezza")
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.show()
