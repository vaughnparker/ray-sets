"""jsonfmt.py - indented JSON that keeps leaf numeric arrays on one line.

Plain json.dumps(indent=2) explodes every 3-vector across five lines, which makes
the generated data files unreadable. jdump() indents structure but prints any list
of numbers (a ray, a depth pair, a histogram row) inline.
"""
import json

__all__ = ["jdump"]

_NUM = (int, float, bool, type(None))


def _leaf(v):
    return isinstance(v, list) and all(isinstance(x, _NUM) for x in v)


def jdump(obj, indent=2, _level=0):
    pad, pad2 = " " * (indent * _level), " " * (indent * (_level + 1))
    if _leaf(obj) or not isinstance(obj, (dict, list)):
        return json.dumps(obj, ensure_ascii=False)
    if isinstance(obj, list):
        if not obj:
            return "[]"
        items = [pad2 + jdump(v, indent, _level + 1) for v in obj]
        return "[\n" + ",\n".join(items) + "\n" + pad + "]"
    if not obj:
        return "{}"
    items = [pad2 + json.dumps(str(k), ensure_ascii=False) + ": " + jdump(v, indent, _level + 1)
             for k, v in obj.items()]
    return "{\n" + ",\n".join(items) + "\n" + pad + "}"
