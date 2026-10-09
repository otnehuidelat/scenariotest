# app.py — Сценарии жизни: ИЛИ + меланхолик
# Запуск: streamlit run app.py

import streamlit as st
import numpy as np
import pandas as pd
import altair as alt

st.set_page_config(layout="wide", page_title="Сценарии жизни")

# ============================================================
# ПРОФИЛЬ
# ============================================================
PROFILE = {
    "introversion": 0.85, "tempo": 0.30, "stress_resilience": 0.20,
    "need_guarantee": 0.85, "need_comfort": 0.85, "need_novelty": 0.75,
    "need_meaning": 0.80, "need_control": 0.70,
}

DOMAIN_WEIGHTS = {
    "relationships": 1.5, "health": 1.3, "meaning": 1.2,
    "career": 1.0, "creativity": 0.9, "social": 0.8, "finances": 0.7,
}
DOMAINS = ["career", "relationships", "social", "health",
           "creativity", "finances", "meaning", "stress", "energy"]
DOMAIN_LABELS = {
    "career": "Карьера", "relationships": "Отношения", "social": "Дружба",
    "health": "Тело", "creativity": "Творчество", "finances": "Финансы",
    "meaning": "Смысл", "stress": "Стресс", "energy": "Энергия",
}

# ============================================================
# ИСТОЧНИКИ СМЫСЛА (регулируемые)
# ============================================================
MEANING_SOURCES = {
    "career":        {"label": "Смысл от работы",       "default": 0.35},
    "relationships": {"label": "Смысл от близости",     "default": 0.30},
    "creativity":    {"label": "Смысл от творчества",   "default": 0.20},
    "growth":        {"label": "Смысл от роста",        "default": 0.15},
}

# ============================================================
# КАРЬЕРНЫЕ ПРЕСЕТЫ
# ============================================================
CAREERS = {
    "office_9_5": {"label": "Офис 9-5",
        "career": {"tempo": 0.5, "public_load": 0.4, "social_load": 0.6, "meaning": 0.4},
        "recovery": 0.4},
    "manager": {"label": "Руководитель",
        "career": {"tempo": 0.7, "public_load": 0.7, "social_load": 0.8, "meaning": 0.6},
        "recovery": 0.3},
    "freelance_burst": {"label": "Фриланс рывками",
        "career": {"tempo": 0.8, "public_load": 0.3, "social_load": 0.3, "meaning": 0.7},
        "recovery": 0.5},
    "creative_studio": {"label": "Творческая студия",
        "career": {"tempo": 0.4, "public_load": 0.3, "social_load": 0.4, "meaning": 0.9},
        "recovery": 0.6},
    "startup_chaos": {"label": "Стартап, хаос",
        "career": {"tempo": 0.9, "public_load": 0.6, "social_load": 0.7, "meaning": 0.8},
        "recovery": 0.2},
    "stable_corporate": {"label": "Стабильная корпорация",
        "career": {"tempo": 0.4, "public_load": 0.3, "social_load": 0.5, "meaning": 0.3},
        "recovery": 0.6},
    "crisis_consulting": {"label": "Кризис-консалтинг",
        "career": {"tempo": 0.9, "public_load": 0.5, "social_load": 0.6, "meaning": 0.8},
        "recovery": 0.3},
    "solo_expert": {"label": "Соло-эксперт",
        "career": {"tempo": 0.3, "public_load": 0.1, "social_load": 0.2, "meaning": 0.8},
        "recovery": 0.7},
    "custom": {"label": "Своя"},
}

# ============================================================
# ЛИЧНЫЕ ПРЕСЕТЫ
# ============================================================
PERSONAL_PRESETS = {
    "family_stable": {"label": "Семья, стабильность",
        "relationship_status": 0.9, "relationship_quality": 0.8,
        "close_friends": 0.6, "social_load": 0.5,
        "sleep": 0.7, "activity": 0.5, "chronic": 0.3,
        "creative_outlet": 0.5, "creative_time": 0.5,
        "fin_stability": 0.8, "fin_cushion": 0.7, "recovery": 0.6},
    "single_isolated": {"label": "Один, изоляция",
        "relationship_status": 0.1, "relationship_quality": 0.1,
        "close_friends": 0.2, "social_load": 0.2,
        "sleep": 0.4, "activity": 0.3, "chronic": 0.5,
        "creative_outlet": 0.3, "creative_time": 0.3,
        "fin_stability": 0.4, "fin_cushion": 0.2, "recovery": 0.3},
    "partner_no_friends": {"label": "Партнёр, без друзей",
        "relationship_status": 0.9, "relationship_quality": 0.7,
        "close_friends": 0.2, "social_load": 0.4,
        "sleep": 0.6, "activity": 0.4, "chronic": 0.3,
        "creative_outlet": 0.5, "creative_time": 0.4,
        "fin_stability": 0.7, "fin_cushion": 0.5, "recovery": 0.5},
    "single_active": {"label": "Один, но активный",
        "relationship_status": 0.2, "relationship_quality": 0.3,
        "close_friends": 0.7, "social_load": 0.5,
        "sleep": 0.6, "activity": 0.7, "chronic": 0.2,
        "creative_outlet": 0.8, "creative_time": 0.6,
        "fin_stability": 0.6, "fin_cushion": 0.5, "recovery": 0.6},
    "burnout_state": {"label": "Уже на грани",
        "relationship_status": 0.5, "relationship_quality": 0.4,
        "close_friends": 0.3, "social_load": 0.3,
        "sleep": 0.2, "activity": 0.2, "chronic": 0.7,
        "creative_outlet": 0.1, "creative_time": 0.1,
        "fin_stability": 0.5, "fin_cushion": 0.3, "recovery": 0.2},
    "custom": {"label": "Своя"},
}

# ============================================================
# ИНТЕРВЕНЦИИ — с шагами, сроками, чек-поинтами
# ============================================================
INTERVENTIONS = {
    "recovery": {
        "label": "Восстановление как приоритет",
        "why": "У меланхолика-ИЛИ истощение идёт в обвал, а не плавно. Без ресурса никакие решения не работают.",
        "when": "Стресс > 60 ИЛИ энергия < 40",
        "duration": "1–2 месяца",
        "steps": [
            "Сон 8+ часов, отбой до 23:00, без экранов за час",
            "Убрать 2–3 обязательства из календаря на этот период",
            "Телесный комфорт: тепло, мягкое, вкусное — как лекарство, не как роскошь",
            "1–2 часа тишины в день без людей и экранов",
            "Отменить все публичные задачи и конфликты",
        ],
        "checkpoint": "Через 3 недели: энергия > 50. Через 6 недель: стресс < 50.",
        "escalate": "Если через 6 недель не легче — не углублять отдых, а менять режим.",
        "effect": {"load": -15}, "recovery_bonus": 15,
    },
    "reduce_load": {
        "label": "Снизить социальную и публичную нагрузку",
        "why": "Интроверту с низкой стрессоустойчивостью публичность стоит 3–4× дороже, чем экстраверту.",
        "when": "public_load > 0.4 ИЛИ social_load > 0.6",
        "duration": "2–4 месяца",
        "steps": [
            "Перевести коммуникацию в письменную, где возможно",
            "Встречи — только 1-на-1, до 60 минут",
            "Убрать выступления, конференции, «нетворкинг»",
            "Найти 1–2 человека, кому можно делегировать контакты",
            "В календаре — пустые блоки после каждой встречи",
        ],
        "checkpoint": "Через месяц: стресс < 55. Через 2 месяца: смысл не падает.",
        "escalate": "Если стресс не падает — вопрос в роли, а не в нагрузке. Смотри role_shift.",
        "effect": {"load": -12}, "recovery_bonus": 5,
    },
    "burst": {
        "label": "Перейти на режим рывков",
        "why": "Равномерная загрузка убивает этот профиль. Работает: интенсив → длинная пауза.",
        "when": "tempo > 0.5 ИЛИ ощущение «постоянно на дне»",
        "duration": "3–6 месяцев",
        "steps": [
            "Один проект за раз, без параллельных задач",
            "Цикл: 2–3 недели интенсивно → 1 неделя полной паузы",
            "Между проектами — минимум 3 дня ничего не делать",
            "Планировать восстановление заранее, а не по факту падения",
            "Защищать паузы как рабочее время",
        ],
        "checkpoint": "Через 2 месяца: энергия в среднем > 55. Через 4: стресс < 50.",
        "escalate": "Если паузы не помогают — тело не восстанавливается. Нужен recovery сначала.",
        "effect": {"load": -5}, "recovery_bonus": 10,
    },
    "meaning": {
        "label": "Вернуть смысл",
        "why": "Без смысла этот профиль не может тянуть нагрузку. Это топливо, а не бонус.",
        "when": "meaning < 50 ИЛИ career.meaning < 0.5",
        "duration": "3–6 месяцев",
        "steps": [
            "Найти 1 проект, где виден результат и он тебе важен",
            "Визуальная мотивация: доска, картинки, конкретный образ цели",
            "Связать задачу со смыслом: «это делается для...»",
            "Убрать задачи, которые не приносят смысла — делегировать или отказаться",
            "Каждый день — 15 минут на то, что даёт ощущение «я живу, а не выживаю»",
        ],
        "checkpoint": "Через 6 недель: смысл > 55. Через 3 месяца: есть 1 проект, который тянет.",
        "escalate": "Если смысла нет ни в чём — это не про работу, а про депрессию. Нужен специалист.",
        "effect": {"meaning": 2}, "recovery_bonus": 0,
    },
    "relations": {
        "label": "Восстановить отношения",
        "why": "Для меланхолика одиночество бьёт сильнее, чем переработка. Близость — базовый ресурс.",
        "when": "relationships < 45 ИЛИ relationship_status < 0.4",
        "duration": "3–12 месяцев",
        "steps": [
            "Если партнёр есть — честный разговор о том, что не так",
            "Если партнёра нет — не «искать», а восстанавливать способность быть близко",
            "Психотерапия или работа с близким человеком",
            "Регулярные 1-на-1 встречи с теми, кто важен",
            "Убрать токсичное окружение, даже если «давно знакомы»",
        ],
        "checkpoint": "Через 3 месяца: relationships > 55. Через 6: есть человек, с кем можно быть настоящим.",
        "escalate": "Если близость разрушает — не входить в неё снова, а разбираться, что притягивает не тех.",
        "effect": {"load": -8, "meaning": 1}, "recovery_bonus": 8,
    },
    "creativity": {
        "label": "Вернуть творчество",
        "why": "Визуал-эмоциональный тип без выхода в творчество медленно угасает.",
        "when": "creativity < 40",
        "duration": "2–6 месяцев",
        "steps": [
            "Найти 1–2 часа в неделю только для своего дела",
            "Не для результата — для процесса",
            "Убрать перфекционизм: делать плохо, но делать",
            "Связать с чем-то визуальным: фото, видео, дизайн, текст",
            "Никому не показывать, пока не стабилизируется",
        ],
        "checkpoint": "Через месяц: creativity > 50. Через 3: смысл растёт.",
        "escalate": "Если творчество не идёт — сначала recovery.",
        "effect": {"meaning": 1}, "recovery_bonus": 4,
    },
    "role_shift": {
        "label": "Сменить роль или профессию",
        "why": "Если карьера фундаментально не подходит профилю, точечные правки не спасут.",
        "when": "career_mismatch > 0.5 ИЛИ спираль нисходящая после остальных мер",
        "duration": "6–18 месяцев",
        "steps": [
            "Определить, какие задачи убивают (публичность, скорость, конфликты)",
            "Найти роль, где этих задач мало, а сильных сторон — много",
            "Тест: 3 месяца на новой роли в мягком режиме",
            "Финансовая подушка на 6 месяцев до перехода",
            "Не уходить в никуда — уходить в конкретное",
        ],
        "checkpoint": "Через 6 месяцев: стресс < 50 без усилий. Через 12: смысл > 60.",
        "escalate": "Если и на новой роли плохо — проблема не в профессии, а в личной жизни или здоровье.",
        "effect": {"load": -20, "meaning": 2}, "recovery_bonus": 10,
    },
}

# ============================================================
# ФАЗЫ — негативные и позитивные
# ============================================================
NEGATIVE_PHASES = [
    {"range": (0, 6), "title": "🔴 Фаза 1: Накопление стресса",
     "signs": ["Раздражение по мелочам", "Плохой сон", "Прокрастинация",
               "«Просто дожить до выходных»"],
     "why": "Нагрузка копится быстрее, чем восстановление. Снаружи незаметно, в теле — уже видно.",
     "action": "Не «собраться». Снять нагрузку сейчас. Неделя отдыха здесь = месяц отсрочки выгорания."},
    {"range": (6, 18), "title": "🔴 Фаза 2: Срыв ритма",
     "signs": ["Эмоциональные качели", "Цинизм", "«Зачем всё это»",
               "Головные боли, ЖКТ, зажимы"],
     "why": "Стресс > 65 — включается нелинейный обвал. У меланхолика он резкий.",
     "action": "Сменить режим, не бороться с симптомами. Убрать публичность и скорость."},
    {"range": (18, 36), "title": "🔴 Фаза 3: Выгорание",
     "signs": ["Нет сил даже на любимое", "Апатия", "Отвращение к работе",
               "Психосоматика"],
     "why": "Энергия < 25 — психика режет всё, что не критично для выживания.",
     "action": "Только восстановление. Не новый проект, не смена работы, не рывок."},
    {"range": (36, 999), "title": "🔴 Фаза 4: Развилка",
     "signs": ["Либо хроническая депрессия", "Либо выход через смену режима"],
     "why": "Система либо перестраивается, либо ломается.",
     "action": "Смена профессии или режима. Экспертная, тихая, смысловая роль."},
]

POSITIVE_PHASES = [
    {"range": (0, 6), "title": "🟢 Фаза 1: Стабилизация",
     "signs": ["Сон нормализовался", "Стресс < 50", "Есть силы на простое",
               "Не раздражают обычные вещи"],
     "why": "Режим совместим с профилем. Тело перестаёт тратить ресурс на борьбу.",
     "action": "Не форсировать. Закрепить ритуалы сна, тишины, восстановления."},
    {"range": (6, 18), "title": "🟢 Фаза 2: Рост смысла",
     "signs": ["Смысл > 55", "Творчество растёт", "Отношения крепнут",
               "Появляется «зачем»"],
     "why": "Энергии хватает на смысл. Начинают работать положительные петли.",
     "action": "Расширять то, что работает. Не перегружать. Держать рывковый режим."},
    {"range": (18, 36), "title": "🟢 Фаза 3: Импульс",
     "signs": ["Карьера растёт без надрыва", "Есть накопления", "Своя среда",
               "Есть выбор"],
     "why": "Система вышла на плато и продолжает укрепляться. Восстановление опережает нагрузку.",
     "action": "Масштабировать аккуратно. Сохранять рывки. Не менять то, что работает."},
    {"range": (36, 999), "title": "🟢 Фаза 4: Зрелость",
     "signs": ["Стабильность без застоя", "Есть выбор", "Есть подушка",
               "Смысл устойчив"],
     "why": "Устойчивая конфигурация. Профиль работает на тебя, а не против.",
     "action": "Держать систему. Раз в год — ревизия: что тянет вниз, что усилить."},
]

# ============================================================
# ХЕЛПЕРЫ
# ============================================================
def clamp(x, lo=0.0, hi=100.0):
    return float(max(lo, min(hi, x)))


def career_mismatch(profile, career):
    t = abs(career.get("tempo", 0.5) - profile["tempo"])
    p = career.get("public_load", 0.5) * profile["introversion"]
    s = career.get("social_load", 0.5) * profile["introversion"] * 0.8
    m = max(0, profile["need_meaning"] - career.get("meaning", 0.5))
    return (t * 0.4 + p * 0.5 + s * 0.4 + m * 0.5) / 1.8


def compute_meaning(state, career_block, meaning_weights):
    """Смысл = взвешенная сумма 4 источников. Считается в каждом шаге."""
    src = {
        "career": career_block.get("meaning", 0.5) * 100,
        "relationships": state["relationships"],
        "creativity": state["creativity"],
        "growth": (state["career"] + state["energy"]) / 2,
    }
    total = sum(meaning_weights.values()) or 1.0
    m = sum(src[k] * meaning_weights[k] for k in src) / total
    return clamp(m, 0, 100)


def spiral_index(state):
    """Единый индекс 0–100: 'здоровье системы' в моменте."""
    num, den = 0.0, 0.0
    for d, w in DOMAIN_WEIGHTS.items():
        num += state.get(d, 0) * w
        den += w
    base = num / den
    stress_pen = max(0.0, state.get("stress", 50) - 50) * 0.5
    return clamp(base - stress_pen, 0, 100)


def domain_initial(profile, career_block, personal, meaning_weights):
    cm = career_mismatch(profile, career_block)
    rs, rq = personal["relationship_status"], personal["relationship_quality"]
    rel_health = rq * rs * 100
    if rs < 0.4:
        rel_health *= 0.5

    soc_health = personal["close_friends"] * 100 - personal["social_load"] * profile["introversion"] * 50
    hp_health = (personal["sleep"] * 0.5 + personal["activity"] * 0.3
                 + (1 - personal["chronic"]) * 0.4) * 100
    cre_health = (personal["creative_outlet"] * 0.6 + personal["creative_time"] * 0.4) * 100
    fin_health = (personal["fin_stability"] * 0.6 + personal["fin_cushion"] * 0.4) * 100

    stress = 25 + cm * 60
    state = {
        "career": clamp(100 - cm * 100, 5, 95),
        "relationships": clamp(rel_health, 5, 95),
        "social": clamp(max(10, min(100, soc_health)), 5, 95),
        "health": clamp(hp_health, 5, 95),
        "creativity": clamp(cre_health, 5, 95),
        "finances": clamp(fin_health, 5, 95),
        "stress": clamp(stress, 5, 95),
        "energy": clamp(100 - stress, 5, 95),
        "meaning": 0.0,
        "tenure": 0,
    }
    state["meaning"] = compute_meaning(state, career_block, meaning_weights)
    return state


def step(state, profile, career_block, personal, meaning_weights, active):
    tenure = state.get("tenure", 0)
    cm = career_mismatch(profile, career_block)
    fit = max(0.0, 1 - cm * 2)
    learning = min(1.0, tenure / 36)

    load = 30 - fit * 20 * learning + cm * 25

    meaning_bonus = (state["meaning"] / 100) * 12
    calm_bonus = max(0.0, (70 - state["stress"]) / 70) * 15
    rel_bonus = (state["relationships"] / 100) * 15
    health_bonus = (state["health"] / 100) * 10
    creative_bonus = (state["creativity"] / 100) * 8
    social_bonus = (state["social"] / 100) * 8

    recovery = 15 * personal["recovery"] + 15 + meaning_bonus + calm_bonus \
               + rel_bonus + health_bonus + creative_bonus + social_bonus

    if state["relationships"] < 30: load += 10
    if state["health"] < 30: load += 12
    if state["finances"] < 30: load += 8
    if state["social"] < 25: load += 6

    for key in active:
        iv = INTERVENTIONS[key]
        load += iv["effect"].get("load", 0)
        recovery += iv.get("recovery_bonus", 0)

    delta = load - recovery
    if state["stress"] > 70:
        delta *= 1.8
    state["stress"] = clamp(state["stress"] + delta * 0.1, 0, 100)
    state["energy"] = clamp(100 - state["stress"], 0, 100)

    # Отношения
    rel_delta = -max(0.0, state["stress"] - 55) * 0.1
    if state["energy"] < 30: rel_delta -= 0.5
    if "relations" in active: rel_delta += 0.5
    state["relationships"] = clamp(state["relationships"] + rel_delta, 0, 100)

    # Дружба
    if state["energy"] < 30:
        state["social"] = clamp(state["social"] - 0.3, 0, 100)
    else:
        state["social"] = clamp(state["social"] + 0.1, 0, 100)

    # Тело
    if state["stress"] > 60:
        state["health"] = clamp(state["health"] - 0.5, 0, 100)
    else:
        state["health"] = clamp(state["health"] + 0.2, 0, 100)

    # Творчество
    cre_boost = 0.5 if "creativity" in active else 0.0
    if state["meaning"] > 50 and state["energy"] > 40:
        state["creativity"] = clamp(state["creativity"] + 0.3 + cre_boost, 0, 100)
    else:
        state["creativity"] = clamp(state["creativity"] - 0.2 + cre_boost, 0, 100)

    # Финансы
    fin_flow = 0.3 if career_block.get("tempo", 0.5) < 0.6 else 0.1
    if state["stress"] > 70: fin_flow -= 0.2
    state["finances"] = clamp(state["finances"] + fin_flow, 0, 100)

    # Карьера
    if state["energy"] > 40 and state["meaning"] > 40:
        state["career"] = clamp(state["career"] + 0.2, 0, 100)
    else:
        state["career"] = clamp(state["career"] - 0.3, 0, 100)

    # Смысл — пересчитываем из источников
    base_meaning = compute_meaning(state, career_block, meaning_weights)
    # интервенция смысла даёт буст
    if "meaning" in active:
        base_meaning = clamp(base_meaning + 8, 0, 100)
    # сглаживание: смысл не прыгает мгновенно
    state["meaning"] = clamp(state["meaning"] * 0.85 + base_meaning * 0.15, 0, 100)

    state["tenure"] = tenure + 1
    return state


def simulate(profile, career_block, personal, meaning_weights, months,
             timeline=None, noise=0.05, runs=8):
    init = domain_initial(profile, career_block, personal, meaning_weights)
    all_runs = []
    for _ in range(runs):
        state = dict(init)
        hist = []
        for month in range(months):
            active = [k for (start, k) in (timeline or []) if month >= start]
            s = dict(state)
            s["stress"] += np.random.normal(0, noise * 10)
            state = step(s, profile, career_block, personal, meaning_weights, active)
            hist.append(dict(state, month=month))
            if state["energy"] < 5:
                break
        all_runs.append(hist)

    max_len = max(len(r) for r in all_runs)
    keys = DOMAINS + ["spiral"]
    out = {k: np.full(max_len, np.nan) for k in keys}
    for i in range(max_len):
        vals = {k: [] for k in keys}
        for r in all_runs:
            if i < len(r):
                for k in DOMAINS:
                    vals[k].append(r[i][k])
                vals["spiral"].append(spiral_index(r[i]))
        for k in keys:
            if vals[k]:
                out[k][i] = float(np.mean(vals[k]))
    return out


def detect_spiral(hist):
    if not hist or "spiral" not in hist:
        return "неизвестно"
    mask = ~np.isnan(hist["spiral"])
    n = int(mask.sum())
    if n < 12:
        return "неизвестно"
    x = np.arange(n)
    spiral_slope = float(np.polyfit(x, hist["spiral"][mask], 1)[0])

    slopes, finals = {}, {}
    for d in DOMAINS:
        if d not in hist:
            continue
        arr = hist[d][mask]
        slopes[d] = float(np.polyfit(x, arr, 1)[0])
        finals[d] = float(arr[-1])

    critical = (finals.get("health", 100) < 25 or
                finals.get("relationships", 100) < 25 or
                finals.get("meaning", 100) < 25)
    if critical:
        return "downward"

    falling = sum(1 for d in DOMAIN_WEIGHTS if slopes.get(d, 0) < -0.05)
    rising = sum(1 for d in DOMAIN_WEIGHTS if slopes.get(d, 0) > 0.05)

    if falling >= 3 or spiral_slope < -0.3:
        return "downward"
    if rising >= 4 and spiral_slope > 0.1:
        return "upward"
    if slopes.get("meaning", 0) > 0.05 and slopes.get("relationships", 0) > 0 and slopes.get("stress", 0) < 0.05:
        return "upward"
    return "plateau"


def get_phase(month, spiral_kind):
    phases = POSITIVE_PHASES if spiral_kind == "upward" else NEGATIVE_PHASES
    for p in phases:
        if p["range"][0] <= month < p["range"][1]:
            return p
    return phases[-1]


def build_plan(profile, career_block, personal, meaning_weights, init_state):
    """Собираем план по состоянию и слабым доменам. Возвращаем список
    словарей: {start_month, key, reason}."""
    cm = career_mismatch(profile, career_block)
    plan = []

    # 1. Восстановление — если стресс высокий или ресурс низкий
    if init_state["stress"] > 60 or init_state["energy"] < 40 or personal["recovery"] < 0.4:
        plan.append({"start": 0, "key": "recovery",
                     "reason": f"стартовый стресс {init_state['stress']:.0f}, энергия {init_state['energy']:.0f}"})

    # 2. Отношения — если слабые
    if init_state["relationships"] < 45 or personal["relationship_status"] < 0.4:
        plan.append({"start": 1, "key": "relations",
                     "reason": f"отношения {init_state['relationships']:.0f}"})

    # 3. Снижение нагрузки — если публичность или соц. нагрузка высокие
    if career_block.get("public_load", 0) > 0.4 or career_block.get("social_load", 0) > 0.6:
        plan.append({"start": 2, "key": "reduce_load",
                     "reason": "высокая публичная/социальная нагрузка"})

    # 4. Рывки — если темп высокий
    if career_block.get("tempo", 0.5) > 0.5:
        plan.append({"start": 3, "key": "burst",
                     "reason": "равномерный высокий темп"})

    # 5. Творчество — если задавлено
    if init_state["creativity"] < 40:
        plan.append({"start": 4, "key": "creativity",
                     "reason": f"творчество {init_state['creativity']:.0f}"})

    # 6. Смысл — если низкий
    if init_state["meaning"] < 50 or career_block.get("meaning", 0.5) < 0.5:
        plan.append({"start": 5, "key": "meaning",
                     "reason": f"смысл {init_state['meaning']:.0f}"})

    # 7. Смена роли — если карьера фундаментально не подходит
    if cm > 0.5:
        plan.append({"start": 6, "key": "role_shift",
                     "reason": f"career mismatch {cm:.2f}"})

    if not plan:
        plan.append({"start": 0, "key": "meaning", "reason": "поддерживающая мера"})
    return plan


def one_change_analysis(profile, career_block, personal, meaning_weights, months=60):
    baseline = simulate(profile, career_block, personal, meaning_weights, months)
    def last(arr):
        m = ~np.isnan(arr)
        return float(arr[m][-1]) if m.sum() else 0.0

    base = {"energy": last(baseline["energy"]), "meaning": last(baseline["meaning"]),
            "stress": last(baseline["stress"]), "relationships": last(baseline["relationships"])}

    results = []
    for key in INTERVENTIONS:
        hist = simulate(profile, career_block, personal, meaning_weights, months,
                        timeline=[(0, key)])
        f = {"energy": last(hist["energy"]), "meaning": last(hist["meaning"]),
             "stress": last(hist["stress"]), "relationships": last(hist["relationships"])}
        d = {k: f[k] - base[k] for k in base}
        results.append({
            "key": key, "label": INTERVENTIONS[key]["label"],
            "energy": f["energy"],
            "d_energy": d["energy"], "d_meaning": d["meaning"],
            "d_stress": d["stress"], "d_relationships": d["relationships"],
            "score": d["energy"] * 0.4 + d["meaning"] * 0.25
                     - d["stress"] * 0.2 + d["relationships"] * 0.15,
        })
    results.sort(key=lambda r: -r["score"])
    return results


def score_career(profile, career_block):
    return max(0.0, min(100.0, 100 - career_mismatch(profile, career_block) * 100))


def autoselect_careers(profile, top_n=3):
    scored = [(k, score_career(profile, d["career"]))
              for k, d in CAREERS.items() if k != "custom"]
    scored.sort(key=lambda x: -x[1])
    return scored[:top_n]


# ============================================================
# SESSION STATE
# ============================================================
for k, v in {"career_key": "manager", "personal_preset": "family_stable",
             "mw_career": 0.35, "mw_relationships": 0.30,
             "mw_creativity": 0.20, "mw_growth": 0.15}.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ============================================================
# UI
# ============================================================
st.title("Сценарии жизни: ИЛИ + меланхолик")
st.caption("Профиль фиксирован. Ввод карьеры и личной жизни. Смысл — настраиваемый. План — по слабым доменам.")

col_in, col_main = st.columns([1, 3])

with col_in:
    # ---------- Автоподбор ----------
    with st.expander("Автоподбор карьеры", expanded=False):
        for key, sc in autoselect_careers(PROFILE, 3):
            cc1, cc2 = st.columns([3, 2])
            cc1.markdown(f"**{CAREERS[key]['label']}**")
            cc2.markdown(f"`{sc:.0f}%`")
            if st.button("Применить", key=f"ap_{key}"):
                st.session_state["career_key"] = key
                st.rerun()

    # ---------- Карьера ----------
    st.subheader("Карьера")
    career_key = st.selectbox(
        "Режим работы", list(CAREERS.keys()),
        index=list(CAREERS.keys()).index(st.session_state["career_key"]),
        format_func=lambda k: CAREERS[k]["label"])
    st.session_state["career_key"] = career_key

    if career_key == "custom":
        career_block = {
            "tempo": st.slider("Темп", 0.0, 1.0, 0.5),
            "public_load": st.slider("Публичность", 0.0, 1.0, 0.3),
            "social_load": st.slider("Соц. нагрузка", 0.0, 1.0, 0.5),
            "meaning": st.slider("Смысл работы", 0.0, 1.0, 0.5),
        }
        career_recovery = st.slider("Восстановление от работы", 0.0, 1.0, 0.5)
    else:
        career_block = CAREERS[career_key]["career"]
        career_recovery = CAREERS[career_key]["recovery"]

    # ---------- Личная жизнь ----------
    st.subheader("Личная жизнь")
    preset_key = st.selectbox(
        "Профиль", list(PERSONAL_PRESETS.keys()),
        index=list(PERSONAL_PRESETS.keys()).index(st.session_state["personal_preset"]),
        format_func=lambda k: PERSONAL_PRESETS[k]["label"])
    st.session_state["personal_preset"] = preset_key
    base = {"relationship_status": 0.5, "relationship_quality": 0.5,
            "close_friends": 0.5, "social_load": 0.4, "sleep": 0.5,
            "activity": 0.5, "chronic": 0.3, "creative_outlet": 0.5,
            "creative_time": 0.5, "fin_stability": 0.6, "fin_cushion": 0.5,
            "recovery": 0.5}
    if preset_key != "custom":
        base = PERSONAL_PRESETS[preset_key]

    with st.expander("Отношения", expanded=True):
        rel_status = st.slider("Есть партнёр", 0.0, 1.0, float(base["relationship_status"]))
        rel_quality = st.slider("Качество отношений", 0.0, 1.0, float(base["relationship_quality"]))
    with st.expander("Дружба", expanded=False):
        close_friends = st.slider("Близкие друзья", 0.0, 1.0, float(base["close_friends"]))
        social_load = st.slider("Соц. нагрузка вне работы", 0.0, 1.0, float(base["social_load"]))
    with st.expander("Тело", expanded=False):
        sleep_q = st.slider("Сон", 0.0, 1.0, float(base["sleep"]))
        activity = st.slider("Активность", 0.0, 1.0, float(base["activity"]))
        chronic = st.slider("Хронические проблемы", 0.0, 1.0, float(base["chronic"]))
    with st.expander("Творчество", expanded=False):
        cre_outlet = st.slider("Есть выход", 0.0, 1.0, float(base["creative_outlet"]))
        cre_time = st.slider("Хватает времени", 0.0, 1.0, float(base["creative_time"]))
    with st.expander("Финансы", expanded=False):
        fin_stab = st.slider("Стабильность дохода", 0.0, 1.0, float(base["fin_stability"]))
        fin_cushion = st.slider("Подушка", 0.0, 1.0, float(base["fin_cushion"]))
    with st.expander("Восстановление", expanded=False):
        recovery_user = st.slider("Общее восстановление", 0.0, 1.0, float(base["recovery"]))

    personal = {
        "relationship_status": rel_status, "relationship_quality": rel_quality,
        "close_friends": close_friends, "social_load": social_load,
        "sleep": sleep_q, "activity": activity, "chronic": chronic,
        "creative_outlet": cre_outlet, "creative_time": cre_time,
        "fin_stability": fin_stab, "fin_cushion": fin_cushion,
        "recovery": (recovery_user + career_recovery) / 2,
    }

    # ---------- Смысл: настройка весов ----------
    with st.expander("Смысл — что его даёт (веса)", expanded=False):
        st.caption("Смысл = Σ (вес × источник). Источники: работа, близость, творчество, рост. "
                   "Веса нормализуются к 1 автоматически.")
        mw_career = st.slider("Смысл от работы", 0.0, 1.0, st.session_state["mw_career"])
        mw_rel = st.slider("Смысл от близости", 0.0, 1.0, st.session_state["mw_relationships"])
        mw_cre = st.slider("Смысл от творчества", 0.0, 1.0, st.session_state["mw_creativity"])
        mw_growth = st.slider("Смысл от роста", 0.0, 1.0, st.session_state["mw_growth"])
        st.session_state["mw_career"] = mw_career
        st.session_state["mw_relationships"] = mw_rel
        st.session_state["mw_creativity"] = mw_cre
        st.session_state["mw_growth"] = mw_growth

    meaning_weights = {
        "career": mw_career, "relationships": mw_rel,
        "creativity": mw_cre, "growth": mw_growth,
    }
    tot = sum(meaning_weights.values()) or 1.0
    meaning_weights = {k: v / tot for k, v in meaning_weights.items()}

    horizon = st.slider("Горизонт, лет", 2, 15, 8)

# ============================================================
# MAIN
# ============================================================
with col_main:
    months = horizon * 12
    init_state = domain_initial(PROFILE, career_block, personal, meaning_weights)
    hist_now = simulate(PROFILE, career_block, personal, meaning_weights, months)
    spiral_now = detect_spiral(hist_now)

    # ---------- Метрики ----------
    cm = career_mismatch(PROFILE, career_block)
    fit = max(0.0, min(100.0, 100 - cm * 100))
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Совместимость карьеры", f"{fit:.0f}%")
    c2.metric("Индекс спирали (старт)", f"{spiral_index(init_state):.0f}")
    c3.metric("Смысл (старт)", f"{init_state['meaning']:.0f}")
    c4.metric("Отношения (старт)", f"{init_state['relationships']:.0f}")

    # ---------- Формула смысла ----------
    with st.expander("Как считается смысл", expanded=False):
        st.markdown(
            f"**Смысл = "
            f"{meaning_weights['career']:.2f} × работа + "
            f"{meaning_weights['relationships']:.2f} × близость + "
            f"{meaning_weights['creativity']:.2f} × творчество + "
            f"{meaning_weights['growth']:.2f} × рост**"
        )
        st.caption("Источники:")
        st.markdown(f"- Работа: {career_block.get('meaning', 0.5)*100:.0f}")
        st.markdown(f"- Близость: {init_state['relationships']:.0f}")
        st.markdown(f"- Творчество: {init_state['creativity']:.0f}")
        st.markdown(f"- Рост: {(init_state['career'] + init_state['energy'])/2:.0f}")
        st.markdown(f"**Итог: {init_state['meaning']:.1f}**")

    # ---------- Спираль ----------
    st.subheader("Индекс спирали")
    df_spiral = pd.DataFrame({
        "Месяц": range(len(hist_now["spiral"])),
        "Индекс спирали": hist_now["spiral"],
    }).set_index("Месяц")
    st.line_chart(df_spiral, height=180)

    spiral_label = {"downward": "🔻 нисходящая", "upward": "🔺 восходящая",
                    "plateau": "➖ плато", "неизвестно": "❓"}[spiral_now]
    st.markdown(f"### Спираль: {spiral_label}")

    # ---------- Heatmap по доменам ----------
    st.subheader("Карта доменов во времени")
    st.caption("Каждая полоса — домен. Цвет: красный (умирает) → зелёный (здоров). "
               "Стресс инвертирован: зелёный = низкий.")

    step_m = max(1, months // 60)
    rows = []
    for i in range(0, len(hist_now["spiral"]), step_m):
        for d in DOMAIN_WEIGHTS:
            if i < len(hist_now[d]) and not np.isnan(hist_now[d][i]):
                val = hist_now[d][i]
                if d == "stress":
                    val = 100 - val
                rows.append({"Месяц": i, "Домен": DOMAIN_LABELS[d], "Значение": float(val)})
    df_heat = pd.DataFrame(rows)

    heat = alt.Chart(df_heat).mark_rect().encode(
        x=alt.X("Месяц:O", axis=alt.Axis(labelAngle=-45, title="Месяц")),
        y=alt.Y("Домен:N", sort=list(DOMAIN_LABELS.values()), title=""),
        color=alt.Color("Значение:Q",
                        scale=alt.Scale(scheme="redyellowgreen", domain=[0, 100]),
                        legend=alt.Legend(title="0 = плохо, 100 = хорошо")),
        tooltip=["Месяц", "Домен", "Значение"],
    ).properties(height=260)
    st.altair_chart(heat, use_container_width=True)

    # ---------- Разбор доменов ----------
    st.subheader("Разбор доменов (в конце горизонта)")
    last_vals = {}
    for d in DOMAINS:
        arr = hist_now[d]
        m = ~np.isnan(arr)
        last_vals[d] = float(arr[m][-1]) if m.sum() else 0.0

    dc1, dc2 = st.columns(2)
    with dc1:
        for d in ["relationships", "health", "meaning", "career"]:
            v = last_vals[d]
            emoji = "🔴" if v < 30 else ("🟡" if v < 55 else "🟢")
            st.markdown(f"{emoji} **{DOMAIN_LABELS[d]}** ({DOMAIN_WEIGHTS[d]}) — {v:.0f}")
    with dc2:
        for d in ["creativity", "social", "finances", "stress", "energy"]:
            v = last_vals[d]
            if d == "stress":
                emoji = "🟢" if v < 40 else ("🟡" if v < 65 else "🔴")
            else:
                emoji = "🔴" if v < 30 else ("🟡" if v < 55 else "🟢")
            st.markdown(f"{emoji} **{DOMAIN_LABELS[d]}** — {v:.0f}")

    # ---------- Фазы ----------
    st.subheader("Фазы сценария")
    st.caption("Показываются фазы в зависимости от типа спирали. "
               "Позитивные — если индекс растёт. Негативные — если падает.")

    phases_to_show = POSITIVE_PHASES if spiral_now == "upward" else NEGATIVE_PHASES
    current_phase = get_phase(len(df_spiral) - 1, spiral_now)
    for phase in phases_to_show:
        is_current = phase is current_phase
        end = phase["range"][1] if phase["range"][1] < 999 else "∞"
        title = f"{'▶ ' if is_current else ''}{phase['title']} ({phase['range'][0]}–{end} мес)"
        with st.expander(title, expanded=is_current):
            cA, cB = st.columns(2)
            with cA:
                st.markdown("**Признаки**")
                for s in phase["signs"]:
                    st.markdown(f"- {s}")
            with cB:
                st.markdown("**Почему так**")
                st.markdown(phase["why"])
            st.markdown("**Что делать**")
            st.info(phase["action"])

    # ---------- План ----------
    st.subheader("План выхода на восходящую петлю")
    st.caption("План строится по слабым доменам и стартовому состоянию. "
               "У каждой интервенции — срок, шаги, чек-поинт, эскалация.")

    plan = build_plan(PROFILE, career_block, personal, meaning_weights, init_state)

    # Таймлайн
    st.markdown("**Таймлайн**")
    tl_rows = []
    for p in plan:
        iv = INTERVENTIONS[p["key"]]
        tl_rows.append({
            "Когда": f"мес {p['start']}",
            "Что": iv["label"],
            "Срок": iv["duration"],
            "Почему сейчас": p["reason"],
        })
    st.dataframe(pd.DataFrame(tl_rows), use_container_width=True, hide_index=True)

    # Детали
    st.markdown("**Что делать конкретно**")
    for p in plan:
        iv = INTERVENTIONS[p["key"]]
        with st.expander(f"{iv['label']} · с месяца {p['start']} · {iv['duration']}", expanded=False):
            st.markdown(f"**Зачем:** {iv['why']}")
            st.markdown(f"**Когда применять:** {iv['when']}")
            st.markdown(f"**Почему у тебя:** {p['reason']}")
            st.markdown("**Шаги:**")
            for i, s in enumerate(iv["steps"], 1):
                st.markdown(f"{i}. {s}")
            st.markdown(f"**Чек-поинт:** {iv['checkpoint']}")
            st.markdown(f"**Если не помогло:** {iv['escalate']}")

    # ---------- Сравнение ----------
    plan_timeline = [(p["start"], p["key"]) for p in plan]
    hist_plan = simulate(PROFILE, career_block, personal, meaning_weights, months,
                         timeline=plan_timeline)
    spiral_plan = detect_spiral(hist_plan)

    st.subheader("Траектория: сейчас vs с планом")
    df_cmp = pd.DataFrame({
        "Месяц": range(len(hist_plan["spiral"])),
        "Спираль (сейчас)": hist_now["spiral"],
        "Спираль (с планом)": hist_plan["spiral"],
    }).set_index("Месяц")
    st.line_chart(df_cmp, height=200)

    # Смысл
    df_meaning = pd.DataFrame({
        "Месяц": range(len(hist_plan["meaning"])),
        "Смысл (сейчас)": hist_now["meaning"],
        "Смысл (с планом)": hist_plan["meaning"],
    }).set_index("Месяц")
    st.line_chart(df_meaning, height=180)

    # Отношения и здоровье
    df_rel = pd.DataFrame({
        "Месяц": range(len(hist_plan["relationships"])),
        "Отношения (сейчас)": hist_now["relationships"],
        "Отношения (с планом)": hist_plan["relationships"],
        "Тело (сейчас)": hist_now["health"],
        "Тело (с планом)": hist_plan["health"],
    }).set_index("Месяц")
    st.line_chart(df_rel, height=180)

    spiral_label2 = {"downward": "🔻", "upward": "🔺",
                     "plateau": "➖", "неизвестно": "❓"}[spiral_plan]
    st.markdown(f"### Спираль после плана: {spiral_label2} {spiral_plan}")

    if spiral_plan == "upward":
        st.success("План выводит на восходящую петлю. Идти по фазам, не менять всё сразу.")
    elif spiral_plan == "plateau":
        st.info("План стабилизирует, но не выводит в рост. Проверь домены выше — что-то осталось слабым.")
    elif spiral_plan == "downward":
        st.warning("Даже с планом спираль нисходящая. Нужна смена роли или работа с личной жизнью.")
    else:
        st.info("Недостаточно данных. Увеличь горизонт.")

    # ---------- Одно изменение ----------
    st.subheader("Что даёт одно изменение")
    st.caption("Считаем эффект каждой интервенции по отдельности. Только по кнопке — тяжёлый расчёт.")
    if st.button("Посчитать эффект каждого изменения"):
        with st.spinner("Считаю..."):
            results = one_change_analysis(PROFILE, career_block, personal,
                                          meaning_weights, months=min(months, 72))
        df_one = pd.DataFrame([{
            "Изменение": r["label"],
            "Энергия": f"{r['energy']:.0f}",
            "Δ Энергия": f"{r['d_energy']:+.1f}",
            "Δ Смысл": f"{r['d_meaning']:+.1f}",
            "Δ Отношения": f"{r['d_relationships']:+.1f}",
            "Δ Стресс": f"{r['d_stress']:+.1f}",
        } for r in results])
        st.dataframe(df_one, use_container_width=True, hide_index=True)
        best = results[0]
        st.success(
            f"**Максимальный эффект: {best['label']}**  \n"
            f"Одно это изменение даёт {best['d_energy']:+.1f} к энергии, "
            f"{best['d_meaning']:+.1f} к смыслу и "
            f"{best['d_relationships']:+.1f} к отношениям."
        )

st.divider()
st.caption("Не диагноз и не приговор. Вероятности, а не судьба.")
