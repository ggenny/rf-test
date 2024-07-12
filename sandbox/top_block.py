#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Top Block
# GNU Radio version: v3.11.0.0git-678-g2ccb54a3

from gnuradio import blocks
import pmt
from gnuradio import gr
from gnuradio.filter import firdes
from gnuradio.fft import window
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation




class top_block(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "Top Block", catch_exceptions=True)

        ##################################################
        # Blocks
        ##################################################

        self.blocks_file_source_0 = blocks.file_source(gr.sizeof_gr_complex*1, '/home/ggenny/Develop/rf-test/generated.complex', False, 0, 0)
        self.blocks_file_source_0.set_begin_tag(pmt.PMT_NIL)
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_short*1, '/home/ggenny/Develop/rf-test/generated.c16', False)
        self.blocks_file_sink_0.set_unbuffered(False)
        self.blocks_complex_to_interleaved_short_0 = blocks.complex_to_interleaved_short(False,62768)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_complex_to_interleaved_short_0, 0), (self.blocks_file_sink_0, 0))
        self.connect((self.blocks_file_source_0, 0), (self.blocks_complex_to_interleaved_short_0, 0))





def main(top_block_cls=top_block, options=None):
    tb = top_block_cls()

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
