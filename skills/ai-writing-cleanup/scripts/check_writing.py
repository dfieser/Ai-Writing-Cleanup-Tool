#!/usr/bin/env python3
"""
check_writing.py: a deterministic scan for machine-writing tells and weak
technical writing.

It does NOT rewrite. It reports, so a rewrite can be targeted and then verified.
Run it on the source to plan the edit, then on the rewrite to confirm em dashes
are gone and the other counts dropped.

Usage:
    python3 check_writing.py path/to/file.md
    cat draft.txt | python3 check_writing.py -
    python3 check_writing.py file.md --quiet     # summary line only

Code blocks and inline code spans are skipped, so command examples do not
create false hits. Several checks are heuristic (passive voice, noun stacks,
tense, cross-references) and will produce occasional false positives. Read each flag and judge it.

Stdlib only.
"""

import bisect
import re
import sys
import statistics

# ---------------------------------------------------------------------------
# Vocabulary tables
# ---------------------------------------------------------------------------

# Buzzwords: single words that plain writing almost always says better.
BUZZWORDS = {
    "leverage": "use", "leverages": "uses", "leveraging": "using",
    "utilize": "use", "utilizes": "uses", "utilizing": "using",
    "utilization": "use", "facilitate": "help", "facilitates": "helps",
    "robust": "(be specific: reliable? tested?)",
    "seamless": "(drop it or say how)", "seamlessly": "(drop it or say how)",
    "cutting-edge": "(drop it or name the tech)",
    "state-of-the-art": "(drop it or name the tech)",
    "game-changer": "(say what it changes)",
    "game-changing": "(say what it changes)",
    "best-in-class": "(drop it)", "world-class": "(drop it)",
    "synergy": "(name the actual benefit)",
    "synergies": "(name the actual benefits)",
    "holistic": "(drop it or be specific)",
    "streamline": "simplify", "streamlines": "simplifies",
    "streamlined": "simplified",
    "empower": "let / enable", "empowers": "lets / enables",
    "unlock": "(say what it enables)", "unlocks": "(say what it enables)",
    "foster": "encourage / support", "fosters": "encourages / supports",
    "delve": "look at / cover", "delving": "looking at",
    "realm": "area / field",
    "landscape": "(drop it; say the actual thing)",
    "tapestry": "(drop it)", "paradigm": "model / approach",
    "myriad": "many", "plethora": "many / plenty", "bespoke": "custom",
    "underpin": "support", "underpins": "supports",
    "supercharge": "speed up / improve", "turnkey": "ready-to-use",
    "frictionless": "(drop it or say how)",
    "actionable": "(often deletable)",
    "impactful": "(say the actual effect)",
}

# Wordy phrases with a shorter plain equivalent.
WORDY_PHRASES = {
    r"prior to": "before",
    r"subsequent to": "after",
    r"in the event that": "if",
    r"in order to": "to",
    r"for the purpose of": "to",
    r"at this point in time": "now",
    r"a large number of": "many",
    r"the majority of": "most",
    r"in close proximity to": "near",
    r"in the vicinity of": "near",
    r"with regard to": "about",
    r"with respect to": "about",
    r"due to the fact that": "because",
    r"in spite of the fact that": "although",
    r"has the ability to": "can",
    r"is able to": "can",
    r"are able to": "can",
    r"is capable of": "can",
}

# Filler phrases: add length, carry no information.
FILLER_PHRASES = [
    r"it'?s important to note that",
    r"it'?s worth (?:noting|mentioning) that",
    r"it should be noted that",
    r"needless to say",
    r"at the end of the day",
    r"in today'?s (?:fast-paced|digital|modern|ever-changing) world",
    r"in the world of",
    r"when it comes to",
    r"the fact of the matter is",
    r"first and foremost",
    r"last but not least",
    r"in conclusion",
    r"in summary",
    r"to sum up",
    r"as we all know",
    r"that being said",
    r"dive into",
    r"deep dive",
    r"navigate the (?:complexities|landscape|world)",
    r"in this day and age",
    r"a testament to",
    r"pave the way",
    r"move the needle",
    r"low-hanging fruit",
    r"boils down to",
    r"plays a (?:crucial|key|vital|pivotal) role",
    r"unlock the (?:power|potential)",
]

# Sentence-opening signposts that are usually deletable.
OPENER_SIGNPOSTS = [
    "moreover", "furthermore", "additionally", "notably", "importantly",
    "indeed", "essentially", "basically", "ultimately", "fundamentally",
    "in essence", "as such",
]

# Hidden verbs: a weak verb plus a nominalization, or an expletive wrapper.
HIDDEN_VERBS = [
    (r"perform(?:s|ed|ing)?\s+(?:an?\s+|the\s+)?\w+(?:tion|sion|ment|ance|ence)",
     "use the verb directly (perform an inspection -> inspect)"),
    (r"conduct(?:s|ed|ing)?\s+(?:an?\s+|the\s+)?\w+(?:tion|sion|ment|ysis)",
     "use the verb directly (conduct an analysis -> analyze)"),
    (r"carr(?:y|ies|ied)\s+out\s+(?:an?\s+|the\s+)?\w+(?:tion|sion|ment)",
     "use the verb directly"),
    (r"provide(?:s|d)?\s+(?:an?\s+|the\s+)?\w+(?:tion|sion|ment|ance)",
     "use the verb directly (provide a description -> describe)"),
    (r"make(?:s)?\s+(?:an?\s+|the\s+)?(?:determination|adjustment|recommendation|assessment|decision|modification)",
     "use the verb directly (make a determination -> determine)"),
    (r"give(?:s|n)?\s+consideration to", "consider"),
    (r"take(?:s|n)?\s+into (?:account|consideration)", "consider / account for"),
    (r"is\s+(?:indicative|reflective|supportive|representative)\s+of",
     "indicates / reflects / supports / represents"),
    (r"effect\s+a\s+reduction", "reduce"),
    (r"achieve\s+compliance", "comply"),
    (r"\bit is necessary to\b", "just give the instruction"),
    (r"\bit is recommended that\b", "just give the instruction"),
    (r"\bit is required that\b", "just give the instruction"),
    (r"\bit is possible to\b", "can"),
    (r"\bthere (?:is|are|was|were)\s+(?:an?|no|three|two|several|many)\b",
     "expletive: name the real subject"),
]

# Irregular past participles, for passive-voice detection.
IRREGULAR_PP = {
    "known", "given", "taken", "written", "made", "done", "shown", "seen",
    "found", "held", "built", "sent", "set", "put", "read", "kept", "left",
    "meant", "run", "drawn", "thrown", "brought", "bought", "caught", "taught",
    "told", "sold", "lost", "met", "paid", "said", "chosen", "driven",
    "broken", "spoken", "frozen", "hidden", "forgotten", "proven", "worn",
    "torn", "born", "cut", "hit", "let", "shut", "split", "spread", "cost",
    "hurt", "begun", "become", "come", "gone", "grown", "blown", "flown",
    "stolen", "risen", "ridden", "eaten", "fallen", "beaten", "bitten",
    "understood", "withheld", "overridden", "rewritten", "rebuilt", "resent",
    "undone", "redone", "overwritten",
}

BE_FORMS = r"(?:am|is|are|was|were|be|been|being|get|gets|got|gotten)"

# Quotation-mark analysis. Straight and curly double quotes.
QUOTE_SPAN = re.compile(r'"([^"\n]{1,120})"|“([^”\n]{1,120})”')

# Verbs of attribution. A quote after one of these is a real quotation.
QUOTE_ATTRIB = re.compile(
    r"\b(?:said|says|saying|wrote|writes|stated|states|noted|notes|asked|"
    r"asks|replied|replies|explained|explains|warned|warns|quoted|quotes|"
    r"argues|argued|adds|added|told|according to|per)\s*[,:]?\s*$",
    re.IGNORECASE)

# Cues that the quoted text is a literal string, name, label, or reference.
QUOTE_LITERAL_BEFORE = re.compile(
    r"\b(?:type|types|typing|enter|enters|entering|named|names|call|calls|"
    r"called|label|labeled|labelled|titled|entitled|marked|tagged|select|"
    r"selects|click|clicks|choose|chooses|press|presses|tap|taps|sets? to|"
    r"values? of|returns?|displays?|shows?|reads?|prints?|outputs?|"
    r"search for|look for|known as|referred to as|term|word|string|"
    r"message|error|warning|status|state|mode|command|key|flag|parameter|"
    r"argument|option|field|button|menu|column|header|see|refer to|"
    r"refers to|described in|shown in|listed in|section|chapter|appendix|"
    r"table|figure|step|topic|procedure|guide|manual|document)"
    r"\W{0,3}$", re.IGNORECASE)

QUOTE_LITERAL_AFTER = re.compile(
    r"^\W{0,3}(?:button|field|menu|option|checkbox|tab|dialog|box|window|"
    r"link|icon|command|key|value|string|column|header|section|page|"
    r"parameter|flag|setting|message|error|folder|file|directory|chapter|"
    r"procedure|topic)\b", re.IGNORECASE)

# "Set the mode to X", "change the level to X": the cue verb and the "to" are
# separated by the thing being set, so this needs its own pattern.
QUOTE_ASSIGN = re.compile(
    r"\b(?:set|sets|change|changes|configure|configures|assign|assigns|"
    r"default|defaults|initialize|initializes|leave|leaves|remains?|"
    r"equals?|is|are)\b[^\"“]{0,30}\b(?:to|as)\s*$", re.IGNORECASE)

SO_CALLED = re.compile(r"\bso[- ]called\W{0,3}$", re.IGNORECASE)

# Parenthesis analysis.
PAREN_SPAN = re.compile(r"\(([^()\n]{1,180})\)")

# Openers that mark a legitimate cross-reference or citation.
PAREN_REFERENCE = re.compile(
    r"^\s*(?:see|refer to|see also|source|sources|adapted from|from|per|"
    r"cf\.?|e\.?g\.?|i\.?e\.?|figure|fig\.?|table|section|chapter|appendix|"
    r"step|part|item|note|para(?:graph)?|eq(?:uation)?|listing|exhibit|"
    r"sheet|page|pp?\.?|vol\.?|rev\.?|issue|no\.?|ref\.?|ch\.?|sec\.?)\b",
    re.IGNORECASE)

# Measurement units and short symbols, which are not prose.
UNIT_TOKENS = {
    "mm", "cm", "km", "kg", "psi", "psig", "kpa", "mpa", "bar", "rpm", "deg",
    "sec", "secs", "min", "mins", "hr", "hrs", "nm", "ft", "in", "lb", "lbs",
    "oz", "gal", "amp", "amps", "volt", "volts", "watt", "watts", "ohm",
    "ohms", "hz", "khz", "mhz", "ghz", "kb", "mb", "gb", "tb", "ms", "ns",
    "us", "db", "dbm", "ppm", "pct", "each", "typ", "max", "min", "nom",
    "ref", "approx", "qty", "ea", "pcs", "awg", "vdc", "vac", "ma", "kw",
}

# Finite verbs. A parenthetical containing one is a clause, not an aside.
PAREN_CLAUSE = re.compile(
    r"\b(?:is|are|was|were|be|been|has|have|had|can|could|will|would|shall|"
    r"should|may|might|must|does|do|did|requires?|needs?|allows?|means?|"
    r"causes?|provides?|includes?|contains?|returns?|sends?|uses?|makes?|"
    r"applies|apply|depends?|varies|vary|works?|runs?|takes?|gives?)\b",
    re.IGNORECASE)

# Words that never start a noun stack. Kept broad on purpose.
STOPWORDS = {
    "a", "an", "the", "and", "or", "but", "nor", "for", "yet", "so", "of",
    "in", "on", "at", "to", "from", "by", "with", "without", "into", "onto",
    "over", "under", "through", "during", "before", "after", "above", "below",
    "between", "among", "against", "about", "as", "than", "then", "if",
    "when", "where", "while", "because", "since", "unless", "until", "although",
    "though", "that", "this", "these", "those", "it", "its", "they", "them",
    "their", "he", "she", "his", "her", "we", "our", "us", "you", "your", "i",
    "my", "me", "who", "whom", "whose", "which", "what", "is", "are", "was",
    "were", "be", "been", "being", "am", "has", "have", "had", "do", "does",
    "did", "will", "would", "shall", "should", "can", "could", "may", "might",
    "must", "not", "no", "all", "any", "each", "every", "some", "such", "only",
    "also", "more", "most", "less", "least", "very", "too", "just", "now",
    "new", "old", "same", "other", "another", "both", "either", "neither",
    "there", "here", "how", "why", "one", "two", "three", "four", "five",
    "first", "second", "third", "next", "last", "own", "see", "use", "used",
    "using", "make", "makes", "made", "set", "sets", "get", "gets", "run",
    "runs", "add", "adds", "per", "via", "up", "down", "out", "off", "on",
    "well", "worth", "far", "much", "many", "few", "several", "enough",
    "quite", "rather", "still", "even", "ever", "never", "always", "often",
    "again", "once", "twice", "able", "sure", "likely", "such",
}

# Common verb forms that would otherwise look like nouns in a stack.
COMMON_VERBS = {
    "regulate", "require", "provide", "contain", "include", "return", "send",
    "receive", "open", "close", "start", "stop", "read", "write", "log",
    "check", "verify", "validate", "detect", "prevent", "enable", "allow",
    "cause", "mean", "show", "indicate", "display", "store", "load", "save",
    "delete", "remove", "create", "update", "handle", "manage", "control",
    "monitor", "report", "trigger", "generate", "process", "support", "need",
    "ensure", "perform", "apply", "connect", "disconnect", "install",
    "replace", "repair", "inspect", "torque", "tighten", "measure", "record",
    "transmit", "convert", "calculate", "determine", "describe", "define",
    "specify", "list", "note", "warn", "reject", "accept", "retry", "restart",
    "reboot", "shut", "lift", "wait", "drop", "raise", "hold", "keep", "let",
    "call", "push", "pull", "fail", "pass", "exceed", "match", "select",
    "choose", "assign", "attach", "detach", "engage", "release", "reset",
    "clear", "flush", "purge", "seal", "mount", "align", "adjust", "test",
    "operate", "activate", "deactivate", "configure", "initialize", "execute",
    "reduce", "increase", "decrease", "improve", "affect", "extend", "expand",
    "limit", "block", "permit", "deny", "grant", "revoke", "encrypt",
    "decrypt", "compress", "parse", "render", "compile", "deploy", "build",
    "merge", "split", "join", "sort", "count", "cover", "carry", "give",
    "take", "put", "find", "know", "want", "seem", "become", "remain", "stay",
    "begin", "end", "continue", "complete", "finish", "follow", "lead",
    "point", "refer", "apply", "occur", "happen", "exist", "belong", "depend",
    "empower", "transform", "deliver", "drive", "offer", "help", "bring",
    "work", "serve", "act", "review", "focus", "enhance", "optimize",
    "maximize", "minimize", "achieve", "address", "consider", "evaluate",
    "identify", "maintain", "obtain", "navigate", "integrate", "implement",
    "automate", "accelerate", "simplify", "standardize", "customize",
    "migrate", "replicate", "scale", "tune", "patch", "upgrade", "restore",
    "streamline", "leverage", "utilize", "facilitate", "unlock", "foster",
    "represent", "reflect", "involve", "consist", "differ", "vary", "remove",
}
COMMON_VERBS |= {v + "s" for v in COMMON_VERBS}

# All-caps tokens that are words or markers, not abbreviations to police.
NON_ABBREV = {
    "I", "A", "AN", "AS", "AT", "BE", "BY", "DO", "GO", "IF", "IN", "IS",
    "IT", "NO", "OF", "ON", "OR", "SO", "TO", "UP", "WE", "US", "AM", "AND",
    "THE", "FOR", "NOT", "BUT", "YOU", "ALL", "CAN", "HAS", "MAY", "NEW",
    "NOW", "ONE", "OUT", "SEE", "TWO", "USE", "WAS", "WHO", "WHY", "YES",
    "TODO", "FIXME", "NOTE", "NOTES", "WARNING", "CAUTION", "DANGER",
    "IMPORTANT", "TRUE", "FALSE", "NULL", "NONE", "OK", "END", "START",
    "STEP", "PART", "OK.", "OR.", "OFF", "OVER",
}

# Abbreviations a general technical reader already knows. These need no
# spelled-out introduction, so a single undefined use of one is not a defect.
WELL_KNOWN_ABBREV = {
    "API", "URL", "URI", "HTTP", "HTTPS", "HTML", "CSS", "XML", "JSON",
    "YAML", "CSV", "PDF", "USB", "CPU", "GPU", "RAM", "ROM", "SSD", "HDD",
    "IP", "TCP", "UDP", "DNS", "SSH", "FTP", "SQL", "ID", "OS", "PC", "LED",
    "LCD", "GPS", "USA", "UK", "EU", "UN", "AC", "DC", "RPM", "PSI", "FAQ",
    "PIN", "SIM", "LAN", "WAN", "VPN", "UI", "UX", "SDK", "CLI", "GUI",
    "IDE", "VM", "ASCII", "UTF", "KB", "MB", "GB", "TB", "NASA", "FAA",
    "ISO", "ANSI", "IEEE", "PDF", "ZIP", "JPEG", "PNG", "GIF", "RSS", "SMS",
    "CD", "DVD", "TV", "GMT", "UTC", "FBI", "CIA", "CEO", "CTO", "CFO",
    "HR", "QA", "AI", "ML", "IT", "PPE", "OEM", "SOP",
}

# Abbreviations for sentence splitting (not the acronym policy check).
SENT_ABBREV = {"e.g", "i.e", "etc", "vs", "mr", "mrs", "ms", "dr", "st", "fig",
               "no", "al", "inc", "ltd", "co", "approx", "cf", "vol"}


# ---------------------------------------------------------------------------
# Input handling
# ---------------------------------------------------------------------------

def read_input(arg):
    if arg == "-" or arg is None:
        return sys.stdin.read()
    with open(arg, "r", encoding="utf-8", errors="replace") as f:
        return f.read()


def strip_code(text):
    """Remove fenced code blocks, indented blocks, and inline code spans."""
    text = re.sub(r"```.*?```", " ", text, flags=re.DOTALL)
    text = re.sub(r"~~~.*?~~~", " ", text, flags=re.DOTALL)
    text = re.sub(r"`[^`\n]+`", " ", text)
    lines = [l for l in text.splitlines()
             if not re.match(r"^(?: {4,}|\t)\S", l)]
    return "\n".join(lines)


def split_sentences(text):
    """Approximate sentence split. Used only for counting."""
    flat = re.sub(r"\s+", " ", text.strip())
    if not flat:
        return []
    flat = re.sub(r"(\d)\.(\d)", r"\1\2", flat)
    flat = re.sub(r"\b(" + "|".join(SENT_ABBREV) + r")\.",
                  lambda m: m.group(0).replace(".", ""),
                  flat, flags=re.IGNORECASE)
    parts = re.split(r"(?<=[.!?])\s+", flat)
    return [p.strip() for p in parts if p.strip()]


def word_count(s):
    return len(re.findall(r"[A-Za-z0-9']+", s))


def _snip(line, pos, width=32):
    start = max(0, pos - width)
    end = min(len(line), pos + width)
    s = line[start:end].strip()
    return ("..." if start > 0 else "") + s + ("..." if end < len(line) else "")


def _clip(s, n=88):
    return s if len(s) <= n else s[:n] + "..."


# ---------------------------------------------------------------------------
# Detectors
# ---------------------------------------------------------------------------

def find_em_dashes(text):
    """Report em dashes and the marks that stand in for one.

    This scans line by line so the report can cite line numbers, which
    strip_code does not preserve. Code is blanked here instead: fenced and
    indented blocks are skipped, and an inline span is overwritten with spaces
    of the same width so the remaining offsets still line up. Without that, a
    command flag such as --quiet reads as a dash.
    """
    hits = []
    in_fence = False
    for i, line in enumerate(text.splitlines(), 1):
        if re.match(r"^\s*(?:```|~~~)", line):
            in_fence = not in_fence
            continue
        if in_fence or re.match(r"^(?: {4,}|\t)\S", line):
            continue
        scan = re.sub(r"`[^`]*`", lambda m: " " * len(m.group(0)), line)
        for m in re.finditer(r"—", scan):
            hits.append((i, "em dash", _snip(line, m.start())))
        for m in re.finditer(r"\s–\s", scan):
            hits.append((i, "en dash used as break", _snip(line, m.start())))
        for m in re.finditer(r"(?<=\w)\s*--\s*(?=\w)", scan):
            hits.append((i, "double hyphen used as dash", _snip(line, m.start())))
    return hits


def find_scare_quotes(text):
    """Quoted spans that are not real quotations.

    Two buckets. 'scare' is a short quoted span with no attribution and no
    literal-string cue. That is the machine tell: quotation marks used for
    emphasis, hedging, or ironic distance. 'literal' is a quoted string,
    name, cross-reference, or interface label, which is a house-style
    question rather than a defect.
    """
    scare, literal = [], []
    for i, line in enumerate(text.splitlines(), 1):
        for m in QUOTE_SPAN.finditer(line):
            inner = m.group(1) if m.group(1) is not None else m.group(2)
            if inner is None or word_count(inner) == 0:
                continue
            before, after = line[:m.start()], line[m.end():]
            # A real quotation: long enough, or punctuated as a full
            # sentence, or introduced by an attribution verb or a colon.
            if word_count(inner) >= 8 or re.search(r"[.!?;]\s*$", inner):
                continue
            if QUOTE_ATTRIB.search(before) or re.search(r":\s*$", before):
                continue
            snip = _snip(line, m.start(), 34)
            if SO_CALLED.search(before):
                scare.append((i, "so-called + quotes", snip))
            elif (QUOTE_LITERAL_BEFORE.search(before)
                  or QUOTE_ASSIGN.search(before)
                  or QUOTE_LITERAL_AFTER.match(after)):
                literal.append((i, snip))
            else:
                scare.append((i, "no attribution", snip))
    return scare, literal


def find_parentheses(text):
    """Parenthetical asides that should be folded into the sentence.

    Skipped as legitimate: abbreviation definitions and spelled-out terms,
    cross-references and citations, list markers, units, numbers, equations,
    and the "(s)" plural marker. Everything else is ordinary prose that the
    writer put in parentheses instead of committing to a sentence.
    """
    hits = []
    for i, line in enumerate(text.splitlines(), 1):
        for m in PAREN_SPAN.finditer(line):
            inner = m.group(1).strip()
            if not inner or PAREN_REFERENCE.match(inner):
                continue
            words = re.findall(r"[A-Za-z][A-Za-z'\-]*", inner)
            # Abbreviation definition, spelled-out term, or proper name:
            # every word is capitalized or fully uppercase.
            if words and all(w[0].isupper() for w in words):
                continue
            # The reverse definition, "HEA (high entropy alloy)": the initials
            # of the aside spell the short form sitting just before it. The
            # capital-letter test above only catches the forward order.
            short = re.search(r"\b([A-Za-z]{2,})\W*$", line[:m.start()])
            if short and words:
                initials = "".join(w[0] for w in words).lower()
                token = short.group(1).lower()
                if initials and token in (initials, initials + "s"):
                    continue
            prose = [w for w in words
                     if len(w) >= 3 and not w.isupper()
                     and w.lower() not in UNIT_TOKENS]
            if len(prose) < 2:
                continue
            kind = ("full clause" if PAREN_CLAUSE.search(inner)
                    else "prose aside")
            hits.append((i, kind, _clip(inner, 64)))
    return hits


def find_buzzwords(text):
    counts = {}
    lower = text.lower()
    for word, sugg in BUZZWORDS.items():
        n = len(re.findall(r"\b" + re.escape(word) + r"\b", lower))
        if n:
            counts[word] = (n, sugg)
    return counts


def find_wordy(text):
    counts = {}
    lower = text.lower()
    for pat, plain in WORDY_PHRASES.items():
        n = len(re.findall(r"\b" + pat + r"\b", lower))
        if n:
            counts[pat] = (n, plain)
    return counts


def find_fillers(text):
    counts = {}
    lower = text.lower()
    for pat in FILLER_PHRASES:
        n = len(re.findall(pat, lower))
        if n:
            counts[pat] = n
    return counts


def find_openers(sentences):
    hits = []
    for s in sentences:
        low = s.lower().lstrip("\"'([ ")
        for sig in OPENER_SIGNPOSTS:
            if low.startswith(sig + " ") or low.startswith(sig + ","):
                hits.append((sig, _clip(s, 60)))
                break
    return hits


def comma_lists(sentences, min_commas=3):
    heavy, rule_of_three = [], 0
    for s in sentences:
        if s.count(",") >= min_commas:
            heavy.append((s.count(","), _clip(s, 80)))
        if re.search(r"\w+,\s+\w+(?:\s+\w+){0,3},?\s+and\s+\w+", s):
            rule_of_three += 1
    return heavy, rule_of_three


def find_front_loaded(sentences):
    """Sentences whose main clause is delayed behind a long front-load."""
    SUBORD = {
        "because", "since", "although", "though", "while", "when", "whenever",
        "if", "unless", "after", "before", "as", "given", "provided",
        "whereas", "once", "until", "assuming", "considering", "despite",
        "having", "being", "upon", "following", "where", "in",
    }
    hits = []
    for s in sentences:
        if "," not in s:
            continue
        intro = s.split(",", 1)[0]
        words = re.findall(r"[A-Za-z0-9']+", intro)
        n = len(words)
        subord = bool(words) and words[0].lower() in SUBORD
        if n >= 10 or (subord and n >= 6):
            hits.append((n, _clip(s, 90)))
    return hits


def find_passive(sentences):
    """be-verb (plus optional adverb) followed by a past participle."""
    pat = re.compile(
        r"\b" + BE_FORMS + r"\s+(?:\w+ly\s+)?(\w+)\b", re.IGNORECASE)
    hits = []
    for s in sentences:
        for m in pat.finditer(s):
            w = m.group(1).lower()
            if w in IRREGULAR_PP or (w.endswith("ed") and len(w) > 4):
                hits.append((m.group(0).strip(), _clip(s, 84)))
                break
    return hits


def find_hidden_verbs(text):
    hits = []
    lower = text.lower()
    for pat, sugg in HIDDEN_VERBS:
        for m in re.finditer(pat, lower):
            hits.append((m.group(0).strip(), sugg))
    # The "the <nominalization> of" pattern, very common in specifications.
    for m in re.finditer(r"\bthe (\w{5,}(?:tion|sion|ment|ance|ence)) of\b",
                         lower):
        hits.append((m.group(0).strip(), "often hides a verb: '-tion of X' -> verb X"))
    return hits


def find_noun_stacks(text):
    """Runs of 3+ consecutive content words. Heuristic; verify by eye."""
    hits = []
    for chunk in re.split(r"[.!?;:,()\[\]\n]", text):
        tokens = re.findall(r"[A-Za-z][A-Za-z\-]*", chunk)
        run = []
        for tok in tokens:
            low = tok.lower()
            content = (
                low not in STOPWORDS
                and low not in COMMON_VERBS
                and len(low) >= 3
                and not low.endswith("ly")
                and not low.endswith("ing")
                and not low.endswith("ed")
                and tok[0].islower()
            )
            if content:
                run.append(tok)
            else:
                if len(run) >= 3:
                    hits.append((len(run), " ".join(run)))
                run = []
        if len(run) >= 3:
            hits.append((len(run), " ".join(run)))
    return hits


def find_abbreviations(text):
    """Report acronym usage counts and whether each was ever defined."""
    tokens = re.findall(r"\b([A-Z][A-Z0-9]{1,7})(?=s?\b)", text)
    counts = {}
    for t in tokens:
        if t in NON_ABBREV or t.isdigit():
            continue
        counts[t] = counts.get(t, 0) + 1
    defined = set(re.findall(r"\(\s*([A-Z][A-Z0-9]{1,7})s?\s*\)", text))
    return counts, defined


def find_pronoun_issues(sentences, text):
    """Vague demonstratives, expletive openers, and first person."""
    vague, first_person, second_person = [], 0, 0
    demo = re.compile(
        r"^(This|That|These|Those)\s+"
        r"(is|are|was|were|will|can|may|must|should|would|has|have|had|does|do|"
        r"did|causes?|means?|allows?|makes?|requires?|results?|provides?|"
        r"ensures?|prevents?|creates?|enables?|gives?|leads?|shows?|"
        r"indicates?|helps?|reduces?|improves?|affects?)\b")
    expl = re.compile(r"^(It (?:is|was)|There (?:is|are|was|were))\b")
    for s in sentences:
        clean = s.lstrip("\"'([ ")
        if demo.match(clean):
            vague.append(("bare demonstrative", _clip(clean, 76)))
        elif expl.match(clean):
            vague.append(("expletive opener", _clip(clean, 76)))
    low = text.lower()
    for w in (r"\bwe\b", r"\bour\b", r"\bours\b", r"\bus\b", r"\bi\b", r"\bmy\b"):
        first_person += len(re.findall(w, low))
    for w in (r"\byou\b", r"\byour\b", r"\byours\b"):
        second_person += len(re.findall(w, low))
    return vague, first_person, second_person


def tense_profile(sentences):
    present = past = future = 0
    for s in sentences:
        low = " " + s.lower() + " "
        if re.search(r"\b(will|shall)\s+\w+", low):
            future += 1
        elif re.search(r"\b(was|were|had|did)\b", low):
            past += 1
        elif re.search(r"\b(is|are|has|have|does|do)\b", low):
            present += 1
    return present, past, future


def _readable(pat):
    return (pat.replace(r"'?", "'").replace(r"(?:", "(")
               .replace(r"\b", "").replace(r"\s+", " "))


# ---------------------------------------------------------------------------
# Cross-references
# ---------------------------------------------------------------------------

# A mention of supporting material. "SI" and "ESI" are matched case-sensitively
# so that silicon (Si) and "SI units" do not trigger.
SUPPORT_MENTION = re.compile(
    r"\b(?:electronic\s+)?(?:supplementary|supplemental)\s+"
    r"(?:information|materials?|data|text|files?|notes?|sections?|methods|"
    r"results|figures?|tables?)\b"
    r"|\bsupporting\s+(?:information|materials?)\b"
    r"|\bthe\s+appendix\b|\bthe\s+appendices\b"
    r"|\bonline\s+(?:resources?|supplements?)\b",
    re.IGNORECASE)
SUPPORT_ABBR = re.compile(r"\bE?SI\b(?!\s*units?\b)")

# Anything that names a specific supporting item.
SUPPORT_SPECIFIC = re.compile(
    r"\b(?:fig(?:ure)?s?|tables?|notes?|sections?|secs?|eqs?|equations?|"
    r"videos?|movies?|algorithms?|schemes?|text|methods?|datasets?|files?)"
    r"\.?\s*~?\s*S\s*~?\s*\d"
    r"|\b(?:supplementary|supplemental|supporting)\s+"
    r"(?:fig(?:ure)?s?|tables?|notes?|sections?|eq(?:uation)?s?|videos?|"
    r"movies?|methods?|data|discussion|files?|text)\.?\s*~?\s*(?:S\s*)?\d"
    r"|\bappendi(?:x|ces)\s+[A-Z0-9]\b"
    r"|\\(?:ref|cref|Cref|autoref)\{"
    r"|\bS\d+[a-z]?\b",
    re.IGNORECASE)

# Pointers that make the reader search. Backward ones that are really
# literature citations ("as shown previously [12]") are skipped.
VAGUE_BACK = re.compile(
    r"\b(?:discussed|mentioned|noted|shown|described|stated|explained|"
    r"outlined|presented|seen|demonstrated|established|defined)\s+"
    r"(?:above|earlier|previously|before|in\s+(?:the\s+)?(?:previous|"
    r"preceding|prior)\s+sections?)\b"
    r"|\b(?:see|cf\.?)\s+above\b"
    r"|\baforementioned\b"
    r"|\bthe\s+(?:previous|preceding|prior)\s+section\b",
    re.IGNORECASE)
VAGUE_BACK_CITATION = re.compile(r"\s*(?:\[|\\cite|by\b|\(\s*[A-Z]|in\s+ref)",
                                 re.IGNORECASE)
VAGUE_FWD = re.compile(
    r"\b(?:see|discussed|described|shown|explained|addressed|detailed|"
    r"presented|examined|explored|given|treated|covered|revisited|seen|"
    r"demonstrated)\s+"
    r"(?:below|later|further\s+below|in\s+(?:the\s+)?(?:next|following|"
    r"later|subsequent)\s+sections?)\b"
    r"|\bin\s+(?:the|a)\s+(?:next|following|later|subsequent)\s+sections?\b"
    r"|\blater\s+in\s+(?:this|the)\s+(?:paper|article|manuscript|work|"
    r"report|document|chapter|study)\b",
    re.IGNORECASE)

SECTION_NUM_REF = re.compile(
    r"\b(?:sections?|secs?\.)\s*~?\s*(\d+(?:\.\d+)*)|§\s*~?\s*(\d+(?:\.\d+)*)",
    re.IGNORECASE)
TEX_REF = re.compile(r"\\(?:ref|cref|Cref|autoref|nameref)\{([^}]+)\}")
TEX_SECTION = re.compile(
    r"\\(section|subsection|subsubsection)(\*?)\s*(?:\[[^\]]*\])?\s*\{")
TEX_LABEL = re.compile(r"\\label\{([^}]+)\}")
MD_NUM_HEADING = re.compile(
    r"^[ ]{0,3}#{1,6}\s+(?:section\s+)?(\d+(?:\.\d+)*)\.?\s+\S", re.IGNORECASE)
PLAIN_NUM_HEADING = re.compile(r"^\s*(\d+(?:\.\d+)*)\.?\s+([A-Z][^.!?:;]{1,70})$")


def _sentence_spans(text):
    """Sentence (start, end) offsets. Abbreviation and decimal periods are
    masked first so that 'Fig. S3' and '3.2' do not end a sentence."""
    masked = re.sub(r"(\d)\.(\d)", lambda m: m.group(1) + "\x00" + m.group(2),
                    text)
    abbrevs = [re.escape(a) for a in SENT_ABBREV] + [
        "figs", "eqs?", "secs?", "refs?", "ch", "pp?", "eq"]
    masked = re.sub(r"\b(?:" + "|".join(abbrevs) + r")\.",
                    lambda m: m.group(0)[:-1] + "\x00", masked,
                    flags=re.IGNORECASE)
    spans, start = [], 0
    boundary = re.compile(
        r"[.!?]+(?=\s)|\n[ \t]*\n"
        r"|\n(?=[ \t]{0,3}#|[ \t]*\\(?:(?:sub)*section|label|begin|end|item)\b)"
        r"|(?m:^(?:[ \t]{0,3}#|[ \t]*\\(?:(?:sub)*section|label|begin|end)\b)"
        r"[^\n]*\n)")
    for m in boundary.finditer(masked):
        spans.append((start, m.end()))
        start = m.end()
    spans.append((start, len(masked)))
    return [(s, e) for s, e in spans if text[s:e].strip()]


def _section_events(text):
    """Numbered headings as (offset, key) plus a LaTeX label map.

    Keys are tuples such as (3, 2) for Section 3.2. LaTeX sections are
    numbered the way LaTeX numbers them. Everything after \\appendix is
    treated as coming after every main section.
    """
    events, labels = [], {}
    lines = text.split("\n")
    offsets, pos = [], 0
    for line in lines:
        offsets.append(pos)
        pos += len(line) + 1

    # Markdown and plain-text numbered headings.
    for idx, line in enumerate(lines):
        m = MD_NUM_HEADING.match(line)
        if m:
            events.append((offsets[idx],
                           tuple(int(x) for x in m.group(1).split("."))))
            continue
        m = PLAIN_NUM_HEADING.match(line)
        if m and word_count(m.group(2)) <= 8:
            above = lines[idx - 1].strip() if idx > 0 else ""
            below = lines[idx + 1].strip() if idx + 1 < len(lines) else ""
            if not above and not below:
                events.append((offsets[idx],
                               tuple(int(x) for x in m.group(1).split("."))))

    # LaTeX sectioning.
    counters = [0, 0, 0]
    depth = {"section": 0, "subsection": 1, "subsubsection": 2}
    tex = []
    appendix_at = text.find("\\appendix")
    for m in TEX_SECTION.finditer(text):
        if 0 <= appendix_at < m.start():
            tex.append((m.start(), m.end(), (10 ** 6,)))
            continue
        if m.group(2):
            tex.append((m.start(), m.end(), None))
            continue
        d = depth[m.group(1)]
        counters[d] += 1
        for j in range(d + 1, 3):
            counters[j] = 0
        tex.append((m.start(), m.end(), tuple(counters[:d + 1])))
    for start, _, key in tex:
        if key is not None:
            events.append((start, key))
    for m in TEX_LABEL.finditer(text):
        prior = [t for t in tex if t[1] <= m.start()]
        if not prior:
            continue
        _, end, key = prior[-1]
        gap = text[end:m.start()]
        if key is not None and len(gap) < 300 and "\\begin{" not in gap:
            labels.setdefault(m.group(1), key)

    events.sort()
    return events, labels


def find_cross_references(text):
    """Section references, forward references, vague pointers, and vague
    references to supporting material."""
    events, labels = _section_events(text)
    starts = [p for p, _ in events]

    def current_key(pos):
        i = bisect.bisect_right(starts, pos) - 1
        return events[i][1] if i >= 0 else None

    def line_of(pos):
        return text.count("\n", 0, pos) + 1

    def fmt(key):
        return "appendix" if key == (10 ** 6,) else ".".join(map(str, key))

    section_refs, forward, vague, support = [], [], [], []
    for s, e in _sentence_spans(text):
        sent = text[s:e]
        snip = _clip(re.sub(r"\s+", " ", sent).strip(), 80)

        # Section references, numeric and LaTeX.
        refs = []
        for m in SECTION_NUM_REF.finditer(sent):
            num = m.group(1) or m.group(2)
            refs.append((s + m.start(), "Section " + num,
                         tuple(int(x) for x in num.split("."))))
        for m in TEX_REF.finditer(sent):
            lab = m.group(1).split(",")[0].strip()
            if lab in labels:
                refs.append((s + m.start(), "\\ref{" + lab + "}", labels[lab]))
            elif lab.lower().startswith("sec"):
                refs.append((s + m.start(), "\\ref{" + lab + "}", None))
        for pos, name, target in refs:
            section_refs.append((line_of(pos), name))
            here = current_key(pos)
            if target and here and target > here:
                forward.append((line_of(pos),
                                f"{name} cited from section {fmt(here)}",
                                snip))

        # Vague pointers, one flag per sentence.
        fwd = VAGUE_FWD.search(sent)
        if fwd:
            vague.append((line_of(s + fwd.start()),
                          f"forward \"{fwd.group(0).lower()}\"", snip))
        else:
            for m in VAGUE_BACK.finditer(sent):
                if VAGUE_BACK_CITATION.match(sent[m.end():m.end() + 20]):
                    continue
                vague.append((line_of(s + m.start()),
                              f"backward \"{m.group(0).lower()}\"", snip))
                break

        # Supporting material with no specific item named.
        hit = SUPPORT_MENTION.search(sent) or SUPPORT_ABBR.search(sent)
        if hit and not SUPPORT_SPECIFIC.search(sent):
            support.append((line_of(s + hit.start()), hit.group(0), snip))

    return section_refs, forward, vague, support, bool(events)


# ---------------------------------------------------------------------------
# Report
# ---------------------------------------------------------------------------

def main():
    args = list(sys.argv[1:])
    # Check help before the option filter below strips it. Otherwise --help
    # falls through to read_input(None), which blocks on stdin.
    if "-h" in args or "--help" in args:
        print(__doc__)
        return
    quiet = "--quiet" in args
    args = [a for a in args if not a.startswith("--")]
    arg = args[0] if args else None

    raw = read_input(arg)
    if not raw.strip():
        print("No text to check.")
        return

    prose = strip_code(raw)
    sentences = split_sentences(prose)
    lengths = [word_count(s) for s in sentences if word_count(s) > 0]

    em = find_em_dashes(raw)
    bz = find_buzzwords(prose)
    wd = find_wordy(prose)
    fl = find_fillers(prose)
    openers = find_openers(sentences)
    heavy, r3 = comma_lists(sentences)
    front = find_front_loaded(sentences)
    passives = find_passive(sentences)
    hidden = find_hidden_verbs(prose)
    stacks = find_noun_stacks(prose)
    abbr_counts, abbr_defined = find_abbreviations(prose)
    vague, fp, sp = find_pronoun_issues(sentences, prose)
    scare, litq = find_scare_quotes(prose)
    paren = find_parentheses(prose)
    pres, past, fut = tense_profile(sentences)
    sec_refs, fwd_refs, vague_ptrs, vague_support, has_headings = \
        find_cross_references(prose)

    total_bz = sum(n for n, _ in bz.values())
    total_wd = sum(n for n, _ in wd.values())
    total_fl = sum(fl.values())
    # Abbreviation triage.
    #   wasteful : spelled out and abbreviated, then barely used. The
    #              definition cost more words than the abbreviation saved.
    #              This is the real defect, so it is the only one counted.
    #   spell_out: coined once, never defined, not widely known. Probably
    #              should just be the full term.
    #   introduce: used repeatedly, never defined, not widely known.
    wasteful = sorted(f"{a} (defined, used {abbr_counts[a]}x)"
                      for a in abbr_defined
                      if abbr_counts.get(a, 0) <= 2)
    spell_out = sorted(a for a, n in abbr_counts.items()
                       if n == 1 and a not in abbr_defined
                       and a not in WELL_KNOWN_ABBREV)
    introduce = sorted(a for a, n in abbr_counts.items()
                       if n >= 2 and a not in abbr_defined
                       and a not in WELL_KNOWN_ABBREV)
    known_once = sorted(a for a, n in abbr_counts.items()
                        if n == 1 and a in WELL_KNOWN_ABBREV)
    big_stacks = [h for h in stacks if h[0] >= 4]

    if not quiet:
        print("=" * 68)
        print("WRITING CHECK")
        print("=" * 68)

        print(f"\n[1] EM DASHES (target: 0)   found: {len(em)}")
        for line_no, kind, snip in em[:30]:
            print(f"    line {line_no}: {kind}  ...{snip}")
        if len(em) > 30:
            print(f"    ...and {len(em) - 30} more")
        if not em:
            print("    none. good.")

        print(f"\n[2] UNNECESSARY QUOTATION MARKS   scare quotes: {len(scare)}"
              f"   literal strings: {len(litq)}")
        for line_no, kind, snip in scare[:20]:
            print(f"    line {line_no}: {kind}  ...{snip}")
        if scare:
            print("    -> quotes used for emphasis or distance. Delete them,")
            print("       or say plainly what you mean.")
        for line_no, snip in litq[:10]:
            print(f"    line {line_no}: literal/label (review)  ...{snip}")
        if litq:
            print("    -> a real string or interface label. House style may")
            print("       want code formatting or bold instead of quotes.")
        if not scare and not litq:
            print("    none flagged.")

        print(f"\n[3] UNNECESSARY PARENTHESES   found: {len(paren)}")
        for line_no, kind, snip in paren[:20]:
            print(f"    line {line_no}: {kind}  ({snip})")
        if paren:
            print("    -> fold into the sentence, or make it its own sentence.")
            print("       Definitions, references, units, and math are exempt.")
        else:
            print("    none flagged.")

        print(f"\n[4] BUZZWORDS   found: {total_bz} across {len(bz)} distinct")
        for word, (n, sugg) in sorted(bz.items(), key=lambda x: -x[1][0])[:20]:
            print(f"    {word} (x{n})  ->  {sugg}")
        if not bz:
            print("    none flagged.")

        print(f"\n[5] WORDY PHRASES   found: {total_wd}")
        for pat, (n, plain) in sorted(wd.items(), key=lambda x: -x[1][0])[:15]:
            print(f"    \"{pat}\" (x{n})  ->  {plain}")
        if not wd:
            print("    none flagged.")

        print(f"\n[6] FILLER PHRASES   found: {total_fl}")
        for pat, n in sorted(fl.items(), key=lambda x: -x[1])[:15]:
            print(f"    \"{_readable(pat)}\" (x{n})")
        if not fl:
            print("    none flagged.")

        print(f"\n[7] SENTENCE LENGTH   sentences: {len(lengths)}")
        if len(lengths) >= 2:
            mean = statistics.mean(lengths)
            cv = statistics.pstdev(lengths) / mean if mean else 0
            over25 = [n for n in lengths if n > 25]
            over30 = [n for n in lengths if n > 30]
            print(f"    mean: {mean:.1f} words   longest: {max(lengths)}   "
                  f"variation (CV): {cv:.2f}")
            if mean > 22:
                print("    -> mean is high. Target 15-20 words for technical prose.")
            if over25:
                print(f"    -> {len(over25)} sentence(s) over 25 words "
                      f"({len(over30)} over 30). Split them.")
            if cv < 0.35:
                print("    -> LOW variation: lengths are too uniform. Vary the rhythm.")
        else:
            print("    too little text to judge.")

        print(f"\n[8] COMMA LISTS   heavy-comma sentences: {len(heavy)}   "
              f"rule-of-three lists: {r3}")
        for commas, snip in heavy[:8]:
            print(f"    {commas} commas: {snip}")
        if r3 > 2:
            print("    -> many 'X, Y, and Z' lists. Vary this; some belong as bullets.")

        print(f"\n[9] FRONT-LOADED SENTENCES (point delayed to the end)   "
              f"found: {len(front)}")
        for n, snip in front[:10]:
            print(f"    {n} words before the first break: {snip}")
        if front:
            print("    -> lead with the main clause; let conditions follow.")
        else:
            print("    none flagged.")

        print(f"\n[10] PASSIVE VOICE   found: {len(passives)}")
        for phrase, snip in passives[:12]:
            print(f"    \"{phrase}\": {snip}")
        if passives:
            print("    -> name the actor and use active voice, unless the actor is")
            print("       genuinely unknown or irrelevant.")
        else:
            print("    none flagged.")

        print(f"\n[11] HIDDEN VERBS (nominalizations)   found: {len(hidden)}")
        seen = set()
        for phrase, sugg in hidden:
            if phrase in seen:
                continue
            seen.add(phrase)
            print(f"    \"{phrase}\"  ->  {sugg}")
            if len(seen) >= 12:
                break
        if not hidden:
            print("    none flagged.")

        print(f"\n[12] NOUN STACK CANDIDATES   3+: {len(stacks)}   4+: {len(big_stacks)}")
        for n, run in sorted(stacks, key=lambda x: -x[0])[:10]:
            mark = "LIKELY DEFECT" if n >= 4 else "candidate"
            print(f"    [{n} nouns, {mark}] {run}")
        if stacks:
            print("    -> heuristic. Established multi-word terms are fine; leave them.")
        else:
            print("    none flagged.")

        print(f"\n[13] ABBREVIATIONS   distinct: {len(abbr_counts)}")
        if wasteful:
            print(f"    NOT EARNING ITS PLACE: {', '.join(wasteful)}")
            print("    -> the definition cost more than the short form saved.")
            print("       Delete the parenthetical and use the full term.")
        if spell_out:
            print(f"    coined once, never defined: {', '.join(spell_out)}")
            print("    -> use the full term instead of inventing a short form.")
        if introduce:
            print(f"    used repeatedly, never introduced: "
                  f"{', '.join(introduce)}")
            print("    -> spell it out on first use if readers may not know it.")
        if known_once:
            print(f"    widely known, used once (no action): "
                  f"{', '.join(known_once)}")
        if not (wasteful or spell_out or introduce):
            print("    no abbreviation problems flagged.")

        print(f"\n[14] PRONOUNS   vague/expletive openers: {len(vague)}   "
              f"first person: {fp}   second person: {sp}")
        for kind, snip in vague[:10]:
            print(f"    {kind}: {snip}")
        if fp:
            print("    -> first person (we/our/I) does not belong in technical pubs.")
        if sp:
            print("    -> second person (you/your): fine in software docs, barred by")
            print("       many tech pub standards. Prefer the imperative.")

        print(f"\n[15] TENSE   present: {pres}   past: {past}   future: {fut}")
        tensed = pres + past + fut
        if tensed:
            if past and pres and min(past, pres) / tensed > 0.2:
                print("    -> mixed past and present. Check for drift; use present")
                print("       tense for how the system behaves.")
            if fut and fut / tensed > 0.15:
                print("    -> heavy 'will/shall'. Use present tense for routine")
                print("       behavior ('the system sends', not 'will send').")

        print(f"\n[16] CROSS-REFERENCES   section refs: {len(sec_refs)}   "
              f"forward: {len(fwd_refs)}   vague pointers: {len(vague_ptrs)}   "
              f"vague supporting-material refs: {len(vague_support)}")
        if vague_support:
            print("    vague supporting material (defect):")
            for line_no, what, snip in vague_support[:12]:
                print(f"      line {line_no}: \"{what}\" names no item: {snip}")
            print("    -> name the exact item (Figure S3, Table S2) and what it")
            print("       shows, or state the finding in the main text. Never")
            print("       guess an item number. Flag it for the author instead.")
        if fwd_refs:
            print("    forward section references (defect):")
            for line_no, what, snip in fwd_refs[:12]:
                print(f"      line {line_no}: {what}: {snip}")
            print("    -> earlier text cannot rely on later sections. Move the")
            print("       result forward, or hold the claim until it appears.")
        if vague_ptrs:
            print("    vague pointers (defect):")
            for line_no, what, snip in vague_ptrs[:12]:
                print(f"      line {line_no}: {what}: {snip}")
            print("    -> name the exact section, figure, table, or equation,")
            print("       or delete the pointer.")
        if sec_refs:
            listed = ", ".join(f"{name} (line {ln})"
                               for ln, name in sec_refs[:12])
            print(f"    section references (review each): {listed}")
            if len(sec_refs) > 12:
                print(f"      ...and {len(sec_refs) - 12} more")
            print("    -> keep only the essential ones. If the reader needs an")
            print("       equation, figure, or table, cite that item instead.")
        if sec_refs and not has_headings:
            print("    no numbered headings found, so forward section")
            print("    references were not checked.")
        if not (sec_refs or vague_ptrs or vague_support):
            print("    none flagged.")

        print("\n" + "=" * 68)

    xref_defects = len(fwd_refs) + len(vague_ptrs) + len(vague_support)
    problems = (len(em) + len(scare) + len(paren) + total_bz + total_wd
                + total_fl + len(passives) + len(hidden) + len(big_stacks)
                + len(wasteful) + len(spell_out) + len(vague)
                + xref_defects)
    verdict = "CLEAN on mechanics" if problems == 0 else "needs work"
    print(f"SUMMARY: {verdict}.  em-dashes={len(em)} scare-quotes={len(scare)} "
          f"parentheses={len(paren)} buzzwords={total_bz} wordy={total_wd} "
          f"filler={total_fl}")
    print(f"         front-loaded={len(front)} passive={len(passives)} "
          f"hidden-verbs={len(hidden)} noun-stacks(4+)={len(big_stacks)}")
    print(f"         weak-abbrev={len(wasteful) + len(spell_out)} "
          f"vague-pronouns={len(vague)} first-person={fp}")
    print(f"         xref-defects={xref_defects} "
          f"section-refs={len(sec_refs)}")
    if not quiet:
        print("A clean report is a floor, not proof the prose is good.")
        print("=" * 68)


if __name__ == "__main__":
    try:
        import signal
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    except (ImportError, AttributeError, ValueError):
        pass
    main()
