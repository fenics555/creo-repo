# -*- coding: utf-8 -*-
"""Обновление путей ссылок Creo/SKILL_x.md -> Creo/<BRANCH>/SKILL_x.md после структуризации."""
import os

ROOT = r"D:\AI\repo\Creo"
BRANCH = {
    "SKILL_creoson_complete.md": "CREOSON", "SKILL_creoson_workflow.md": "CREOSON",
    "SKILL_creoson_sessions_workdirs.md": "CREOSON", "SKILL_creoson_rename_mechanism.md": "CREOSON",
    "SKILL_creoson_write_rules.md": "CREOSON", "SKILL_creoson_probe_method.md": "CREOSON",
    "SKILL_creoson_inbox_deepseek.md": "CREOSON", "SKILL_creo_commands.md": "CREOSON",
    "SKILL_copy_assembly_project.md": "COPY", "SKILL_copy_rename.md": "COPY",
    "SKILL_creo_company.md": "STANDARDS", "SKILL_company_config.md": "STANDARDS",
    "SKILL_naming_spec.md": "STANDARDS", "SKILL_drawings_eskd.md": "STANDARDS",
    "SKILL_creo_templates.md": "STANDARDS", "SKILL_parameters_guide.md": "STANDARDS",
    "SKILL_reference_limits.md": "STANDARDS", "SKILL_creo_cards.md": "STANDARDS",
    "SKILL_creo_relations.md": "RELATIONS", "SKILL_relations_constitution.md": "RELATIONS",
    "SKILL_relations_basics.md": "RELATIONS", "SKILL_relations_examples.md": "RELATIONS",
    "SKILL_curves_from_equation.md": "RELATIONS", "SKILL_curves_examples.md": "RELATIONS",
    "SKILL_spring_compression_generator.md": "RELATIONS", "SKILL_spring_tension_master.md": "RELATIONS",
    "SKILL_davydovka_creoson_map.md": "DAVYDOVKA",
    "SKILL_creojs_api.md": "API", "SKILL_creo_api_ecosystem.md": "API",
    "SKILL_creo_docs_map.md": "DOCS",
    "SKILL_creostart_fleet.md": "INFRA", "SKILL_object_creoson_tests-01_asm.md": "INFRA",
}
changed = 0
for dirpath, _, files in os.walk(ROOT):
    for fn in files:
        if not fn.endswith(".md"):
            continue
        p = os.path.join(dirpath, fn)
        s = open(p, encoding="utf-8").read()
        o = s
        for name, br in BRANCH.items():
            s = s.replace("Creo/" + name, "Creo/" + br + "/" + name)
            s = s.replace("Creo\\" + name, "Creo\\" + br + "\\" + name)
        if s != o:
            open(p, "w", encoding="utf-8").write(s)
            changed += 1
            print("updated", os.path.relpath(p, ROOT))
print("files changed:", changed)