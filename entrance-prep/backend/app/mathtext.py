"""LaTeX for the exporters: real Word equations, and readable text for PDF.

The question bank stores LaTeX in `content["math"]` and inline between `$…$` in
prose, which KaTeX renders in the browser. Word has its own equation format
(OMML), and reportlab has no mathematics at all, so both need a conversion.

This covers the bounded subset an entrance-exam paper uses -- scripts,
fractions, roots, delimiters, accents, named functions, sums and integrals,
Greek letters and the usual operators. Anything unrecognised degrades to its
literal text rather than raising, so an export never fails because of one
unusual formula.
"""
import re
from xml.sax.saxutils import escape

M_NS = "http://schemas.openxmlformats.org/officeDocument/2006/math"
W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"

SYMBOLS = {
    "alpha": "α", "beta": "β", "gamma": "γ", "delta": "δ", "epsilon": "ε",
    "varepsilon": "ε", "zeta": "ζ", "eta": "η", "theta": "θ", "vartheta": "ϑ",
    "iota": "ι", "kappa": "κ", "lambda": "λ", "mu": "μ", "nu": "ν", "xi": "ξ",
    "pi": "π", "rho": "ρ", "sigma": "σ", "tau": "τ", "upsilon": "υ",
    "phi": "φ", "varphi": "φ", "chi": "χ", "psi": "ψ", "omega": "ω",
    "Gamma": "Γ", "Delta": "Δ", "Theta": "Θ", "Lambda": "Λ", "Xi": "Ξ",
    "Pi": "Π", "Sigma": "Σ", "Upsilon": "Υ", "Phi": "Φ", "Psi": "Ψ",
    "Omega": "Ω",
    "times": "×", "div": "÷", "pm": "±", "mp": "∓", "cdot": "·",
    "ast": "∗", "star": "⋆", "circ": "∘", "bullet": "∙",
    "leq": "≤", "le": "≤", "geq": "≥", "ge": "≥", "neq": "≠", "ne": "≠",
    "approx": "≈", "equiv": "≡", "sim": "∼", "simeq": "≃", "propto": "∝",
    "ll": "≪", "gg": "≫",
    "rightarrow": "→", "to": "→", "leftarrow": "←", "Rightarrow": "⇒",
    "Leftarrow": "⇐", "leftrightarrow": "↔", "Leftrightarrow": "⇔",
    "mapsto": "↦",
    "infty": "∞", "partial": "∂", "nabla": "∇", "degree": "°", "deg": "°",
    "angle": "∠", "perp": "⊥", "parallel": "∥", "therefore": "∴",
    "because": "∵", "in": "∈", "notin": "∉", "subset": "⊂", "cup": "∪",
    "cap": "∩", "forall": "∀", "exists": "∃", "emptyset": "∅",
    "prime": "′", "ldots": "…", "dots": "…", "cdots": "⋯",
    "%": "%", "&": "&", "#": "#", "$": "$", "_": "_", "{": "{", "}": "}",
}
SPACES = {",": " ", ";": " ", ":": " ", "!": "", " ": " ",
          "quad": "  ", "qquad": "    "}
FUNCTIONS = {"sin", "cos", "tan", "cot", "sec", "csc", "arcsin", "arccos",
             "arctan", "sinh", "cosh", "tanh", "log", "ln", "exp", "lim",
             "max", "min", "gcd", "det"}
NARY = {"sum": "∑", "prod": "∏", "int": "∫", "iint": "∬", "oint": "∮"}
ACCENTS = {"vec": "⃗", "bar": "̄", "overline": "̄", "hat": "̂", "tilde": "̃",
           "dot": "̇", "ddot": "̈"}
OPEN = {"(": "(", "[": "[", "\\{": "{", "|": "|", "\\langle": "⟨", ".": ""}
CLOSE = {")": ")", "]": "]", "\\}": "}", "|": "|", "\\rangle": "⟩", ".": ""}

# A multi-letter command swallows the spaces that end its name, so "\Delta v"
# is "Δv" rather than "Δ v".
TOKEN = re.compile(r"\\[A-Za-z]+ *|\\.|[\^_{}]|[^\\^_{}]")


COMMAND = re.compile(r"\\[A-Za-z]+ *")


def tokenize(latex):
    return [t.rstrip() if COMMAND.fullmatch(t) else t
            for t in TOKEN.findall(latex or "")]


class Parser:
    def __init__(self, tokens):
        self.t, self.i = tokens, 0

    def peek(self):
        return self.t[self.i] if self.i < len(self.t) else None

    def next(self):
        tok = self.peek()
        if tok is not None:
            self.i += 1
        return tok

    def group(self):
        """One argument: a braced group, or a single token."""
        if self.peek() == "{":
            self.next()
            nodes = self.sequence(stop="}")
            if self.peek() == "}":
                self.next()
            return nodes
        tok = self.next()
        return [] if tok is None else self.atom(tok)

    def raw_group(self):
        """Argument kept as literal text, for \\text and \\mathrm."""
        if self.peek() != "{":
            tok = self.next()
            return tok or ""
        self.next()
        depth, out = 1, []
        while self.i < len(self.t):
            tok = self.next()
            if tok == "{":
                depth += 1
            elif tok == "}":
                depth -= 1
                if depth == 0:
                    break
            out.append(tok)
        return "".join(out)

    def sequence(self, stop=None):
        nodes = []
        while True:
            tok = self.peek()
            if tok is None or tok == stop:
                break
            self.next()
            nodes.extend(self.scripted(self.atom(tok)))
        return nodes

    def scripted(self, base):
        """Attach any ^ and _ that follow, in either order."""
        sub = sup = None
        while self.peek() in ("^", "_"):
            which = self.next()
            arg = self.group()
            if which == "^":
                sup = arg
            else:
                sub = arg
        if sub is not None and sup is not None:
            return [("subsup", base, sub, sup)]
        if sub is not None:
            return [("sub", base, sub)]
        if sup is not None:
            return [("sup", base, sup)]
        return base

    def atom(self, tok):
        if tok == "\\frac" or tok == "\\dfrac" or tok == "\\tfrac":
            return [("frac", self.group(), self.group())]
        if tok == "\\sqrt":
            degree = None
            if self.peek() == "[":
                self.next()
                degree = self.sequence(stop="]")
                if self.peek() == "]":
                    self.next()
            return [("rad", degree, self.group())]
        if tok in ("\\text", "\\mathrm", "\\textrm", "\\mathbf", "\\operatorname"):
            return [("text", self.raw_group())]
        if tok == "\\left":
            opener = self.next() or "("
            body = self.sequence(stop="\\right")
            if self.peek() == "\\right":
                self.next()
            closer = self.next() or ")"
            return [("delim", OPEN.get(opener, opener), CLOSE.get(closer, closer), body)]
        name = tok[1:] if tok.startswith("\\") else None
        if name in ACCENTS:
            return [("acc", ACCENTS[name], self.group())]
        if name in NARY:
            sub = sup = None
            while self.peek() in ("^", "_"):
                which = self.next()
                arg = self.group()
                if which == "^":
                    sup = arg
                else:
                    sub = arg
            body = []
            if self.peek() not in (None, "}", "\\right"):
                body = self.scripted(self.atom(self.next()))
            return [("nary", NARY[name], sub, sup, body)]
        if name in FUNCTIONS:
            sub = sup = None
            while self.peek() in ("^", "_"):
                which = self.next()
                arg = self.group()
                if which == "^":
                    sup = arg
                else:
                    sub = arg
            body = self.group() if self.peek() is not None else []
            return [("func", name, sub, sup, body)]
        if name in SPACES:
            return [("run", SPACES[name])]
        if name in SYMBOLS:
            return [("run", SYMBOLS[name])]
        if tok == "{":
            nodes = self.sequence(stop="}")
            if self.peek() == "}":
                self.next()
            return nodes
        if tok in ("}", "$"):
            return []
        if tok.startswith("\\"):
            return [("run", tok[1:])]  # unknown command: show its name
        return [("run", tok)]


def parse(latex):
    return Parser(tokenize(latex)).sequence()


# ---------------------------------------------------------------- OMML (Word)

def _r(text, normal=False):
    pr = "<m:rPr><m:nor/></m:rPr>" if normal else ""
    return f'<m:r>{pr}<m:t xml:space="preserve">{escape(text)}</m:t></m:r>'


def _omml(nodes):
    out = []
    for n in nodes:
        kind = n[0]
        if kind == "run":
            out.append(_r(n[1]))
        elif kind == "text":
            out.append(_r(n[1], normal=True))
        elif kind == "sup":
            out.append(f"<m:sSup><m:e>{_omml(n[1])}</m:e><m:sup>{_omml(n[2])}</m:sup></m:sSup>")
        elif kind == "sub":
            out.append(f"<m:sSub><m:e>{_omml(n[1])}</m:e><m:sub>{_omml(n[2])}</m:sub></m:sSub>")
        elif kind == "subsup":
            out.append(
                f"<m:sSubSup><m:e>{_omml(n[1])}</m:e><m:sub>{_omml(n[2])}</m:sub>"
                f"<m:sup>{_omml(n[3])}</m:sup></m:sSubSup>")
        elif kind == "frac":
            out.append(f"<m:f><m:num>{_omml(n[1])}</m:num><m:den>{_omml(n[2])}</m:den></m:f>")
        elif kind == "rad":
            if n[1]:
                out.append('<m:rad><m:radPr><m:degHide m:val="0"/></m:radPr>'
                           f"<m:deg>{_omml(n[1])}</m:deg><m:e>{_omml(n[2])}</m:e></m:rad>")
            else:
                out.append('<m:rad><m:radPr><m:degHide m:val="1"/></m:radPr>'
                           f"<m:deg/><m:e>{_omml(n[2])}</m:e></m:rad>")
        elif kind == "delim":
            out.append(f'<m:d><m:dPr><m:begChr m:val="{escape(n[1])}"/>'
                       f'<m:endChr m:val="{escape(n[2])}"/></m:dPr>'
                       f"<m:e>{_omml(n[3])}</m:e></m:d>")
        elif kind == "acc":
            out.append(f'<m:acc><m:accPr><m:chr m:val="{escape(n[1])}"/></m:accPr>'
                       f"<m:e>{_omml(n[2])}</m:e></m:acc>")
        elif kind == "func":
            scripts = _r(n[1], normal=True)
            if n[2] is not None or n[3] is not None:
                base = scripts
                if n[2] is not None and n[3] is not None:
                    scripts = (f"<m:sSubSup><m:e>{base}</m:e><m:sub>{_omml(n[2])}</m:sub>"
                               f"<m:sup>{_omml(n[3])}</m:sup></m:sSubSup>")
                elif n[2] is not None:
                    scripts = f"<m:sSub><m:e>{base}</m:e><m:sub>{_omml(n[2])}</m:sub></m:sSub>"
                else:
                    scripts = f"<m:sSup><m:e>{base}</m:e><m:sup>{_omml(n[3])}</m:sup></m:sSup>"
            out.append(f"<m:func><m:fName>{scripts}</m:fName><m:e>{_omml(n[4])}</m:e></m:func>")
        elif kind == "nary":
            sub = f"<m:sub>{_omml(n[2])}</m:sub>" if n[2] else "<m:sub/>"
            sup = f"<m:sup>{_omml(n[3])}</m:sup>" if n[3] else "<m:sup/>"
            hide = "" if n[2] else '<m:subHide m:val="1"/>'
            hide += "" if n[3] else '<m:supHide m:val="1"/>'
            out.append(f'<m:nary><m:naryPr><m:chr m:val="{escape(n[1])}"/>'
                       f'<m:limLoc m:val="undOvr"/>{hide}</m:naryPr>'
                       f"{sub}{sup}<m:e>{_omml(n[4])}</m:e></m:nary>")
    return "".join(out)


def latex_to_omml(latex):
    """An <m:oMath> fragment, namespace-declared so it can be parsed alone."""
    return (f'<m:oMath xmlns:m="{M_NS}" xmlns:w="{W_NS}">'
            f"{_omml(parse(latex))}</m:oMath>")


# --------------------------------------------------------------- Unicode (PDF)

SUPS = str.maketrans("0123456789+-=()n i", "⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻⁼⁽⁾ⁿ ⁱ")
# Kept to U+2080–U+209C, which printing fonts carry. The phonetic-extension
# subscripts for i, j, r, u and v are not reliably present, and a missing glyph
# prints as a box on an exam paper, so those fall back to "_(…)" instead.
SUBS = str.maketrans("0123456789+-=()aeoxhklmnpst ",
                     "₀₁₂₃₄₅₆₇₈₉₊₋₌₍₎ₐₑₒₓₕₖₗₘₙₚₛₜ ")


def _flat(nodes):
    return "".join(_unicode(n) for n in nodes)


def _script(nodes, table):
    text = _flat(nodes)
    converted = text.translate(table)
    # Fall back to an explicit marker when a character has no small form.
    if any(c not in "⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻⁼⁽⁾ⁿⁱ₀₁₂₃₄₅₆₇₈₉₊₋₌₍₎ₐₑₒₓₕₖₗₘₙₚₛₜ "
           for c in converted):
        return None
    return converted


def _unicode(n):
    kind = n[0]
    if kind in ("run", "text"):
        return n[1]
    if kind == "sup":
        s = _script(n[2], SUPS)
        return _flat(n[1]) + (s if s is not None else "^(" + _flat(n[2]) + ")")
    if kind == "sub":
        s = _script(n[2], SUBS)
        return _flat(n[1]) + (s if s is not None else "_(" + _flat(n[2]) + ")")
    if kind == "subsup":
        sub = _script(n[2], SUBS)
        sup = _script(n[3], SUPS)
        return (_flat(n[1])
                + (sub if sub is not None else "_(" + _flat(n[2]) + ")")
                + (sup if sup is not None else "^(" + _flat(n[3]) + ")"))
    if kind == "frac":
        return "(" + _flat(n[1]) + ")/(" + _flat(n[2]) + ")"
    if kind == "rad":
        root = ("" if not n[1] else _script(n[1], SUPS) or _flat(n[1]))
        return root + "√(" + _flat(n[2]) + ")"
    if kind == "delim":
        return (n[1] or "") + _flat(n[3]) + (n[2] or "")
    if kind == "acc":
        return _flat(n[2]) + n[1]
    if kind == "func":
        inner = _flat(n[4])
        scripts = ""
        if n[2]:
            scripts += _script(n[2], SUBS) or ("_(" + _flat(n[2]) + ")")
        if n[3]:
            scripts += _script(n[3], SUPS) or ("^(" + _flat(n[3]) + ")")
        return f"{n[1]}{scripts} {inner}".strip()
    if kind == "nary":
        scripts = ""
        if n[2]:
            scripts += _script(n[2], SUBS) or ("_(" + _flat(n[2]) + ")")
        if n[3]:
            scripts += _script(n[3], SUPS) or ("^(" + _flat(n[3]) + ")")
        return (n[1] + scripts + " " + _flat(n[4]).lstrip()).rstrip()
    return ""


# A renderer supplies the spacing around relational operators; plain text has to
# write it. Only relations, never + or -, which are also unary.
RELATIONS = re.compile(r"\s*([=≤≥≠≈≡→⇒↔∝])\s*")


def latex_to_unicode(latex):
    return RELATIONS.sub(r" \1 ", _flat(parse(latex))).strip()


# ------------------------------------------------------------------- inline $…$

INLINE = re.compile(r"\$([^$]+)\$")


def split_inline(text):
    """[(is_math, chunk), …] for prose that may contain $…$ segments."""
    out, last = [], 0
    for match in INLINE.finditer(text or ""):
        if match.start() > last:
            out.append((False, text[last:match.start()]))
        out.append((True, match.group(1)))
        last = match.end()
    if last < len(text or ""):
        out.append((False, text[last:]))
    return out or [(False, text or "")]


def inline_to_unicode(text):
    return "".join(latex_to_unicode(c) if is_math else c
                   for is_math, c in split_inline(text))
