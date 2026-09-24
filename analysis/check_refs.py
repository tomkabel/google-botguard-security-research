"""Reference check for paper.md (Phase 7): every [n] citation has an entry, every entry is cited,
no placeholder text. `--renumber` rewrites paper.md so entries are numbered in order of first
citation (IEEE style) and uncited entries are dropped.

  python3 analysis/check_refs.py [--renumber]
"""
import pathlib, re, sys

PAPER = pathlib.Path(__file__).resolve().parent.parent / "paper.md"
CITE = re.compile(r"\[(\d+(?:[–-]\d+)?(?:[,;]\s*(?:see also\s+)?\d+(?:[–-]\d+)?)*)\](?!\()")
ENTRY = re.compile(r"^\*\*\[(\d+)\]\*\*", re.M)


def expand(group):
    out = []
    for part in re.split(r"[,;]\s*(?:see also\s+)?", group):
        a, _, b = part.replace("-", "–").partition("–")
        out += range(int(a), int(b or a) + 1)
    return out


def compress(nums):
    nums, out, i = sorted(set(nums)), [], 0
    while i < len(nums):
        j = i
        while j + 1 < len(nums) and nums[j + 1] == nums[j] + 1:
            j += 1
        out.append(f"{nums[i]}–{nums[j]}" if j - i >= 2 else ", ".join(map(str, nums[i:j + 1])))
        i = j + 1
    return ", ".join(out)


def split(text):
    i = text.index("\n## References")
    j = text.find("\n## Appendix", i)
    return text[:i], text[i:j if j > 0 else len(text)], text[j:] if j > 0 else ""


def check(text):
    body, refs, app = split(text)
    cited = [n for g in CITE.findall(body + app) for n in expand(g)]
    entries = [int(n) for n in ENTRY.findall(refs)]
    missing = sorted(set(cited) - set(entries))
    uncited = sorted(set(entries) - set(cited))
    dup = sorted({n for n in entries if entries.count(n) > 1})
    placeholders = re.findall(r"\[(?:Author|TBD|citation needed|\?)[^\]]*\]", text, re.I)
    return cited, entries, missing, uncited, dup, placeholders


def renumber(text):
    body, refs, app = split(text)
    order = []
    for g in CITE.findall(body + app):
        for n in expand(g):
            if n not in order:
                order.append(n)
    new = {old: i + 1 for i, old in enumerate(order)}
    sub = lambda m: "[" + compress(new[n] for n in expand(m.group(1))) + "]"
    blocks = {int(m.group(1)): m for m in ENTRY.finditer(refs)}
    starts = sorted(m.start() for m in blocks.values())
    chunk = {n: refs[m.start():next((s for s in starts if s > m.start()), len(refs))].strip() for n, m in blocks.items()}
    head = refs[:starts[0]]
    entries = [ENTRY.sub(f"**[{new[o]}]**", chunk[o], count=1) for o in order]
    return CITE.sub(sub, body) + head + "\n\n".join(entries) + "\n" + CITE.sub(sub, app)


def selfcheck():
    assert expand("23, 69–73") == [23, 69, 70, 71, 72, 73] and expand("18; see also 16") == [18, 16]
    assert compress([3, 1, 2, 7, 9, 10]) == "1–3, 7, 9, 10"
    t = "x [5] y [2, 5] z [9]\n## References\n\n**[2]** B.\n\n**[5]** A.\n\n**[7]** C.\n\n**[9]** D.\n"
    r = renumber(t)
    assert r.startswith("x [1] y [1, 2] z [3]") and "**[1]** A." in r and "**[2]** B." in r and "C." not in r, r
    assert check(r)[2:5] == ([], [], [])


if __name__ == "__main__":
    selfcheck()
    text = PAPER.read_text()
    if "--renumber" in sys.argv:
        text = renumber(text)
        PAPER.write_text(text)
        print("renumbered")
    cited, entries, missing, uncited, dup, ph = check(text)
    print(f"{len(set(cited))} cited, {len(entries)} entries; missing {missing}; uncited {uncited}; duplicate {dup}; placeholders {ph}")
    sys.exit(1 if missing or dup else 0)
