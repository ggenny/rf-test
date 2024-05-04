import numpy as np

# Parametri
fs = 250000  # Frequenza di campionamento in Hz
f_c = 433944000  # Frequenza della portante in Hz
duration = 5e-3  # Durata di ogni singola trasmissione del segnale in secondi
data =  "1000100010001110100011101000111010001110100011101000100010001110100011101000111010001110100010001"
data2 = "1000100010001110100011101000111010001110100011101000100010001110100011101000111010001110111011101"
repeat_count = 10  # Numero di ripetizioni del segnale

# Calcolo dei parametri del segnale
samples_per_bit = int(fs * duration / len(data))
n_samples = samples_per_bit * len(data)
t = np.linspace(0, duration, n_samples, endpoint=False)

# Array che conterrà il segnale finale con ripetizioni e pause
final_signal = np.array([], dtype=np.float32)

# Generazione del segnale ASK ripetuto
for _ in range(repeat_count):
    signal = np.zeros(n_samples)  # Reset del segnale per ogni ripetizione
    for i, bit in enumerate(data):
        if bit == '1':
            signal[i * samples_per_bit:(i + 1) * samples_per_bit] = np.sin(2 * np.pi * f_c * t[i * samples_per_bit:(i + 1) * samples_per_bit])
    
    # Aggiungi il segnale generato all'array finale
    final_signal = np.concatenate((final_signal, signal))
    
    # Aggiungi una pausa della stessa durata del segnale
    final_signal = np.concatenate((final_signal, np.zeros(n_samples * 10)))

for _ in range(repeat_count):
    signal = np.zeros(n_samples)  # Reset del segnale per ogni ripetizione
    for i, bit in enumerate(data2):
        if bit == '1':
            signal[i * samples_per_bit:(i + 1) * samples_per_bit] = np.sin(2 * np.pi * f_c * t[i * samples_per_bit:(i + 1) * samples_per_bit])
    
    # Aggiungi il segnale generato all'array finale
    final_signal = np.concatenate((final_signal, signal))
    
    # Aggiungi una pausa della stessa durata del segnale
    final_signal = np.concatenate((final_signal, np.zeros(n_samples * 10)))

# Converti float I, Q in U8
I_u8 = np.uint8((final_signal + 1) * 127.5)  # normalizza da [-1,1] a [0,255]
Q_u8 = np.uint8(np.zeros_like(final_signal))  # Q componente non usata, mantenuta a zero

# Intercalare I e Q per il formato I/Q
iq_u8 = np.empty(2 * len(final_signal), dtype=np.uint8)
iq_u8[0::2] = I_u8
iq_u8[1::2] = Q_u8

# Salva il file raw
with open('output.iq', 'wb') as f:
    f.write(iq_u8.tobytes())

print("File I/Q U8 raw creato con successo per trasmissione a 433.94 MHz.")

