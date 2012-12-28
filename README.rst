Inirama
#######

Inirama -- Simple parser for INI files

.. image:: https://secure.travis-ci.org/klen/inirama.png?branch=develop
    :target: http://travis-ci.org/klen/inirama
    :alt: Build Status

.. contents::

Requirements
=============

- python 2.7, 3.2


Installation
=============

**Inirama** should be installed using pip: ::

    pip install inirama


Usage
=====

::

    from inirama import Namespace

    parser = Namespace()
    parser.read('config.ini')

    print Parser['section']['key']

    parser['other']['new'] = 'value'
    parser.write('new_config.ini')


Interpolation
-------------
::

    from inirama import Namespace

    parser = Namespace()
    parser.parse("""
    [main]
    test = value
    foo = bar {test}
    more_deep = wow {foo}
    """)
    print parser['main']['more_deep']  # wow bar value


Bug tracker
===========

If you have any suggestions, bug reports or
annoyances please report them to the issue tracker
at https://github.com/klen/inirama/issues


Contributing
============

Development of inirama happens at github: https://github.com/klen/inirama


Contributors
=============

* klen_ (Kirill Klenov)


License
=======

Licensed under a `BSD license`_.


.. _BSD license: http://www.linfo.org/bsdlicense.html
.. _klen: http://klen.github.com/
