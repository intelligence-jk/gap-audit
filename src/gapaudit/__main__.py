import json
import sys
from fractions import Fraction
from .core import report


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if len(argv) != 1:
        print("usage: python -m gapaudit data.json  (keys: prereqs, scores)")
        return 2
    with open(argv[0]) as f:
        d = json.load(f)
    scores = {k: tuple(v) for k, v in d["scores"].items()}
    print(report(d["prereqs"], scores, Fraction(d.get("pass_line", "1/2"))))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
