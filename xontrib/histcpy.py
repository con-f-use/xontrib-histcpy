#!/usr/bin/env xonsh
"""Useful aliases and shortcuts for extracting links and text from command
output history and putting them into the clipboard."""


if __xonsh__.env.get('XONSH_STORE_STDOUT') is not True or __xonsh__.env.get('XONSH_HISTORY_BACKEND') != 'json':
    raise ValueError('xontrib histcpy cannot be loaded, set `$XONSH_STORE_STDOUT=True` and `$XONSH_HISTORY_BACKEND="json"`')


import re
import pyperclip


__all__ = ()


ansi_escape = re.compile(r'(\x9B|\x1B\[)[0-?]*[ -/]*[@-~]')  # or colorama
urlex = re.compile(
    # See:
    # - https://gist.github.com/dperini/729294
    # - https://gist.github.com/pchc2005/b5f13e136a9c9bb2984e5b92802fc7c9
    # protocol identifier
    r"(?:(?:(?:https?|ftp):)?//)"
    # user:pass authentication
    r"(?:\S+(?::\S*)?@)?"
    r"(?:"
    # IP address exclusion
    # private & local networks
    r"(?!(?:10|127)(?:\.\d{1,3}){3})"
    r"(?!(?:169\.254|192\.168)(?:\.\d{1,3}){2})"
    r"(?!172\.(?:1[6-9]|2\d|3[0-1])(?:\.\d{1,3}){2})"
    # IP address dotted notation octets
    # excludes loopback network 0.0.0.0
    # excludes reserved space >= 224.0.0.0
    # excludes network & broadcast addresses
    # (first & last IP address of each class)
    r"(?:[1-9]\d?|1\d\d|2[01]\d|22[0-3])"
    r"(?:\.(?:1?\d{1,2}|2[0-4]\d|25[0-5])){2}"
    r"(?:\.(?:[1-9]\d?|1\d\d|2[0-4]\d|25[0-4]))"
    r"|"
    # host & domain names, may end with dot
    # can be replaced by a shortest alternative
    # u"(?![-_])(?:[-\w\u00a1-\uffff]{0,63}[^-_]\.)+"
    # u"(?:(?:[a-z\u00a1-\uffff0-9]-?)*[a-z\u00a1-\uffff0-9]+)"
    # # domain name
    # u"(?:\.(?:[a-z\u00a1-\uffff0-9]-?)*[a-z\u00a1-\uffff0-9]+)*"
    r"(?:"
    r"(?:"
    r"[a-z0-9\u00a1-\uffff]"
    r"[a-z0-9\u00a1-\uffff_-]{0,62}"
    r")?"
    r"[a-z0-9\u00a1-\uffff]\."
    r")+"
    # TLD identifier name, may end with dot
    r"(?:[a-z\u00a1-\uffff]{2,}\.?)"
    r")"
    # port number (optional)
    r"(?::\d{2,5})?"
    # resource path (optional)
    r"(?:[/?#]\S*)?"
    , re.UNICODE | re.I
)

### getlinks - completion menu based history link extractor

def _histlinks(args=None, stdin=None):
    for itm in filter(lambda x: x.out is not None, reversed(__xonsh__.history)):
        urls = urlex.finditer(itm.out)
        for url in urls:
            yield url.group(0)

def _printlinks(args=None, stdin=None, stdout=None):
    links, out, num = _histlinks(), {}, float(args[0]) if args else 10
    while not args or len(out) < num:
        try:
            itm = "'"+ next(links) +"'"
            oldnum = len(out)
            out[itm] = None  # abused to ensure only unique itmes are printed
            if stdout and len(out)>oldnum:
                print(itm)
        except StopIteration:
            if stdout:
                stdout.close()
                return
            break
    return out.keys()

def _histlink_completer(prefix, line, begidx, endidx, ctx):
    if not any(line.lstrip().startswith(x) for x in ('openbrowser', 'cpyclip')):
        return set()
    return _printlinks()

def _cpy_clip(args=None, stdin=None, stdout=None):
    if not args:
        return
    txt = str(next(iter(args))).strip()
    if txt == '-':
        txt = stdin.read().strip()
    pyperclip.copy(txt)

def _open_browser(args=None, **kw):
    if not args:
        return
    import webbrowser
    webbrowser.open(args[0].strip(), new=1)
    for url in args[1:]:
        webbrowser.open(url.strip(), new=0)


#### getout - Get output from past commands

def _getoutputs(args=None, stdin=None, stdout=None, **kwargs):
    num = float(args[0]) if args else 10
    outs = {}
    for h in filter(lambda x: x.out is not None, reversed(__xonsh__.history)):
        if len(outs) >= num:
            break
        cmd = h.cmd.strip()
        if stdout and cmd not in outs:
            stdout.write(h.out)
        outs[cmd] = h.out
    if stdout is None:
        return outs

def _getouts_completer(prefix, line, begidx, endidx, ctx):
    if not line.lstrip().startswith('getout'):
        return set()
    # ToDo: handle quotation marks better
    def canonize(s):
        return "'"+s.replace('"', '\\"').replace("'", "\\'")+"'"
    return {canonize(o) for o in _getoutputs().keys() if o.startswith(prefix)}

def _getouts(args=None, stdin=None, stdout=None):
    # ToDo: parameterize (lookback, clipboard, printing, returning)
    outs = _getoutputs()
    try:
        out = outs[args[0]].strip()
        pyperclip.copy(ansi_escape.sub('', out))
        if stdout is not None:
            stdout.write(out)
        else:
            return out
    except KeyError:
        pass

### keybindings

aliases['cpyclip'] = _cpy_clip
__xonsh__.completers['cpyclip'] = _histlink_completer
__xonsh__.completers.move_to_end('cpyclip', last=False)


aliases['openbrowser'] = _open_browser
__xonsh__.completers['openbrowser'] = _histlink_completer
__xonsh__.completers.move_to_end('openbrowser', last=False)

aliases['getout'] = _getouts
__xonsh__.completers['getout'] = _getouts_completer
__xonsh__.completers.move_to_end('getout', last=False)

try:
    from prompt_toolkit.keys import Keys
    @events.on_ptk_create
    def outout_keybindings(prompter, history, completer, bindings, **kw):
        """Register keybindings for cpyhist
        See:

            https://python-prompt-toolkit.readthedocs.io/en/master/pages/advanced_topics/key_bindings.html
        """
        if __xonsh__.env.get('SHELL_TYPE') in ["prompt_toolkit", "prompt_toolkit2"]:
            handler = bindings.add
        else:
            handler = bindings.registry.add_binding

        @handler(Keys.Escape, 'y')  # actually alt+y
        def cpy_links_handler(event):
            links = _printlinks()
            if not links:
                return
            elif len(links) == 1:
                _cpy_clip(links)
                return
            event.current_buffer.reset()
            event.current_buffer.insert_text('cpyclip ')
            event.current_buffer.start_completion(select_first=True)


        @handler(Keys.Escape, 'u')  # actually alt+u
        def browse_links_handler(event):
            links = _printlinks()
            if not links:
                return
            event.current_buffer.reset()
            event.current_buffer.insert_text('openbrowser ')
            event.current_buffer.start_completion(select_first=True)
except Exception as e:
    import logging
    logging.debug('Cannot set xontrib-histcpy shortcuts', exc_info=True)
