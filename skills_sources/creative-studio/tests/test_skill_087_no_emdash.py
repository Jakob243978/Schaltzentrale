"""SKILL-087 — Tests fuer das Gedankenstrich-Verbot (Em-/En-Dash TABU) in Copy.

1 EARS = mind. 1 Test. Der Validator findet Em-/En-Dash (mit Position), laesst den
normalen Bindestrich durch; die Copy-Vorpruef-Flows (Bild: AdContent.warnings,
Reel: content_structure_warnings) haengen ihn ein; alle Framework-/Hook-Templates
sind gedankenstrichfrei.

Wie die uebrigen Copy-Checks ist alles WARNUNG (keine harte Sperre).
"""
from creative_studio.specs import (
    AdContent,
    check_no_emdash,
    dash_warnings,
    DashViolation,
    FORBIDDEN_DASHES,
)
from creative_studio.content import content_structure_warnings
from creative_studio.frameworks import HOOKS, FRAMEWORKS


# --- EARS-1: check_no_emdash findet Em-/En-Dash mit Position ------------------
def test_check_no_emdash_findet_emdash_mit_position():
    text = "Gib mir 3 Sekunden — dann Klarheit."
    v = check_no_emdash(text)
    assert len(v) == 1
    assert isinstance(v[0], DashViolation)
    assert v[0].char == "—"
    assert v[0].index == text.index("—")


def test_check_no_emdash_findet_endash():
    v = check_no_emdash("Mo–Fr erreichbar")
    assert len(v) == 1
    assert v[0].char == "–"


def test_check_no_emdash_findet_alle_verbotenen_varianten():
    # Figure-Dash, Horizontal-Bar, Minus werden vorsorglich mit erfasst.
    for ch in FORBIDDEN_DASHES:
        assert check_no_emdash(f"vorher {ch} nachher"), f"{ch!r} nicht erkannt"


def test_check_no_emdash_zaehlt_mehrere_funde():
    assert len(check_no_emdash("a — b – c")) == 2


# --- EARS-2: normaler Bindestrich bleibt erlaubt (Gegenprobe) ----------------
def test_check_no_emdash_erlaubt_normalen_bindestrich():
    assert check_no_emdash("Kurzzeit-Vermieter sparen Zeit") == []
    assert check_no_emdash("DISC-rot, produkt-bezogen, 24-7") == []


def test_check_no_emdash_leer_und_none():
    assert check_no_emdash("") == []
    assert check_no_emdash(None) == []


# --- EARS-3: dash_warnings ist der Warn-Wrapper (analog compliance_warnings) --
def test_dash_warnings_meldet_pro_fund():
    w = dash_warnings("Heute A — bald B – jetzt C")
    assert len(w) == 2
    assert all("Gedankenstrich-Verstoss" in x for x in w)
    assert "Bindestrich" in " ".join(w)  # Ersatz-/Erlaubt-Hinweis vorhanden


def test_dash_warnings_clean_ist_leer():
    assert dash_warnings("Sauberer Text mit Kurzzeit-Vermieter.") == []


# --- EARS-4: Bild-Copy-Vorpruef-Flow (AdContent.warnings) haengt es ein -------
def _joined(warns):
    return " || ".join(warns)


def test_adcontent_warnings_flaggt_emdash():
    c = AdContent(headline="Mehr Freiheit — weniger Aufwand", cta="Jetzt starten")
    assert any("Gedankenstrich-Verstoss" in w for w in c.warnings())


def test_adcontent_warnings_clean_copy_kein_dash_warning():
    c = AdContent(headline="Mehr Freiheit, weniger Aufwand",
                  subline="Fuer Kurzzeit-Vermieter", cta="Jetzt starten")
    assert not any("Gedankenstrich" in w for w in c.warnings())


def test_adcontent_warnings_prueft_alle_copy_felder():
    # En-Dash in der Subline muss ebenso anschlagen wie in der Headline.
    c = AdContent(headline="Klarer Kopf", subline="Mo–Fr fuer dich da", cta="Los")
    assert any("Gedankenstrich-Verstoss" in w for w in c.warnings())


# --- EARS-5: Reel-Copy-Vorpruef-Flow (content_structure_warnings) ------------
def test_content_structure_warnings_flaggt_emdash_in_reel_copy():
    spec = {
        "hook": "3 Fehler — die dich Zeit kosten",
        "subline": "Der eine Hebel, den alle uebersehen.",
        "cta": "Folge fuer mehr",
        "captions": [{"text": "Hallo", "startMs": 0, "endMs": 500}],
    }
    warns = content_structure_warnings(spec)
    assert any("Gedankenstrich-Verstoss" in w for w in warns)


def test_content_structure_warnings_flaggt_emdash_in_caption():
    spec = {
        "hook": "3 Fehler, die dich Zeit kosten",
        "subline": "Der eine Hebel.",
        "cta": "Folge fuer mehr",
        "captions": [{"text": "vorher–nachher", "startMs": 0, "endMs": 500}],
    }
    assert any("Gedankenstrich-Verstoss" in w for w in content_structure_warnings(spec))


def test_content_structure_warnings_clean_reel_kein_dash_warning():
    spec = {
        "hook": "3 Fehler, die dich Zeit kosten",
        "subline": "Der eine Hebel, den alle uebersehen.",
        "cta": "Folge fuer mehr",
        "captions": [{"text": "Kurzzeit-Vermieter", "startMs": 0, "endMs": 500}],
    }
    assert not any("Gedankenstrich" in w for w in content_structure_warnings(spec))


# --- EARS-6: Bestand ist gedankenstrichfrei (Beispiel-Copy-Durchlauf) --------
def test_alle_hook_templates_sind_dashfrei():
    for key, hook in HOOKS.items():
        assert check_no_emdash(hook.template) == [], f"Hook '{key}' hat einen langen Strich"


def test_alle_framework_templates_sind_dashfrei():
    for key, fw in FRAMEWORKS.items():
        assert check_no_emdash(fw.template) == [], f"Framework '{key}' hat einen langen Strich"


def test_beispiel_copy_durchlauf_ist_dashfrei():
    # Ein realistischer Copy-Durchlauf: gefuellte Hook-Templates -> AdContent.
    filled = {
        "give_me_x": HOOKS["give_me_x"].template.format(seconds=30, payoff="mehr Klarheit"),
        "friction_statement": HOOKS["friction_statement"].template.format(
            reibung="Du arbeitest zu viel", falsche_ursache="deiner Disziplin"),
        "specific_number": HOOKS["specific_number"].template.format(
            anteil=80, zielgruppe="Vermieter", schmerz="verlieren Stunden"),
    }
    for key, text in filled.items():
        c = AdContent(headline=text, cta="Jetzt starten")
        assert not any("Gedankenstrich" in w for w in c.warnings()), key
