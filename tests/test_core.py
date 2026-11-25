from fractions import Fraction
import pytest
from gapaudit import failed_topics, root_gaps, teach_order, GapError

P = {"a": [], "b": ["a"], "c": ["b"], "d": []}


def test_failed_uses_exact_pass_line():
    assert failed_topics({"a": (1, 2)}) == set()          # exactly 1/2 passes
    assert failed_topics({"a": (49, 100)}) == {"a"}


def test_root_gap_is_lowest_failed():
    s = {"a": (1, 10), "b": (1, 10), "c": (1, 10), "d": (9, 10)}
    assert root_gaps(P, s) == ["a"]


def test_two_roots():
    s = {"a": (9, 10), "b": (1, 10), "c": (1, 10), "d": (1, 10)}
    assert root_gaps(P, s) == ["b", "d"]


def test_no_failures():
    s = {t: (9, 10) for t in P}
    assert root_gaps(P, s) == [] and teach_order(P, s) == []


def test_order_puts_prereqs_first():
    s = {"a": (1, 10), "b": (1, 10), "c": (1, 10), "d": (1, 10)}
    o = teach_order(P, s)
    assert o.index("a") < o.index("b") < o.index("c")


def test_cycle_rejected():
    with pytest.raises(GapError):
        root_gaps({"a": ["b"], "b": ["a"]}, {"a": (1, 2), "b": (1, 2)})


def test_unknown_prereq_rejected():
    with pytest.raises(GapError):
        root_gaps({"a": ["zzz"]}, {"a": (1, 2)})


def test_zero_marks_rejected():
    with pytest.raises(GapError):
        failed_topics({"a": (0, 0)})


def test_custom_pass_line():
    assert failed_topics({"a": (6, 10)}, Fraction(7, 10)) == {"a"}
