"""校验 evidence-driven 共享定义、分级依赖图及可选的已安装生成包。"""

import argparse
from pathlib import Path
import re
import sys

PROFILE_DIR = Path(__file__).resolve().parent / "evidence-driven"
sys.path.insert(0, str(PROFILE_DIR))

from build_profiles import (
    ProfileError,
    load_profiles,
    read_yaml,
    render_template,
    require,
    validate_schema,
    yaml,
)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--installed", type=Path, help="额外检查目标 openspec/schemas 生成包")
    args = parser.parse_args()
    try:
        policy, profiles = load_profiles()
        for template in (PROFILE_DIR / "templates").glob("*.md"):
            for comment in re.findall(r"<!--.*?-->", template.read_text(encoding="utf-8"), re.S):
                require(not re.search(r"^[-*]\s*\[[ xX]\]", comment, re.M),
                        f"{template}: 注释含可被 CLI 解析的任务示例")
        print("PASS: 共享 schema、模板、策略与实际 requires 顺序一致")
        for tier, profile in profiles.items():
            print(f"  {tier} / {profile['name']}: " +
                  " → ".join(artifact["id"] for artifact in profile["artifacts"]))
            if args.installed:
                directory = args.installed.resolve() / profile["name"]
                installed = read_yaml(directory / "schema.yaml")
                validate_schema(installed, directory / "templates")
                require(installed == profile, f"{directory}: schema 已漂移，请重新生成")
                require(read_yaml(directory / "flow-policy.yaml") == policy,
                        f"{directory}: flow-policy 已漂移，请重新生成")
                for artifact in profile["artifacts"]:
                    template = directory / "templates" / artifact["template"]
                    require(template.read_text(encoding="utf-8") ==
                            render_template(artifact, tier, policy["tiers"][tier]),
                            f"{template}: 模板已漂移，请重新生成")
        print("  P3: 直改 + 相关验证，不创建 change")
        if args.installed:
            print("PASS: 已安装的三个档位与共享源码一致")
    except (ProfileError, OSError, yaml.YAMLError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
