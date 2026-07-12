# Ad-Copy-Sheet — Vorlage (SKILL-100)

Projektneutrale Vorlage fuer das **veroeffentlichungsfertige Ad-Copy-Sheet**, das zu JEDEM
Ad-Satz gehoert (neben den Creatives + `ad-report.html`). Platzhalter `<…>` ersetzen.
Voice-Regeln: siehe SKILL.md Abschnitt 2 (Workshop-Brand „How You Sound", SKILL-101).

---
```
---
title: Ad-Copy · <Kampagne>
kampagne: <kampagne-slug>
status: vorschlag (Review <Owner>)
last_updated: <YYYY-MM-DD>
voice: <Brand-Voice-Quelle, z. B. Workshop „How You Sound">
---

# Ad-Copy · <Kampagne>

**Ziel-URL (alle):** `https://<lp>/?utm_source=meta&utm_campaign=<kampagne>&utm_content=<ad-id>`

**Voice-Regeln (verbindlich):** direkt/energetisch/motivierend/nahbar · Emotionsraum statt Angst ·
Wachstum verkaufen, nicht Entlastung · „du", nie „Geschaeftsfuehrer" · „individueller" statt
„komplizierter" · keine Tool-Namen · „KI" nur als Loesungsbenennung · keine Gedankenstriche ·
Komma nur wo grammatisch noetig. Beweis: <Proof-Line>.

## Mapping · Creative ↔ Persona ↔ Kategorie ↔ Layout ↔ BG ↔ utm_content
| utm_content | Persona | Kategorie | Layout | BG | Set |
|---|---|---|---|---|---|
| `<ad-id>` | <Persona> | <Kategorie> | <Layout> | <BG> | <Set> |

## <Set-Name>
### `<ad-id>` · <Persona> · <Kategorie>
**On-Image:** Topline „<Auftakt>" · Headline „<Wunsch-/Pain-Szene, kurz>" · Subline „<Mehrwert>" · CTA-Button „<Jetzt + Aktion>"
**Headline-Feld:** <kurz> · **Beschreibung:** <Nutzen/Neugier, nicht zielgruppen-gatend> · **Meta-CTA:** <Registrieren|Anmelden|Mehr dazu> · **utm_content:** `<ad-id>`

**A · Langform (Primaertext):**
> <Hook = Auftakt+Headline>
>
> <Tension/Resolution im Alltag, nach vorne>
>
> <Proof: eigener Betrieb verdoppelt>
>
> <Ask: weicher CTA + 👇>

- **B · Kurz (< 125):** <eine starke Zeile> 👇
```
---

**Regeln fuer das Sheet:**
- Pro Hook GENAU die Felder oben (nichts weglassen).
- CTA-Button = Handlungs-Aufforderung MIT Zeit-/Ort-Komponente („Jetzt …", „Hier …").
- Topline benennt NIE die Zielgruppe (haelt die Ausstrahlung breit).
- Headline ist ein vollstaendiger, logischer Satz und **face-safe** (kurz genug, dass der Text
  bei Foto-Ads nicht ueber dem Gesicht liegt).
- Copy-Arc = `frameworks.FRAMEWORKS[<key>]`-Slots (Hook → Tension → Resolution → Proof → Ask).
