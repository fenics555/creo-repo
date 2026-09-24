# -*- coding: utf-8 -*-
"""Генератор _INDEX.md по подразделам темы Creo."""
import os

ROOT = r"D:\AI\repo\Creo"
B = {
 "API": ("каналы API, pfc, creojs, otk, jlink, vbapi, weblink", [
   ("SKILL_creojs_api.md", "Creo.JS — родной API `pfc*`, карта по страницам руководства"),
   ("SKILL_creo_api_ecosystem.md", "экосистема API: один `pfc*` у Creo.JS/OTK/VB/Web.Link/JLINK/CREOSON")]),
 "DOCS": ("документация, справка, help, pdf", [
   ("SKILL_creo_docs_map.md", "карта документации: где хелпы/PDF/API-руководства в `D:\\PTC\\CREO12`")]),
 "CREOSON": ("creoson, сессии, переключение, rename, backup, пробы, команды", [
   ("SKILL_creoson_workflow.md", "полный цикл работы в CREOSON (подключение, папки/переключение, чтение/запись)"),
   ("SKILL_creoson_complete.md", "полная карта API CREOSON"),
   ("SKILL_creoson_sessions_workdirs.md", "сессии, старт Creo, рабочие директории"),
   ("SKILL_creo_commands.md", "быстрый подбор команды CREOSON"),
   ("SKILL_creoson_write_rules.md", "пишущие операции (backup, rename, копия)"),
   ("SKILL_creoson_rename_mechanism.md", "механизм переименования (onlysession → save)"),
   ("SKILL_creoson_probe_method.md", "методика безопасных проб"),
   ("SKILL_creoson_inbox_deepseek.md", "долги темы CREOSON")]),
 "COPY": ("копия, переименование, семейства, mfg, проект", [
   ("SKILL_copy_assembly_project.md", "умная копия проекта (сборка+детали+чертежи+спутники+семейства)"),
   ("SKILL_copy_rename.md", "методика копии/переименования моделей")]),
 "STANDARDS": ("стандарты КБ, имена, шаблоны, чертежи, параметры, карточки", [
   ("SKILL_creo_company.md", "паспорт компании: единицы, шаблоны, чертежи ЕСКД"),
   ("SKILL_company_config.md", "живые значения `config.pro`"),
   ("SKILL_naming_spec.md", "имена, шифры, обязательные параметры"),
   ("SKILL_drawings_eskd.md", "чертежи ЕСКД/ГОСТ"),
   ("SKILL_creo_templates.md", "канон-шаблоны моделей"),
   ("SKILL_parameters_guide.md", "параметры и массовые MP_"),
   ("SKILL_reference_limits.md", "лимиты и синтаксис"),
   ("SKILL_creo_cards.md", "карточки моделей, сырые близнецы")]),
 "RELATIONS": ("relations, уравнения, кривые, пружины", [
   ("SKILL_creo_relations.md", "справочник relations"),
   ("SKILL_relations_constitution.md", "конституция relations"),
   ("SKILL_relations_basics.md", "база relations"),
   ("SKILL_relations_examples.md", "примеры relations"),
   ("SKILL_curves_from_equation.md", "кривые из уравнения"),
   ("SKILL_curves_examples.md", "рецепты кривых"),
   ("SKILL_spring_compression_generator.md", "генератор пружины сжатия"),
   ("SKILL_spring_tension_master.md", "эталон пружины растяжения")]),
 "DAVYDOVKA": ("давыдовка, creojs-приложение, копия сборки, семейства", [
   ("SKILL_davydovka_creoson_map.md", "карта операций Давыдовка ↔ CREOSON")]),
 "INFRA": ("флот, старт машин, логи, объектные пробы", [
   ("SKILL_creostart_fleet.md", "флот КБ: старт машин, логи, трейлы, сеть"),
   ("SKILL_object_creoson_tests-01_asm.md", "объектные пробы CREOSON на сборках")]),
}
for br, (kw, items) in B.items():
    p = os.path.join(ROOT, br, "_INDEX.md")
    L = ["name: %s-index" % br.lower(), "system: Creo",
         "description: Use when: подраздел %s темы Creo — указатель на скиллы" % br,
         "when: creo, %s" % kw, "priority: medium", "",
         "# ПОДРАЗДЕЛ %s (тема Creo)" % br,
         "Вход темы — главный индекс: `..\\SKILL_creo_index.md`.", "", "Скиллы:"]
    for f, d in items:
        L.append("- `%s` — %s" % (f, d))
    open(p, "w", encoding="utf-8").write("\n".join(L) + "\n")
    print("wrote", br)
print("done")