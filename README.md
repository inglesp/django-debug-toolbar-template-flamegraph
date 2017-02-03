# django-debug-toolbar-template-flamegraph

This provides a Django Debug Toolbar panel which generates a [Flame Graph](http://www.brendangregg.com/flamegraphs.html) for the rendering of a template.

It is probably worth using in conjunction with the [Template Profiler](https://github.com/node13h/django-debug-toolbar-template-profiler) and/or [Template Timings](https://github.com/orf/django-debug-toolbar-template-timings) panels.

It borrows a lot from 23andMe's [DjDT Flame Graph](https://github.com/23andMe/djdt-flamegraph).

## Setup

* Install `django-debug-toolbar-template-flamegraph` via `pip`
* Add `template_flamegraph` to `INSTALLED_APPS`
* Add `'template_flamegraph.TemplateFlamegraphPanel'` to `DEBUG_TOOLBAR_PANELS`
