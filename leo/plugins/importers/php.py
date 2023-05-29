#@+leo-ver=5-thin
#@+node:ekr.20140723122936.18148: * @file ../plugins/importers/php.py
"""The @auto importer for the php language."""
from __future__ import annotations
import re
from typing import TYPE_CHECKING
from leo.core import leoGlobals as g  # required
from leo.plugins.importers.base_importer import Importer

if TYPE_CHECKING:
    from leo.core.leoCommands import Commands as Cmdr
    from leo.core.leoNodes import Position

#@+others
#@+node:ekr.20161129213243.2: ** class Php_Importer(Importer)
class Php_Importer(Importer):
    """The importer for the php lanuage."""

    language = 'php'

    #@+others
    #@+node:ekr.20161129213243.4: *3* php_i.compute_headline
    def compute_headline(self, s: str) -> str:
        """Return a cleaned up headline s."""
        return s.rstrip('{').strip()
    #@+node:ekr.20161130044051.1: *3* php_i.skip_heredoc_string (not used)
    # EKR: This is Dave Hein's heredoc code from the old PHP scanner.
    # I have included it for reference in case heredoc problems arise.
    #
    # php_i.scan dict uses r'<<<\s*([\w_]+)' instead of the more complex pattern below.
    # This is likely good enough. Importers can assume that code is well formed.

    def skip_heredoc_string(self, s: str, i: int) -> int:  # pragma: no cover (not used)
        #@+<< skip_heredoc docstrig >>
        #@+node:ekr.20161130044051.2: *4* << skip_heredoc docstrig >>
        #@@nocolor-node
        """
        08-SEP-2002 DTHEIN:  added function skip_heredoc_string
        A heredoc string in PHP looks like:

          <<<EOS
          This is my string.
          It is mine. I own it.
          No one else has it.
          EOS

        It begins with <<< plus a token (naming same as PHP variable names).
        It ends with the token on a line by itself (must start in first position.
        """
        #@-<< skip_heredoc docstrig >>
        j = i
        assert g.match(s, i, "<<<")
        m = re.match(r"\<\<\<([a-zA-Z_\x7f-\xff][a-zA-Z0-9_\x7f-\xff]*)", s[i:])
        if m is None:
            i += 3
            return i
        # 14-SEP-2002 DTHEIN: needed to add \n to find word, not just string
        delim = m.group(1) + '\n'
        i = g.skip_line(s, i)  # 14-SEP-2002 DTHEIN: look after \n, not before
        n = len(s)
        while i < n and not g.match(s, i, delim):
            i = g.skip_line(s, i)  # 14-SEP-2002 DTHEIN: move past \n
        if i >= n:
            g.scanError("Run on string: " + s[j:i])
        elif g.match(s, i, delim):
            i += len(delim)
        return i
    #@-others
#@-others

def do_import(c: Cmdr, parent: Position, s: str) -> None:
    """The importer callback for php."""
    Php_Importer(c).import_from_string(parent, s)

importer_dict = {
    'extensions': ['.php'],
    'func': do_import,
}
#@@language python
#@@tabwidth -4
#@-leo
