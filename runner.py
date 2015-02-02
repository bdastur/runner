#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
The Runner, is a generic utility that can be plugged in
with any python modules to run several tasks in various orders.
'''

import sys
import os
import re
from ConfigParser import SafeConfigParser
import logger
import logging


def get_absolute_path_for_file(file_name, splitdir=None):
    '''
    Return the filename in absolute path for any file
    passed as relative path.
    '''
    base = os.path.basename(__file__)
    if splitdir is not None:
        splitdir = splitdir + "/" + base
    else:
        splitdir = base

    if os.path.isabs(__file__):
        abs_file_path = os.path.join(__file__.split(splitdir)[0],
                                     file_name)
    else:
        abs_file = os.path.abspath(__file__)
        abs_file_path = os.path.join(abs_file.split(splitdir)[0],
                                     file_name)

    return abs_file_path


class RunnerConfig(object):
    '''
    The class handles the parsing of the runner setup
    config file.
    '''
    def __init__(self):
        '''
        Initialize RunnerConfig
        '''
        self.setupfile = get_absolute_path_for_file("./configs/setupfile.txt")
        self.cfgparser = SafeConfigParser()
        self.cfgparser.read(self.setupfile)
        self.operpattern = re.compile(r'STAGE[-|_](\w+)')

    def dump_parsed_config(self):
        '''
        Function to parse the entire config and dump
        the output
        '''
        print "Dump Parsed Config"
        parser = self.cfgparser
        for section in parser.sections():
            print "Section: ", section
            for (name, value) in parser.items(section):
                print "%s = %s" % (name, value)


    def parse_all_operations(self):
        '''
        Return a dict list with parsed operations.
        '''
        parser = self.cfgparser
        operations = []
        for section in parser.sections():
            operation = {}
            #Check if this is a stage pattern.
            mobj = self.operpattern.match(section)
            if mobj:
                operation['name'] = mobj.group(1)
                operation['dependency'] = \
                    parser.get(section, "dependency").strip("\"")
                operation['group'] = parser.get(section, "group").strip("\"")
                operation['modulename'] = \
                    parser.get(section, "module").strip("\"")
                operation['id'] = parser.get(section, "id").strip("\"")

                operations.append(operation)

        return operations


class Runner(object):
    '''
    Run Forest Run.
    '''
    ######################
    # Operation status.
    ######################

    OPER_STATUS_NOTRUNNING = 0
    OPER_STATUS_RUNNING = 1
    OPER_STATUS_PASSED = 2
    OPER_STATUS_FAILED = 3

    def __init__(self):
        '''
        Initialize Runner.
        '''
        self.runcfg = RunnerConfig()
        self.operations = []
        self.populate_runner_info()

        logger_inst = logger.Logger(name="Runner", level="debug")
        self.log = logger_inst.get_logger()
        self.log.setLevel(logging.DEBUG)
        self.log.debug("Start Runner...")



    def validate_operation_module(self, module):
        '''
        We want to make sure that the plugin modules
        have the correct functions available.
        '''
        for func_name in ['run', 'checkstart']:
            if not hasattr(module, func_name):
                raise ImportError("Module %s has not implemented %s function"
                                  % (module.__class__, func_name))


    def populate_runner_info(self):
        '''
        Parse the user configuration file.
        '''
        self.operations = self.runcfg.parse_all_operations()
        for operation in self.operations:
            operation['status'] = Runner.OPER_STATUS_NOTRUNNING
            __import__(operation['modulename'])
            operation['module'] = sys.modules[operation['modulename']]
            self.validate_operation_module(operation['module'])


    def runner_run_sequential(self):
        '''
        The method will run all the Operations/Stages
        in a sequence.
        '''
        soperlist = sorted(self.operations, key=lambda k: k['id'])
        #For all the stages. start with the lowest id.
        for operation in soperlist:
            #Lets get the lowest operation
            self.log.info("Operation: %s starting...", operation['modulename'])
            operation['module'].run()


def main():
    runner = Runner()
    runner.runner_run_sequential()


if __name__ == '__main__':
    main()
