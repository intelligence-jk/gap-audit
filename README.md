# gap-audit

Finds the root gaps in a student's topic results. If fractions, ratio and percentages all went badly, the real gap is fractions, and fixing it first is what unlocks the other two.

## What it solves
After a diagnostic test a tutor sees many weak topics at once and has to decide where to start. You give the tool a prerequisite graph (which topic needs which) and the marks per topic. It marks a topic as failed below a pass line, finds the **root gaps** (failed topics none of whose prerequisites failed) and gives a **teaching order** with prerequisites first. Pure Python 3.10+, standard library only. The example data below is invented and describes no real student.

## Example
```bash
python -m gapaudit examples/invented.json
```
```
Root gaps (start here): fractions, linear equations
Teaching order: fractions -> ratio -> linear equations -> percentages -> simultaneous equations
```
(Output pasted from a real run.)

## The maths behind it
A topic fails when marks/out_of is below the pass line, compared as an exact `Fraction` (so 1 out of 2 passes a pass line of 1/2 and 49 out of 100 does not). The prerequisite graph must be a directed acyclic graph; a cycle or an unknown prerequisite is rejected. A root gap is a failed vertex with no failed in-neighbour. The teaching order is a topological order of the graph restricted to failed topics, so every prerequisite that failed comes before the topic that needs it.

## Install and run
```bash
python -m pip install -e .
python -m pytest
```

## Licence
MIT. Made by Math & Myth (mathandmyth.ae): one to one maths mentoring, online, across the UAE.
