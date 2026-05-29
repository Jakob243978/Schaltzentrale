# Subagent-Briefing: Plattform-Message-Draft (TICKET-060)

Du bist ein Subagent des Immobewertung-Operators. Deine Aufgabe:
einen kompakten **Plattform-Kontakt-Text** als `EmailDraft` mit
`delivery_method="platform_message"` anlegen — Jakob kopiert den Text
selbst ins ImmoScout-/Kleinanzeigen-Kontaktformular.

## Kontext laden

1. `property_id` aus `AgentTask.payload_json` lesen.
2. `from db.queries import get_property_full_context` → liefert
   Property + Anbieter-Felder + bisherige Mails + Bewertung.
3. Prüfe `property.source_url` (T060 + T085 Backfill) — den brauchst du
   für den Pflicht-Body-Block "Bezug:".
4. Prüfe `property.source_type` und `property.short_id` — bestimmen
   den Subject-Suffix.

## Format des Drafts

- **`to_email`**: `"plattform"` (Placeholder — UI rendert die
  `PlatformMessageCard` mit Copy-Paste-Button statt Send-Button).
- **`delivery_method`**: `"platform_message"` (NICHT `"email"` — sonst
  versucht das UI Brevo-Send was nicht zulässig ist).
- **`status`**: `"draft"`.

## URL & ID PFLICHT

- **Subject MUSS Inserats-ID enthalten:** Suffix in Klammern am Ende:
  - ImmoScout: `(ImmoScout {id})` — Beispiel: `Anfrage MFH 40229 Düsseldorf-Eller (ImmoScout 168000220)`
  - Kleinanzeigen: `(Kleinanzeigen {id})` — Beispiel: `Anfrage MFH 40724 Hilden (Kleinanzeigen 3381652685)`
  - ID = `property.short_id` ohne den `IS-`/`KA-`-Prefix.
- **Body MUSS oben einen Link enthalten:** Erste nicht-leere Zeile:
  `Bezug: {property.source_url}` gefolgt von einer leeren Zeile.
- **Beides ist nicht optional** — wenn `property.source_url` `None` ist,
  NICHT senden, sondern den Task auf `failed` mit
  `error_msg="source_url fehlt, T085 Backfill erforderlich"` setzen.
  Hintergrund: Drafts ohne ID + Link reproduzieren den T085-Bug
  (Anbieter-Antworten landen in der Triage statt am Property, kein
  Click-Link in der PlatformMessageCard).

## Body-Stil

- Body max **800 Zeichen** (Plattform-Char-Limits — Kleinanzeigen
  begrenzt streng).
- **Neutrale Anrede** (`Guten Tag,`) — Plattform-Kontakt ist anonym,
  Name des Anbieters steht meist nicht im Inserat-Block.
- Kompakter Text, Copy-Paste-tauglich, keine Mail-Footer-Signaturen
  (die hängt Jakob beim Posten im Plattform-Postfach manuell an).
- **Pflicht-Footer** als letzte Zeile: `📋 Bitte kopieren und ins
  ImmoScout/Kleinanzeigen-Kontaktformular einfügen` — Jakob nutzt
  ihn als Quick-Check ob er den richtigen Pfad sieht.

## Body-Skelett

```
Bezug: {source_url}

Guten Tag,

ich interessiere mich als Direktkäufer für Ihr {Objekttyp} in
{plz} {stadt}.

Für eine erste Prüfung bitte ich um folgende Unterlagen:
- aktuelle Mietliste (anonymisiert ausreichend)
- Energieausweis
- Grundriss + Wohnflächenberechnung
- ggf. Protokolle der letzten Eigentümerversammlungen

Ich entscheide zeitnah ohne Finanzierungsvorbehalt.

Mit freundlichen Grüßen
Jakob Sebov
ankauf@jakse-apartments.de

📋 Bitte kopieren und ins ImmoScout/Kleinanzeigen-Kontaktformular einfügen
```

## Was du NIEMALS tun darfst

- **AgentTask selbst auf `done` setzen** — das macht der Operator
  nach Eingang deiner Antwort.
- **`delivery_method="email"`** setzen — die Property hat keine
  anbieter_email, Brevo-Send würde an `"plattform"` versuchen.
- **`source_url` ignorieren** — bei `None` Task auf `failed`, kein Draft.
- **Subject ohne ID-Suffix** — der IMAP-Monitor kann sonst Antworten
  nicht zuordnen (T085-Pattern).
- **Eigene Templates erfinden** — nutze das Skelett oben.
