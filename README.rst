django-debug-toolbar-template-flamegraph
========================================

This generates a [Flame Graph](http://www.brendangregg.com/flamegraphs.html) for the rendering of a template.

It borrows a lot from 23andMe's [DjDT Flame Graph](https://github.com/23andMe/djdt-flamegraph).

Setup
-----

* Install ``django-debug-toolbar-template-flamegraph`` via ``pip``
* Add ``template_flamegraph`` to ``INSTALLED_APPS``
* Add ``'template_flamegraph.TemplateFlamegraphPanel'`` to ``DEBUG_TOOLBAR_PANELS``
