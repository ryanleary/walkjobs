from walkjobs.execution import Task, LocalTarget
import logging

logger = logging.getLogger(__name__)


class Sleeper(Task):

    @staticmethod
    def cmd(time):
        return ['sleep', str(time)]


class ExternalAdder(Task):
    #stdout = LocalTarget('external_adder.out', ephemeral=True)
    #stderr = None

    @staticmethod
    def cmd(a, b):
        logging.debug('In ExternalAdder cmd')
        return ['expr', str(a), '+', str(b)]

    def return_value(self):
        return self.stdout.get()

'''
    # example usage
def main():
    a = 187
    b = 5
    t1 = ExternalAdder(a, b)
    t1.set_executor(LocalExecutionStrategy)
    t1.execute()
    print 'T1 state: ' + str(t1.status.state)
    print 'T1 exitcode: ' + str(t1.status.exitcode)
    t1.wait()

    print 'T1 state: ' + str(t1.status.state)
    print 'T1 exitcode: ' + str(t1.status.exitcode)
    print 'T1 return value: ' + str(t1.return_value())
'''