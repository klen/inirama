|logo| Inirama
##############

.. _description:

Inirama -- Simplest parser for INI-style files.

Features:

    - One single module;
    - No requirements;
    - Tiny interface;
    - Supports variable interpolation;

.. _badges:

.. image:: https://travis-ci.org/klen/inirama.png?branch=develop
    :target: http://travis-ci.org/klen/inirama
    :alt: Build Status

.. image:: https://coveralls.io/repos/klen/inirama/badge.png?branch=develop
    :target: https://coveralls.io/r/klen/inirama
    :alt: Coverals

.. image:: https://pypip.in/v/Inirama/badge.png
    :target: https://crate.io/packages/Inirama
    :alt: Version

.. image:: https://pypip.in/d/Inirama/badge.png
    :target: https://crate.io/packages/Inirama
    :alt: Downloads

.. image:: https://dl.dropboxusercontent.com/u/487440/reformal/donate.png
    :target: https://www.gittip.com/klen/
    :alt: Donate


.. _contents:

Docs are available at https://inirama.readthedocs.org/. Pull requests with
documentation enhancements and/or fixes are awesome and most welcome.


.. contents:: Contents:


.. _requirements:

Requirements
=============

- python (2.6, 2.7, 3.2, 3.3)


.. _installation:

Installation
=============

**Inirama** could be installed using pip: ::

    pip install inirama


.. _quickstart:

Quickstart
==========

::

    from inirama import Namespace

    ns = Namespace()
    ns.read('config.ini')

    print ns['section']['key']

    ns['other']['new'] = 'value'
    ns.write('new_config.ini')


.. _interpolation:

Interpolation
-------------
::

    from inirama import InterpolationNamespace

    ns = InterpolationNamespace()
    ns.parse("""
        [main]
        test = value
        foo = bar {test}
        more_deep = wow {foo}
    """)
    print ns['main']['more_deep']  # wow bar value


.. _bagtracker:

Bug tracker
===========

If you have any suggestions, bug reports or
annoyances please report them to the issue tracker
at https://github.com/klen/inirama/issues


.. _contributing:

Contributing
============

Development of inirama happens at github: https://github.com/klen/inirama


.. _contributors:

Contributors
=============

* klen_ (Kirill Klenov)


.. _license:

License
=======

Licensed under a `BSD license`_.


.. _links:

.. _BSD license: http://www.linfo.org/bsdlicense.html
.. _klen: http://klen.github.com/
.. |logo| image:: https://raw.github.com/klen/inirama/develop/docs/_static/logo.png
                  :width: 100
