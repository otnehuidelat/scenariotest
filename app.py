# app.py — Сценарии жизни: ИЛИ + меланхолик + визуал-эмоциональный
# Запуск: streamlit run app.py

import streamlit as st
import numpy as np
import pandas as pd

st.set_page_config(layout="wide", page_title="Сценарии жизни")

# ============================================================
# ПРОФИЛЬ (ядро)
# ============================================================
PROFILE = {
    "introversion": 0.85,
    "tempo": 0.30,
    "stress_resilience": 0.20,
    "need_guarantee": 0.85,
    "need_comfort": 0.85,
    "need_novelty": 0.75,
    "need_meaning": 0.80,
    "need_control": 0.70,
}

DOMAIN_WEIGHTS = {
    "relationships": 1.5,
    "health": 1.3,
    "meaning": 1.2,
    "career": 1.0,
    "creativity": 0.9,
    "social": 0.8,
    "finances": 0.7,
}

DOMAINS = ["career", "relationships", "social", "health",
           "creativity", "finances", "meaning", "stress", "energy"]

DOMAIN_LABELS = {
    "career": "Карьера",
    "relationships": "Отношения",
    "social": "Дружба",
    "health": "Тело",
    "creativity": "Творчество",
    "finances": "Финансы",
    "meaning": "Смысл",
    "stress": "Стресс",
    "energy": "Энергия",
}

# ============================================================
# ПРЕСЕТЫ КАРЬЕРЫ
# ============================================================
CAREERS = {
    "office_9_5": {
        "label": "Офис 9-5",
        "career": {"tempo": 0.5, "public_load": 0.4, "social_load": 0.6, "meaning": 0.4},
        "recovery": 0.4,
    },
    "manager": {
        "label": "Руководитель",
        "career": {"tempo": 0.7, "public_load": 0.7, "social_load": 0.8, "meaning": 0.6},
        "recovery": 0.3,
    },
    "freelance_burst": {
        "label": "Фриланс рывками",
        "career": {"tempo": 0.8, "public_load": 0.3, "social_load": 0.3, "meaning": 0.7},
        "recovery": 0.5,
    },
    "creative_studio": {
        "label": "Творческая студия",
        "career": {"tempo": 0.4, "public_load": 0.3, "social_load": 0.4, "meaning": 0.9},
        "recovery": 0.6,
    },
    "startup_chaos": {
        "label": "Стартап, хаос",
        "career": {"tempo": 0.9, "public_load": 0.6, "social_load": 0.7, "meaning": 0.8},
        "recovery": 0.2,
    },
    "stable_corporate": {
        "label": "Стабильная корпорация",
        "career": {"tempo": 0.4, "public_load": 0.3, "social_load": 0.5, "meaning": 0.3},
        "recovery": 0.6,
    },
    "crisis_consulting": {
        "label": "Кризис-консалтинг",
        "career": {"tempo": 0.9, "public_load": 0.5, "social_load": 0.6, "meaning": 0.8},
        "recovery": 0.3,
    },
    "solo_expert": {
        "label": "Соло-эксперт",
        "career": {"tempo": 0.3, "public_load": 0.1, "social_load": 0.2, "meaning": 0.8},
        "recovery": 0.7,
    },
    "custom": {"label": "Своя"},
}

# ============================================================
# ПРЕСЕТЫ ЛИЧНОЙ ЖИЗНИ
# ============================================================
PERSONAL_PRESETS = {
    "family_stable": {
        "label": "Семья, стабильность",
        "relationship_status": 0.9, "relationship_quality": 0.8,
        "close_friends": 0.6, "social_load": 0.5,
        "sleep": 0.7, "activity": 0.5, "chronic": 0.3,
        "creative_outlet": 0.5, "creative_time": 0.5,
        "fin_stability": 0.8, "fin_cushion": 0.7,
        "recovery": 0.6,
    },
    "single_isolated": {
        "label": "Один, изоляция",
        "relationship_status": 0.1, "relationship_quality": 0.1,
        "close_friends": 0.2, "social_load": 0.2,
        "sleep": 0.4, "activity": 0.3, "chronic": 0.5,
        "creative_outlet": 0.3, "creative_time": 0.3,
        "fin_stability": 0.4, "fin_cushion": 0.2,
        "recovery": 0.3,
    },
    "partner_no_friends": {
        "label": "Партнёр, но без друзей",
        "relationship_status": 0.9, "relationship_quality": 0.7,
        "close_friends": 0.2, "social_load": 0.4,
        "sleep": 0.6, "activity": 0.4, "chronic": 0.3,
        "creative_outlet": 0.5, "creative_time": 0.4,
        "fin_stability": 0.7, "fin_cushion": 0.5,
        "recovery": 0.5,
    },
    "single_active": {
        "label": "Один, но активный",
        "relationship_status": 0.2, "relationship_quality": 0.3,
        "close_friends": 0.7, "social_load": 0.5,
        "sleep": 0.6, "activity": 0.7, "chronic": 0.2,
        "creative_outlet": 0.8, "creative_time": 0.6,
        "fin_stability": 0.6, "fin_cushion": 0.5,
        "recovery": 0.6,
    },
    "burnout_state": {
        "label": "Уже на грани",
        "relationship_status": 0.5, "relationship_quality": 0.4,
        "close_friends": 0.3, "social_load": 0.3,
        "sleep": 0.2, "activity": 0.2, "chronic": 0.7,
        "creative_outlet": 0.1, "creative_time": 0.1,
        "fin_stability": 0.5, "fin_cushion": 0.3,
        "recovery": 0.2,
    },
    "custom": {"label": "Своя"},
}

# ============================================================
# ИНТЕРВЕНЦИИ
# ============================================================
INTERVENTIONS = {
    "recovery": {
        "label": "Восстановление как приоритет",
        "desc": "Сон, тишина, снять обязательства, телесный комфорт. 1–2 месяца только на это.",
        "effect": {"load": -15, "meaning": 0},
        "recovery_bonus": 15,
        "cost": "1–2 месяца",
    },
    "reduce_load": {
        "label": "Снизить социальную и публичную нагрузку",
        "desc": "Убрать выступления и конфликты. Письменная коммуникация, 1-на-1.",
        "effect": {"load": -12, "meaning": 0},
        "recovery_bonus": 5,
        "cost": "2–4 месяца",
    },
    "burst": {
        "label": "Перейти на режим рывков",
        "desc": "Один проект за раз. Интенсив → длинная пауза. Без равномерной загрузки.",
        "effect": {"load": -5, "meaning": 0},
        "recovery_bonus": 10,
        "cost": "3–6 месяцев",
    },
    "meaning": {
        "label": "Вернуть смысл",
        "desc": "Свой проект, визуальная мотивация, тема, в которую веришь.",
        "effect": {"load": 0, "meaning": 2},
        "recovery_bonus": 0,
        "cost": "3–6 месяцев",
    },
    "relations": {
        "label": "Восстановить отношения",
        "desc": "Терапия, честный разговор с партнёром, поиск близких, выход из изоляции.",
        "effect": {"load": -8, "meaning": 1},
        "recovery_bonus": 8,
        "cost": "3–12 месяцев",
    },
    "role_shift": {
        "label": "Сменить роль или профессию",
        "desc": "Уйти из публичной/менеджерской/скоростной роли в экспертную и тихую.",
        "effect": {"load": -20, "meaning": 2},
        "recovery_bonus": 10,
        "cost": "6–18 месяцев",
    },
}

# ============================================================
# ФАЗЫ
# ============================================================
PHASES = [
    {
        "range": (0, 6),
        "title": "Фаза 1: Накопление стресса",
        "signs": [
            "Раздражение по мелочам",
            "Плохой сон, трудно вставать",
            "Прокрастинация на лёгких задачах",
            "«Просто дожить до выходных»",
        ],
        "why": "Меланхолик-ИЛИ накапливает нагрузку быстрее, чем восстанавливается. Снаружи незаметно, в теле — уже видно.",
        "action": "Не «собраться». Снять нагрузку сейчас. Неделя отдыха в этой фазе = месяц отсрочки выгорания.",
    },
    {
        "range": (6, 18),
        "title": "Фаза 2: Срыв ритма",
        "signs": [
            "Эмоциональные качели",
            "Цинизм к работе и людям",
            "«Зачем всё это»",
            "Головные боли, ЖКТ, зажимы",
        ],
        "why": "Стресс перешёл порог 65 — включается нелинейный обвал. У меланхолика он резкий.",
        "action": "Сменить режим, не бороться с симптомами. Убрать публичность, конфликты, скорость.",
    },
    {
        "range": (18, 36),
        "title": "Фаза 3: Выгорание",
        "signs": [
            "Нет сил даже на то, что нравилось",
            "Апатия",
            "Отвращение к профессии",
            "Психосоматика",
        ],
        "why": "Энергия ниже 25 — психика режет всё, что не критично для выживания.",
        "action": "Только восстановление. Не новый проект, не смена работы, не рывок.",
    },
    {
        "range": (36, 999),
        "title": "Фаза 4: Развилка",
        "signs": [
            "Либо хроническая депрессия и телесные болезни",
            "Либо выход через смену роли и режима",
        ],
        "why": "Система либо перестраивается, либо ломается. Середины нет.",
        "action": "Смена профессии или режима. Экспертная, тихая, смысловая роль. Рывки. Комфорт.",
    },
]

# ============================================================
# ХЕЛПЕРЫ
# ============================================================
def clamp(x, lo=0.0, hi=100.0):
    return float(max(lo, min(hi, x)))


def career_mismatch(profile, career):
    """Насколько карьерный блок не подходит профилю (0..1)."""
    t = abs(career.get("tempo", 0.5) - profile["tempo"])
    p = career.get("public_load", 0.5) * profile["introversion"]
    s = career.get("social_load", 0.5) * profile["introversion"] * 0.8
    m = max(0, profile["need_meaning"] - career.get("meaning", 0.5))
    return (t * 0.4 + p * 0.5 + s * 0.4 + m * 0.5) / 1.8


def domain_initial(profile, career_block, personal):
    cm = career_mismatch(profile, career_block)

    # Отношения
    rs = personal["relationship_status"]
    rq = personal["relationship_quality"]
    rel_health = rq * rs * 100
    if rs < 0.4:
        rel_health *= 0.5  # одиночество жёстко бьёт

    # Дружба
    cf = personal["close_friends"]
    sl = personal["social_load"]
    soc_health = cf * 100 - sl * profile["introversion"] * 50
    soc_health = max(10.0, min(100.0, soc_health))

    # Тело
    slp = personal["sleep"]
    act = personal["activity"]
    ch = personal["chronic"]
    hp_health = (slp * 0.5 + act * 0.3 + (1 - ch) * 0.4) * 100

    # Творчество
    co = personal["creative_outlet"]
    ct = personal["creative_time"]
    cre_health = (co * 0.6 + ct * 0.4) * 100

    # Финансы
    fs = personal["fin_stability"]
    fc = personal["fin_cushion"]
    fin_health = (fs * 0.6 + fc * 0.4) * 100

    # Смысл
    meaning = career_block.get("meaning", 0.5) * 100 * (0.4 + profile["need_meaning"] * 0.6)
    meaning -= cm * 40

    # Стресс стартовый
    stress = 25 + cm * 60
    energy = 100 - stress

    return {
        "career": clamp(100 - cm * 100, 5, 95),
        "relationships": clamp(rel_health, 5, 95),
        "social": clamp(soc_health, 5, 95),
        "health": clamp(hp_health, 5, 95),
        "creativity": clamp(cre_health, 5, 95),
        "finances": clamp(fin_health, 5, 95),
        "meaning": clamp(meaning, 5, 95),
        "stress": clamp(stress, 5, 95),
        "energy": clamp(energy, 5, 95),
        "tenure": 0,
    }


def step(state, profile, career_block, personal, active):
    tenure = state.get("tenure", 0)
    cm = career_mismatch(profile, career_block)
    fit = max(0.0, 1 - cm * 2)
    learning = min(1.0, tenure / 36)

    # Нагрузка
    load = 30 - fit * 20 * learning + cm * 25

    # Положительные петли
    meaning_bonus = (state["meaning"] / 100) * 12
    calm_bonus = max(0.0, (70 - state["stress"]) / 70) * 15
    rel_bonus = (state["relationships"] / 100) * 15
    health_bonus = (state["health"] / 100) * 10
    creative_bonus = (state["creativity"] / 100) * 8
    social_bonus = (state["social"] / 100) * 8

    recovery = 15 * personal["recovery"] + 15 + meaning_bonus + calm_bonus \
               + rel_bonus + health_bonus + creative_bonus + social_bonus

    # Отрицательные петли
    if state["relationships"] < 30:
        load += 10
    if state["health"] < 30:
        load += 12
    if state["finances"] < 30:
        load += 8
    if state["social"] < 25:
        load += 6

    # Интервенции
    meaning_gain = career_block.get("meaning", 0.5) * 3
    for key in active:
        iv = INTERVENTIONS[key]
        load += iv["effect"].get("load", 0)
        recovery += iv.get("recovery_bonus", 0)
        meaning_gain += iv["effect"].get("meaning", 0)

    # Стресс / энергия
    delta = load - recovery
    if state["stress"] > 70:
        delta *= 1.8
    state["stress"] = clamp(state["stress"] + delta * 0.1, 0, 100)
    state["energy"] = clamp(100 - state["stress"], 0, 100)

    # Смысл
    state["meaning"] = clamp(state["meaning"] + meaning_gain * 0.3 - 0.8, 0, 100)

    # Отношения
    rel_delta = -max(0.0, state["stress"] - 55) * 0.1
    if state["energy"] < 30:
        rel_delta -= 0.5
    if "relations" in active:
        rel_delta += 0.4
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
    if state["meaning"] > 50 and state["energy"] > 40:
        state["creativity"] = clamp(state["creativity"] + 0.3, 0, 100)
    else:
        state["creativity"] = clamp(state["creativity"] - 0.2, 0, 100)

    # Финансы
    fin_flow = 0.3 if career_block.get("tempo", 0.5) < 0.6 else 0.1
    if state["stress"] > 70:
        fin_flow -= 0.2
    state["finances"] = clamp(state["finances"] + fin_flow, 0, 100)

    # Карьера
    if state["energy"] > 40 and state["meaning"] > 40:
        state["career"] = clamp(state["career"] + 0.2, 0, 100)
    else:
        state["career"] = clamp(state["career"] - 0.3, 0, 100)

    state["tenure"] = tenure + 1
    return state


def simulate(profile, career_block, personal, months, timeline=None,
             noise=0.05, runs=8):
    init = domain_initial(profile, career_block, personal)
    all_runs = []
    for _ in range(runs):
        state = dict(init)
        hist = []
        for month in range(months):
            active = [k for (start, k) in (timeline or []) if month >= start]
            s = dict(state)
            s["stress"] += np.random.normal(0, noise * 10)
            state = step(s, profile, career_block, personal, active)
            hist.append(dict(state, month=month))
            if state["energy"] < 5:
                break
        all_runs.append(hist)

    max_len = max(len(r) for r in all_runs)
    out = {k: np.full(max_len, np.nan) for k in DOMAINS}
    for i in range(max_len):
        vals = {k: [] for k in DOMAINS}
        for r in all_runs:
            if i < len(r):
                for k in DOMAINS:
                    vals[k].append(r[i][k])
        for k in DOMAINS:
            if vals[k]:
                out[k][i] = float(np.mean(vals[k]))
    return out


def detect_spiral(hist):
    if not hist or "energy" not in hist or len(hist["energy"]) < 12:
        return "неизвестно"

    mask = ~np.isnan(hist["energy"])
    n = int(mask.sum())
    if n < 12:
        return "неизвестно"

    x = np.arange(n)
    slopes, finals = {}, {}
    for d in DOMAINS:
        if d not in hist:
            continue
        arr = hist[d][mask]
        slopes[d] = float(np.polyfit(x, arr, 1)[0])
        finals[d] = float(arr[-1])

    critical_fail = (
        finals.get("health", 100) < 25 or
        finals.get("relationships", 100) < 25 or
        finals.get("meaning", 100) < 25
    )

    weighted = 0.0
    rising = 0
    falling = 0
    for d, w in DOMAIN_WEIGHTS.items():
        if d not in slopes:
            continue
        s = slopes[d]
        weighted += s * w
        if s > 0.05:
            rising += 1
        elif s < -0.05:
            falling += 1

    weighted -= slopes.get("stress", 0) * 1.0

    if critical_fail:
        return "downward"
    if falling >= 3 or weighted < -0.3:
        return "downward"
    if rising >= 4 and weighted > 0.1:
        return "upward"
    if (slopes.get("meaning", 0) > 0.05 and
        slopes.get("relationships", 0) > 0 and
        slopes.get("stress", 0) < 0.05):
        return "upward"
    return "plateau"


def get_phase(month):
    for p in PHASES:
        if p["range"][0] <= month < p["range"][1]:
            return p
    return PHASES[-1]


def recommend_plan(profile, career_block, personal):
    cm = career_mismatch(profile, career_block)
    rel_weak = personal["relationship_status"] < 0.4 or personal["relationship_quality"] < 0.4
    recovery_weak = personal["recovery"] < 0.4

    plan = []
    if recovery_weak:
        plan.append((0, "recovery"))
    if rel_weak:
        plan.append((1, "relations"))
    if cm > 0.5:
        plan += [(2, "reduce_load"), (4, "burst"), (6, "meaning"), (9, "role_shift")]
    elif cm > 0.3:
        plan += [(2, "burst"), (4, "meaning")]
    else:
        plan.append((2, "meaning"))
    return plan if plan else [(0, "meaning")]


def one_change_analysis(profile, career_block, personal, months=60):
    baseline = simulate(profile, career_block, personal, months)

    def last(arr):
        m = ~np.isnan(arr)
        return float(arr[m][-1]) if m.sum() else 0.0

    base_final = {
        "energy": last(baseline["energy"]),
        "meaning": last(baseline["meaning"]),
        "stress": last(baseline["stress"]),
        "relationships": last(baseline["relationships"]),
    }

    results = []
    for key in INTERVENTIONS:
        hist = simulate(profile, career_block, personal, months, timeline=[(0, key)])
        final = {
            "energy": last(hist["energy"]),
            "meaning": last(hist["meaning"]),
            "stress": last(hist["stress"]),
            "relationships": last(hist["relationships"]),
        }
        d_e = final["energy"] - base_final["energy"]
        d_m = final["meaning"] - base_final["meaning"]
        d_s = final["stress"] - base_final["stress"]
        d_r = final["relationships"] - base_final["relationships"]
        results.append({
            "key": key,
            "label": INTERVENTIONS[key]["label"],
            "energy": final["energy"],
            "d_energy": d_e,
            "d_meaning": d_m,
            "d_stress": d_s,
            "d_relationships": d_r,
            "score": d_e * 0.4 + d_m * 0.25 - d_s * 0.2 + d_r * 0.15,
        })
    results.sort(key=lambda r: -r["score"])
    return results


def score_career(profile, career_block):
    cm = career_mismatch(profile, career_block)
    return max(0.0, min(100.0, 100 - cm * 100))


def autoselect_careers(profile, top_n=3):
    scored = []
    for key, data in CAREERS.items():
        if key == "custom":
            continue
        scored.append((key, score_career(profile, data["career"])))
    scored.sort(key=lambda x: -x[1])
    return scored[:top_n]


# ============================================================
# SESSION STATE
# ============================================================
DEFAULTS = {
    "career_key": "manager",
    "personal_preset": "family_stable",
}
for k, v in DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ============================================================
# UI
# ============================================================
st.title("Сценарии жизни: ИЛИ + меланхолик + визуал-эмоциональный")
st.caption("Профиль фиксирован. Карьера и личная жизнь — вводятся. Прогноз — по доменам.")

col_in, col_main = st.columns([1, 3])

with col_in:
    # -------------------- КАРЬЕРА --------------------
    st.subheader("Карьера")

    with st.expander("Автоподбор под профиль", expanded=False):
        top = autoselect_careers(PROFILE, top_n=3)
        for key, score in top:
            label = CAREERS[key]["label"]
            cc1, cc2 = st.columns([3, 2])
            with cc1:
                st.markdown(f"**{label}**")
            with cc2:
                st.markdown(f"`{score:.0f}%`")
            if st.button("Применить", key=f"apply_career_{key}"):
                st.session_state["career_key"] = key
                st.rerun()

    career_key = st.selectbox(
        "Режим работы",
        list(CAREERS.keys()),
        index=list(CAREERS.keys()).index(st.session_state["career_key"]),
        format_func=lambda k: CAREERS[k]["label"],
    )
    st.session_state["career_key"] = career_key

    if career_key == "custom":
        c_tempo = st.slider("Темп", 0.0, 1.0, 0.5)
        c_public = st.slider("Публичность", 0.0, 1.0, 0.3)
        c_social = st.slider("Соц. нагрузка", 0.0, 1.0, 0.5)
        c_meaning = st.slider("Смысл работы", 0.0, 1.0, 0.5)
        career_block = {"tempo": c_tempo, "public_load": c_public,
                        "social_load": c_social, "meaning": c_meaning}
        career_recovery = st.slider("Восстановление от работы", 0.0, 1.0, 0.5)
    else:
        career_block = CAREERS[career_key]["career"]
        career_recovery = CAREERS[career_key]["recovery"]

    # -------------------- ЛИЧНАЯ ЖИЗНЬ --------------------
    st.subheader("Личная жизнь")

    preset_key = st.selectbox(
        "Быстрый профиль",
        list(PERSONAL_PRESETS.keys()),
        index=list(PERSONAL_PRESETS.keys()).index(st.session_state["personal_preset"]),
        format_func=lambda k: PERSONAL_PRESETS[k]["label"],
    )
    st.session_state["personal_preset"] = preset_key

    if preset_key == "custom":
        base = {
            "relationship_status": 0.5, "relationship_quality": 0.5,
            "close_friends": 0.5, "social_load": 0.4,
            "sleep": 0.5, "activity": 0.5, "chronic": 0.3,
            "creative_outlet": 0.5, "creative_time": 0.5,
            "fin_stability": 0.6, "fin_cushion": 0.5,
            "recovery": 0.5,
        }
    else:
        base = PERSONAL_PRESETS[preset_key]

    with st.expander("Отношения", expanded=True):
        rel_status = st.slider("Есть партнёр", 0.0, 1.0,
                               float(base["relationship_status"]),
                               help="0 — нет, 1 — стабильные отношения")
        rel_quality = st.slider("Качество отношений", 0.0, 1.0,
                                float(base["relationship_quality"]))

    with st.expander("Дружба", expanded=False):
        close_friends = st.slider("Близкие друзья", 0.0, 1.0,
                                  float(base["close_friends"]),
                                  help="0 — никого, 1 — 2–3 близких")
        social_load = st.slider("Соц. нагрузка вне работы", 0.0, 1.0,
                                float(base["social_load"]))

    with st.expander("Тело", expanded=False):
        sleep_q = st.slider("Сон", 0.0, 1.0, float(base["sleep"]))
        activity = st.slider("Активность", 0.0, 1.0, float(base["activity"]))
        chronic = st.slider("Хронические проблемы", 0.0, 1.0,
                            float(base["chronic"]))

    with st.expander("Творчество", expanded=False):
        cre_outlet = st.slider("Есть выход", 0.0, 1.0,
                               float(base["creative_outlet"]))
        cre_time = st.slider("Хватает времени", 0.0, 1.0,
                             float(base["creative_time"]))

    with st.expander("Финансы", expanded=False):
        fin_stab = st.slider("Стабильность дохода", 0.0, 1.0,
                             float(base["fin_stability"]))
        fin_cushion = st.slider("Подушка", 0.0, 1.0,
                                float(base["fin_cushion"]))

    with st.expander("Восстановление", expanded=False):
        recovery_user = st.slider("Общее восстановление", 0.0, 1.0,
                                  float(base["recovery"]))

    personal = {
        "relationship_status": rel_status,
        "relationship_quality": rel_quality,
        "close_friends": close_friends,
        "social_load": social_load,
        "sleep": sleep_q,
        "activity": activity,
        "chronic": chronic,
        "creative_outlet": cre_outlet,
        "creative_time": cre_time,
        "fin_stability": fin_stab,
        "fin_cushion": fin_cushion,
        "recovery": (recovery_user + career_recovery) / 2,
    }

    horizon = st.slider("Горизонт, лет", 2, 15, 8)

# ============================================================
# MAIN
# ============================================================
with col_main:
    months = horizon * 12
    hist_now = simulate(PROFILE, career_block, personal, months)
    spiral_now = detect_spiral(hist_now)

    # --- Метрики ---
    cm = career_mismatch(PROFILE, career_block)
    fit = max(0.0, min(100.0, 100 - cm * 100))
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Совместимость карьеры", f"{fit:.0f}%")
    with c2:
        m0 = hist_now["meaning"][0]
        st.metric("Смысл (старт)", f"{m0:.0f}")
    with c3:
        r0 = hist_now["relationships"][0]
        st.metric("Отношения (старт)", f"{r0:.0f}")

    # --- Прогноз ---
    df_now = pd.DataFrame({"Месяц": range(len(hist_now["energy"]))})
    for d in DOMAINS:
        df_now[DOMAIN_LABELS[d]] = hist_now[d]
    df_now = df_now.set_index("Месяц")

    st.subheader("Прогноз без изменений — все домены")
    st.line_chart(df_now)

    spiral_label = {"downward": "🔻 нисходящая", "upward": "🔺 восходящая",
                    "plateau": "➖ плато", "неизвестно": "❓"}[spiral_now]
    st.markdown(f"### Спираль: {spiral_label}")

    if spiral_now == "downward":
        st.error("Режим ведёт в нисходящую петлю. Смотри, какие домены падают.")
    elif spiral_now == "upward":
        st.success("Режим устойчив и выводит на восходящую петлю.")
    else:
        st.warning("Плато. Не рушится, но и не растёт.")

    # --- Доменный разбор ---
    st.subheader("Разбор доменов")
    last_vals = {}
    for d in DOMAINS:
        arr = hist_now[d]
        mask = ~np.isnan(arr)
        last_vals[d] = float(arr[mask][-1]) if mask.sum() else 0.0

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

    # --- Фазы ---
    st.subheader("Карточки фаз")
    current_phase = get_phase(len(df_now) - 1)
    for phase in PHASES:
        is_current = phase is current_phase
        end = phase["range"][1] if phase["range"][1] < 999 else "∞"
        title = f"{'🔴 ' if is_current else ''}{phase['title']} ({phase['range'][0]}–{end} мес)"
        with st.expander(title, expanded=is_current):
            cA, cB = st.columns(2)
            with cA:
                st.markdown("**Ранние признаки**")
                for s in phase["signs"]:
                    st.markdown(f"- {s}")
            with cB:
                st.markdown("**Почему так**")
                st.markdown(phase["why"])
            st.markdown("**Что делать**")
            st.info(phase["action"])

    # --- План выхода ---
    st.subheader("План выхода на восходящую петлю")
    plan = recommend_plan(PROFILE, career_block, personal)
    for start, key in plan:
        iv = INTERVENTIONS[key]
        st.markdown(f"**{iv['label']}** · через {start} мес · {iv['cost']}")
        st.caption(iv["desc"])

    hist_plan = simulate(PROFILE, career_block, personal, months, timeline=plan)
    spiral_plan = detect_spiral(hist_plan)

    df_cmp = pd.DataFrame({"Месяц": range(len(hist_plan["energy"]))})
    for d in ["energy", "meaning", "relationships", "stress", "career"]:
        df_cmp[f"{DOMAIN_LABELS[d]} (сейчас)"] = hist_now[d]
        df_cmp[f"{DOMAIN_LABELS[d]} (с планом)"] = hist_plan[d]
    df_cmp = df_cmp.set_index("Месяц")

    st.line_chart(df_cmp)

    spiral_label2 = {"downward": "🔻", "upward": "🔺",
                     "plateau": "➖", "неизвестно": "❓"}[spiral_plan]
    st.markdown(f"### Спираль после плана: {spiral_label2} {spiral_plan}")

    if spiral_plan == "upward":
        st.success("План выводит на восходящую петлю. Идти по фазам, не менять всё сразу.")
    elif spiral_plan == "plateau":
        st.info("План стабилизирует, но не выводит в рост. Возможно, нужна смена роли или работа с отношениями.")
    elif spiral_plan == "downward":
        st.warning("Даже с планом спираль нисходящая. Режим фундаментально несовместим — нужна смена профессии или серьёзная работа с личной жизнью.")
    else:
        st.info("Недостаточно данных, чтобы понять динамику. Увеличь горизонт.")

    # --- Одно изменение ---
    st.subheader("Что даёт одно изменение")
    st.caption("Считаем эффект каждой интервенции по отдельности. Только по кнопке — тяжёлый расчёт.")

    if st.button("Посчитать эффект каждого изменения"):
        with st.spinner("Считаю..."):
            results = one_change_analysis(PROFILE, career_block, personal,
                                          months=min(months, 72))

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
            f"{best['d_relationships']:+.1f} к отношениям. "
            f"Начни с этого — не пытайся менять всё сразу."
        )

st.divider()
st.caption(
    "Это не диагноз и не приговор. Вероятности, а не судьба. "
    "Тип компенсируется средой, ролью, партнёром и инструментами."
)

st.divider()
st.caption("Это не диагноз и не приговор. Вероятности, а не судьба. "
           "Тип компенсируется средой, ролью, партнёром и инструментами.")
