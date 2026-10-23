# -*- coding: utf-8 -*-
"""window_meter.py — ТОЧНЫЙ ЗАМЕР ОКНА КОНТЕКСТА и положения ноги (без API, по логам Ollama).

Зачем: «схлопывание окна» — момент, когда Ollama начинает вытеснять старые токены и нога теряет
начало задачи. Владелец измерил своё окно: 202752 токена. Здесь — живой счётчик положения.

Что читает:
  1) `%LOCALAPPDATA%\\Ollama\\context-autofix.log` — сколько токенов ПРОПИСАНО (живая настройка);
  2) `%LOCALAPPDATA%\\Ollama\\server.log` — `n_tokens` слота: сколько токенов СЕЙЧАС в контексте,
     и записи `erased invalidated context checkpoint` — вытеснение (это и есть «плохой момент»).

Запуск: python window_meter.py
Итог: окно, занято токенов, % и вердикт по ЗДОРОВЬЮ ноги (по закону §1.7).
"""
import os
import re
import sys
from datetime import datetime

LOG_DIR = os.path.join(os.environ.get("LOCALAPPDATA", ""), "Ollama")
AUTOFIX = os.path.join(LOG_DIR, "context-autofix.log")
SERVER = os.path.join(LOG_DIR, "server.log")
# Порог «вытеснения» — взято из живой практики: Ollama чистит чекпойнты задолго до полного окна.
EVICT_TOKENS = 31000


def measure():
    out = {"window": 0, "settings_window": 0, "n_tokens": 0, "evictions": 0, "source": []}
    # 1) прописанное окно из лога авто-фикса настроек
    if os.path.isfile(AUTOFIX):
        try:
            with open(AUTOFIX, encoding="utf-8", errors="replace") as f:
                lines = f.read().splitlines()
            last = lines[-1] if lines else ""
            m = re.search(r"\((\d+)\|", last)
            if m:
                out["settings_window"] = int(m.group(1))
                out["source"].append("context-autofix.log: %s" % last.strip())
                out["window"] = out["settings_window"]
        except OSError:
            pass
    # 2) живое положение из лога сервера: последний n_tokens и число вытеснений
    if os.path.isfile(SERVER):
        try:
            with open(SERVER, encoding="utf-8", errors="replace") as f:
                tail = f.read()
            toks = re.findall(r"n_tokens = (\d+)", tail)
            if toks:
                out["n_tokens"] = max(int(t) for t in toks)
                out["source"].append("server.log: n_tokens = %d (макс. в файле)" % out["n_tokens"])
            ev = re.findall(r"erased invalidated context checkpoint", tail)
            out["evictions"] = len(ev)
            if ev:
                out["source"].append("server.log: вытеснений чекпойнта: %d" % out["evictions"])
        except OSError:
            pass
    return out


def verdict(w, n, ev):
    """Вердикт по ЗДОРОВЬЮ ноги (закон §1.7): % окна + факт вытеснения."""
    if not w:
        return "НЕТ ДАННЫХ: прописанное окно не найдено"
    pct = 100.0 * n / w if w else 0.0
    if ev and n >= EVICT_TOKENS:
        return "здоровье 2/5 — идут ВЫТЕСНЕНИЯ (%d), ногу на смену" % ev
    if pct >= 60:
        return "здоровье 3/5 — окно больше половины, длинное не читать"
    if pct >= 30:
        return "здоровье 4/5 — рабочая"
    return "здоровье 5/5 — свежая, полные чтения разрешены"


def main():
    m = measure()
    w, n, ev = m["window"], m["n_tokens"], m["evictions"]
    print("окно (прописано): %s токенов" % (w or "?"))
    print("занято сейчас   : %s токенов%s" % (n or "?", (" (%.1f%%)" % (100.0 * n / w) if w and n else "")))
    print("вытеснений      : %d  (порог внимания ~%d токенов)" % (ev, EVICT_TOKENS))
    for s in m["source"]:
        print("  источник:", s)
    print("ВЕРДИКТ:", verdict(w, n, ev))
    print("снято:", datetime.now().strftime("%d.%m.%Y %H:%M:%S"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
