"""从共享定义生成可独立安装的 OpenSpec 分级 schema。"""

import argparse
import copy
from pathlib import Path, PurePosixPath
import re
import shutil
import sys

try:
    import yaml
except ImportError:
    raise SystemExit("需要 PyYAML：python3 -m pip install PyYAML")


SOURCE_DIR = Path(__file__).resolve().parent


class ProfileError(ValueError):
    pass


class SchemaDumper(yaml.SafeDumper):
    pass


def represent_string(dumper, value):
    return dumper.represent_scalar(
        "tag:yaml.org,2002:str", value, style="|" if "\n" in value else None
    )


SchemaDumper.add_representer(str, represent_string)


def require(condition, message):
    if not condition:
        raise ProfileError(message)


def relative_path(value):
    return (
        isinstance(value, str) and bool(value)
        and not PurePosixPath(value).is_absolute()
        and "\\" not in value and ":" not in value
        and ".." not in PurePosixPath(value).parts
    )


def read_yaml(path):
    document = yaml.safe_load(path.read_text(encoding="utf-8"))
    require(isinstance(document, dict), f"{path}: 必须为 mapping")
    return document


def validate_schema(schema, templates_dir):
    for field in ("name", "description"):
        require(isinstance(schema.get(field), str) and schema[field], f"schema.{field} 必填")
    require(type(schema.get("version")) is int and schema["version"] > 0,
            "schema.version 必须为正整数")
    artifacts = schema.get("artifacts")
    require(isinstance(artifacts, list) and artifacts, "artifacts 必须为非空列表")
    by_id = {}
    for artifact in artifacts:
        require(isinstance(artifact, dict), "artifact 必须为 mapping")
        artifact_id = artifact.get("id")
        require(isinstance(artifact_id, str) and artifact_id, "artifact.id 必填")
        require(artifact_id not in by_id, f"重复 artifact: {artifact_id}")
        by_id[artifact_id] = artifact
        require(relative_path(artifact.get("generates")), f"{artifact_id}: 非法 generates")
        require(relative_path(artifact.get("template")), f"{artifact_id}: 非法 template")
        require((templates_dir / artifact["template"]).is_file(), f"{artifact_id}: 模板不存在")
        for field in ("description", "instruction"):
            require(isinstance(artifact.get(field), str) and artifact[field],
                    f"{artifact_id}: {field} 必填")
        dependencies = artifact.get("requires")
        require(isinstance(dependencies, list) and
                all(isinstance(dependency, str) for dependency in dependencies),
                f"{artifact_id}: requires 必须为字符串列表")
        require(len(dependencies) == len(set(dependencies)), f"{artifact_id}: 重复依赖")

    visiting, visited = set(), set()

    def visit(artifact_id):
        require(artifact_id not in visiting, f"依赖环涉及 {artifact_id}")
        if artifact_id in visited:
            return
        visiting.add(artifact_id)
        for dependency in by_id[artifact_id]["requires"]:
            require(dependency in by_id, f"{artifact_id}: 未知依赖 {dependency}")
            visit(dependency)
        visiting.remove(artifact_id)
        visited.add(artifact_id)

    for artifact_id in by_id:
        visit(artifact_id)
    apply = schema.get("apply")
    require(isinstance(apply, dict), "apply 必填")
    dependencies = apply.get("requires")
    require(isinstance(dependencies, list) and dependencies and
            all(isinstance(dependency, str) and dependency in by_id
                for dependency in dependencies), "apply.requires 非法")
    require(relative_path(apply.get("tracks")), "apply.tracks 非法")
    require(isinstance(apply.get("instruction"), str) and apply["instruction"],
            "apply.instruction 必填")
    return by_id


def validate_policy(policy, schema):
    require(type(policy.get("version")) is int and policy["version"] == 1,
            "flow-policy.version 必须为 1")
    rules = policy.get("rules")
    require(isinstance(rules, dict) and
            rules.get("selection") == "stricter-of-complexity-and-risk" and
            rules.get("on_doubt") == "escalate" and
            rules.get("revision") == "record-and-reselect", "flow-policy.rules 非法")
    tiers = policy.get("tiers")
    require(isinstance(tiers, dict) and set(tiers) == {"P0", "P1", "P2", "P3"},
            "tiers 必须包含且仅包含 P0/P1/P2/P3")
    artifacts = {artifact["id"]: artifact for artifact in schema["artifacts"]}
    allowed = {
        "review_mode": {"none", "fresh-context", "cross-model"},
        "review_timing": {"none", "once"},
        "design_depth": {"skip", "brief", "full"},
        "tdd": {"none", "optional", "mandatory"},
        "coverage": {"none", "acceptance", "inline", "ledger"},
        "adr": {"none", "when-long-lived"},
        "verify_depth": {"none", "full"},
    }
    schema_names = set()
    for tier, settings in tiers.items():
        require(isinstance(settings, dict), f"{tier}: 必须为 mapping")
        require(isinstance(settings.get("label"), str) and settings["label"], f"{tier}: label 必填")
        criteria = settings.get("criteria")
        require(isinstance(criteria, list) and criteria and
                all(isinstance(item, str) and item for item in criteria),
                f"{tier}: criteria 必须为非空字符串列表")
        for field, values in allowed.items():
            value = settings.get(field)
            require(isinstance(value, str) and value in values, f"{tier}: {field} 非法: {value}")
        flow = settings.get("flow")
        require(isinstance(flow, list) and
                all(isinstance(step, str) and step in artifacts for step in flow),
                f"{tier}: flow 含未知 artifact 或类型非法")
        require(len(flow) == len(set(flow)), f"{tier}: flow 含重复 artifact")
        if tier == "P3":
            require(not flow and settings.get("schema") is None, "P3 必须为零 artifact")
            require(all(settings[field] in {"none", "skip"} for field in allowed),
                    "P3 的环节模式必须为 none/skip")
            continue
        schema_name = settings.get("schema")
        require(isinstance(schema_name, str) and
                re.fullmatch(r"[a-z][a-z0-9]*(?:-[a-z0-9]+)*", schema_name),
                f"{tier}: schema 名称非法")
        require(schema_name not in schema_names, f"重复 schema 名称: {schema_name}")
        schema_names.add(schema_name)
        require(flow and flow[0] == "proposal" and
                {"proposal", "specs", "design", "tasks"}.issubset(flow),
                f"{tier}: flow 必须以 proposal 起步并保留 spec-driven 主干")
        for step in flow:
            for dependency in artifacts[step]["requires"]:
                if dependency in flow:
                    require(flow.index(dependency) < flow.index(step),
                            f"{tier}: {step} 位于前置 {dependency} 之前")
        require(("review" in flow) == (settings["review_mode"] != "none"),
                f"{tier}: review_mode 与 flow 不一致")
        require(settings["review_timing"] == ("once" if "review" in flow else "none"),
                f"{tier}: review_timing 必须为 once/none，与 flow 一致")
        require(settings["design_depth"] != "skip", f"{tier}: design 不能 skip")
        require(("test-plan" in flow) == (settings["coverage"] == "ledger"),
                f"{tier}: coverage=ledger 必须与 test-plan 同时启用")
        require(settings["coverage"] != "none", f"{tier}: 必须提供验收/覆盖")
        require(("verify" in flow) == (settings["verify_depth"] == "full"),
                f"{tier}: verify_depth 与 flow 不一致")
    require(tiers["P0"]["schema"] == schema["name"], "P0 schema 名称必须与共享定义一致")
    require(tiers["P0"]["flow"] == [artifact["id"] for artifact in schema["artifacts"]],
            "P0 flow 必须与共享定义的完整 artifact 列表及顺序一致")
    return tiers


def make_profile(schema, tier, settings):
    profile = copy.deepcopy(schema)
    profile["name"] = settings["schema"]
    profile["description"] = f"证据驱动 {tier}（{settings['label']}）：" + " → ".join(settings["flow"])
    source_artifacts = {artifact["id"]: artifact for artifact in profile["artifacts"]}
    prefix = (
        f"当前 schema 固定对应 {tier}，名称为 {settings['schema']}。\n"
        f"先读实际 schema 目录的 flow-policy.yaml 中 tiers.{tier}；"
        "Tier 与 schema 不一致时停止并重新选择档位。\n\n"
    )
    profile["artifacts"] = [source_artifacts[step] for step in settings["flow"]]
    for artifact in profile["artifacts"]:
        artifact["requires"] = [dependency for dependency in artifact["requires"]
                                if dependency in settings["flow"]]
        artifact["instruction"] = prefix + artifact["instruction"]
    profile["apply"]["instruction"] = prefix + profile["apply"]["instruction"]
    return profile


def load_profiles(source_dir=SOURCE_DIR):
    schema = read_yaml(source_dir / "schema.yaml")
    policy = read_yaml(source_dir / "flow-policy.yaml")
    templates_dir = source_dir / "templates"
    validate_schema(schema, templates_dir)
    require(schema["apply"]["requires"] == ["tasks"] and
            schema["apply"]["tracks"] == "tasks.md", "apply 必须由 tasks 解锁并跟踪 tasks.md")
    tiers = validate_policy(policy, schema)
    profiles = {}
    for tier, settings in tiers.items():
        if settings["flow"]:
            profiles[tier] = make_profile(schema, tier, settings)
            validate_schema(profiles[tier], templates_dir)
            for index, step in enumerate(settings["flow"]):
                completed = set(settings["flow"][:index])
                ready = [artifact["id"] for artifact in profiles[tier]["artifacts"]
                         if artifact["id"] not in completed and
                         set(artifact["requires"]).issubset(completed)]
                require(ready == [step],
                        f"{tier}: 实际依赖图不能保证下一步 {step}，就绪项为 {ready}")
    return policy, profiles


def render_template(artifact, tier, settings):
    template = (SOURCE_DIR / "templates" / artifact["template"]).read_text(encoding="utf-8")
    template = template.replace("Tier: <P0|P1|P2>", f"Tier: {tier}")
    if artifact["id"] == "tasks" and settings["coverage"] != "inline":
        template = re.sub(r"\n## Coverage Mapping\n.*?(?=\n## |\Z)", "", template, flags=re.S)
    return template


def write_profiles(output, policy, profiles, force=False):
    destinations = [output / profile["name"] for profile in profiles.values()]
    for destination in destinations:
        require(destination.resolve() != SOURCE_DIR, "不能覆盖共享源码目录")
        require(not destination.exists() or force, f"{destination} 已存在；更新请使用 --force")
        require(not destination.exists() or destination.is_dir(), f"{destination} 不是目录")
    for tier, profile in profiles.items():
        destination = output / profile["name"]
        destination.mkdir(parents=True, exist_ok=True)
        (destination / "schema.yaml").write_text(
            yaml.dump(profile, Dumper=SchemaDumper, allow_unicode=True, sort_keys=False),
            encoding="utf-8",
        )
        shutil.copyfile(SOURCE_DIR / "flow-policy.yaml", destination / "flow-policy.yaml")
        for artifact in profile["artifacts"]:
            template_path = destination / "templates" / artifact["template"]
            template_path.parent.mkdir(parents=True, exist_ok=True)
            template_path.write_text(
                render_template(artifact, tier, policy["tiers"][tier]), encoding="utf-8"
            )
        readme = (
            f"> 生成包：**{tier} / {profile['name']}**，"
            f"{len(profile['artifacts'])} 个 artifact。此目录的 schema.yaml 是本档依赖图，"
            "下文共享定义/构建命令指本仓库源码；不要直接修改生成文件。\n\n"
            + (SOURCE_DIR / "README.md").read_text(encoding="utf-8")
        )
        (destination / "README.md").write_text(readme, encoding="utf-8")
        print(f"{tier}: {destination} ({len(profile['artifacts'])} artifacts)")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True, help="目标 openspec/schemas 目录")
    parser.add_argument("--force", action="store_true", help="更新已有的生成包，不删除其他文件")
    args = parser.parse_args()
    try:
        policy, profiles = load_profiles()
        write_profiles(args.output.resolve(), policy, profiles, args.force)
    except (ProfileError, OSError, yaml.YAMLError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
