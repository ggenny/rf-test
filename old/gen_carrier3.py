import numpy as np

# sudo ../rpitx/sendiq -s 200000 -f 433.958e6 -t u8 -i repeated_ask_signal.iq

# Parametri del segnale
sample_rate = 200000  # Frequenza di campionamento in Hz
bit_duration = 0.00035  # Durata di ogni bit in secondi (350 microsecondi)
frequency = 1000  # Frequenza della portante in Hz
sequence = "1000100010001110100011101000111010001110100011101000100010001110100011101000111010001110111011101"
repetitions = 10  # Numero di ripetizioni
pause_duration_ms = 10  # Durata della pausa in millisecondi

# Calcola il numero di campioni per la pausa
pause_samples = int(sample_rate * pause_duration_ms / 1000)

# Crea un array per il segnale I e Q con spazio sufficiente per ripetizioni e pause
total_samples = repetitions * (len(sequence) * int(bit_duration * sample_rate) + pause_samples)
I = np.zeros(total_samples)
Q = np.zeros_like(I)  # Q rimane zero per un segnale ASK

# Compila il segnale con ripetizioni e pause
current_sample = 0
for _ in range(repetitions):
    for bit in sequence:
        num_samples = int(bit_duration * sample_rate)
        t = np.linspace(0, bit_duration, num_samples, endpoint=False)
        if bit == '1':
            I[current_sample:current_sample + num_samples] = np.sin(2 * np.pi * frequency * t)
        current_sample += num_samples
    current_sample += pause_samples  # Aggiungi pause dopo ogni ripetizione del segnale

# Converti i segnali in unsigned 8-bit format (range da 0 a 255)
I_u8 = np.uint8((I + 1) * 127.5)
Q_u8 = np.uint8((Q + 1) * 127.5)

# Intercala I e Q per il formato I/Q
iq_samples = np.empty(2 * len(I), dtype=np.uint8)
iq_samples[0::2] = I_u8
iq_samples[1::2] = Q_u8

# Salva il segnale I/Q in un file
with open('repeated_ask_signal.iq', 'wb') as f:
    f.write(iq_samples.tobytes())

print("File .iq creato con successo per il segnale ASK ripetuto con pause.")

