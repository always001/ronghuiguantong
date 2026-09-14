# -*- coding: utf-8 -*-
import os, re

# 路径相对化：无论从哪个目录运行都指向本脚本同级的 js/data.js
HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(HERE, "js", "data.js")
src = open(P, encoding="utf-8").read()

CN = ["零", "一", "二", "三", "四", "五", "六", "七", "八", "九", "十", "十一", "十二"]
GRADE_NUM = {f"{CN[g]}年级": g for g in range(1, 13)}
STAGE_NUM = {"小学": 1, "中学": 2, "高中": 3}

# id -> (stage, grade)。中学=初中(七~九年级)，高中=十~十二年级
MAP = {
    "count": ("小学", "一年级"), "addsub": ("小学", "一年级"),
    "multi": ("小学", "二年级"), "divide": ("小学", "二年级"),
    "fourops": ("小学", "三年级"), "plant": ("小学", "三年级"), "average": ("小学", "三年级"),
    "cycle": ("小学", "三年级"), "speedcalc": ("小学", "三年级"), "arithseq": ("小学", "三年级"),
    "sumdiff": ("小学", "四年级"), "profitloss": ("小学", "四年级"), "guiyi": ("小学", "四年级"),
    "parity": ("小学", "四年级"), "divisibility": ("小学", "四年级"), "remainder": ("小学", "四年级"),
    "prime": ("小学", "四年级"),
    "fraction": ("小学", "五年级"), "decimal": ("小学", "五年级"), "ratio": ("小学", "五年级"),
    "chicken": ("小学", "五年级"), "perim": ("小学", "五年级"), "area_equal": ("小学", "五年级"),
    "pigeon": ("小学", "五年级"), "inclusion": ("小学", "五年级"),
    "percent": ("小学", "六年级"), "trip": ("小学", "六年级"), "engineer": ("小学", "六年级"),
    "profit": ("小学", "六年级"), "circle": ("小学", "六年级"), "cylinder": ("小学", "六年级"),
    "equation": ("小学", "六年级"), "meet": ("小学", "六年级"), "chase": ("小学", "六年级"),
    "boat": ("小学", "六年级"), "circle_track": ("小学", "六年级"), "cowgrass": ("小学", "六年级"),
    "concentration": ("小学", "六年级"),
    "rational": ("中学", "七年级"), "integral": ("中学", "七年级"), "linear1": ("中学", "七年级"),
    "inequal": ("中学", "七年级"), "system": ("中学", "七年级"), "segangle": ("中学", "七年级"),
    "triangle": ("中学", "七年级"), "stats": ("中学", "七年级"),
    "congruent": ("中学", "八年级"), "similar": ("中学", "八年级"), "pyth": ("中学", "八年级"),
    "quad": ("中学", "八年级"), "func1": ("中学", "八年级"), "inverse": ("中学", "八年级"),
    "circ": ("中学", "九年级"), "general": ("中学", "九年级"), "melon": ("中学", "九年级"),
    "moving": ("中学", "九年级"), "quadfunc": ("中学", "九年级"), "prob": ("中学", "九年级"),
    "set": ("高中", "十年级"), "funcconcept": ("高中", "十年级"), "explog": ("高中", "十年级"),
    "complex": ("高中", "十年级"),
    "trig": ("高中", "十一年级"), "sequence": ("高中", "十一年级"), "vector": ("高中", "十一年级"),
    "solid": ("高中", "十一年级"), "trig_id": ("高中", "十一年级"), "seqsum": ("高中", "十一年级"),
    "solid_axis": ("高中", "十一年级"), "solid_angle": ("高中", "十一年级"),
    "stat_case": ("高中", "十二年级"),
    "derivative": ("高中", "十二年级"), "conic": ("高中", "十二年级"), "deriv_mon": ("高中", "十二年级"),
    "deriv_ineq": ("高中", "十二年级"), "func_zero": ("高中", "十二年级"), "conic_link": ("高中", "十二年级"),
    "conic_chord": ("高中", "十二年级"), "conic_prop": ("高中", "十二年级"), "param_eq": ("高中", "十二年级"),
    "dist_exp": ("高中", "十二年级"), "dist_binom": ("高中", "十二年级"),
}

# 1) 解析 prereq
prereqs = {}
for m in re.finditer(r'id:\s*"([^"]+)"', src):
    tid = m.group(1)
    # 找该对象范围内最近的 prereq
    after = src[m.end():m.end() + 400]
    pm = re.search(r'prereq:\s*("?[^,\n]+"?)', after)
    if pm:
        v = pm.group(1).strip()
        prereqs[tid] = v.strip('"') if v.startswith('"') else None
    else:
        prereqs[tid] = None

# 2) 校验：仅同阶段且年级更高才算真正倒置
warn = []
for tid, pr in prereqs.items():
    if pr and pr in MAP and tid in MAP:
        s1, g1 = MAP[tid]; s2, g2 = MAP[pr]
        if STAGE_NUM[s1] == STAGE_NUM[s2] and GRADE_NUM[g1] < GRADE_NUM[g2]:
            warn.append(f"  ⚠ 同阶段倒置: {tid}({s1}{g1}) prereq {pr}({s1}{g2})")

# 3) 重写每个对象所在行：同行的 id 与 grade 都在，按 id 查 MAP 改写 grade 并插入 stage
def repl(line):
    mid = re.search(r'id:\s*"([^"]+)"', line)
    if not mid:
        return line
    tid = mid.group(1)
    if tid not in MAP:
        return line
    # 幂等：已含 stage 则不重复写入（避免 grade:"X",stage:"Y",stage:"Y"）
    if "stage:" in line:
        return line
    stage, grade = MAP[tid]
    # 替换 grade 值，并在其后插入 stage（保持同行，后续还有 name 等属性）
    return re.sub(r'grade:\s*"[^"]*"',
                  f'grade: "{grade}", stage: "{stage}"', line, count=1)

out_lines = [repl(l) for l in src.splitlines()]
new_src = "\n".join(out_lines)
open(P, "w", encoding="utf-8").write(new_src + "\n")

# 4) 报告
changed = sum(1 for l in out_lines if "stage:" in l and 'id:' in l)
new_count = {}
for s, g in MAP.values():
    new_count.setdefault(s, {}).setdefault(g, 0)
    new_count[s][g] += 1
print(f"已写入 stage/grade 的对象行数: {changed}（应=82）")
for s in ["小学", "中学", "高中"]:
    tot = sum(new_count[s].values())
    detail = " ".join(f"{g}{n}" for g, n in sorted(new_count[s].items(), key=lambda x: GRADE_NUM[x[0]]))
    print(f"  {s}: 共{tot}  {detail}")
print("真正倒置警告:", len(warn))
for w in warn:
    print(w)
