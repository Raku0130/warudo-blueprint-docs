import pathlib, yaml, textwrap

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "nodes"

def md_escape(s: str) -> str:
    return s.replace('|', '\\|')

def render(node: dict) -> str:
    id = node.get("id","")
    name = node.get("name","")
    category = node.get("category","")
    since = node.get("since","")
    deprecated = node.get("deprecated", False)
    summary = node.get("summary","")
    description = node.get("description","")
    ports = node.get("ports", {})
    behavior = node.get("behavior", {})
    examples = node.get("examples", [])
    links = node.get("links", {})

    lines = []
    lines.append(f"# {name}")
    meta = [f"**ID**: `{id}`", f"**Category**: {category}"]
    if since: meta.append(f"**Since**: {since}")
    if deprecated: meta.append("**Deprecated**: true")
    lines.append("  |  ".join(meta))
    lines.append("")
    if summary: lines.append(summary + "\n")
    if description: lines.append(description + "\n")

    lines.append("## Ports\n")

    def list_flow(title, arr):
        lines.append(f"### {title}")
        if not arr:
            lines.append("- (none)")
        else:
            for p in arr:
                nm = p.get("name","")
                desc = p.get("description","")
                lines.append(f"- **{nm}** — {desc}")
        lines.append("")

    def table_data(title, arr):
        lines.append(f"### {title}")
        if not arr:
            lines.append("- (none)\n")
            return
        lines.append("| name | type | required | default | notes |")
        lines.append("|------|------|----------|---------|-------|")
        for p in arr:
            nm = p.get("name","")
            ty = p.get("type","")
            req = "yes" if p.get("required", False) else "no"
            default = p.get("default","")
            notes = p.get("description","")
            lines.append(f"| `{md_escape(nm)}` | `{md_escape(ty)}` | {req} | {md_escape(str(default))} | {md_escape(notes)} |")
        lines.append("")

    list_flow("Flow Inputs", ports.get("flow_inputs", []))
    list_flow("Flow Outputs", ports.get("flow_outputs", []))
    table_data("Data Inputs", ports.get("data_inputs", []))
    table_data("Data Outputs", ports.get("data_outputs", []))

    if behavior:
        lines.append("## Behavior")
        if "triggers" in behavior:
            lines.append("- **Triggers**:")
            for t in behavior["triggers"]:
                ttype = t.get("type","")
                cond = t.get("condition")
                lines.append(f"  - {ttype}" + (f" ({cond})" if cond else ""))
        if "notes" in behavior:
            lines.append("- **Notes**:")
            for n in behavior["notes"]:
                lines.append(f"  - {n}")
        lines.append("")

    if examples:
        lines.append("## Examples")
        for ex in examples:
            title = ex.get("title","Example")
            lines.append(f"### {title}")
            if ex.get("mermaid"):
                lines.append("```mermaid")
                lines.append(ex["mermaid"])
                lines.append("```")
            if ex.get("snippet"):
                lines.append("```yaml")
                lines.append(ex["snippet"])
                lines.append("```")
        lines.append("")

    if links:
        rel = links.get("related_nodes", [])
        refs = links.get("references", [])
        if rel or refs:
            lines.append("## Links")
            if rel:
                lines.append("- Related: " + ", ".join(f"`{r}`" for r in rel))
            for r in refs:
                label = r.get("label", r.get("url","link"))
                url = r.get("url","#")
                lines.append(f"- [{label}]({url})")
            lines.append("")

    return "\n".join(lines)

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for yml in (ROOT / "data" / "nodes").rglob("*.yaml"):
        node = yaml.safe_load(yml.read_text(encoding="utf-8"))
        cat = node.get("category","Uncategorized").replace(" ", "_")
        out_dir = OUT / cat
        out_dir.mkdir(parents=True, exist_ok=True)
        out_path = out_dir / f"{node.get('id','node')}.md"
        out_path.write_text(render(node), encoding="utf-8")
        print(f"[GEN] {out_path}")

if __name__ == "__main__":
    main()