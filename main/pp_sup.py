
import pp

class MPCompute(object):
    def __init__(self):
        self.job_server = pp.Server()
        self.ncpus = self.job_server.get_ncpus()
        self.jobs = []

    def compute(self, func, args=(), depfuncs=(), modules=(), callback=None, callbackargs=()):
        '''
        func - function to be executed
        args - tuple with arguments of the 'func'
        depfuncs - tuple with functions which might be called from 'func'
        modules - tuple with module names to import
        callback - callback function which will be called with argument
                list equal to callbackargs+(result,)
                as soon as calculation is done
        callbackargs - additional arguments for callback function
        '''
        self.job_server.submit(func, args, depfuncs, modules, callback, callbackargs)
    
    def get_stats(self):
        return self.job_server.get_stats()
    
    def shutdown(self):
        self.job_server.destroy()
        self.job_server = None