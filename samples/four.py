#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logger
import logging


def run():
    '''
    Runner
    '''
    logger_inst = logger.Logger(name=__name__, level="debug")
    log = logger_inst.get_logger()
    log.setLevel(logging.DEBUG)
    log.debug("Start running...")


def checkstart():
    '''
    check if we should start
    '''
    print "Check start"


