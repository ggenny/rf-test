import numpy as np
from scipy.signal import resample
import argparse

def convert_c8_to_c16(c8_data):
    data_int8 = np.frombuffer(c8_data, dtype=np.int8)
    # Converti int8 a int16
    real = data_int8[0::2].astype(np.int16) * 256
    imag = data_int8[1::2].astype(np.int16) * 256
    # Prepariamo l'array di output
    combined = np.empty((real.size + imag.size,), dtype=np.int16)
    combined[0::2] = real
    combined[1::2] = imag
    return combined

def convert_c16_to_cf32(c16_data):
    # Interpretare i dati come array di int16
    data_int16 = np.frombuffer(c16_data, dtype=np.int16)
    
    # Scala per normalizzare all'intervallo [-1, 1]
    scale_factor = 32767.0  # Massimo valore per int16
    real = (data_int16[0::2] / scale_factor).astype(np.float32)
    imag = (data_int16[1::2] / scale_factor).astype(np.float32)
    
    # Creazione del segnale complesso
    data_cf32 = real + 1j * imag
    
    return data_cf32

def resample_signal(original_data, original_rate, target_rate):
    num_samples = int(len(original_data) * (target_rate / original_rate))
    resampled_data = resample(original_data, num_samples)
    
    # Normalizzazione per mantenere l'energia del segnale costante
    energy_original = np.sum(np.abs(original_data)**2)
    energy_resampled = np.sum(np.abs(resampled_data)**2)
    resampled_data *= np.sqrt(energy_original / energy_resampled)
    
    return resampled_data

def convert_cf32_to_c16(cf32_data):
    # Scala i dati da -1/+1 a -32768/+32767
    scale_factor = 32767.0  # Massimo valore per int16
    real_scaled = (cf32_data.real * scale_factor).clip(-32768, 32767).astype(np.int16)
    imag_scaled = (cf32_data.imag * scale_factor).clip(-32768, 32767).astype(np.int16)
    
    # Combina le parti reali e immaginarie in un unico array intercalato
    combined = np.empty((real_scaled.size + imag_scaled.size,), dtype=np.int16)
    combined[0::2] = real_scaled
    combined[1::2] = imag_scaled
    return combined

def convert_c16_to_c8(c16_data):
    # Converti da int16 a int8 scalando i valori
    real = (c16_data[0::2].astype(np.int32) * 128 // 32768).astype(np.int8)
    imag = (c16_data[1::2].astype(np.int32) * 128 // 32768).astype(np.int8)
    combined = np.empty((real.size + imag.size,), dtype=np.int8)
    combined[0::2] = real
    combined[1::2] = imag
    return combined

def parse_arguments():
    parser = argparse.ArgumentParser(description='Convert and resample audio signals.')
    parser.add_argument('--input', required=True, help='Input file')
    parser.add_argument('--output', required=True, help='Output file')
    parser.add_argument('--from_format', choices=['c8', 'c16', 'cf32'], required=True, help='Input format type')
    parser.add_argument('--to_format', choices=['c8', 'c16', 'cf32'], required=True, help='Output format type')
    parser.add_argument('--original_rate', type=int, help='Original sample rate for resampling')
    parser.add_argument('--target_rate', type=int, help='Target sample rate for resampling')
    return parser.parse_args()

def main():
    args = parse_arguments()
    
    with open(args.input, 'rb') as f:
        input_data = f.read()

    # Perform the requested conversion
    processed_data = None
    
    if args.from_format and args.to_format:
        if args.from_format == 'c8' and args.to_format == 'c16':
            processed_data = convert_c8_to_c16(input_data)
        elif args.from_format == 'c16' and args.to_format == 'cf32':
            processed_data = convert_c16_to_cf32(input_data)
        elif args.from_format == 'cf32' and args.to_format == 'c16':
            processed_data = convert_cf32_to_c16(np.frombuffer(input_data, dtype=np.complex64))
        elif args.from_format == 'c16' and args.to_format == 'c8':
            processed_data = convert_c16_to_c8(np.frombuffer(input_data, dtype=np.int16))
    else:
        # Assume data is already in the correct format for resampling
        if args.from_format == 'cf32':
            processed_data = np.frombuffer(input_data, dtype=np.complex64)
        elif args.from_format == 'c16':
            processed_data = np.frombuffer(input_data, dtype=np.int16)
        elif args.from_format == 'c8':
            processed_data = np.frombuffer(input_data, dtype=np.int8)

    # Handle resampling if required
    if args.original_rate and args.target_rate:
        # Ensure data is in a format that can be resampled
        if args.from_format != 'cf32':
            # Temporarily convert to CF32 if not already
            if args.from_format == 'c16':
                processed_data = convert_c16_to_cf32(processed_data.tobytes())
            elif args.from_format == 'c8':
                processed_data = convert_c8_to_c16(processed_data.tobytes())
            processed_data = np.frombuffer(processed_data, dtype=np.complex64)
        processed_data = resample_signal(processed_data, args.original_rate, args.target_rate)

    # Save the processed data
    with open(args.output, 'wb') as f:
        if isinstance(processed_data, np.ndarray):
            f.write(processed_data.tobytes())
        else:
            raise TypeError("Processed data is not in expected format")

if __name__ == '__main__':
    main()
