import numpy as np
import matplotlib.pyplot as plt
from scipy.special import erfc

# Parametri del segnale
Ns = 4
no_of_bits = int(1e4)
bits_in = np.random.randint(0, 2, no_of_bits)
differential_bits = np.abs(np.diff(np.concatenate(([0], bits_in))))
bipolar_symbols = differential_bits * 2 - 1
symbols_oversampled = np.repeat(bipolar_symbols, Ns) / Ns
cumulative_phase = (np.pi / 2) * np.cumsum(symbols_oversampled)
tx_signal = np.exp(1j * cumulative_phase)

# Aggiunta di rumore AWGN
Eb = Ns
EbNodB = 10
EbNo = 10**(EbNodB / 10)
sigma = np.sqrt(Eb / (2 * EbNo))
AWGN_noise = (np.random.randn(Ns * no_of_bits) + 1j * np.random.randn(Ns * no_of_bits)) * sigma
rx_signal = tx_signal + AWGN_noise

# Demodulazione
sin_waveform = np.sin(np.arange(1, Ns + 1) * (np.pi / (2 * Ns)))
rx_real = np.concatenate((np.real(rx_signal[Ns:]), np.zeros(Ns)))
rx_imag = np.imag(rx_signal)

rx_I_metric = np.zeros(no_of_bits // 2)
rx_Q_metric = np.zeros(no_of_bits // 2)

for n in range(no_of_bits // 2):
    rx_I_metric[n] = np.dot(sin_waveform, rx_real[n * Ns: (n + 1) * Ns])
    rx_Q_metric[n] = np.dot(sin_waveform, rx_imag[n * Ns: (n + 1) * Ns])

n = np.arange(1, no_of_bits // 2 + 1)
rx_I_metric = (-1)**(n + 1) * rx_I_metric
rx_Q_metric = (-1)**(n + 1) * rx_Q_metric

rx = np.concatenate((rx_Q_metric, rx_I_metric))
rx = np.transpose(rx.reshape(-1, 1)).flatten()

demodulated_symbols = np.sign(rx)
bits_out = demodulated_symbols * 0.5 + 0.5

# Calcolo del BER
ber_simulated = np.sum(bits_out != bits_in) / no_of_bits
ber_theoretical = 0.5 * erfc(np.sqrt(EbNo))

print("BER Simulato:", ber_simulated)
print("BER Teorico:", ber_theoretical)

# Plot del segnale MSK e del diagramma di costellazione
plt.figure(figsize=(12, 10))

plt.subplot(4, 1, 1)
plt.plot(np.real(tx_signal[:500]), label="I (MSK)")
plt.title("Segnale MSK - Componente I")
plt.xlabel("Campioni")
plt.ylabel("Ampiezza")
plt.grid(True)
plt.legend()

plt.subplot(4, 1, 2)
plt.plot(np.imag(tx_signal[:500]), label="Q (MSK)")
plt.title("Segnale MSK - Componente Q")
plt.xlabel("Campioni")
plt.ylabel("Ampiezza")
plt.grid(True)
plt.legend()

# Calcolo della fase complessiva
phase_msk = np.angle(tx_signal)

plt.subplot(4, 1, 3)
plt.plot(phase_msk[:500], label="Fase Complessiva (MSK)")
plt.title("Segnale MSK - Fase Complessiva")
plt.xlabel("Campioni")
plt.ylabel("Fase (radiani)")
plt.grid(True)
plt.legend()

# Diagramma di costellazione
plt.subplot(4, 1, 4)
plt.scatter(np.real(tx_signal[:1000]), np.imag(tx_signal[:1000]), s=1, label="Costellazione MSK")
plt.title("Diagramma di Costellazione MSK")
plt.xlabel("In-Phase (I)")
plt.ylabel("Quadrature (Q)")
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.show()
