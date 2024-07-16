#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import signal
import argparse
from gnuradio import gr, qtgui, analog, blocks, digital, filter, network
from gnuradio.filter import firdes
from gnuradio.fft import window
import osmosdr
import ASK_CAPTURE_epy_block_0 as epy_block_0  # embedded python block

class ASK_CAPTURE(gr.top_block):

    def __init__(self, samp_rate, samp_per_sym, gain, freq, cut):
        gr.top_block.__init__(self, "ASK_CAPTURE", catch_exceptions=True)

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate
        self.samp_per_sym = samp_per_sym
        self.gain = gain
        self.freq = freq
        self.cut = cut

        ##################################################
        # Blocks
        ##################################################
        self.rtlsdr_source_0 = osmosdr.source(args="numchan=1")
        self.rtlsdr_source_0.set_time_unknown_pps(osmosdr.time_spec_t())
        self.rtlsdr_source_0.set_sample_rate(samp_rate)
        self.rtlsdr_source_0.set_center_freq(freq, 0)
        self.rtlsdr_source_0.set_freq_corr(0, 0)
        self.rtlsdr_source_0.set_dc_offset_mode(0, 0)
        self.rtlsdr_source_0.set_iq_balance_mode(0, 0)
        self.rtlsdr_source_0.set_gain_mode(False, 0)
        self.rtlsdr_source_0.set_gain(10, 0)
        self.rtlsdr_source_0.set_if_gain(20, 0)
        self.rtlsdr_source_0.set_bb_gain(20, 0)
        self.rtlsdr_source_0.set_antenna('', 0)
        self.rtlsdr_source_0.set_bandwidth(0, 0)

        self.low_pass_filter_0 = filter.fir_filter_ccf(
            1,
            firdes.low_pass(
                5,
                samp_rate,
                cut,
                100000,
                window.WIN_HAMMING,
                6.76))

        self.analog_agc_xx_0 = analog.agc_cc(1e-4, 1.0, 1.0, gain)
        self.blocks_complex_to_mag_squared_0 = blocks.complex_to_mag_squared(1)
        self.blocks_threshold_ff_0 = blocks.threshold_ff(0.5, 1.0, 0)
        self.digital_clock_recovery_mm_xx_0 = digital.clock_recovery_mm_ff(samp_per_sym*(1+0.0), 0.25*0.175*0.175, 0.5, 0.175, 0.005)
        self.blocks_float_to_uchar_1 = blocks.float_to_uchar(1, 1, 0)
        self.blocks_pack_k_bits_bb_0 = blocks.pack_k_bits_bb(8)
        self.epy_block_0 = epy_block_0.blk(null_limit=50)
        self.network_udp_sink_0 = network.udp_sink(gr.sizeof_char, 1, '127.0.0.1', 2000, 0, 1472, False)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.rtlsdr_source_0, 0), (self.low_pass_filter_0, 0))
        self.connect((self.low_pass_filter_0, 0), (self.analog_agc_xx_0, 0))
        self.connect((self.analog_agc_xx_0, 0), (self.blocks_complex_to_mag_squared_0, 0))
        self.connect((self.blocks_complex_to_mag_squared_0, 0), (self.blocks_threshold_ff_0, 0))
        self.connect((self.blocks_threshold_ff_0, 0), (self.digital_clock_recovery_mm_xx_0, 0))
        self.connect((self.digital_clock_recovery_mm_xx_0, 0), (self.blocks_float_to_uchar_1, 0))
        self.connect((self.blocks_float_to_uchar_1, 0), (self.blocks_pack_k_bits_bb_0, 0))
        self.connect((self.blocks_pack_k_bits_bb_0, 0), (self.epy_block_0, 0))
        self.connect((self.blocks_pack_k_bits_bb_0, 0), (self.network_udp_sink_0, 0))

def main():
    parser = argparse.ArgumentParser(description="GNU Radio ASK_CAPTURE Script")
    parser.add_argument('--samp_rate', type=float, default=1000000, help="Sample rate")
    parser.add_argument('--samp_per_sym', type=int, default=320, help="Samples per symbol")
    parser.add_argument('--gain', type=float, default=20, help="Gain")
    parser.add_argument('--freq', type=float, default=433.90e6, help="Frequency")
    parser.add_argument('--cut', type=int, default=32000, help="Cutoff frequency")
    args = parser.parse_args()

    tb = ASK_CAPTURE(args.samp_rate, args.samp_per_sym, args.gain, args.freq, args.cut)

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()
        sys.exit(0)

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    tb.start()
    tb.wait()

if __name__ == '__main__':
    main()
