#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""最小示例：一条 JSONL 对话 → 四个值的时间曲线（纯文本，无第三方依赖）。

    python3 demo.py demo.jsonl

每行一条消息：{"ts": 1793000000, "role": "her", "text": "..."}
role=me 时只认「认错/道歉」那一种（悔）。
"""
import json, sys, time
import endocrine as E


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else ''
    if not path:
        print(__doc__)
        return
    t0 = None
    n = 0
    for line in open(path, encoding='utf-8'):
        line = line.strip()
        if not line:
            continue
        try:
            d = json.loads(line)
        except Exception:
            continue
        ts = float(d.get('ts') or 0)
        t0 = t0 or ts
        txt = d.get('text') or ''
        if d.get('role') == 'me':
            E.observe_me(txt, ts=ts)
        else:
            E.observe_her(txt, ts=ts)
        n += 1
        if n % 5 == 0:                      # 每五条打一次曲线点
            v = E.snapshot(ts)
            bar = lambda x: '▓' * int(round(x / 100.0 * 20))
            m = E.mood(ts)
            print('%s  da%3.0f %s   %-6s %s | %s' % (
                time.strftime('%H:%M', time.localtime(ts)), v['da'], bar(v['da']),
                m['label'], m['tense'] + '/' + m['pace'], m['line']))
    print('\n%d 条消息，%d 笔账。' % (n, E._conn().execute('select count(*) from luna_hormone').fetchone()[0]))


if __name__ == '__main__':
    main()
