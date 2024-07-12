import argparse
import crcmod
import itertools

def bits_to_bytes(bits):
    return int(bits, 2).to_bytes((len(bits) + 7) // 8, byteorder='big')

def test_crc_parameters(data_crc_pairs):
    # Genera tutte le combinazioni possibili di polinomi, valori iniziali e valori XOR finali
    for poly, init, xor_out in itertools.product(range(256), repeat=3):
        try:
            # Crea la funzione CRC con i parametri attuali
            crc_func = crcmod.mkCrcFun(poly + (1 << 8), initCrc=init, xorOut=xor_out)
            # Verifica se il CRC calcolato corrisponde per tutte le coppie di dati forniti
            if all(crc_func(data) == expected for data, expected in data_crc_pairs):
                print(f"Match found! Poly: 0x{poly:02X}, Init: 0x{init:02X}, XOR Out: 0x{xor_out:02X}")
                #return
                continue
        except Exception as e:
            # Ignora i polinomi invalidi
            continue

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Brute force CRC parameters for multiple bit strings.")
    parser.add_argument('data_crc_pairs', type=str, nargs='+', help='Pairs of data and expected CRC in the format <data_bits>:<crc_hex>')

    args = parser.parse_args()

    data_crc_pairs = []
    for pair in args.data_crc_pairs:
        data_bits, crc_hex = pair.split(':')
        data_bytes = bits_to_bytes(data_bits)
        expected_crc = int(crc_hex, 16)
        data_crc_pairs.append((data_bytes, expected_crc))

    test_crc_parameters(data_crc_pairs)
