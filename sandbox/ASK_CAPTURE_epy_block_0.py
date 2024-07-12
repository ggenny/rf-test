"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr
import sys

class blk(gr.sync_block):
    def __init__(self, null_limit=10):
        gr.sync_block.__init__(self,
            name='Data Stream Printer',
            in_sig=[np.uint8],  # Assume the input signal is bytes
            out_sig=None)  # This block does not produce output

        self.null_limit = null_limit
        self.printing = False
        self.null_count = 0

    def work(self, input_items, output_items):
        in_data = input_items[0]
        for byte in in_data:
            if byte != 0:
                if not self.printing:
                    self.printing = True  # Start printing when the first non-null byte is encountered
                self.null_count = 0  # Reset null count when a non-null byte is received
            else:
                self.null_count += 1  # Increment null count

            if self.printing:
                print(self.print_bits(byte), end='')
                sys.stdout.flush()  # Esegue un flush del buffer di stdout per mostrare l'output immediatamente
        
            if self.null_count >= self.null_limit:
                self.printing = False  # Stop printing after the limit of null bytes

        return len(in_data)

    def print_bits(self, byte):
        return ''.join(f'{b:08b}' for b in [byte])

