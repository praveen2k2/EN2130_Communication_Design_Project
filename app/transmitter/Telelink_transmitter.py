#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Telelink_cdp
# Author: Telelink
# Copyright: Telelink
# Description: cdp project
# GNU Radio version: 3.10.9.2

from gnuradio import blocks
import pmt
from gnuradio import digital
from gnuradio import fec
from gnuradio import gr
from gnuradio.filter import firdes
from gnuradio.fft import window
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import soapy




class Telelink_transmitter(gr.top_block):

    def __init__(self, MTU=1500):
        gr.top_block.__init__(self, "Telelink_cdp", catch_exceptions=True)

        ##################################################
        # Parameters
        ##################################################
        self.MTU = MTU

        ##################################################
        # Variables
        ##################################################
        self.sps = sps = 4
        self.qpsk = qpsk = digital.constellation_rect([0.707+0.707j, -0.707+0.707j, -0.707-0.707j, 0.707-0.707j], [0, 1, 2, 3],
        4, 2, 2, 1, 1).base()
        self.polys = polys = [109, 79]
        self.nfilts = nfilts = 32
        self.k = k = 7
        self.variable_adaptive_algorithm_0 = variable_adaptive_algorithm_0 = digital.adaptive_algorithm_cma( qpsk, .0001, 4).base()
        self.txgain = txgain = 50
        self.txbw = txbw = 9000
        self.tx_freq = tx_freq = 600e6
        self.taps = taps = [1.0, 0.25-0.25j, 0.50 + 0.10j, -0.3 + 0.2j]
        self.spr = spr = 750000
        self.samp_rate_blade = samp_rate_blade = 600e3
        self.samp_rate = samp_rate = 600e3
        self.rxbw = rxbw = 10000
        self.rx_freq_ = rx_freq_ = 433e6
        self.rrc_taps = rrc_taps = firdes.root_raised_cosine(nfilts, nfilts, 1.0/float(sps), 0.35, 11*sps*nfilts)
        self.hdr_format = hdr_format = digital.header_format_default('11100001010110101110100010010011',1, 1)
        self.freq = freq = 2.4e9
        self.excess_bw = excess_bw = .5
        self.cc_enc = cc_enc = fec.cc_encoder_make((MTU*8),k, 2, polys, 0, fec.CC_TAILBITING, True)
        self.cc_dec = cc_dec = list(map( (lambda a: fec.cc_decoder.make((MTU*8),k, 2, polys, 0, (-1), fec.CC_TAILBITING, True)),range(0,1)))
        self.arity = arity = 4

        ##################################################
        # Blocks
        ##################################################

        self.soapy_bladerf_sink_0 = None
        dev = 'driver=bladerf'
        stream_args = ''
        tune_args = ['']
        settings = ['']

        self.soapy_bladerf_sink_0 = soapy.sink(dev, "fc32", 1, '',
                                  stream_args, tune_args, settings)
        self.soapy_bladerf_sink_0.set_sample_rate(0, samp_rate_blade*2)
        self.soapy_bladerf_sink_0.set_bandwidth(0, 10000)
        self.soapy_bladerf_sink_0.set_frequency(0, freq)
        self.soapy_bladerf_sink_0.set_frequency_correction(0, 0)
        self.soapy_bladerf_sink_0.set_gain(0, min(max(txgain, 17.0), 73.0))
        self.fec_extended_tagged_encoder_0_1 = fec.extended_tagged_encoder(encoder_obj_list=cc_enc, puncpat='11', lentagname="packet_len", mtu=MTU)
        self.digital_protocol_formatter_bb_0 = digital.protocol_formatter_bb(hdr_format, "packet_len")
        self.digital_constellation_modulator_0 = digital.generic_mod(
            constellation=qpsk,
            differential=True,
            samples_per_symbol=sps,
            pre_diff_code=True,
            excess_bw=excess_bw,
            verbose=False,
            log=False,
            truncate=False)
        self.blocks_throttle2_1 = blocks.throttle( gr.sizeof_char*1, samp_rate, True, 0 if "auto" == "auto" else max( int(float(0.1) * samp_rate) if "auto" == "time" else int(0.1), 1) )
        self.blocks_throttle2_0_0 = blocks.throttle( gr.sizeof_char*1, spr, True, 0 if "auto" == "auto" else max( int(float(0.1) * spr) if "auto" == "time" else int(0.1), 1) )
        self.blocks_tagged_stream_mux_0 = blocks.tagged_stream_mux(gr.sizeof_char*1, "packet_len", 0)
        self.blocks_stream_to_tagged_stream_0 = blocks.stream_to_tagged_stream(gr.sizeof_char, 1, 8, "packet_len")
        self.blocks_repack_bits_bb_0_0_0 = blocks.repack_bits_bb(1, 8, 'packet_len', False, gr.GR_MSB_FIRST)
        self.blocks_repack_bits_bb_0_0 = blocks.repack_bits_bb(8, 1, 'packet_len', False, gr.GR_MSB_FIRST)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_cc(0.8)
        self.blocks_file_source_0 = blocks.file_source(gr.sizeof_char*1, './input.tmp', False, 0, 0)
        self.blocks_file_source_0.set_begin_tag(pmt.PMT_NIL)
        self.blocks_file_sink_1 = blocks.file_sink(gr.sizeof_char*1, './out', False)
        self.blocks_file_sink_1.set_unbuffered(False)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_file_source_0, 0), (self.blocks_throttle2_0_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.soapy_bladerf_sink_0, 0))
        self.connect((self.blocks_repack_bits_bb_0_0, 0), (self.fec_extended_tagged_encoder_0_1, 0))
        self.connect((self.blocks_repack_bits_bb_0_0_0, 0), (self.blocks_tagged_stream_mux_0, 1))
        self.connect((self.blocks_repack_bits_bb_0_0_0, 0), (self.digital_protocol_formatter_bb_0, 0))
        self.connect((self.blocks_stream_to_tagged_stream_0, 0), (self.blocks_file_sink_1, 0))
        self.connect((self.blocks_stream_to_tagged_stream_0, 0), (self.blocks_repack_bits_bb_0_0, 0))
        self.connect((self.blocks_tagged_stream_mux_0, 0), (self.blocks_throttle2_1, 0))
        self.connect((self.blocks_throttle2_0_0, 0), (self.blocks_stream_to_tagged_stream_0, 0))
        self.connect((self.blocks_throttle2_1, 0), (self.digital_constellation_modulator_0, 0))
        self.connect((self.digital_constellation_modulator_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.digital_protocol_formatter_bb_0, 0), (self.blocks_tagged_stream_mux_0, 0))
        self.connect((self.fec_extended_tagged_encoder_0_1, 0), (self.blocks_repack_bits_bb_0_0_0, 0))


    def get_MTU(self):
        return self.MTU

    def set_MTU(self, MTU):
        self.MTU = MTU

    def get_sps(self):
        return self.sps

    def set_sps(self, sps):
        self.sps = sps
        self.set_rrc_taps(firdes.root_raised_cosine(self.nfilts, self.nfilts, 1.0/float(self.sps), 0.35, 11*self.sps*self.nfilts))

    def get_qpsk(self):
        return self.qpsk

    def set_qpsk(self, qpsk):
        self.qpsk = qpsk

    def get_polys(self):
        return self.polys

    def set_polys(self, polys):
        self.polys = polys

    def get_nfilts(self):
        return self.nfilts

    def set_nfilts(self, nfilts):
        self.nfilts = nfilts
        self.set_rrc_taps(firdes.root_raised_cosine(self.nfilts, self.nfilts, 1.0/float(self.sps), 0.35, 11*self.sps*self.nfilts))

    def get_k(self):
        return self.k

    def set_k(self, k):
        self.k = k

    def get_variable_adaptive_algorithm_0(self):
        return self.variable_adaptive_algorithm_0

    def set_variable_adaptive_algorithm_0(self, variable_adaptive_algorithm_0):
        self.variable_adaptive_algorithm_0 = variable_adaptive_algorithm_0

    def get_txgain(self):
        return self.txgain

    def set_txgain(self, txgain):
        self.txgain = txgain
        self.soapy_bladerf_sink_0.set_gain(0, min(max(self.txgain, 17.0), 73.0))

    def get_txbw(self):
        return self.txbw

    def set_txbw(self, txbw):
        self.txbw = txbw

    def get_tx_freq(self):
        return self.tx_freq

    def set_tx_freq(self, tx_freq):
        self.tx_freq = tx_freq

    def get_taps(self):
        return self.taps

    def set_taps(self, taps):
        self.taps = taps

    def get_spr(self):
        return self.spr

    def set_spr(self, spr):
        self.spr = spr
        self.blocks_throttle2_0_0.set_sample_rate(self.spr)

    def get_samp_rate_blade(self):
        return self.samp_rate_blade

    def set_samp_rate_blade(self, samp_rate_blade):
        self.samp_rate_blade = samp_rate_blade
        self.soapy_bladerf_sink_0.set_sample_rate(0, self.samp_rate_blade*2)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.blocks_throttle2_1.set_sample_rate(self.samp_rate)

    def get_rxbw(self):
        return self.rxbw

    def set_rxbw(self, rxbw):
        self.rxbw = rxbw

    def get_rx_freq_(self):
        return self.rx_freq_

    def set_rx_freq_(self, rx_freq_):
        self.rx_freq_ = rx_freq_

    def get_rrc_taps(self):
        return self.rrc_taps

    def set_rrc_taps(self, rrc_taps):
        self.rrc_taps = rrc_taps

    def get_hdr_format(self):
        return self.hdr_format

    def set_hdr_format(self, hdr_format):
        self.hdr_format = hdr_format

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.soapy_bladerf_sink_0.set_frequency(0, self.freq)

    def get_excess_bw(self):
        return self.excess_bw

    def set_excess_bw(self, excess_bw):
        self.excess_bw = excess_bw

    def get_cc_enc(self):
        return self.cc_enc

    def set_cc_enc(self, cc_enc):
        self.cc_enc = cc_enc

    def get_cc_dec(self):
        return self.cc_dec

    def set_cc_dec(self, cc_dec):
        self.cc_dec = cc_dec

    def get_arity(self):
        return self.arity

    def set_arity(self, arity):
        self.arity = arity



def argument_parser():
    description = 'cdp project'
    parser = ArgumentParser(description=description)
    parser.add_argument(
        "--MTU", dest="MTU", type=intx, default=1500,
        help="Set MTU [default=%(default)r]")
    return parser


def main(top_block_cls=Telelink_transmitter, options=None):
    if options is None:
        options = argument_parser().parse_args()
    tb = top_block_cls(MTU=options.MTU)

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        sys.exit(0)

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    tb.start()

    try:
        input('Press Enter to quit: ')
    except EOFError:
        pass
    tb.stop()
    tb.wait()


if __name__ == '__main__':
    main()
