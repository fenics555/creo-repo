# -*- coding: utf-8 -*-
"""Проба: читаем КОНФИГ ЖИВОЙ сессии Creo через CREOSON creo:get_config.
Отвечает на вопрос: загружен ли боевой config.pro (форматки, MY_ESKD.dtl, table.pnt)."""
import json, urllib.request

CREOSON = "http://127.0.0.1:8080/creoson"
KEYS = ["pro_format_dir", "format_setup_file", "drawing_setup_file", "pro_dtl_setup_dir",
        "pen_table_file", "pro_plot_config_dir", "pdf_use_pentable", "use_8_plotter_pens",
        "start_model_dir", "template_solidpart", "template_drawing", "template_designasm",
        "pro_symbol_dir", "pro_group_dir", "pro_material_dir", "pro_table_dir",
        "search_path", "search_path_file", "tolerance_standard", "plot_file_dir",
        "pro_library_dir", "pro_group_dir", "toolpath_mfg_mode", "pdf_export_mode_default"]


def post(o):
    r = urllib.request.Request(CREOSON, json.dumps(o).encode("utf-8"),
                               {"Content-Type": "application/json"})
    return json.loads(urllib.request.urlopen(r, timeout=60).read().decode("utf-8"))


sid = post({"command": "connection", "function": "connect", "data": {}}).get("sessionId")
print("session:", sid)
print("-" * 78)
for k in KEYS:
    try:
        r = post({"sessionId": sid, "command": "creo", "function": "get_config", "data": {"name": k}})
        st = r.get("status") or {}
        if st.get("error"):
            print("%-24s ОШИБКА: %s" % (k, st.get("message")))
        else:
            print("%-24s = %s" % (k, (r.get("data") or {}).get("values")))
    except Exception as e:
        print("%-24s сбой: %s" % (k, e))