=============
Editor Client
=============

EditorClient is a small application which supports the `ODB protocol
<http://www.barebones.com/support/develop/odbsuite.html>`_ developed
by `Bare Bones Software: <http://www.barebones.com/>`_ and runs a
shell command to start an editor in response.  It was originally
written for use with Emacs, but can be used with any editor which can
be started from the command line and blocks until it has finished
editing the file.

Environment Variables
=====================

What editor to open and how can be customized by setting environment
variables (or by editing ``EditorClientWorker.py``).  The variables in
question in order of preference are:

- ``EDITOR_CLIENT_COMMAND`` can be used to specify the whole command
  line.  In this case it must be ready to print ``linenum`` and
  ``filename``.  See below.
- ``EMACSCLIENT`` is used for the editor and ``EMACS`` for the alternate.
- Defaults to ``/Applications/Emacs.app/Contents/MacOS/bin/emacsclient``
  for emacsclient and empty for alternate.

If ``EDITOR_CLIENT_COMMAND`` is set it should be something ready for
Python string formatting taking ``linenum`` and ``filename`` as the
keys (you can ignore linenum if your editor doesn't support it.)
Setting ``EMACSCLIENT`` and ``EMACS`` will produce the same as if you
set ``EDITOR_CLIENT_COMMAND`` to::

    "$EMACSCLIENT -c -a '$EMACS' +%(linenum)s '%(filename)s'"

A Note on Environment Variables in OS X
---------------------------------------

Working with environment variables in OS X can be confusing since
exporting them in ``.bashrc`` for example is ineffective.  Instead you
must `set them
<http://developer.apple.com/mac/library/qa/qa2001/qa1067.html>`_ in
``~/.MacOSX/environment.plist``.  Brian D Foy `wrote about
<http://use.perl.org/~brian_d_foy/journal/8915>`_ a way to
update/create this file based on your shell environment (and which can
be run in ``.bashrc`` for example).
