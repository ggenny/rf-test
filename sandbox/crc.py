import argparse
import crcmod

def calculate_crcs(data):
    # Dizionario di funzioni CRC comuni con output di 8 bit
    crc_functions = {
        'crc-8': crcmod.predefined.mkCrcFun('crc-8'),
        'crc-8-darc': crcmod.predefined.mkCrcFun('crc-8-darc'),
        'crc-8-i-code': crcmod.predefined.mkCrcFun('crc-8-i-code'),
        'crc-8-maxim': crcmod.predefined.mkCrcFun('crc-8-maxim'),
        'crc-8-wcdma': crcmod.predefined.mkCrcFun('crc-8-wcdma'),
        'crc-8-rohc': crcmod.predefined.mkCrcFun('crc-8-rohc'),
#        'crc-8-cdma2000': crcmod.predefined.mkCrcFun('crc-8-cdma2000'),
#        'crc-8-dvb-s2': crcmod.predefined.mkCrcFun('crc-8-dvb-s2'),
#        'crc-8-ebu': crcmod.predefined.mkCrcFun('crc-8-ebu'),
        'crc-8-itu': crcmod.predefined.mkCrcFun('crc-8-itu'),
#        'crc-8-atecc': crcmod.predefined.mkCrcFun('crc-8-atecc'),
#        'crc-8-autosar': crcmod.predefined.mkCrcFun('crc-8-autosar'),
#        'crc-8-bluetooth': crcmod.predefined.mkCrcFun('crc-8-bluetooth'),
#        'crc-8-lte': crcmod.predefined.mkCrcFun('crc-8-lte'),
    }
    
    results = {}
    for name, func in crc_functions.items():
        crc_result = func(data)
        results[name] = crc_result

    return results

def bits_to_bytes(bits):
    return int(bits, 2).to_bytes((len(bits) + 7) // 8, byteorder='big')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Calculate various CRC-8 variants for a 128-bit binary string.")
    parser.add_argument("bit_string", type=str, help="Enter a 128-bit binary string.")
    args = parser.parse_args()

    if len(args.bit_string) != 128 or any(c not in '01' for c in args.bit_string):
        parser.error("The bit string must be exactly 128 bits long and contain only 0s and 1s.")

    data_bytes = bits_to_bytes(args.bit_string)
    crc_results = calculate_crcs(data_bytes)

    for crc_name, crc_value in crc_results.items():
        print(f"{crc_name}: {bin(crc_value)[2:].zfill(8)}")  # Output the CRC value in binary format
