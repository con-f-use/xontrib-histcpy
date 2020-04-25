xontrib-histcpy
---------------
Useful aliases and shortcuts for extracting links and text from command
output history in [xonsh](https://xon.sh).

![xontrib-histcpy in action](https://user-images.githubusercontent.com/11145016/58191616-3cabca80-7cbf-11e9-9472-b8fd74187189.png)

------

Usage
=====

If you use [prompt toolkit](https://python-prompt-toolkit.readthedocs.io/en/master/), `histcpy` will bind the follow shortcuts:

 * <kbd>Alt</kbd> + <kbd>u</kbd>: Open one of the URLs that a previous command wrote to output in your web browser
 * <kbd>Alt</kbd> + <kbd>y</kbd>: Copy one of the URLs to clipboard

The same functionality and more is available with the following command aliases (even when not using ptk):

 * `getout`: Copy the output of one of the last few commands to clipboard (without re-running the command - uses history)
 * `cpyclip`: Copy one of the last few URLs that a command wrote to stdout to clipboard (Alt+y keybinding)
 * `cpyclip`: Open one of the last few URLs that a command wrote to stdout in your browser (Alt+u keybinding)

Currently, `histcpy` can only work with the default `$XONSH_HISTORY_BACKEND` 
(i.e. it does not work with the `sqlite` backend, only `json`).
You also need to set `$XONSH_STORE_STDOUT=True`, obviously.

Installation
============

Just do a
```console
pip install xontrib-histcpy
```

or you can clone the repo with pip
```console
pip install git+https://github.com/con-f-use/xontrib-histcpy
```

Configuration
=============

To automatically load `histcpy` on startup, put
```console
xontrib load histcpy
```

in your `.xonshrc`.

ToDo
====

 * Do an alias+shortcut for getting paths for files and directories and such from history (only existing on filesystem?)
 * Make shortcuts configurable
 * Use `@events.onpostcommand` as fallback if not `XONSH_STORE_STDOUT` (see #14)
