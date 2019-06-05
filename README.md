xontrib-histcpy
---------------
Useful aliases and shortcuts for extracting links and text from command
output history in [xonsh](https://xon.sh).

![xontrib-histcpy in action](https://user-images.githubusercontent.com/11145016/58191616-3cabca80-7cbf-11e9-9472-b8fd74187189.png)

------

Usage
=====

If you use [ptk(2)-prompts](https://python-prompt-toolkit.readthedocs.io/en/master/), `histcpy` will bind the follow shortcuts:

 * <kbd>Alt</kbd> + <kbd>u</kbd>: Open one of the URLs that a previous command wrote to output in your web browser
 * <kbd>Alt</kbd> + <kbd>y</kbd>: Copy one of the URLs to clipboard

The same functionality and more is available with the following command aliases (even when not using ptk):

 * `getout`: Copy the output of one of the last few commands to clipboard (without re-running the command - uses history)
 * `cpyclip`: Copy one of the last few URLs that a command wrote to stdout to clipboard (Alt+y keybinding)
 * `cpyclip`: Open one of the last few URLs that a command wrote to stdout in your browser (Alt+u keybinding)

If there is only one command/url in history that histcpy could grab,
it might omit displaying a menu entirely.

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

Some commands in xonsh's subprocess mode will not be captured by default.
For those you may enable `$XONSH_STORE_STDOUT=True`. 
However, that might be buggy or slow.

