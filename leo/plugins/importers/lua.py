#@+leo-ver=5-thin
#@+node:ekr.20170530024520.2: * @file ../plugins/importers/lua.py
"""
The @auto importer for the lua language.

Created 2017/05/30 by the `importer;;` abbreviation.
"""
import re
from typing import Any, Dict, List
from leo.core import leoGlobals as g
from leo.plugins.importers.linescanner import Importer, scan_tuple
delete_blank_lines = True
#@+others
#@+node:ekr.20170530024520.3: ** class Lua_Importer
class Lua_Importer(Importer):
    """The importer for the lua lanuage."""

    def __init__(self, c):
        """Lua_Importer.__init__"""
        super().__init__(
            c,
            language='lua',
            state_class=Lua_ScanState,
        )
        # Contains entries for all constructs that end with 'end'.
        self.start_stack = []

    # Define necessary overrides.
    #@+others
    #@+node:ekr.20170530024520.5: *3* lua_i.compute_headline
    def compute_headline(self, s: str) -> str:
        """Return a cleaned up headline s."""
        s = s.strip()
        for tag in ('local', 'function'):
            if s.startswith(tag):
                s = s[len(tag) :]
        i = s.find('(')
        if i > -1:
            s = s[:i]
        return s.strip()
    #@+node:ekr.20170530031729.1: *3* lua_i.get_new_dict
    #@@nobeautify

    def get_new_dict(self, context):
        """The scan dict for the lua language."""
        comment, block1, block2 = self.single_comment, self.block1, self.block2
        assert (comment, block1, block2) == ('--', '', ''), f"lua: {comment!r} {block1!r} {block2!r}"

        def add_key(d, pattern, data):
            key = pattern[0]
            aList = d.get(key,[])
            aList.append(data)
            d[key] = aList

        d: Dict[str, List[Any]]

        if context:
            d = {
                # key    kind   pattern  ends?
                '\\':   [('len+1', '\\', None),],
                '"':    [('len', '"',    context == '"'),],
                "'":    [('len', "'",    context == "'"),],
            }
            # End Lua long brackets.
            for i in range(10):
                open_pattern = '--[%s[' % ('='*i)
                # Both --]] and ]]-- end the long bracket.
                pattern = ']%s]--' % ('='*i)
                add_key(d, pattern, ('len', pattern, context==open_pattern))
                pattern = '--]%s]' % ('='*i)
                add_key(d, pattern, ('len', pattern, context==open_pattern))
        else:
            # Not in any context.
            d = {
                # key    kind pattern new-ctx  deltas
                '--':   [('all', comment, context, None)],  # Regular comment.
                '\\':   [('len+1', '\\', context, None)],
                '"':    [('len', '"', '"',     None)],
                "'":    [('len', "'", "'",     None)],
                '{':    [('len', '{', context, (1,0,0))],
                '}':    [('len', '}', context, (-1,0,0))],
                '(':    [('len', '(', context, (0,1,0))],
                ')':    [('len', ')', context, (0,-1,0))],
                '[':    [('len', '[', context, (0,0,1))],
                ']':    [('len', ']', context, (0,0,-1))],
            }
            # Start Lua long brackets.
            for i in range(10):
                pattern = '--[%s[' % ('='*i)
                add_key(d, pattern, ('len', pattern, pattern, None))
        return d
    #@+node:ekr.20170530035601.1: *3* lua_i.starts_block
    # Buggy: this could appear in a string or comment.
    # The function must be an "outer" function, without indentation.
    function_pattern = re.compile(r'^(local\s+)?function')
    function_pattern2 = re.compile(r'(local\s+)?function')

    def starts_block(self, i, lines, new_state, prev_state):
        """True if the new state starts a block."""

        def end(line):
            # Buggy: 'end' could appear in a string or comment.
            # However, this code is much better than before.
            i = line.find('end')
            return i if i > -1 and g.match_word(line, i, 'end') else -1

        if prev_state.context:
            return False
        line = lines[i]
        m = self.function_pattern.match(line)
        if m and end(line) < m.start():
            self.start_stack.append('function')
            return True
        # Don't create separate nodes for assigned functions,
        # but *do* push 'function2' on the start_stack for the later 'end' statement.
        m = self.function_pattern2.search(line)
        if m and end(line) < m.start():
            self.start_stack.append('function2')
            return False
        # Not a function. Handle constructs ending with 'end'.
        line = line.strip()
        if end(line) == -1:
            for z in ('do', 'for', 'if', 'while',):
                if g.match_word(line, 0, z):
                    self.start_stack.append(z)
                    break
        return False
    #@-others
#@+node:ekr.20170530024520.7: ** class Lua_ScanState
class Lua_ScanState:
    """A class representing the state of the lua line-oriented scan."""

    def __init__(self, d: Dict=None) -> None:
        if d:
            prev = d.get('prev')
            self.context = prev.context
        else:
            self.context = ''

    def __repr__(self) -> str:
        return "Lua_ScanState context: %r " % (self.context)
    __str__ = __repr__

    #@+others
    #@+node:ekr.20170530024520.8: *3* lua_state.level
    def level(self) -> int:
        """Lua_ScanState.level."""
        return 0  # Never used.
    #@+node:ekr.20170530024520.9: *3* lua_state.update
    def update(self, data: scan_tuple) -> int:
        """
        Lua_ScanState.update: Update the state using the given scan_tuple.
        Return i = data[1]
        """
        self.context = data.context
        return data.i
    #@-others

#@-others
importer_dict = {
    'func': Lua_Importer.do_import(),
    'extensions': ['.lua',],
}
#@@language python
#@@tabwidth -4


#@-leo
