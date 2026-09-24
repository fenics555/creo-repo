# -*- coding: utf-8 -*-
"""ПРИЁМКА «ЧЕРЕЗ ИИ»: вход в агент и вопрос по Creo (полный путь /ask).
Пароль берётся из файла дома login.json и НЕ печатается."""
import json, urllib.request, time

AG = "http://127.0.0.1:8765"


def post(path, body, token=None, timeout=600):
    h = {"Content-Type": "application/json"}
    if token:
        h["X-Token"] = token
    r = urllib.request.Request(AG + path, json.dumps(body).encode("utf-8"), h)
    return json.loads(urllib.request.urlopen(r, timeout=timeout).read().decode("utf-8"))


cred = json.load(open(r"D:\AI\tools\agent\login.json", encoding="utf-8"))
login = post("/login", {"login": cred.get("login"), "pw": cred.get("password")})
print("вход: логин=%s роль=%s токен=%s" % (login.get("login"), login.get("role"),
                                           "получен" if login.get("token") else "НЕТ"))
tok = login.get("token")
if not tok:
    print("ответ сервера:", {k: v for k, v in login.items() if k != "token"})
    raise SystemExit(1)

print("-" * 70)
try:
    r = post("/ask", {"q": "creo_status"}, tok, timeout=120)
    print("1) прямой вызов инструмента 'creo_status':")
    print("   ", str(r.get("answer")).replace("\n", " ")[:200])
except Exception as e:
    print("1) прямой вызов: ошибка", e)

print("-" * 70)
t0 = time.time()
try:
    r = post("/ask", {"q": "какие модели открыты в Creo?"}, tok, timeout=900)
    print("2) вопрос к модели (%.0f с):" % (time.time() - t0))
    print("   ОТВЕТ:", str(r.get("answer")).replace("\n", " ")[:500])
    print("   шаги:", r.get("steps"))
    print("   ход:", "; ".join(str(x) for x in (r.get("log") or []))[:400])
except Exception as e:
    print("2) вопрос модели: ошибка", e)
print("-" * 70)
print("ПРИЁМКА ИИ ЗАВЕРШЕНА")