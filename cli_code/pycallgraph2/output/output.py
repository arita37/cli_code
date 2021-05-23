import re
import os
from distutils.spawn import find_executable

from ..exceptions import PyCallGraphException
from ..color import Color


class Output(object):
    """Base class for all outputters."""

    def __init__(self, **kwargs):
        self.node_color_func = self.node_color
        self.edge_color_func = self.edge_color
        self.node_label_func = self.node_label
        self.edge_label_func = self.edge_label

        # Update the defaults with anything from kwargs
        [setattr(self, k, v) for k, v in kwargs.items()]

    def set_config(self, config):
        """
        This is a quick hack to move the config variables set in Config into
        the output module config variables.
        """
        for k, v in config.__dict__.items():
            if hasattr(self, k) and \
                    callable(getattr(self, k)):
                continue
            setattr(self, k, v)

    def node_color(self, node):
        value = float(node.time.fraction * 2 + node.calls.fraction) / 3
        return Color.hsv(value / 2 + .5, value, 0.9)

    def edge_color(self, edge):
        value = float(edge.time.fraction * 2 + edge.calls.fraction) / 3
        return Color.hsv(value / 2 + .5, value, 0.7)

    def node_label(self, node):
        parts = [
            '{0.name}',
            'calls: {0.calls.value:n}',
            'time: {0.time.value:f}s',
        ]

        if self.processor.config.memory:
            parts += [
                'memory in: {0.memory_in.value_human_bibyte}',
                'memory out: {0.memory_out.value_human_bibyte}',
            ]

        return r'\n'.join(parts).format(node)

    def edge_label(self, edge):
        return '{0}'.format(edge.calls.value)

    def sanity_check(self):
        """Basic checks for certain libraries or external applications.  Raise
        or warn if there is a problem.
        """
        pass

    @classmethod
    def add_arguments(cls, subparsers):
        pass

    def reset(self):
        pass

    def set_processor(self, processor):
        self.processor = processor

    def start(self):
        """Initialise variables after initial configuration."""
        pass

    def update(self):
        """Called periodically during a trace, but only when should_update is
        set to True.
        """
        raise NotImplementedError('update')

    def should_update(self):
        """Return True if the update method should be called periodically."""
        return False

    def done(self):
        """Called when the trace is complete and ready to be saved."""
        raise NotImplementedError('done')

    def ensure_binary(self, cmd):
        if find_executable(cmd):
            return

        raise PyCallGraphException(
            'The command "{0}" is required to be in your path.'.format(cmd))

    def normalize_path(self, path):
        regex_user_expand = re.compile('\A~')
        if regex_user_expand.match(path):
            path = os.path.expanduser(path)
        else:
            path = os.path.expandvars(path)  # expand, just in case
        return path

    def prepare_output_file(self):
        if self.fp is None:
            self.output_file = self.normalize_path(self.output_file)
            self.fp = open(self.output_file, 'wb')

    def verbose(self, text):
        self.processor.config.log_verbose(text)

    def debug(self, text):
        self.processor.config.log_debug(text)

    @classmethod
    def add_output_file(cls, subparser, defaults, help):
        subparser.add_argument(
            '-o', '--output-file', type=str, default=defaults.output_file,
            help=help,
        )
