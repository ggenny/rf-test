import numpy as np
import scipy.signal as signal

# Parametri del segnale
sample_rate = 200000  # Frequenza di campionamento in Hz
duration = 1  # Durata del segnale in secondi
frequency = 100  # Frequenza della portante in Hz per la generazione del segnale
cutoff_frequency = 300  # Frequenza di taglio del filtro passa-basso in Hz

# Genera il tempo
t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)

# Genera il segnale portante (componente I)
I = np.sin(2 * np.pi * frequency * t)
Q = np.zeros_like(I)  # Componente Q a zero

# Design del filtro passa-basso
nyquist = 0.5 * sample_rate
norm_cutoff = cutoff_frequency / nyquist
b, a = signal.butter(4, norm_cutoff, btype='low')  # Filtro Butterworth di 4° ordine

# Applica il filtro a I e Q
I_filtered = signal.filtfilt(b, a, I)
Q_filtered = signal.filtfilt(b, a, Q)  # La componente Q rimane zero

# Converti i segnali in unsigned 8-bit format (range da 0 a 255)
I_u8 = np.uint8((I_filtered + 1) * 127.5)
Q_u8 = np.uint8((Q_filtered + 1) * 127.5)

# Intercala I e Q per il formato I/Q
iq_samples = np.empty(2 * len(I), dtype=np.uint8)
iq_samples[0::2] = I_u8
iq_samples[1::2] = Q_u8

# Salva il segnale I/Q in un file
with open('record_filtered.iq', 'wb') as f:
    f.write(iq_samples.tobytes())

print("File .iq con filtro applicato creato con successo.")
