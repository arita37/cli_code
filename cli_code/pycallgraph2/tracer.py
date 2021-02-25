from __future__ import division

import inspect
import sys
import os
import time
from distutils import sysconfig
from collections import defaultdict
from threading import Thread
try:
    from Queue import Queue, Empty
except ImportError:
    from queue import Queue, Empty

from .util import Util


class SynchronousTracer(object):

    def __init__(self, outputs, config):
        self.processor = TraceProcessor(outputs, config)
        self.config = config

    def tracer(self, frame, event, arg):
        self.processor.process(frame, event, self.memory())
        return self.tracer

    def memory(self):
        if self.config.memory:
            from .memory_profiler import memory_usage
            return int(memory_usage(-1, 0)[0] * 1000000)

    def start(self):
        sys.settrace(self.tracer)

    def stop(self):
        sys.settrace(None)

    def done(self):
        pass


class AsynchronousTracer(SynchronousTracer):

    def start(self):
        self.processor.start()
        SynchronousTracer.start(self)

    def tracer(self, frame, event, arg):
        self.processor.queue(frame, event, arg, self.memory())
        return self.tracer

    def done(self):
        self.processor.done()
        self.processor.join()


class TraceProcessor(Thread):
    """
    Contains a callback used by sys.settrace, which collects information about
    function call count, time taken, etc.
    """

    def __init__(self, outputs, config):
        Thread.__init__(self)
        self.trace_queue = Queue()
        self.keep_going = True
        self.outputs = outputs
        self.config = config
        self.updatables = [a for a in self.outputs if a.should_update()]

        self.init_trace_data()
        self.init_libpath()

    def init_trace_data(self):
        self.previous_event_return = False

        # A mapping of which function called which other function
        self.call_dict = defaultdict(lambda: defaultdict(int))

        # Current call stack
        self.call_stack = ['__main__']

        # Counters for each function
        self.func_count = defaultdict(int)
        self.func_count_max = 0
        self.func_count['__main__'] = 1

        # Accumulative time per function
        self.func_time = defaultdict(float)
        self.func_time_max = 0

        # Accumulative memory addition per function
        self.func_memory_in = defaultdict(int)
        self.func_memory_in_max = 0

        # Accumulative memory addition per function once exited
        self.func_memory_out = defaultdict(int)
        self.func_memory_out_max = 0

        # Keeps track of the start time of each call on the stack
        self.call_stack_timer = []
        self.call_stack_memory_in = []
        self.call_stack_memory_out = []

    def init_libpath(self):
        self.lib_path = sysconfig.get_python_lib()
        path = os.path.split(self.lib_path)
        if path[1] == 'site-packages':
            self.lib_path = path[0]
        self.lib_path = self.lib_path.lower()

    def queue(self, frame, event, arg, memory):
        data = {
            'frame': frame,
            'event': event,
            'arg': arg,
            'memory': memory,
        }
        self.trace_queue.put(data)

    def run(self):
        while self.keep_going:
            try:
                data = self.trace_queue.get(timeout=0.1)
            except Empty:
                pass
            self.process(**data)

    def done(self):
        while not self.trace_queue.empty():
            time.sleep(0.1)
        self.keep_going = False

    def process(self, frame, event, memory=None):
        """This function processes a trace result. Keeps track of
        relationships between calls.
        """

        if memory is not None and self.previous_event_return:
            # Deal with memory when function has finished so local variables
            # can be cleaned up
            self.previous_event_return = False

            if self.call_stack_memory_out:
                full_name, m = self.call_stack_memory_out.pop(-1)
            else:
                full_name, m = (None, None)

            # NOTE: Call stack is no longer the call stack that may be
            # expected. Potentially need to store a copy of it.
            if full_name and m:
                call_memory = memory - m

                self.func_memory_out[full_name] += call_memory
                self.func_memory_out_max = max(
                    self.func_memory_out_max, self.func_memory_out[full_name]
                )

        if event == 'call':
            keep = True
            code = frame.f_code

            # Stores all the parts of a human readable name of the current call
            full_name_list = []

            # Work out the module name
            module = inspect.getmodule(code)
            if module:
                module_name = module.__name__
                module_path = module.__file__

                if not self.config.include_stdlib \
                        and self.is_module_stdlib(module_path):
                    keep = False

                if module_name == '__main__':
                    module_name = ''
            else:
                module_name = ''

            if module_name:
                full_name_list.append(module_name)

            # Work out the class name
            try:
                class_name = frame.f_locals['self'].__class__.__name__
                full_name_list.append(class_name)
            except (KeyError, AttributeError):
                pass

            # Work out the current function or method
            func_name = code.co_name
            if func_name == '?':
                func_name = '__main__'
            full_name_list.append(func_name)

            # Create a readable representation of the current call
            full_name = '.'.join(full_name_list)

            if len(self.call_stack) > self.config.max_depth:
                keep = False

            # Load the trace filter, if any. 'keep' determines if we should
            # ignore this call
            if keep and self.config.trace_filter:
                keep = self.config.trace_filter(full_name)

            # Store the call information
            if keep:

                if self.call_stack:
                    src_func = self.call_stack[-1]
                else:
                    src_func = None

                self.call_dict[src_func][full_name] += 1

                self.func_count[full_name] += 1
                self.func_count_max = max(
                    self.func_count_max, self.func_count[full_name]
                )

                self.call_stack.append(full_name)
                self.call_stack_timer.append(time.time())

                if memory is not None:
                    self.call_stack_memory_in.append(memory)
                    self.call_stack_memory_out.append([full_name, memory])

            else:
                self.call_stack.append('')
                self.call_stack_timer.append(None)

        if event == 'return':

            self.previous_event_return = True

            if self.call_stack:
                full_name = self.call_stack.pop(-1)

                if self.call_stack_timer:
                    start_time = self.call_stack_timer.pop(-1)
                else:
                    start_time = None

                if start_time:
                    call_time = time.time() - start_time

                    self.func_time[full_name] += call_time
                    self.func_time_max = max(
                        self.func_time_max, self.func_time[full_name]
                    )

                if memory is not None:
                    if self.call_stack_memory_in:
                        start_mem = self.call_stack_memory_in.pop(-1)
                    else:
                        start_mem = None

                    if start_mem:
                        call_memory = memory - start_mem
                        self.func_memory_in[full_name] += call_memory

                        self.func_memory_in_max = max(
                            self.func_memory_in_max,
                            self.func_memory_in[full_name],
                        )

    def is_module_stdlib(self, file_name):
        """
        Returns True if the file_name is in the lib directory. Used to check
        if a function is in the standard library or not.
        """
        return file_name.lower().startswith(self.lib_path)

    def __getstate__(self):
        """Used for when creating a pickle. Certain instance variables can't
        pickled and aren't used anyway.
        """
        odict = self.__dict__.copy()
        dont_keep = [
            'outputs',
            'config',
            'updatables',
            'lib_path',
        ]
        for key in dont_keep:
            del odict[key]

        return odict

    def groups(self):
        grp = defaultdict(list)
        for node in self.nodes():
            grp[node.group].append(node)
        for g in grp.items():
            yield g

    def stat_group_from_func(self, func, calls):
        stat_group = StatGroup()
        stat_group.name = func
        stat_group.group = self.config.trace_grouper(func)
        stat_group.calls = Stat(calls, self.func_count_max)
        stat_group.time = Stat(self.func_time.get(func, 0), self.func_time_max)
        stat_group.memory_in = Stat(
            self.func_memory_in.get(func, 0), self.func_memory_in_max
        )
        stat_group.memory_out = Stat(
            self.func_memory_in.get(func, 0), self.func_memory_in_max
        )
        return stat_group

    def nodes(self):
        for func, calls in self.func_count.items():
            yield self.stat_group_from_func(func, calls)

    def edges(self):
        for src_func, dests in self.call_dict.items():
            if not src_func:
                continue
            for dst_func, calls in dests.items():
                edge = self.stat_group_from_func(dst_func, calls)
                edge.src_func = src_func
                edge.dst_func = dst_func
                yield edge


class Stat(object):
    """Stores a "statistic" value, e.g. "time taken" along with the maximum
    possible value of the value, which is used to calculate the fraction of 1.
    The fraction is used for choosing colors.
    """

    def __init__(self, value, total):
        self.value = value
        self.total = total
        try:
            self.fraction = value / total
        except ZeroDivisionError:
            self.fraction = 0

    @property
    def value_human_bibyte(self):
        """Mebibyte of the value in human readable a form."""
        return Util.human_readable_bibyte(self.value)


class StatGroup(object):
    pass


def simple_memoize(callable_object):
    """Simple memoization for functions without keyword arguments.

    This is useful for mapping code objects to module in this context.
    inspect.getmodule() requires a number of system calls, which may slow down
    the tracing considerably. Caching the mapping from code objects (there is
    *one* code object for each function, regardless of how many simultaneous
    activations records there are).

    In this context we can ignore keyword arguments, but a generic memoizer
    ought to take care of that as well.
    """

    cache = dict()

    def wrapper(*rest):
        if rest not in cache:
            cache[rest] = callable_object(*rest)
        return cache[rest]

    return wrapper


inspect.getmodule = simple_memoize(inspect.getmodule)
