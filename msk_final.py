import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import gaussian, convolve
from scipy.integrate import cumtrapz
from numpy import pi

# Parametri del segnale
sample_rate = 250000  # Frequenza di campionamento in Hz
bit_duration = 0.001  # Durata di ogni bit in secondi
sequence = "00000000001111111111000000000011111111110000000000111111001100000000001111111111000000000011111111110000000000"

# Calcolo del numero di campioni per bit
samples_per_bit = int(sample_rate * bit_duration)

# Funzione per modulazione MSK
def msk_modulation(sequence, sample_rate, bit_duration):
    samples_per_bit = int(sample_rate * bit_duration)
    t = np.arange(0, len(sequence) * bit_duration, 1 / sample_rate)

    I = np.zeros_like(t)
    Q = np.zeros_like(t)

    # Parametri per MSK
    freq_deviation = 0.5 / bit_duration
    phase = 0.0  # Fase iniziale

    for i, bit in enumerate(sequence):
        freq = freq_deviation if bit == '1' else -freq_deviation
        t_bit = np.linspace(i * bit_duration, (i + 1) * bit_duration, samples_per_bit, endpoint=False)

        # Aggiorna le fasi per garantire la continuità
        phase_incr = 2 * np.pi * freq * (t_bit - t_bit[0])
        I[i * samples_per_bit:(i + 1) * samples_per_bit] = np.cos(2 * np.pi * 1000 * t_bit + phase + phase_incr)
        Q[i * samples_per_bit:(i + 1) * samples_per_bit] = np.sin(2 * np.pi * 1000 * t_bit + phase + phase_incr)

        # Aggiorna la fase per il prossimo bit
        phase += phase_incr[-1]

    return I, Q


def gmsk_modulation(data, sample_rate, bt = 0.3):
    samples_per_symbol = int(sample_rate * bit_duration)
    ntaps = 4 * samples_per_symbol
    # Creazione del filtro gaussiano
    gaussian_taps = gaussian(ntaps, std=bt * samples_per_symbol)
    gaussian_taps /= np.sum(gaussian_taps)  # Normalizzazione del filtro
    # Finestra rettangolare
    sqwave = np.ones(samples_per_symbol)
    # Convoluzione per formare il filtro complessivo
    taps = convolve(gaussian_taps, sqwave, mode='full')

    # Modulazione di frequenza
    # Converti i dati in formato NRZ (-1 per '0', +1 per '1')
    nrz_data = 2 * np.array(data) - 1
    # Ripetizione dei simboli per adattarsi ai samples_per_symbol
    nrz_upsampled = np.repeat(nrz_data, samples_per_symbol)
    # Applica il filtro
    filtered_signal = convolve(nrz_upsampled, taps, mode='same')

    # Integrazione per la fase (simula la modulazione di frequenza)
    phase = cumtrapz(filtered_signal, initial=0)

    #La sensibilità nella modulazione di frequenza (FM) nel contesto della GMSK determina quanto la fase del
    #segnale cambia per unità di segnale in ingresso. Nel tuo caso, dove vuoi ottenere una frequenza di modulazione di circa 1000 Hz,

    sensitivity = 0.0251 # (2 * pi * 1000) / sample_rate #0.0251 #pi / 2  # Sensibilità della modulazione FM
    phase *= sensitivity

    # Generazione del segnale modulato
    I = np.cos(phase)
    Q = np.sin(phase)

    return I, Q

# Modulazione MSK
I_msk, Q_msk = msk_modulation(sequence, sample_rate, bit_duration)

# Modulazione GMSK
I_gmsk, Q_gmsk = gmsk_modulation(np.array(list(sequence), dtype=int), sample_rate, bit_duration)

# Normalizza e converti in formato uint8 per MSK
I_msk_u8 = np.uint8((I_msk / np.max(np.abs(I_msk)) + 1) * 127.5)
Q_msk_u8 = np.uint8((Q_msk / np.max(np.abs(Q_msk)) + 1) * 127.5)

# Intercala I e Q per MSK
iq_samples_msk = np.empty(2 * len(I_msk), dtype=np.uint8)
iq_samples_msk[0::2] = I_msk_u8
iq_samples_msk[1::2] = Q_msk_u8

# Salva il segnale I/Q in un file per MSK
with open('msk_signal.iq', 'wb') as f:
    f.write(iq_samples_msk.tobytes())

print("File .iq creato con successo per il segnale MSK")

# Normalizza e converti in formato uint8 per GMSK
I_gmsk_u8 = np.uint8((I_gmsk / np.max(np.abs(I_gmsk)) + 1) * 127.5)
Q_gmsk_u8 = np.uint8((Q_gmsk / np.max(np.abs(Q_gmsk)) + 1) * 127.5)

# Intercala I e Q per GMSK
iq_samples_gmsk = np.empty(2 * len(I_gmsk), dtype=np.uint8)
iq_samples_gmsk[0::2] = I_gmsk_u8
iq_samples_gmsk[1::2] = Q_gmsk_u8

# Salva il segnale I/Q in un file per GMSK
with open('gmsk_signal.iq', 'wb') as f:
    f.write(iq_samples_gmsk.tobytes())

print("File .iq creato con successo per il segnale GMSK")

# Plot del segnale MSK e GMSK
plt.figure(figsize=(12, 10))

plt.subplot(4, 2, 1)
plt.plot(I_msk, label="I (MSK)")
plt.title("Segnale MSK - Componente I")
plt.xlabel("Campioni")
plt.ylabel("Ampiezza")
plt.grid(True)
plt.legend()

plt.subplot(4, 2, 2)
plt.plot(Q_msk, label="Q (MSK)")
plt.title("Segnale MSK - Componente Q")
plt.xlabel("Campioni")
plt.ylabel("Ampiezza")
plt.grid(True)
plt.legend()

plt.subplot(4, 2, 3)
plt.plot(np.angle(I_msk + 1j * Q_msk), label="Fase Complessiva (MSK)")
plt.title("Segnale MSK - Fase Complessiva")
plt.xlabel("Campioni")
plt.ylabel("Fase (radiani)")
plt.grid(True)
plt.legend()

plt.subplot(4, 2, 4)
plt.scatter(I_msk, Q_msk, s=1, label="Costellazione MSK")
plt.title("Diagramma di Costellazione MSK")
plt.xlabel("In-Phase (I)")
plt.ylabel("Quadrature (Q)")
plt.grid(True)
plt.legend()

plt.subplot(4, 2, 5)
plt.plot(I_gmsk, label="I (GMSK)")
plt.title("Segnale GMSK - Componente I")
plt.xlabel("Campioni")
plt.ylabel("Ampiezza")
plt.grid(True)
plt.legend()

plt.subplot(4, 2, 6)
plt.plot(Q_gmsk, label="Q (GMSK)")
plt.title("Segnale GMSK - Componente Q")
plt.xlabel("Campioni")
plt.ylabel("Ampiezza")
plt.grid(True)
plt.legend()

plt.subplot(4, 2, 7)
plt.plot(np.angle(I_gmsk + 1j * Q_gmsk), label="Fase Complessiva (GMSK)")
plt.title("Segnale GMSK - Fase Complessiva")
plt.xlabel("Campioni")
plt.ylabel("Fase (radiani)")
plt.grid(True)
plt.legend()

plt.subplot(4, 2, 8)
plt.scatter(I_gmsk, Q_gmsk, s=1, label="Costellazione GMSK")
plt.title("Diagramma di Costellazione GMSK")
plt.xlabel("In-Phase (I)")
plt.ylabel("Quadrature (Q)")
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.show()
