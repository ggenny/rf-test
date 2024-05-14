import numpy as np
import matplotlib.pyplot as plt

# Parametri del segnale
sample_rate = 250000  # Frequenza di campionamento in Hz
bit_duration = 0.001  # Durata di ogni bit in secondi
sequence = "1011001110001111"

# Calcolo del numero di campioni per bit
samples_per_bit = int(sample_rate * bit_duration)


def msk_modulation(sequence, sample_rate, bit_duration):
    samples_per_bit = int(sample_rate * bit_duration)
    t = np.linspace(0, len(sequence) * bit_duration, len(sequence) * samples_per_bit, endpoint=False)

    I = np.zeros_like(t)
    Q = np.zeros_like(t)

    # Parametri per MSK
    freq_deviation = 0.25 / bit_duration
    phase = 0.0  # Fase iniziale

    for i, bit in enumerate(sequence):
        freq = freq_deviation if bit == '1' else -freq_deviation
        t_bit = np.linspace(i * bit_duration, (i + 1) * bit_duration, samples_per_bit, endpoint=False)

        # Aggiorna le fasi per garantire la continuità
        phase_incr = 2 * np.pi * freq * (t_bit - t_bit[0]) + phase
        I[i * samples_per_bit:(i + 1) * samples_per_bit] = np.cos(2 * np.pi * 1000 * t_bit + phase_incr)
        Q[i * samples_per_bit:(i + 1) * samples_per_bit] = np.sin(2 * np.pi * 1000 * t_bit + phase_incr)

        # Aggiorna la fase per il prossimo bit
        phase = phase_incr[-1]

    return I, Q


# Modulazione MSK
I_msk, Q_msk = msk_modulation(sequence, sample_rate, bit_duration)

# Calcolo della fase complessiva
phase_msk = np.angle(I_msk + 1j * Q_msk)

# Plot del segnale MSK
plt.figure(figsize=(12, 8))

plt.subplot(3, 1, 1)
plt.plot(I_msk[:5 * samples_per_bit], label="I (MSK)")
plt.title("Segnale MSK - Componente I")
plt.xlabel("Campioni")
plt.ylabel("Ampiezza")
plt.grid(True)
plt.legend()

plt.subplot(3, 1, 2)
plt.plot(Q_msk[:5 * samples_per_bit], label="Q (MSK)")
plt.title("Segnale MSK - Componente Q")
plt.xlabel("Campioni")
plt.ylabel("Ampiezza")
plt.grid(True)
plt.legend()

plt.subplot(3, 1, 3)
plt.plot(phase_msk[:5 * samples_per_bit], label="Fase Complessiva (MSK)")
plt.title("Segnale MSK - Fase Complessiva")
plt.xlabel("Campioni")
plt.ylabel("Fase (radiani)")
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.show()
