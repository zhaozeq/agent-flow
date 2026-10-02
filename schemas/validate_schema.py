"""校验 evidence-driven/schema.yaml：YAML 语法 + OpenSpec 校验规则（types.ts/schema.ts 的移植）"""
import sys, os, json
try:
    import yaml
except ImportError:
    print("PyYAML 不可用", ); sys.exit(2)

PATH = os.path.join(os.path.dirname(__file__), "evidence-driven", "schema.yaml")
with open(PATH, encoding="utf-8") as f:
    s = yaml.safe_load(f)

errs = []
if not s.get("name"): errs.append("name required")
v = s.get("version")
if not isinstance(v, int) or v < 1: errs.append("version must be positive int")
arts = s.get("artifacts")
if not isinstance(arts, list) or not arts: errs.append("artifacts required")

ids = set()
for a in arts or []:
    if not a.get("id"): errs.append("artifact id required"); continue
    if a["id"] in ids: errs.append(f"duplicate id: {a['id']}")
    ids.add(a["id"])
    g = a.get("generates")
    if not g or g.startswith(("/", "\\")) or ".." in (g or "").split("/"): errs.append(f"{a['id']}: bad generates")
    if not a.get("description"): errs.append(f"{a['id']}: description required")
    if not a.get("template"): errs.append(f"{a['id']}: template required")

for a in arts or []:
    for r in a.get("requires") or []:
        if r not in ids: errs.append(f"{a['id']}: requires unknown '{r}'")

# 环检测（DFS）
color = {}
def dfs(i):
    color[i] = 1
    node = next(x for x in arts if x["id"] == i)
    for r in node.get("requires") or []:
        if color.get(r) == 1: errs.append(f"cycle: {i} -> {r}")
        elif color.get(r) is None: dfs(r)
    color[i] = 2
for a in arts or []:
    if color.get(a["id"]) is None: dfs(a["id"])

ap = s.get("apply")
if ap:
    if not ap.get("requires"): errs.append("apply.requires needs >=1")
    for r in ap.get("requires") or []:
        if r not in ids: errs.append(f"apply requires unknown '{r}'")

if errs:
    print("FAIL:"); [print(" -", e) for e in errs]; sys.exit(1)

print("PASS: schema 结构合法（YAML 语法 + OpenSpec 校验规则）")
print("artifacts:", " -> ".join(a["id"] for a in arts))

tpl_dir = os.path.join(os.path.dirname(PATH), "templates")
missing = [a["template"] for a in arts if not os.path.exists(os.path.join(tpl_dir, a["template"]))]
if missing:
    print("缺失模板:", ", ".join(missing)); sys.exit(1)
print(f"全部 {len(arts)} 个模板文件存在")

# ---------------------------------------------------------------------------
# flow-policy.yaml 与 schema 静态依赖图的一致性检查
# ---------------------------------------------------------------------------
FP = os.path.join(os.path.dirname(PATH), "flow-policy.yaml")
if not os.path.exists(FP):
    print("缺失 flow-policy.yaml"); sys.exit(1)
with open(FP, encoding="utf-8") as f:
    fp = yaml.safe_load(f)

perrs = []
tiers = fp.get("tiers") or {}
if not tiers: perrs.append("tiers 为空")

STATIC_DEPS = {  # schema 的存在性依赖（启用某环节时其前置必须在 flow 中）
    "design": [], "review": ["design"], "test-plan": [],
    "verify": [], "proposal": [], "specs": [], "tasks": [],
}
# tasks 的 specs 前置仅在 flow 含 specs 时要求（specs→tasks 是主干，
# 但 P2 的 flow 不含 specs，tasks 直接跟在 design 后）
SPECIAL_PRECONDITIONS = {("tasks", "specs"): lambda flow: "specs" in flow}
for name, t in tiers.items():
    flow = t.get("flow") or []
    direct_mode = len(flow) == 0  # 直改模式（如 P3）：零 artifact，不经 openspec
    if direct_mode:
        # PyYAML(1.1) 会把 no/yes 解析为 False/True，归一化后比较
        if t.get("adr") not in (None, "no", "none", False):
            perrs.append(f"{name}: flow 为空（直改模式）但 adr={t.get('adr')} 应为 no")
        for key in ("review_mode", "design_depth", "tdd", "verify_depth"):
            if t.get(key) not in (None, "none", "skip", "no", False):
                perrs.append(f"{name}: flow 为空（直改模式）但 {key}={t.get(key)} 应为 none/skip/no")
        continue
    for art_id in ("tasks",):
        if art_id not in flow:
            perrs.append(f"{name}: flow 缺少主干环节 {art_id}")
    if "proposal" in flow and flow and flow[0] != "proposal":
        perrs.append(f"{name}: flow 含 proposal 但未以 proposal 起步")
    for step in flow:
        if step not in ids:
            perrs.append(f"{name}: flow 含未知 artifact '{step}'")
        for dep in STATIC_DEPS.get(step, []):
            cond = SPECIAL_PRECONDITIONS.get((step, dep))
            if cond is not None:
                if not cond(flow):
                    perrs.append(f"{name}: flow 启用 {step} 但缺其前置 {dep}")
            elif dep not in flow:
                perrs.append(f"{name}: flow 启用 {step} 但缺其前置 {dep}")
    rm, dd, vd, td, adr = (t.get("review_mode"), t.get("design_depth"),
                            t.get("verify_depth"), t.get("tdd"), t.get("adr"))
    rt = t.get("review_timing")
    if rt not in (None, "none", "staged", "once"):
        perrs.append(f"{name}: 未知 review_timing '{rt}'")
    if rt == "staged" and "specs" not in flow:
        perrs.append(f"{name}: review_timing=staged 但 flow 不含 specs（S2 规范审需要）")
    if rm == "none" and "review" in flow: perrs.append(f"{name}: review_mode=none 但 flow 含 review")
    if rm != "none" and "review" not in flow: perrs.append(f"{name}: review_mode={rm} 但 flow 不含 review")
    if dd == "skip" and "design" in flow: perrs.append(f"{name}: design_depth=skip 但 flow 含 design")
    if dd not in ("skip", None) and "design" not in flow: perrs.append(f"{name}: design_depth={dd} 但 flow 不含 design")
    if vd == "none" and "verify" in flow: perrs.append(f"{name}: verify_depth=none 但 flow 含 verify")
    if vd not in ("none", None) and "verify" not in flow: perrs.append(f"{name}: verify_depth={vd} 但 flow 不含 verify")
    if td == "mandatory" and "test-plan" not in flow:
        perrs.append(f"{name}: tdd=mandatory 但 flow 不含 test-plan")
    if rm not in (None, "none", "self", "fresh-context", "cross-model"):
        perrs.append(f"{name}: 未知 review_mode '{rm}'")
    if dd not in (None, "skip", "brief", "full"):
        perrs.append(f"{name}: 未知 design_depth '{dd}'")
    if vd not in (None, "none", "minimal", "full"):
        perrs.append(f"{name}: 未知 verify_depth '{vd}'")
    if td not in (None, "none", "optional", "mandatory"):
        perrs.append(f"{name}: 未知 tdd '{td}'")

if perrs:
    print("flow-policy FAIL:"); [print(" -", e) for e in perrs]; sys.exit(1)
print("PASS: flow-policy 与 schema 依赖图一致")
for name, t in tiers.items():
    flow = t.get("flow") or []
    flow_str = " → ".join(flow) if flow else "（直改模式：不经 openspec）"
    print(f"  {name} ({t.get('label','')}): {flow_str} | review={t.get('review_mode')} design={t.get('design_depth')} tdd={t.get('tdd')} adr={t.get('adr')} verify={t.get('verify_depth')}")
