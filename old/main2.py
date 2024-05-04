import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt

# Parametri del segnale
Tb = 350e-6  # Durata del bit in secondi
fc = 433.94e6  # Frequenza della portante in Hz
fs = 200e3  # Frequenza di campionamento in Hz
t = np.arange(0, Tb, 1/fs)  # Tempo per un bit
c = np.sqrt(2/Tb) * np.sin(2 * np.pi * fc * t)  # Segnale portante

# Sequenza di bit (esempio lungo)
data = "100010001000111010001110100011101000111010001110100010001000111010001110100011101000111011101110100000000000000000000000000000000000000000000100010001000111010001110100011101000111010001110100010001000111010001110100011101000111010001000100000000000000000000000000000000"

# Genera il segnale del messaggio e ASK
message = np.array([], dtype=np.float32)
ask_sig = np.array([], dtype=np.float32)

for bit in data:
    m_s = np.ones(int(Tb * fs)) if bit == '1' else np.zeros(int(Tb * fs))
    message = np.concatenate((message, m_s))
    ask_sig = np.concatenate((ask_sig, c * m_s))

# Demodulazione del segnale ASK (se necessario)
# In questo esempio non includiamo la demodulazione per focalizzarci sulla generazione del segnale.

# Plot dei segnali
plt.figure(figsize=(12, 6))
plt.plot(ask_sig[:int(fs * len(data) * Tb)])
plt.title('ASK Signal Generated')
plt.xlabel('Samples')
plt.ylabel('Amplitude')
plt.grid(True)
#plt.show()

# Parametri del segnale
fs = 200e3  # Frequenza di campionamento in Hz
cutoff = 100e3  # Frequenza di taglio a 100 kHz
nyquist = 0.5 * fs

if cutoff >= nyquist:
    print("Frequenza di taglio ridotta per adattarsi al limite di Nyquist")
    cutoff = nyquist * 0.9  # Riduci la frequenza di taglio per essere sicuro

norm_cutoff = cutoff / nyquist  # Normalizza la frequenza di taglio

# Coefficenti del filtro Butterworth
b, a = butter(6, norm_cutoff, btype='low', analog=False)

# Genera un segnale di esempio (aggiungi il tuo segnale ASK qui)
t = np.linspace(0, 1, int(fs), endpoint=False)
signal = np.sin(2 * np.pi * 50 * t) + 0.5 * np.sin(2 * np.pi * 120 * t)

# Applica il filtro
filtered_signal = filtfilt(b, a, signal)

# Plot del segnale originale e filtrato
plt.figure(figsize=(10, 6))
plt.plot(t, signal, label='Original Signal')
plt.plot(t, filtered_signal, label='Filtered Signal', linewidth=2)
plt.title('Signal Filtering')
plt.xlabel('Time [seconds]')
plt.ylabel('Amplitude')
plt.legend()
#plt.show()

# Generazione dei campioni I/Q
I_samples = filtered_signal  # Componente in fase
Q_samples = np.zeros_like(I_samples)  # Componente in quadratura

# Converti i campioni in formato raw I/Q U8
max_val = np.max(np.abs(I_samples))  # Trova il valore massimo per la normalizzazione
I_samples_u8 = np.uint8((I_samples / max_val + 1) * 127.5)  # Normalizza e scala
Q_samples_u8 = np.uint8((Q_samples + 1) * 127.5)  # Normalizza e scala (sempre zero)

# Salva i campioni I/Q in un file binario
iq_samples = np.vstack((I_samples_u8, Q_samples_u8)).reshape(-1, order='F')
with open('output.iq', 'wb') as f:
    f.write(iq_samples)

print("File I/Q raw creato con successo.")
