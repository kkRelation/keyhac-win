from keyhac import *


# ---------------------------------------------------------------------------
# Trie node
# ---------------------------------------------------------------------------
class _Trie:
    __slots__ = ("ch", "action", "trig")
    def __init__(self):
        self.ch     = {}    # str -> _Trie
        self.action = None
        self.trig   = None  # "up" | "down"


# ---------------------------------------------------------------------------
# Active sequence context  (one at a time, shared across all scopes)
# ---------------------------------------------------------------------------
class _Ctx:
    __slots__ = ("pfx", "pfx_nm", "nodes", "down", "done", "matched", "gen")
    def __init__(self, pfx, pfx_nm, nodes):
        self.pfx     = pfx
        self.pfx_nm  = pfx_nm
        self.nodes   = nodes   # list[_Trie] current candidates
        self.down    = True    # is prefix physically held?
        self.done    = False   # action fired or fully cancelled?
        self.matched = []      # suffix keys matched so far
        self.gen     = 0       # tap-schedule generation


# ---------------------------------------------------------------------------
# Shared dispatcher  (one instance per Keyhac session)
# ---------------------------------------------------------------------------
class _Dispatcher:
    TAP_TIMEOUT = 50  # ms, time to wait for suffix after prefix tap or release

    def __init__(self, keymap):
        self.keymap = keymap
        self.roots  = {}   # (pfx, scope|None) -> _Trie root
        self.ctx    = None # _Ctx | None

    # ---- Trie registration ----
    def register(self, scope, pfx, keys, action, trig):
        rk = (pfx, scope)
        if rk not in self.roots:
            self.roots[rk] = _Trie()
        node = self.roots[rk]
        for k in keys:
            if k not in node.ch:
                node.ch[k] = _Trie()
            node = node.ch[k]
        node.action = action
        node.trig   = trig

    # ---- Key name helper ----
    _KN = {
        ";": "Semicolon", ",": "Comma",  ".": "Period",  "/": "Slash",
        "[": "OpenBracket", "]": "CloseBracket", "\\": "BackSlash",
        "'": "Quote",  "-": "Minus",  "=": "Plus",  "`": "BackQuote",
        "esc": "Escape",  "return": "Enter",
        "capital": "CapsLock", "caps": "CapsLock",
    }
    def kn(self, key):
        n = str(key).lower()
        return self._KN.get(n, str(key))

    def emit(self, key_name):
        self.keymap.InputKeyCommand(key_name)()

    def fire(self, action):
        if callable(action):
            action()
        elif isinstance(action, (list, tuple)):
            for a in action:
                if callable(a): a()

    # ---- Sequence logic ----
    def try_sfx_down(self, key):
        """Try to advance active sequence. Returns True if key was consumed."""
        c = self.ctx
        if c is None or c.done:
            return False
        c.gen += 1
        nxt = [n.ch[key] for n in c.nodes if key in n.ch]
        if not nxt:
            self._cancel(c, emit_pfx=not c.done)
            return False
        c.nodes = nxt
        c.matched.append(key)
        for node in nxt:
            if node.action is not None and node.trig == "down":
                self.fire(node.action)
                c.done = True
                self.ctx = None
                return True
        return True

    def try_sfx_up(self, key):
        """Handle suffix key-up. Returns True if we handled it."""
        c = self.ctx
        if c is None or c.done:
            return False
        if not c.matched or key != c.matched[-1]:
            return False
        # Fire regardless of whether prefix is still held (supports fast typing
        # where prefix releases before suffix, e.g. D-g D-n U-g U-n)
        for node in c.nodes:
            if node.action is not None and node.trig == "up":
                self.fire(node.action)
                c.done = True
                self.ctx = None
                return True
        # Typing-friendly fallback:
        # If prefix is already released and current branch is still incomplete,
        # releasing the current suffix key means user likely wanted raw typing
        # (e.g. "sp..."), so replay immediately instead of waiting for more.
        if not c.down:
            has_next = any(bool(n.ch) for n in c.nodes)
            if has_next:
                self._cancel(c, emit_pfx=True)
                return True
        # If we got here, it's a suffix release but no 'up' action is defined.
        # Keep ctx for possible chained suffix (e.g. g-p-p) while prefix is held.
        return True

    def _cancel(self, c, emit_pfx):
        self.ctx = None
        if emit_pfx:
            self.emit(c.pfx_nm)
        for k in c.matched:
            self.emit(self.kn(k))

    def sched_tap(self, c):
        c.gen += 1
        gen = c.gen
        d   = self
        def _tap():
            if d.ctx is c and c.gen == gen and not c.done:
                d.emit(c.pfx_nm)
                d.ctx = None
        self.keymap.delayedCall(_tap, self.TAP_TIMEOUT)

    def sched_sfx_up_wait(self, c):
        """Prefix released before suffix U-event: wait up to 50ms for the suffix.
        If it arrives, try_sfx_up will handle it. If not, cancel and emit raw keys."""
        c.gen += 1
        gen = c.gen
        d   = self
        def _expire():
            if d.ctx is c and c.gen == gen and not c.done:
                d._cancel(c, emit_pfx=True)
        self.keymap.delayedCall(_expire, self.TAP_TIMEOUT)

    def sched_cont_wait(self, c):
        """Prefix released mid-sequence: wait briefly for remaining suffix D-events."""
        c.gen += 1
        gen = c.gen
        d   = self
        def _expire():
            if d.ctx is c and c.gen == gen and not c.done:
                d._cancel(c, emit_pfx=True)
        self.keymap.delayedCall(_expire, self.TAP_TIMEOUT)



# ---------------------------------------------------------------------------
# Per-scope key binder
# ---------------------------------------------------------------------------
_FLUSHER_KEYS = (
    [chr(c) for c in range(ord("a"), ord("z") + 1)]
    + [str(n) for n in range(10)]
    + [
        "Minus", "Plus", "Comma", "Period", "Semicolon", "Slash",
        "BackQuote", "OpenBracket", "BackSlash", "CloseBracket",
        "Quote", "Space", "Tab", "Back", "Enter", "Escape",
        "Insert", "Delete", "Home", "End", "PageUp", "PageDown",
        "Left", "Right", "Up", "Down", "Apps", "PrintScreen",
        "ScrollLock", "Pause", "NumLock", "Divide", "Multiply",
        "Subtract", "Add", "Decimal",
    ]
    + ["F%d" % i for i in range(1, 13)]
    + ["Num%d" % i for i in range(10)]
    + ["LWin", "RWin"]
)


class _ScopeKm:
    """Manages key bindings for one scope's window_keymap."""
    def __init__(self, d, scope, km):
        self.d      = d       # _Dispatcher
        self.scope  = scope   # str|None
        self.km     = km      # Keyhac window_keymap
        self.pfxs   = {}      # pfx -> key_name
        self.sfxs   = set()   # normalized suffix keys
        self.fls    = set()   # "D-KeyName" strings already bound as flushers
        self._dirty = False   # needs refresh_fl?

    def bind_pfx(self, pfx):
        if pfx in self.pfxs:
            return
        nm = self.d.kn(pfx)
        dk = "D-" + nm
        # Overwrites any existing flusher bound at the same D- slot
        self.km[dk]           = self._mk_pfx_d(pfx, nm)
        self.km["U-" + nm]    = self._mk_pfx_u(pfx, nm)
        self.pfxs[pfx]        = nm
        self.fls.discard(dk)
        self._dirty = True

    def bind_sfx(self, key):
        n = str(key).lower()
        if n in self.pfxs or n in self.sfxs:
            return
        nm = self.d.kn(key)
        dk = "D-" + nm
        # Overwrites any existing flusher bound at the same D- slot
        self.km[dk]           = self._mk_sfx_d(n, nm)
        self.km["U-" + nm]    = self._mk_sfx_u(n, nm)
        self.sfxs.add(n)
        self.fls.discard(dk)
        self._dirty = True

    def flush_if_dirty(self):
        """Register flushers for all remaining unbound keys (call once after all sequences)."""
        if not self._dirty:
            return
        self._dirty = False
        excl = set(self.pfxs) | self.sfxs
        for k in _FLUSHER_KEYS:
            n  = str(k).lower()
            nm = self.d.kn(k)
            dk = "D-" + nm
            if n in excl or dk in self.fls:
                continue
            self.km[dk] = self._mk_fl(n, nm)
            self.fls.add(dk)

    # ---- Prefix handlers ----
    def _mk_pfx_d(self, pfx, nm):
        d     = self.d
        scope = self.scope
        def handler():
            c = d.ctx
            if c is not None:
                if c.pfx == pfx:
                    if not c.done:
                        c.gen += 1   # cancel any pending tap
                        if c.down:
                            # OS key-repeat: key never released, stay in ctx
                            c.done = True
                            d.emit(nm)   # emit the pending/current char
                            return
                        else:
                            # Quick re-press: prefix was released between presses
                            d.emit(nm)   # emit the pending/current char
                            # Clear old ctx and fall through to start a fresh one
                            d.ctx = None
                    else:
                        # c.done=True: already in OS repeat mode, keep emitting
                        d.emit(nm)
                        return
                else:
                    # Different prefix active -> try as suffix
                    if d.try_sfx_down(pfx):
                        return
                    # Dead end -> cancel old ctx, fall through to start new
            # Start new prefix context: look up this scope's Trie + global Trie
            nodes = []
            if scope is not None and (pfx, scope) in d.roots:
                nodes.append(d.roots[(pfx, scope)])
            if (pfx, None) in d.roots:
                nodes.append(d.roots[(pfx, None)])
            if not nodes:
                d.emit(nm)
                return
            d.ctx = _Ctx(pfx, nm, nodes)
        return handler

    def _mk_pfx_u(self, pfx, nm):
        d = self.d
        def handler():
            c = d.ctx
            if c is None or c.pfx != pfx:
                d.try_sfx_up(pfx)
                return
            c.down = False
            if c.done:
                d.ctx = None
                return
            if not c.matched:
                d.sched_tap(c)
                return
            # matched non-empty: if nodes have a trig='up' action, give suffix
            # U-event a timeout tolerance window before cancelling
            has_up = any(n.action is not None and n.trig == "up" for n in c.nodes)
            if has_up:
                d.sched_sfx_up_wait(c)
                return
            # If current nodes still have children, sequence is incomplete
            # (e.g. s-p-5). Keep ctx briefly so final D-event can arrive.
            has_next = any(bool(n.ch) for n in c.nodes)
            if has_next:
                d.sched_cont_wait(c)
                return
            d._cancel(c, emit_pfx=True)
        return handler

    # ---- Suffix handlers ----
    def _mk_sfx_d(self, key, nm):
        d = self.d
        def handler():
            if not d.try_sfx_down(key):
                d.emit(nm)
        return handler

    def _mk_sfx_u(self, key, nm):
        d = self.d
        def handler():
            d.try_sfx_up(key)
        return handler

    # ---- Flusher ----
    def _mk_fl(self, key, nm):
        d = self.d
        def handler():
            c = d.ctx
            if c is not None:
                d._cancel(c, emit_pfx=not c.done)
            d.emit(nm)
        return handler


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------
class PowerKeyManager:
    """
    Per-scope PowerKey manager using a shared Trie dispatcher.

    Usage (unchanged from previous versions):
        km, pk = PowerKeyManager.for_scope(keymap, "exe:foo.exe", exe_name="foo.exe")
        pk.add("f", {"n": some_action})
        pk.finalize()   # call once after all pk.add() calls for this scope
    """

    _disp      = None  # shared _Dispatcher
    _scopes    = {}    # scope_key -> _ScopeKm
    _global_km = None  # global km created first so exe-keymaps defined later win

    @classmethod
    def _get_disp(cls, keymap):
        if cls._disp is not None and cls._disp.keymap is not keymap:
            cls._disp = None
            cls._scopes = {}
            cls._global_km = None

        if cls._disp is None:
            # Create global km FIRST: Keyhac gives higher priority to later-defined
            # keymaps, so all exe-specific keymaps created afterward will win.
            cls._global_km = keymap.defineWindowKeymap()
            cls._disp      = _Dispatcher(keymap)
            skm = _ScopeKm(cls._disp, None, cls._global_km)
            cls._scopes["__global__"] = skm
        return cls._disp

    @classmethod
    def for_scope(cls, keymap, scope_name, **wk):
        d = cls._get_disp(keymap)  # ensures global km is pre-created first

        scope = None
        if wk.get("exe_name"):
            scope = str(wk["exe_name"]).lower()
        elif str(scope_name).lower().startswith("exe:"):
            scope = str(scope_name)[4:].lower()

        sk = scope or "__global__"
        if sk == "__global__":
            km = cls._global_km  # reuse pre-created km; do NOT redefine
        else:
            km = keymap.defineWindowKeymap(**wk)

        if sk not in cls._scopes:
            cls._scopes[sk] = _ScopeKm(d, scope, km)

        skm = cls._scopes[sk]
        return km, _Proxy(d, skm, scope)


class _Proxy:
    """Thin proxy returned to caller code."""
    __slots__ = ("d", "skm", "scope")
    def __init__(self, d, skm, scope):
        self.d    = d
        self.skm  = skm
        self.scope = scope

    def add(self, pfx_key, combos, **kw):
        for seq, action in combos.items():
            self.add_sequence(pfx_key, seq, action, **kw)

    def add_sequence(self, pfx_key, seq, action, trigger_on=None, **_kw):
        pfx = str(pfx_key).lower()
        if isinstance(seq, str):
            keys = [p for p in seq.split("-") if p]
        elif isinstance(seq, (list, tuple)):
            keys = list(seq)
        else:
            keys = [seq]
        keys = [str(k).lower() for k in keys]

        if trigger_on is None:
            trigger_on = "up" if len(keys) == 1 else "down"

        self.d.register(self.scope, pfx, keys, action, trigger_on)
        self.skm.bind_pfx(pfx)
        for k in keys:
            self.skm.bind_sfx(k)

    def finalize(self):
        """Register flushers for all remaining keys. Call once after all add() calls."""
        self.skm.flush_if_dirty()
