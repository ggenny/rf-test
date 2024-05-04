import struct

# Parametri
frequency_hz = 433944000  # Frequenza di trasmissione in Hz per bit '1'
duration_ns = 350000  # Durata di ogni bit in nanosecondi
sequence = "1000100010001110100011101000111010001110100011101000100010001110100011101000111010001110111011101"
sequence2 ="1000100010001110100011101000111010001110100011101000100010001110100011101000111010001110100010001"

freq_bytes = struct.pack('d', frequency_hz)  # 'd' per double precision float

# Creazione del file .ft
with open('doorbell.ft', 'wb') as f:
    # Il primo chunk potrebbe essere un valore di offset, se necessario
    # Per semplicità, assumiamo che non ci sia un offset iniziale necessario
    for bit in sequence:
        if bit == '1':
            amplitude = struct.pack('f', 10)  # 'd' per double precision float
        else:
            amplitude = struct.pack('f', 0)  # 'd' per double precision float
        
        duration_bytes = struct.pack('I', duration_ns)  # 'I' per unsigned int
        padding_bytes = struct.pack('I', 0)  # 4 byte di padding
        
        f.write(freq_bytes + duration_bytes + amplitude + padding_bytes)  # Scrivi il chunk completo

    for i in range(1,25000):
        amplitude = struct.pack('f', 0)  # 'd' per double precision float
        duration_bytes = struct.pack('I', duration_ns)  # 'I' per unsigned int
        padding_bytes = struct.pack('I', 0)  # 4 byte di padding
        f.write(freq_bytes + duration_bytes + amplitude + padding_bytes)  # Scrivi il chunk completo

    for bit in sequence2:
        if bit == '1':
            amplitude = struct.pack('f', 10)  # 'd' per double precision float
        else:
            amplitude = struct.pack('f', 0)  # 'd' per double precision float

        duration_bytes = struct.pack('I', duration_ns)  # 'I' per unsigned int
        padding_bytes = struct.pack('I', 0)  # 4 byte di padding

        f.write(freq_bytes + duration_bytes + amplitude + padding_bytes)  # Scrivi il chunk completo

    for i in range(1,25000): 
        amplitude = struct.pack('f', 0)  # 'd' per double precision float
        duration_bytes = struct.pack('I', duration_ns)  # 'I' per unsigned int
        padding_bytes = struct.pack('I', 0)  # 4 byte di padding
        f.write(freq_bytes + duration_bytes + amplitude + padding_bytes)  # Scrivi il chunk completo


print("File .ft creato con successo.")
