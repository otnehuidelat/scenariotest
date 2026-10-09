# app.py
# Симулятор сценариев жизни: ИЛИ + меланхолик + визуал-эмоциональный
# Запуск: streamlit run app.py

import streamlit as st
import numpy as np
import pandas as pd

st.set_page_config(layout="wide", page_title="Сценарии жизни")

# ============================================================
# ПРОФИЛЬ (ядро: ИЛИ + меланхолик + визуал-эмоциональный)
# ============================================================
PROFILE = {
    "introversion": 0.85,
    "logic": 0.80,
    "intuition": 0.75,
    "ethics": 0.35,
    "sensory": 0.30,
    "tempo": 0.30,
    "stress_resilience": 0.20,
    "energy_reserve": 0.25,
    "recovery_need": 0.85,
    "emotional_sensitivity": 0.85,
    "emotional_influence": 0.70,
    "visual_motivation": 0.80,
    "need_guarantee": 0.85,
    "need_meaning": 0.80,
    "need_comfort": 0.85,
    "need_novelty": 0.75,
    "need_control": 0.70,
}
DIMS = ["introversion", "tempo", "stress_resilience", "need_guarantee",
        "need_comfort", "need_novelty", "need_meaning", "need_control"]

# ============================================================
# РЕЖИМЫ ЖИЗНИ
# ============================================================
LIFE_MODES = {
    "office_9_5": {
        "label": "Офис 9-5",
        "introversion": 0.5, "tempo": 0.5, "stress_resilience": 0.5,
        "need_guarantee": 0.7, "need_comfort": 0.5, "need_novelty": 0.2,
        "need_meaning": 0.4, "need_control": 0.3,
        "social_load": 0.6, "public_load": 0.4, "recovery": 0.4,
    },
    "manager": {
        "label": "Руководитель",
        "introversion": 0.4, "tempo": 0.7, "stress_resilience": 0.7,
        "need_guarantee": 0.5, "need_comfort": 0.6, "need_novelty": 0.4,
        "need_meaning": 0.6, "need_control": 0.8,
        "social_load": 0.8, "public_load": 0.7, "recovery": 0.3,
    },
    "freelance_burst": {
        "label": "Фриланс рывками",
        "introversion": 0.7, "tempo": 0.8, "stress_resilience": 0.5,
        "need_guarantee": 0.3, "need_comfort": 0.5, "need_novelty": 0.7,
        "need_meaning": 0.7, "need_control": 0.8,
        "social_load": 0.3, "public_load": 0.3, "recovery": 0.5,
    },
    "creative_studio": {
        "label": "Творческая студия",
        "introversion": 0.7, "tempo": 0.4, "stress_resilience": 0.5,
        "need_guarantee": 0.5, "need_comfort": 0.7, "need_novelty": 0.8,
        "need_meaning": 0.9, "need_control": 0.6,
        "social_load": 0.4, "public_load": 0.3, "recovery": 0.6,
    },
    "startup_chaos": {
        "label": "Стартап, хаос",
        "introversion": 0.5, "tempo": 0.9, "stress_resilience": 0.7,
        "need_guarantee": 0.1, "need_comfort": 0.3, "need_novelty": 0.9,
        "need_meaning": 0.8, "need_control": 0.6,
        "social_load": 0.7, "public_load": 0.6, "recovery": 0.2,
    },
    "stable_corporate": {
        "label": "Стабильная корпорация",
        "introversion": 0.5, "tempo": 0.4, "stress_resilience": 0.5,
        "need_guarantee": 0.9, "need_comfort": 0.7, "need_novelty": 0.1,
        "need_meaning": 0.3, "need_control": 0.3,
        "social_load": 0.5, "public_load": 0.3, "recovery": 0.6,
    },
    "crisis_consulting": {
        "label": "Кризис-консалтинг",
        "introversion": 0.5, "tempo": 0.9, "stress_resilience": 0.6,
        "need_guarantee": 0.4, "need_comfort": 0.4, "need_novelty": 0.9,
        "need_meaning": 0.8, "need_control": 0.6,
        "social_load": 0.6, "public_load": 0.5, "recovery": 0.3,
    },
    "solo_expert": {
        "label": "Соло-эксперт (аналитика, тексты)",
        "introversion": 0.9, "tempo": 0.3, "stress_resilience": 0.4,
        "need_guarantee": 0.7, "need_comfort": 0.8, "need_novelty": 0.5,
        "need_meaning": 0.8, "need_control": 0.9,
        "social_load": 0.2, "public_load": 0.1, "recovery": 0.7,
    },
}

# ============================================================
# ПРОФЕССИИ
# ============================================================
PROFESSIONS = {
    "analyst":  {"label": "Аналитик / стратег",      "tempo": 0.3, "public_load": 0.2, "social_load": 0.3, "need_meaning": 0.7},
    "manager":  {"label": "Менеджер",                "tempo": 0.7, "public_load": 0.6, "social_load": 0.8, "need_meaning": 0.5},
    "teacher":  {"label": "Преподаватель / эксперт", "tempo": 0.5, "public_load": 0.8, "social_load": 0.7, "need_meaning": 0.7},
    "designer": {"label": "Дизайнер / творец",       "tempo": 0.4, "public_load": 0.2, "social_load": 0.4, "need_meaning": 0.8},
    "engineer": {"label": "Инженер / разработчик",   "tempo": 0.4, "public_load": 0.1, "social_load": 0.3, "need_meaning": 0.6},
    "sales":    {"label": "Продажи / переговоры",    "tempo": 0.8, "public_load": 0.5, "social_load": 0.9, "need_meaning": 0.3},
    "writer":   {"label": "Писатель / исследователь","tempo": 0.2, "public_load": 0.1, "social_load": 0.2, "need_meaning": 0.9},
    "custom":   {"label": "Своя (вручную ниже)"},
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
        "desc": "Один проект за раз. Интенсив → длинная пауза. Никакой равномерной загрузки.",
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
    "role_shift": {
        "label": "Сменить роль или профессию",
        "desc": "Уйти из публичной/менеджерской/скоростной роли в экспертную и тихую.",
        "effect": {"load": -20, "meaning": 2},
        "recovery_bonus": 10,
        "cost": "6–18 месяцев",
    },
}

# ============================================================
# ФАЗЫ СЦЕНАРИЯ
# ============================================================
PHASES = [
    {
        "range": (0, 6),
        "title": "Фаза 1: Накопление стресса",
        "signs": [
            "Раздражение по мелочам",
            "Плохой сон, трудно вставать",
            "Прокрастинация на лёгких задачах",
            "Желание «просто дожить до выходных»",
        ],
        "why": "Меланхолик с низкой стрессоустойчивостью накапливает нагрузку быстрее, чем восстанавливается. Снаружи ещё незаметно, в теле — уже видно.",
        "action": "Не «собраться». Снять нагрузку сейчас. Неделя отдыха в этой фазе = месяц отсрочки выгорания.",
    },
    {
        "range": (6, 18),
        "title": "Фаза 2: Срыв ритма",
        "signs": [
            "Эмоциональные качели",
            "Цинизм к работе и людям",
            "Падение смысла: «зачем всё это»",
            "Тело: головные боли, ЖКТ, зажимы",
        ],
        "why": "Стресс перешёл порог 65 — включается нелинейный обвал. У меланхолика он резкий, а не постепенный.",
        "action": "Сменить режим, а не бороться с симптомами. Убрать публичность, конфликты, скорость. Перейти на рывки.",
    },
    {
        "range": (18, 36),
        "title": "Фаза 3: Выгорание",
        "signs": [
            "Нет сил даже на то, что раньше нравилось",
            "Апатия, «всё равно»",
            "Отвращение к профессии",
            "Психосоматика: давление, сердце, иммунитет",
        ],
        "why": "Энергия ниже 25 — психика режет всё, что не критично для выживания. Мотивация исчезает не от слабости, а от экономии.",
        "action": "Только восстановление. Не новый проект, не смена работы, не рывок. Сначала базовый ресурс, потом решения.",
    },
    {
        "range": (36, 999),
        "title": "Фаза 4: Развилка",
        "signs": [
            "Либо хроническая депрессия и телесные болезни",
            "Либо выход через смену роли и режима",
            "Середины нет: плато здесь не держится",
        ],
        "why": "Система либо перестраивается, либо ломается. Меланхолик-ИЛИ не выдерживает длительного давления, но хорошо восстанавливается при смене условий.",
        "action": "Смена профессии или режима. Экспертная, тихая, смысловая роль. Рывки. Комфорт. Управление через структуры.",
    },
]

# ============================================================
# ХЕЛПЕРЫ
# ============================================================
def clamp(x, lo=0.0, hi=100.0):
    return float(max(lo, min(hi, x)))

def combine(mode, profession):
    result = dict(mode)
    for k, v in profession.items():
        if k == "label":
            continue
        result[k] = (result.get(k, v) + v) / 2 if k in result else v
    return result

def distance(profile, mode):
    return sum(abs(profile[k] - mode.get(k, 0.5)) for k in DIMS) / len(DIMS)

def env_penalty(profile, mode):
    p = 0.0
    p += mode.get("social_load", 0.5) * profile["introversion"] * 0.5
    p += mode.get("public_load", 0.5) * profile["introversion"] * 0.6
    p += mode.get("tempo", 0.5) * (1 - profile["stress_resilience"]) * 0.3
    return p

def mismatch(profile, mode):
    return distance(profile, mode) + env_penalty(profile, mode)

def initial_state(profile, mode):
    m = mismatch(profile, mode)
    stress = 20 + m * 70
    energy = 85 - m * 60
    meaning = mode.get("need_meaning", 0.5) * 100 * (1 - profile["need_meaning"] * 0.3)
    health = 85 - stress * 0.4
    return {
        "stress":  clamp(stress, 5, 95),
        "energy":  clamp(energy, 5, 95),
        "meaning": clamp(meaning, 5, 95),
        "health":  clamp(health, 5, 95),
    }

def step(state, profile, mode, active):
    load = 30 + mismatch(profile, mode) * 50
    recovery = 30 * mode.get("recovery", 0.5) + 10
    meaning_gain = mode.get("need_meaning", 0.5) * 3

    for key in active:
        iv = INTERVENTIONS[key]
        load += iv["effect"].get("load", 0)
        recovery += iv.get("recovery_bonus", 0)
        meaning_gain += iv["effect"].get("meaning", 0)

    delta = load - recovery
    if state["stress"] > 65:
        delta *= 1.5
    state["stress"] = clamp(state["stress"] + delta * 0.12, 0, 100)
    state["energy"] = clamp(100 - state["stress"], 0, 100)
    state["meaning"] = clamp(
        state["meaning"] + meaning_gain * 0.15 - state["meaning"] * 0.02, 0, 100)

    if state["stress"] > 60:
        state["health"] = clamp(state["health"] - 0.7, 0, 100)
    else:
        state["health"] = clamp(state["health"] + 0.2, 0, 100)
    return state

def simulate(profile, mode, months, timeline=None, noise=0.05, runs=30):
    init = initial_state(profile, mode)
    all_runs = []
    for _ in range(runs):
        state = dict(init)
        hist = []
        for month in range(months):
            active = [k for (start, k) in (timeline or []) if month >= start]
            s = dict(state)
            s["stress"] += np.random.normal(0, noise * 10)
            state = step(s, profile, mode, active)
            hist.append(dict(state, month=month))
            if state["energy"] < 5:
                break
        all_runs.append(hist)

    max_len = max(len(r) for r in all_runs)
    keys = ["energy", "stress", "meaning", "health"]
    out = {k: np.full(max_len, np.nan) for k in keys}
    for i in range(max_len):
        vals = {k: [] for k in keys}
        for r in all_runs:
            if i < len(r):
                for k in keys:
                    vals[k].append(r[i][k])
        for k in keys:
            if vals[k]:
                out[k][i] = float(np.mean(vals[k]))
    return out

def detect_spiral(hist):
    if not hist or "energy" not in hist:
        return "неизвестно"
    mask = ~np.isnan(hist["energy"])
    if mask.sum() < 12:
        return "неизвестно"
    x = np.arange(mask.sum())
    e_slope = np.polyfit(x, hist["energy"][mask], 1)[0]
    s_slope = np.polyfit(x, hist["stress"][mask], 1)[0]
    m_slope = np.polyfit(x, hist["meaning"][mask], 1)[0]
    if s_slope > 0.3 and e_slope < -0.3:
        return "downward"
    if m_slope > 0.2 and e_slope > -0.15:
        return "upward"
    return "plateau"

def get_phase(month):
    for p in PHASES:
        if p["range"][0] <= month < p["range"][1]:
            return p
    return PHASES[-1]

# ============================================================
# АНАЛИЗ
# ============================================================
def score_profession(profile, profession):
    score = 100.0
    score -= abs(profession.get("tempo", 0.5) - profile["tempo"]) * 40
    score -= profession.get("public_load", 0.5) * profile["introversion"] * 50
    score -= profession.get("social_load", 0.5) * profile["introversion"] * 40
    score -= max(0, profile["need_meaning"] - profession.get("need_meaning", 0.5)) * 50
    return max(0.0, min(100.0, score))

def autoselect_professions(profile, top_n=3):
    scored = []
    for key, prof in PROFESSIONS.items():
        if key == "custom":
            continue
        scored.append((key, score_profession(profile, prof)))
    scored.sort(key=lambda x: -x[1])
    return scored[:top_n]

def recommend_plan(profile, mode):
    m = mismatch(profile, mode)
    if m > 0.55:
        return [(0, "recovery"), (2, "reduce_load"), (4, "burst"),
                (6, "meaning"), (9, "role_shift")]
    if m > 0.35:
        return [(0, "recovery"), (2, "burst"), (4, "meaning")]
    return [(0, "meaning")]

def one_change_analysis(profile, mode, months=120):
    baseline = simulate(profile, mode, months)
    def last(arr):
        m = ~np.isnan(arr)
        return float(arr[m][-1]) if m.sum() else 0.0
    base_final = {
        "energy": last(baseline["energy"]),
        "meaning": last(baseline["meaning"]),
        "stress": last(baseline["stress"]),
    }
    results = []
    for key in INTERVENTIONS:
        hist = simulate(profile, mode, months, timeline=[(0, key)])
        final = {
            "energy": last(hist["energy"]),
            "meaning": last(hist["meaning"]),
            "stress": last(hist["stress"]),
        }
        d_e = final["energy"] - base_final["energy"]
        d_m = final["meaning"] - base_final["meaning"]
        d_s = final["stress"] - base_final["stress"]
        results.append({
            "key": key,
            "label": INTERVENTIONS[key]["label"],
            "energy": final["energy"],
            "d_energy": d_e,
            "d_meaning": d_m,
            "d_stress": d_s,
            "score": d_e * 0.5 + d_m * 0.3 - d_s * 0.2,
        })
    results.sort(key=lambda r: -r["score"])
    return results

# ============================================================
# SESSION STATE
# ============================================================
if "prof_key" not in st.session_state:
    st.session_state["prof_key"] = "analyst"
if "mode_key" not in st.session_state:
    st.session_state["mode_key"] = "manager"

# ============================================================
# UI
# ============================================================
st.title("Сценарии жизни: ИЛИ + меланхолик + визуал-эмоциональный")
st.caption("Один профиль. Текущий режим. Автоподбор. План выхода. Одно изменение.")

col_in, col_main = st.columns([1, 3])

with col_in:
    st.subheader("Текущий режим")
    mode_key = st.selectbox(
        "Режим жизни",
        list(LIFE_MODES.keys()),
        index=list(LIFE_MODES.keys()).index(st.session_state["mode_key"]),
        format_func=lambda k: LIFE_MODES[k]["label"],
    )
    st.session_state["mode_key"] = mode_key

    st.subheader("Профессия")
    prof_key = st.selectbox(
        "Профессия",
        list(PROFESSIONS.keys()),
        index=list(PROFESSIONS.keys()).index(st.session_state["prof_key"]),
        format_func=lambda k: PROFESSIONS[k]["label"],
    )
    st.session_state["prof_key"] = prof_key

    if prof_key == "custom":
        custom_tempo = st.slider("Темп", 0.0, 1.0, 0.5)
        custom_public = st.slider("Публичность", 0.0, 1.0, 0.3)
        custom_social = st.slider("Соц. нагрузка", 0.0, 1.0, 0.5)
        custom_meaning = st.slider("Смысл в работе", 0.0, 1.0, 0.5)
        profession = {"label": "Своя", "tempo": custom_tempo,
                      "public_load": custom_public, "social_load": custom_social,
                      "need_meaning": custom_meaning}
    else:
        profession = PROFESSIONS[prof_key]

    st.subheader("Автоподбор под профиль")
    top = autoselect_professions(PROFILE, top_n=3)
    for key, score in top:
        label = PROFESSIONS[key]["label"]
        col_a, col_b = st.columns([3, 2])
        with col_a:
            st.markdown(f"**{label}**")
        with col_b:
            st.markdown(f"`{score:.0f}%`")
        if st.button("Применить", key=f"apply_{key}"):
            st.session_state["prof_key"] = key
            st.rerun()

    horizon = st.slider("Горизонт, лет", 2, 15, 8)

# Собираем режим
current = combine(LIFE_MODES[mode_key], profession)
m_val = mismatch(PROFILE, current)
months = horizon * 12

with col_main:
    # --- Метрики ---
    c1, c2, c3 = st.columns(3)
    fit = max(0.0, min(100.0, 100 - m_val * 100))
    with c1:
        st.metric("Совместимость режима", f"{fit:.0f}%")
    with c2:
        soc = current.get("social_load", 0.0)
        st.metric("Соц. нагрузка", f"{soc:.2f}",
                  delta=f"{soc - PROFILE['introversion']:+.2f}")
    with c3:
        pub = current.get("public_load", 0.0)
        st.metric("Публичность", f"{pub:.2f}",
                  delta=f"{pub - PROFILE['introversion'] * 0.3:+.2f}")

    # --- Прогноз без изменений ---
    hist_now = simulate(PROFILE, current, months)
    spiral_now = detect_spiral(hist_now)

    df_now = pd.DataFrame({
        "Месяц": range(len(hist_now["energy"])),
        "Энергия": hist_now["energy"],
        "Стресс": hist_now["stress"],
        "Смысл": hist_now["meaning"],
        "Здоровье": hist_now["health"],
    }).set_index("Месяц")

    st.subheader("Прогноз без изменений")
    st.line_chart(df_now)

    spiral_label = {
        "downward": "🔻 нисходящая",
        "upward": "🔺 восходящая",
        "plateau": "➖ плато",
        "неизвестно": "❓",
    }[spiral_now]
    st.markdown(f"### Спираль: {spiral_label}")

    if spiral_now == "downward":
        st.error("Режим ведёт в нисходящую петлю. Энергия падает, стресс растёт, смысл проседает.")
    elif spiral_now == "upward":
        st.success("Режим устойчив и выводит на восходящую петлю.")
    else:
        st.warning("Плато. Не рушится, но и не растёт. Меланхолик в плато медленно теряет смысл.")

    # --- Карточки фаз ---
    st.subheader("Карточки фаз")
    last_month = len(df_now) - 1
    current_phase = get_phase(last_month)
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
    plan = recommend_plan(PROFILE, current)
    for start, key in plan:
        iv = INTERVENTIONS[key]
        st.markdown(f"**{iv['label']}** · через {start} мес · {iv['cost']}")
        st.caption(iv["desc"])

    hist_plan = simulate(PROFILE, current, months, timeline=plan)
    spiral_plan = detect_spiral(hist_plan)

    df_cmp = pd.DataFrame({
        "Месяц": range(len(hist_plan["energy"])),
        "Энергия (сейчас)": hist_now["energy"],
        "Энергия (с планом)": hist_plan["energy"],
        "Смысл (сейчас)": hist_now["meaning"],
        "Смысл (с планом)": hist_plan["meaning"],
        "Стресс (сейчас)": hist_now["stress"],
        "Стресс (с планом)": hist_plan["stress"],
    }).set_index("Месяц")

    st.line_chart(df_cmp)

    spiral_label2 = {
        "downward": "🔻", "upward": "🔺", "plateau": "➖", "неизвестно": "❓",
    }[spiral_plan]
    st.markdown(f"### Спираль после плана: {spiral_label2} {spiral_plan}")

    if spiral_plan == "upward":
        st.success("План выводит на восходящую петлю. Ключ — не менять всё сразу, а идти по фазам.")
    elif spiral_plan == "plateau":
        st.info("План стабилизирует, но не выводит в рост. Возможно, нужна смена роли.")
    else:
        st.warning("Даже с планом спираль нисходящая. Режим фундаментально несовместим — нужна смена профессии.")

    # --- Одно изменение ---
    st.subheader("Что даёт одно изменение")
    with st.spinner("Считаю эффект каждой интервенции по отдельности..."):
        results = one_change_analysis(PROFILE, current, months=min(months, 120))

    df_one = pd.DataFrame([{
        "Изменение": r["label"],
        "Энергия": f"{r['energy']:.0f}",
        "Δ Энергия": f"{r['d_energy']:+.1f}",
        "Δ Смысл": f"{r['d_meaning']:+.1f}",
        "Δ Стресс": f"{r['d_stress']:+.1f}",
    } for r in results])
    st.dataframe(df_one, use_container_width=True, hide_index=True)

    best = results[0]
    st.success(
        f"**Максимальный эффект: {best['label']}**  \n"
        f"Одно это изменение даёт {best['d_energy']:+.1f} к энергии и "
        f"{best['d_meaning']:+.1f} к смыслу. "
        f"Не пытайся менять всё сразу — начни с этого."
    )

st.divider()
st.caption("Это не диагноз и не приговор. Вероятности, а не судьба. "
           "Тип компенсируется средой, ролью, партнёром и инструментами.")
