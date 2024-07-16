import sys

def print_bits(byte):
    return ''.join(f'{b:08b}' for b in byte)

# Controllo di inizio e fine della stampa
printing = False
null_count = 0
null_limit = 10  # Imposta il limite di byte nulli a 10

try:
    while True:
        data = sys.stdin.buffer.read(1)  # Legge 1 byte per volta
        if not data:
            break
        
        if data[0] != 0:
            if not printing:
                printing = True  # Inizia a stampare quando arriva il primo byte non nullo
            null_count = 0  # Resetta il conteggio dei nulli quando si riceve un byte non nullo
        else:
            null_count += 1  # Incrementa il conteggio dei nulli
        
        if printing:
            sys.stdout.write(print_bits(data))
            sys.stdout.flush()
        
        # Verifica se il conteggio dei nulli ha raggiunto il limite
        if null_count >= null_limit:
            printing = False

except KeyboardInterrupt:
    sys.exit(0)
