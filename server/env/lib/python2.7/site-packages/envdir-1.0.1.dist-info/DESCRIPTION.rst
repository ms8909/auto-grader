envdir (Python port)
====================

.. image:: https://api.travis-ci.org/jezdez/envdir.svg
   :alt: Linux Build Status
   :target: https://travis-ci.org/jezdez/envdir

.. image:: https://ci.appveyor.com/api/projects/status/0fh77wei6cj5hei5?svg=true
   :alt: Windows Build Status
   :target: https://ci.appveyor.com/project/jezdez/envdir

This is a Python port of daemontools_' tool envdir_. It works on Windows and
other systems which can run Python. It's well tested and doesn't need a
compiler to be installed.

envdir runs another program with a modified environment according to files
in a specified directory.

So for example, imagine a software you want to run on a server but don't
want to leave certain configuration variables embedded in the program's source
code. A common pattern to solve this problem is to use environment variables
to separate configuration from code.

envdir allows you to set a series of environment variables at once to simplify
maintaining complicated environments, for example in which you have multiple sets
of those configuration variables depending on the infrastructure you run your
program on (e.g. Windows vs. Linux, Staging vs. Production, Old system vs.
New system etc).

Let's have a look at a typical envdir:

.. code-block:: console

    $ tree envs/prod/
    envs/prod/
    ├── DJANGO_SETTINGS_MODULE
    ├── MYSITE_DEBUG
    ├── MYSITE_DEPLOY_DIR
    ├── MYSITE_SECRET_KEY
    └── PYTHONSTARTUP

    0 directories, 3 files
    $ cat envs/prod/DJANGO_SETTINGS_MODULE
    mysite.settings
    $

As you can see each file has a capitalized name and contains the value of the
environment variable to set when running your program. To use it, simply
prefix the call to your program with envdir:

.. code-block:: console

    $ envdir envs/prod/ python manage.py runserver

That's it, nothing more and nothing less. The way you structure your envdir
is left to you but can easily match your configuration requirements and
integrate with other configuration systems. envdirs contain just files after
all.

An interesting summary about why it's good to store configuration values in
environment variables can be found on the 12factor_ site.

.. note::

   This Python port behaves different for multi line environment variables.
   It will not only read the first line of the file but the whole file. Take
   care with big files!

.. tip::

    Feel free to open tickets at https://github.com/jezdez/envdir/issues.

.. _12factor: http://12factor.net/config
.. _daemontools: http://cr.yp.to/daemontools.html
.. _envdir: http://cr.yp.to/daemontools/envdir.html


Changelog
---------


1.0.0 (26/03/2018)
^^^^^^^^^^^^^^^^^^

* Drop python 2.6, 3.2 and 3.3

* Add explicit support for python 3.6

* Add support for symlinks

* Improved support for windows

0.7 (08/10/2014)
^^^^^^^^^^^^^^^^

* Use `exec` (`os.execvpe`) to replace the envdir process with the child
  process (fixes #20).

* Change `isenvvar()` to only check for `=` in var names.

0.6.1 (12/23/2013)
^^^^^^^^^^^^^^^^^^

* Fixed handling SIGTERM signals to make sure all children of the forked
  process are killed, too. Thanks to Horst Gutmann for the report and
  help fixing it.

0.6 (12/03/2013)
^^^^^^^^^^^^^^^^

* Rewrote tests with pytest.

* Vastly extended Python API.

* Added Sphinx based docs: https://envdir.readthedocs.io/

* Fixed killing child process when capturing keyboard interrupt.

* Added standalone script based on PEPs 441 and 397, compatible with
  Python Launcher for Windows. See the installation instructions for more
  info.

0.5 (09/22/2013)
^^^^^^^^^^^^^^^^

* Added check if the the provided path is a directory and throw an error if
  not. This adds compatibility to the daemontools' envdir.

* Make sure to convert Nulls (``\0``) to newlines as done so in daemontools'
  envdir.

0.4.1 (08/21/2013)
^^^^^^^^^^^^^^^^^^

* Fixed ``envdir.read()`` to actually work with already existing environment
  variables. Extended docs to test Python use.

0.4 (08/09/2013)
^^^^^^^^^^^^^^^^

* Added ``envshell`` command which launches a subshell using the environment
  as defined in the given envdir. Example::

    $ envshell ~/mysite/envs/prod/
    Launching envshell for /home/jezdez/mysite/envs/prod. Type 'exit' or 'Ctrl+D' to return.
    $ python manage.py runserver
    ..

0.3 (07/30/2013)
^^^^^^^^^^^^^^^^

* Catch ``KeyboardInterrupt`` exceptions to not show a traceback from envdir
  but the repsonse from the called command.

* Allow multiline environment variables. Thanks to Horst Gutmann for the
  suggestion. This is a departure from daemontools' standard which only
  allows the first line of the environment variable file.

0.2.1 (07/11/2013)
^^^^^^^^^^^^^^^^^^

* Fixed ``python -m envdir``
* Extended README to better describe the purpose

0.2 (07/10/2013)
^^^^^^^^^^^^^^^^

* Added ability to use envdir from Python.

0.1 (07/10/2013)
^^^^^^^^^^^^^^^^

* Initial release.


