import argparse
import logging
import re


class Interface(object):
    def parse(self):
        raise NotImplementedError

    @staticmethod
    def run(tasks, override_defaults={}):
        pass


class ArgParseInterface(Interface):
    def parse(self, cmdline_args=None, main_task_cls=None):
        parser = argparse.ArgumentParser()
        parser.add_argument('-s', '--sge', required=False)

        args = parser.parse_args(args=cmdline_args)
        print args


def run(cmdline_args=None, main_task_cls=None):
    interface = ArgParseInterface()
    tasks = interface.parse(cmdline_args, main_task_cls=main_task_cls)
    interface.run(tasks)