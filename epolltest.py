#import subprocess
#import sys
#import os
#import select
## returns command exit status, stdout text, stderr text
## rtoutput: show realtime output while running
#def run_script(cmd,rtoutput=0):
    #p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    #poller = select.poll()
    #poller.register(p.stdout, select.POLLIN)
    #poller.register(p.stderr, select.POLLIN)

    #coutput=''
    #cerror=''
    #fdhup={}
    #fdhup[p.stdout.fileno()]=0
    #fdhup[p.stderr.fileno()]=0
    #while sum(fdhup.values()) < len(fdhup):
        #try:
            #r = poller.poll(1)
        #except select.error, err:
            #if err.args[0] != EINTR:
                #raise
            #r=[]
        #for fd, flags in r:
            #if flags & (select.POLLIN | select.POLLPRI):
                #c = os.read(fd, 1024)
                #if rtoutput:
                    #sys.stdout.write(c)
                    #sys.stdout.flush()
                #if fd == p.stderr.fileno():
                    #cerror+=c
                #else:
                    #coutput+=c
            #else:
                #fdhup[fd]=1
    #return p.poll(), coutput.strip(), cerror.strip()
#run_script('top')
#import threading
#import subprocess
#import logging
#import os

#class LogAdapter(threading.Thread):

    #def __init__(self, logname, level = logging.INFO):
        #super().__init__()
        #self.log = logging.getLogger(logname)
        #self.readpipe, self.writepipe = os.pipe()

        #logFunctions = {
            #logging.DEBUG: self.log.debug,
            #logging.INFO: self.log.info,
            #logging.WARN: self.log.warn,
            #logging.ERROR: self.log.warn,
        #}

        #try:
            #self.logFunction = logFunctions[level]
        #except KeyError:
            #self.logFunction = self.log.info

    #def fileno(self):
        ##when fileno is called this indicates the subprocess is about to fork => start thread
        #self.start()
        #return self.writepipe

    #def finished(self):
        #"""If the write-filedescriptor is not closed this thread will
        #prevent the whole program from exiting. You can use this method
        #to clean up after the subprocess has terminated."""
        #os.close(self.writepipe)

    #def run(self):
        #inputFile = os.fdopen(self.readpipe)

        #while True:
            #line = inputFile.readline()

            #if len(line) == 0:
                ##no new data was added
                #break

            #self.logFunction(line.strip())


#import subprocess

## This will raise a CalledProcessError if the program return a nonzero code.
## You can use call() instead if you don't care about that case.
#subprocess.check_call(['top'])

#import sys
#from subprocess import Popen, PIPE
#from threading  import Thread

#def tee(infile, *files):
    #"""Print `infile` to `files` in a separate thread."""
    #def fanout(infile, *files):
        #for line in iter(infile.readline, ''):
            #for f in files:
                #f.write(line)
        #infile.close()
    #t = Thread(target=fanout, args=(infile,)+files)
    #t.daemon = True
    #t.start()
    #return t

#def teed_call(cmd_args, **kwargs):    
    #stdout, stderr = [kwargs.pop(s, None) for s in 'stdout', 'stderr']
    #p = Popen(cmd_args,
              #stdout=PIPE if stdout is not None else None,
              #stderr=PIPE if stderr is not None else None,
              #**kwargs)
    #threads = []
    #if stdout is not None: threads.append(tee(p.stdout, stdout, sys.stdout))
    #if stderr is not None: threads.append(tee(p.stderr, stderr, sys.stderr))
    #for t in threads: t.join() # wait for IO completion
    #return p.wait()

#outf, errf = open('out.txt', 'wa'), open('err.txt', 'wa')
##assert not teed_call(["cat", __file__], stdout=None, stderr=errf)
##assert not teed_call(["echo", "abc"], stdout=outf, stderr=errf, bufsize=0)
#assert teed_call(["ping", "-c","5","baidu.com"], close_fds=True, stdout=outf, stderr=errf)
#assert teed_call(["ping", "-c","5","1.com"], close_fds=True, stdout=outf, stderr=errf)
#assert teed_call(["ping", "-c","5","2.com"], close_fds=True, stdout=outf, stderr=errf)


#import subprocess
#import sys
#import logging
#import sys

#class StreamToLogger(object):
    #"""
    #Fake file-like stream object that redirects writes to a logger instance.
    #"""
    #def __init__(self, logger, log_level=logging.INFO):
        #self.logger = logger
        #self.log_level = log_level
        #self.linebuf = ''

    #def write(self, buf):
        #for line in buf.rstrip().splitlines():
            #self.logger.log(self.log_level, line.rstrip())

#logging.basicConfig(
    #level=logging.DEBUG,
   #format='%(asctime)s:%(levelname)s:%(name)s:%(message)s',
   #filename="/home/jimmy/Desktop/out.log",
   #filemode='a'
#)

#stdout_logger = logging.getLogger('STDOUT')
###stdout_logger.info('stdout_logger')
#sl1 = StreamToLogger(stdout_logger, logging.INFO)
###sys.stdout = sl

#stderr_logger = logging.getLogger('STDERR')
#sl2 = StreamToLogger(stderr_logger, logging.ERROR)
#sys.stderr = sl
#stderr_logger.error('error')
#print "Test to standard out"
#raise Exception('Test to standard error') 

#process = subprocess.check_call(['top'],stdout=sl)


##! /usr/bin/env python
#from subprocess import PIPE, Popen
#from threading import Thread
#from Queue import Queue, Empty
#import time

#q = Queue()

#def parsestring(mystr):
    #newstring = mystr[0:mystr.find('bytes')]
    #return newstring

#def enqueue(out, q):
    #for line in proc1.stderr:
        #q.put(line)
    #out.close()

#def getstatus():
    #while proc1.poll() == None:
        #proc2 = Popen(["kill -USR1 $(pgrep ^dd)"], bufsize=1, shell=True)
        #time.sleep(2)

#with open("log_file.log", mode="a") as log_fh:
    #start_time = time.time()

    ##start the imaging
    #proc1 = Popen(["ping -c 1000 baidu.com"], bufsize=1, stderr=PIPE, shell=True)

    ##define and start the queue function thread
    #t = Thread(target=enqueue, args=(proc1.stderr, q))
    #t.daemon = True
    #t.start()

    ##define and start the getstatus function thread
    #t_getstatus = Thread(target=getstatus, args=())
    #t_getstatus.daemon
    #t_getstatus.start()

    ##get the string from the queue

    #while proc1.poll() == None:
        #try: nline = q.get_nowait()
        #except Empty:
            #continue
        #else:
            #mystr = nline.decode('utf-8')           
            #if mystr.find('bytes') > 0:
                #log_fh.write(str(time.time()) + ' - ' + parsestring(mystr))
                #log_fh.flush()

        ##put in a delay
        ##time.sleep(2)

    ##print duration
    #end_time=time.time()
    #duration=end_time-start_time
    #print('Took ' + str(duration) + ' seconds')     
    

#import io
#from subprocess import PIPE, Popen
#from time import time

#cmd = "ping -c 10 baidu.com".split()
#with Popen(cmd, stderr=PIPE) as process, open("log_file.log", "a") as log_file:
    #start_time = time()
    #for line in io.TextIOWrapper(process.stderr, newline=''):
        #print line, True, '' # no newline ('\n')
        #if 'bytes' in line:
            ## XXX parse line here, add flush=True if necessary
            #file=log_file
            ##print(line, file=log_file)
            #print 1,line
    ## print duration
    #print('Took {duration} seconds'.format(duration=time() - start_time))
    
#import shlex
#import logging
#import subprocess
#from StringIO import StringIO
#from subprocess import CalledProcessError
#import sys

#logging.basicConfig(
    #level=logging.DEBUG,
   #format='%(asctime)s:%(levelname)s:%(name)s:%(message)s',
   #filename="/home/jimmy/Desktop/out.log",
   #filemode='a'
#)
#stdout_logger = logging.getLogger('STDOUT')

#def log_subprocess_output(pipe):
    #for line in iter(pipe.readline, b''): # b'\n'-separated lines
        ##sys.stdout.write(line)
        #stdout_logger.info('got line from subprocess: %r', line)

#def run_shell_command(command_line):
    #command_line_args = shlex.split(command_line)

    #logging.info('Subprocess: "' + command_line + '"')

    #try:
        #command_line_process = subprocess.Popen(
            #command_line_args,
            #stdout=subprocess.PIPE,
            #stderr=subprocess.STDOUT,
        #)

        #process_output, _ =  command_line_process.communicate()

        ## process_output is now a string, not a file,
        ## you may want to do:
        ##process_output = StringIO(process_output)
        #log_subprocess_output(process_output)
        #log_subprocess_output(_)
    #except (OSError, CalledProcessError) as exception:
        #logging.info('Exception occured: ' + str(exception))
        #logging.info('Subprocess failed')
        #return False
    #else:
        ## no exception was raised
        #logging.info('Subprocess finished')

    #return True    
#run_shell_command('ping -c 100 baidu.com')

#from subprocess import Popen, PIPE, STDOUT

#def log_subprocess_output(pipe):
    #for line in iter(pipe.readline, b''): # b'\n'-separated lines
        #logging.info('got line from subprocess: %r', line)
        
#process = Popen('/bin/ping -c 100 baidu.com', stdout=PIPE, stderr=STDOUT)
#with process.stdout:
    #log_subprocess_output(process.stdout)
#exitcode = process.wait() # 0 means success

#import logging
#import subprocess
#rootLogger = logging.getLogger()
#logging.basicConfig(
    #level=logging.DEBUG,
   #format='%(asctime)s:%(levelname)s:%(name)s:%(message)s',
   #filename="/home/jimmy/Desktop/out.log",
   #filemode='a'
#)
#proc = subprocess.Popen('ping -c 1 baidu.com', stdout=subprocess.PIPE, shell=True)
#(out, err) = proc.communicate()
#logging.info('This is the main script. Here\'s the program output:')
#logging.info(out)

#import subprocess
#import shlex
#import logging

##process = subprocess.Popen(shlex.split('ping -c 100 baidu.com'), stdout=subprocess.PIPE)



#logging.basicConfig(
    #level=logging.DEBUG,
   #format='%(asctime)s:%(levelname)s:%(name)s:%(message)s',
   #filename="/home/jimmy/Desktop/out.log",
   #filemode='a'
#)
#rootLogger = logging.getLogger(__name__)
#def run_command(command):
    #process = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    
    #while True:
        #stdout = process.stdout.readline()
        #if process.stderr is None:
            #stderr = None
        #else:
            #stderr = process.stderr.readline()
        #if stdout == '' and process.poll() is not None:
            #break
        #if stdout:
            #rootLogger.info(stdout.strip())
            #print stdout.strip()
        #if stderr == '' and process.poll() is not None:
            #break
        #if stderr:
            #rootLogger.error(stderr.strip())
            #print stderr.strip()    
    #rc = process.poll()
    
    ##return rc
##run_command('cat /etc/pass')
#run_command('ping -c 100 192.168.1.1')
##print 111111111111111111
##run_command('ping -c 10 taobao.com')

#import logging
#import threading
#import os
#import subprocess
#import sys

#logging.basicConfig(format='%(asctime)s:%(levelname)s:%(name)s:%(message)s', level=logging.INFO,filename="/home/jimmy/Desktop/out.log",)

#class LogPipe(threading.Thread):

    #def __init__(self, level):
        #"""Setup the object with a logger and a loglevel
        #and start the thread
        #"""
        #threading.Thread.__init__(self)
        #self.daemon = False
        #self.level = level
        #self.fdRead, self.fdWrite = os.pipe()
        #self.pipeReader = os.fdopen(self.fdRead)
        #self.start()

    #def fileno(self):
        #"""Return the write file descriptor of the pipe
        #"""
        #return self.fdWrite

    #def run(self):
        #"""Run the thread, logging everything.
        #"""
        #for line in iter(self.pipeReader.readline, ''):
            #logging.log(self.level, line.strip('\n'))
            #if self.level in (logging.ERROR,logging.CRITICAL,logging.WARNING):
                #sys.stderr.write(line)
            #else:
                #sys.stdout.write(line)
        #self.pipeReader.close()

    #def close(self):
        #"""Close the write end of the pipe.
        #"""
        #os.close(self.fdWrite)

## For testing
#if __name__ == "__main__":
    #import traceback
    #try:    
        #logpipe = LogPipe(logging.INFO)
        #logpipeerr = LogPipe(logging.ERROR)
        #subprocess.Popen(['ping','-c','100','baidu.com'], stdout=logpipe, stderr=logpipeerr)
        #logpipe.close()
        #sys.exit()
    #except Exception:
        #print traceback.print_exc()

"""
http://stefaanlippens.net/python-asynchronous-subprocess-pipe-reading/
"""
import sys
import subprocess
import random
import time
import threading
import Queue
import shlex
import thread

class AsynchronousFileReader(threading.Thread):
    '''
    Helper class to implement asynchronous reading of a file
    in a separate thread. Pushes read lines on a queue to
    be consumed in another thread.
    '''

    def __init__(self, fd, queue):
        assert isinstance(queue, Queue.Queue)
        assert callable(fd.readline)
        threading.Thread.__init__(self)
        self._fd = fd
        self._queue = queue

    def run(self):
        '''The body of the tread: read lines and put them on the queue.'''
        for line in iter(self._fd.readline, ''):
            self._queue.put(line)

    def eof(self):
        '''Check whether there is no more content to expect.'''
        return not self.is_alive() and self._queue.empty()

def consume(command,tasknum):
    '''
    Example of how to consume standard output and standard error of
    a subprocess asynchronously without risk on deadlocking.
    '''

    # Launch the command as subprocess.
    process = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Launch the asynchronous readers of the process' stdout and stderr.
    stdout_queue = Queue.Queue()
    stdout_reader = AsynchronousFileReader(process.stdout, stdout_queue)
    stdout_reader.start()
    stderr_queue = Queue.Queue()
    stderr_reader = AsynchronousFileReader(process.stderr, stderr_queue)
    stderr_reader.start()

    # Check the queues if we received some output (until there is nothing more to get).
    while not stdout_reader.eof() or not stderr_reader.eof():
        # Show what we received from standard output.
        while not stdout_queue.empty():
            line = stdout_queue.get()
            print 'Received tasknum %d line on standard output: ' %(tasknum) + repr(line)

        # Show what we received from standard error.
        while not stderr_queue.empty():
            line = stderr_queue.get()
            print 'Received tasknum %d line on standard error: ' %(tasknum) + repr(line)

        # Sleep a bit before asking the readers again.
        time.sleep(.01)

    # Let's be tidy and join the threads we've started.
    stdout_reader.join()
    stderr_reader.join()

    # Close subprocess' file descriptors.
    process.stdout.close()
    process.stderr.close()

def produce(items=10):
    '''
    Dummy function to randomly render a couple of lines
    on standard output and standard error.
    '''
    for i in range(items):
        output = random.choice([sys.stdout, sys.stderr])
        output.write('Line %d on %s\n' % (i, output))
        output.flush()
        time.sleep(random.uniform(.1, 1))

#if __name__ == '__main__':
    ## The main flow:
    ## if there is an command line argument 'produce', act as a producer
    ## otherwise be a consumer (which launches a producer as subprocess).
    ##if len(sys.argv) == 2 and sys.argv[1] == 'produce':
        ##produce(10)
    ##else:
        ##consume(['python', sys.argv[0], 'produce'])
    #for task in range(100):
        #print task
        #t=threading.Thread(target=consume,args=('ping -c %s baidu.com' %(task),task)) 
        ##t.daemon = True
        #t.start()
        ##t.setName(str(task))
        ##t.join()
        ##thread.start_new(consume,('ping -c %s baidu.com' %(task),task))
        #time.sleep(.1)
        
    #produce(10)



#!/usr/bin/env python
"""Redirect stdout to a file and a terminal inside a script."""
import os
import pty
import sys

def main():
    print 'put your code here'
    for task in range(100):
        print task
        t=threading.Thread(target=consume,args=('ping -c %s baidu.com' %(task),task)) 
        #t.daemon = True
        t.start()
        t.setName(str(task))
        #t.join()
        #thread.start_new(consume,('ping -c %s baidu.com' %(task),task))
        time.sleep(.1)

if __name__=="__main__":
    sentinel_option = '--dont-spawn'
    if sentinel_option not in sys.argv:
        # run itself copying output to the log file
        with open('script.log', 'wb') as log_file:
            def read(fd):
                data = os.read(fd, 1024)
                log_file.write(data)
                return data

            argv = [sys.executable] + sys.argv + [sentinel_option]
            rc = pty.spawn(argv, read)
    else:
        sys.argv.remove(sentinel_option)
        rc = main()
    sys.exit(rc)