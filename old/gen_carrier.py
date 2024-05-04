import numpy as np

# Parametri del segnale
sample_rate = 200000  # Frequenza di campionamento in Hz
duration = 1  # Durata del segnale in secondi
frequency = 100  # Frequenza della portante in Hz per la generazione del segnale

# Genera il tempo
t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)

# Genera il segnale portante (componente I) e imposta la componente Q a zero
I = np.sin(2 * np.pi * frequency * t)
Q = np.zeros_like(I)

# Converti i segnali in unsigned 8-bit format (range da 0 a 255)
I_u8 = np.uint8((I + 1) * 127.5)  # Normalizza da -1->1 a 0->255
Q_u8 = np.uint8((Q + 1) * 127.5)  # Normalizza da -1->1 a 0->255

# Intercala I e Q per il formato I/Q
iq_samples = np.empty(2 * len(I), dtype=np.uint8)
iq_samples[0::2] = I_u8
iq_samples[1::2] = Q_u8

# Salva il segnale I/Q in un file
with open('record.iq', 'wb') as f:
    f.write(iq_samples.tobytes())

print("File .iq creato con successo.")
