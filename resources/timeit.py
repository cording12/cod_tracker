# Created by Thiago in this thread:
# https://discuss.streamlit.io/t/how-to-tell-which-variables-are-being-recomputed/359/3

import streamlit as st
import time


class TimeIt(object):
    """Simple timer for profiling Streamlit apps.
    Usage
    -----
    t = TimeIt()
    do_stuff()
    t.tick('did stuff')
    do_more_stuff()
    t.tick('did more stuff')
    """
    def __init__(self):
        self.prev_time = time.time()

    def tick(self, msg=''):
        new_time = time.time()
        delta = new_time - self.prev_time

        st.write('_%s [Ellapsed time: %0.3fs]_' % (msg, delta))

        self.prev_time = new_time