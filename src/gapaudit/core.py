"""Find the root gaps in a student's results using a prerequisite graph.

A topic is failed when the score (as a Fraction of full marks) is below the
pass line. A root gap is a failed topic none of whose prerequisites failed:
fixing it first is what makes the later failures fixable.
"""
from fractions import Fraction
from graphlib import TopologicalSorter, CycleError


class GapError(ValueError):
    pass


def _check(prereqs):
    for topic, ps in prereqs.items():
        for p in ps:
            if p not in prereqs:
                raise GapError(f"{topic!r} needs unknown prerequisite {p!r}")
    try:
        list(TopologicalSorter({t: set(p) for t, p in prereqs.items()}).static_order())
    except CycleError as e:
        raise GapError("prerequisite graph has a cycle") from e


def failed_topics(scores, pass_line=Fraction(1, 2)):
    """scores: {topic: (marks, out_of)}. Failed when marks/out_of < pass_line."""
    pass_line = Fraction(pass_line)
    out = set()
    for topic, (m, total) in scores.items():
        if total <= 0:
            raise GapError(f"{topic!r} has no marks available")
        if Fraction(m, total) < pass_line:
            out.add(topic)
    return out


def root_gaps(prereqs, scores, pass_line=Fraction(1, 2)):
    _check(prereqs)
    bad = failed_topics(scores, pass_line)
    return sorted(t for t in bad if not (set(prereqs.get(t, ())) & bad))


def teach_order(prereqs, scores, pass_line=Fraction(1, 2)):
    """Failed topics, prerequisites first."""
    _check(prereqs)
    bad = failed_topics(scores, pass_line)
    order = TopologicalSorter({t: set(p) for t, p in prereqs.items()}).static_order()
    return [t for t in order if t in bad]


def report(prereqs, scores, pass_line=Fraction(1, 2)):
    roots = root_gaps(prereqs, scores, pass_line)
    order = teach_order(prereqs, scores, pass_line)
    lines = ["Root gaps (start here): " + (", ".join(roots) or "none"),
             "Teaching order: " + (" -> ".join(order) or "nothing to teach")]
    return "\n".join(lines)
