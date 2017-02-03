from django.template import Node
from debug_toolbar.panels import Panel

from .flamegraph_utils import Stack, wrap_for_flamegraph


class TemplateFlamegraphPanel(Panel):
    title = 'Template Flamegraph'
    template = 'template_flamegraph/template.html'

    def enable_instrumentation(self):
        self.original_render_annotated = Node.render_annotated
        self.stack = Stack()
        def labeller(args, kwargs):
            return type(args[0]).__name__
        Node.render_annotated = wrap_for_flamegraph(Node.render_annotated, labeller, self.stack)

    def disable_instrumentation(self):
        Node.render_annotated = self.original_render_annotated

    def process_response(self, request, response):
        self.record_stats({'flamegraph': self.stack.to_svg()})
