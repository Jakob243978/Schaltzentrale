---
title: Research n8n Human-Readability + Bewerbung-Bot v0.5.5 → v0.7.2 Diff-Analyse
date: 2026-05-29
ticket: SKILL-010
---

# Research: n8n Workflows lesbar machen

Forschungs-Backing fuer [[SKILL-010]] (`n8n-human-readable`-Skill).
Zwei Teile: (A) Web-Best-Practices, (B) konkrete Diff-Analyse des
Bewerbung-Bots vom 10-Node-Stand (v0.5.5) auf den 33-Node-Stand
(v0.7.2), wo das Lesbarkeits-Problem akut wurde.

---

## Teil A — Web-Best-Practices (Stand Mai 2026)

### A.1 Sticky Notes als zentrales Werkzeug

n8n liefert seit langem Sticky Notes ein, aber sie sind laut Community
**dramatisch unterbenutzt**. Die offizielle n8n-Doku und mehrere
Tutorials (siehe Quellen unten) konvergieren auf folgende Regeln:

- **Eine Note pro Idee/Sektion** — nicht eine Mega-Note ueber dem
  ganzen Canvas. Mehrere kleine, gut platzierte Notes schlagen eine
  riesige.
- **Why, not What** — "HTTP-Request fetcht Stripe" ist nutzlos. "Holt
  alle unbezahlten Rechnungen der letzten 30 Tage weil Klausel X im
  Mahnprozess das verlangt" ist Pflicht.
- **Naehe zur Erklaerung** — Notes nahe an den Nodes, die sie
  beschreiben, sonst muss man visuell suchen, was wozu gehoert.
- **Markdown** wird unterstuetzt — Headers `#`/`##`, Bold,
  Backticks fuer Code, Listen. Wer das nicht nutzt, verschenkt
  Lesbarkeit.
- **Color Coding** mit Konventions-Bedeutung — blau = Info, gelb =
  Warnung/Known-Issue, gruen = Config/Credentials, rot = Known-Issue
  oder TODO. Konvention muss pro Team/Repo dokumentiert sein.
- **Section-Header-Pattern**: bei mehrphasigen Workflows (Fetch →
  Transform → Validate → Output) am Beginn jeder Phase eine
  Header-Note ("## 2. Routing", "## 3. Calendly-Path") — der
  Workflow wird damit visuell scannbar.

### A.2 Naming-Konventionen

Konvergente Empfehlungen aus mehreren Quellen:

- **Workflow-Namen:** `[STATUS] Domain - Outcome` — `[PROD] Recruiting -
  Bewerber qualifizieren via WhatsApp`. STATUS-Prefix erlaubt
  alphabetische Sortierung in der Workflow-Liste, gruppiert PROD-
  Workflows.
- **Node-Namen:** Generisch verboten. Statt "HTTP Request" → "POST
  Pool-Insert" oder "GET Bewerber by Phone". Verb + Objekt + ggf.
  Zielsystem. Bei Debugging unter Druck rettet der Name den Tag.
- **Branching-Outputs:** Switch- und IF-Nodes muessen ihre
  Output-Pfade nicht nur per Connection-Index unterscheiden — der
  benachbarte Folge-Node bekommt einen sprechenden Namen ("Track
  qualified - Calendly", "Track unqualified - Abschluss").
- Konvention muss schriftlich existieren und im Team-Onboarding
  gelernt werden — die Konvention selbst ist wertvoller als ihr
  konkreter Inhalt.

### A.3 Lane- und Color-Pattern (Lessons aus BPMN/Camunda)

n8n hat **kein** natives Swimlane-Konstrukt. Aus dem BPMN-Umfeld
(Camunda-Docs zu "readable process models") gilt:

- **Symmetrie und einheitliche Flussrichtung** sind wichtiger als
  visuelle Lanes. Camunda empfiehlt sogar, BPMN-Swimlanes oft zu
  vermeiden, weil sie Symmetrie und Flow-Konsistenz brechen.
- Uebertragen auf n8n: **Tracks per Y-Offset** (z.B. jeder
  Switch-Output 200-220px tiefer als der vorherige) sind die
  praktische Annaeherung. Sticky-Note-Boxes hinter den Tracks
  uebernehmen die "Lane-Beschriftung".
- **Explicit > Implicit** — wenn unklar, eher explizit modellieren
  (mehr Nodes, mehr Notes) als implizit (Logik in einer Code-Node
  versteckt).

### A.4 Sub-Workflows als Skalierungsmechanismus

Konvergente Empfehlung mehrerer Quellen (hatchworks.com,
n8nautomation.cloud, dev.to-Analyse von 6000+ Workflows):

- **15-20 Nodes ODER > 3 Branching-Pfade** sind ein Refactor-Kandidat
  fuer Sub-Workflows.
- Sub-Workflows isolieren Failures (was kaputt geht, geht in genau
  EINEM Sub-Workflow kaputt), erleichtern Test/Redeploy einzelner
  Komponenten und brechen Monolithen auf.
- n8n-Vorteil: Sub-Workflow-Executions zaehlen nicht aufs Plan-Limit
  — also kein Cost-Argument gegen Splittung.
- **Counterpoint Workflow-Builder-Vision**:
  [[PROJECT_VISION]] Prinzip 9 `kein-multi-workflow-monolith`
  spiegelt genau diese Empfehlung. Allerdings darf der Skill nicht
  **automatisch splitten** — das ist eine inhaltliche Entscheidung
  (Webhook-Signatur, Datatable-Schreibungen), die nur Jakob treffen
  kann. Der Skill darf nur **vorschlagen**.

### A.5 Wie machen es andere Tools?

- **Camunda/BPMN:** Pools+Lanes formal definiert, aber laut Camunda-
  Best-Practice oft schaedlich fuer Lesbarkeit (vgl. A.3). Camunda
  empfiehlt eher mehrere getrennte Pools statt Lanes — uebertragbar
  auf "lieber Sub-Workflows als interne Lane-Aufteilung".
- **Make.com:** Hat keinen formellen Lane-Mechanismus. Nutzer
  loesen Lesbarkeit primaer ueber Naming + visuelle Anordnung
  (Spaghetti-Vermeidung). Kein Pattern, der signifikant besser waere
  als n8n-Sticky-Notes-Pattern.
- **BPMN-Tools allgemein:** Swimlanes funktionieren am besten bei
  "strategischer" Modellierung (Wer-tut-was). Bei operationaler
  Modellierung (Wie-tut-das-System-das) sind sie eher Last —
  passt zu n8n, das ja operational ist.

---

## Teil B — Diff-Analyse Bewerbung-Bot v0.5.5 → v0.7.2

### B.1 Quantitatives

| Metrik | v0.5.5 | v0.7.2 | Delta |
|---|---|---|---|
| Nodes total | 10 | 33 | **+230 %** |
| IF-/Switch-Nodes | 1 (Filter) | 5 (Filter, IF-Reader, IF-Standort, IF-alle-7, Switch-Class) | +400 % |
| AI-Nodes (Agents+LLM-Calls) | 2 (Agent + Memory) | 7 (Main-Agent, Classifier-LLM, Reader-Agent, Reader-Memory, Reader-Tool, Reader-LLM, Score-LLM) | +250 % |
| Sub-Trigger-Pfade | 1 (WhatsAble) | 2 (WhatsAble Main + Reader-Label-Pfad) | +100 % |
| Pool-Insert/Update-Nodes | 0 | 4 (Pool-Insert qual, Pool-Insert unq, Pool-Update Score, Pool-Update Alert) | neu |
| Sticky Notes | 0 | **0** | **kein Fortschritt** |
| Markdown-Headers im Canvas | 0 | 0 | kein Fortschritt |

### B.2 Was visuell passiert ist

v0.5.5 hatte einen klar linearen Flow: `Trigger → Filter → Agent →
WhatsAble Out (+ Logging)`. In etwa fuenf Nodes lesbar, ein einziges
IF, beide Pfade visuell sichtbar.

v0.7.2 hat fuenf neue "Tracks":

1. **Reader-Pfad** (oben links bei y≈250): IF-Reader-Label → Reader-
   Agent → Send Reader → Reader-Log. Eigene OpenAI/Memory/Tool-Nodes.
2. **Klassifizierungs-Track** (oben rechts ab Switch): Classifier-LLM
   → Switch → 4 Outputs.
3. **Calendly-Track** (qualifiziert + Standort aktiv): Standort-Lookup
   → IF aktiv? → Set Calendly → Pool-Insert → Send → Log.
4. **Pool-Wartetext-Track** (qualifiziert + Standort inaktiv): Set
   Pool-Wartetext → Pool-Insert → Send → Log.
5. **Top-Scoring-Track** (nach jedem Out): Score-LLM → Pool-Update
   Score → IF alle 7 → Template-Alert → Pool-Update Alert.

### B.3 Wo Lesbarkeit konkret kaputt ist

- **Switch by Classification** hat 4 Outputs (`qualified`,
  `unqualified`, `incomplete`, fallback-extra) — drei davon fuehren
  zu Set-Nodes mit unterschiedlichen Response-Texten. **Ohne Sticky
  Note ist die Pfad-Semantik aus dem Canvas nicht erkennbar.** Man
  muss in jeden Set-Node klicken, um die Bedeutung zu erkennen.
- **Reader-Pfad ueberlappt visuell mit Main-Pfad**: Reader-Agent
  liegt auf y=-16, gleich neben dem AI Agent bei y=-16. Die
  Reader-Nodes (OpenAI/Memory/Tool) sind bei y=250-255, mitten im
  Filter→Log-Bereich des Main-Pfads. Sieht im Canvas wie
  Zusammenhang aus, ist aber komplett getrennter Pfad.
- **IF-Reader-Label** ist die erste Verzweigung im Trigger-Pfad
  (bei y=-96), aber kein einziger Hinweis im Canvas erklaert die
  Reader-Funktion (Pool-Abfrage via WhatsApp-Sub-User).
- **Top-Scoring-Track ist nach `Bewerber-Log Outbound` versteckt**
  — die LLM-basierte Janina-Alarmierung haengt am Logging-Output
  des Out-WhatsApp, nicht direkt am Klassifikationsergebnis. Visuell
  wirkt das wie ein "Anhang an Logging", inhaltlich ist es aber der
  haerteste Business-Hebel.
- **Switch-Output fuer `incomplete` und fallback `extra`** zeigen
  beide auf "Send non template via notifyer1" — ein Legacy-Node aus
  v0.5.5, dessen Bedeutung in der neuen Welt nur durch Lesen des
  Filter-Pfads erschliessbar ist.
- **Naming inkonsistent**: "Send non template via notifyer1",
  "Send via WhatsAble (qualified)", "Send via WhatsAble (Reader)" —
  drei verschiedene Schreibweisen fuer die gleiche Aktion (Out-
  WhatsApp). Camel/Kebab/Klammern gemischt.

### B.4 Was gut geblieben ist

- Filter-Node ist um zwei Bedingungen erweitert (`qualified`,
  `unqualified`) — verhindert Double-Process. Diese Erweiterung
  ist die einzige Stelle, die im JSON klar dokumentiert ist (in
  Form von Connection-IDs `qualified-block-c001`).
- Bewerber-Log-Inbound/Outbound-Pattern ist konsistent geblieben.

### B.5 Quick-Win-Vorschlaege fuer v0.8 (vor Skill-Bau)

Diese drei Patterns wuerden in einer halben Stunde Hand-Arbeit die
Lesbarkeit deutlich verbessern und sind als Validierung des
Skill-Konzepts ideal:

1. **Sticky-Section-Headers (Markdown `##`)** mit Farbcode:
   - Blau: "## 1. Inbound + Filter" ueber dem oberen Track
   - Blau: "## 2. Reader-Pfad (Janinas Pool-Abfrage)" ueber dem Reader-Pfad
   - Blau: "## 3. Main-Klassifikation + Routing" ueber Classifier/Switch
   - Gruen: "## 4a. Qualified → Calendly" ueber Calendly-Track
   - Gruen: "## 4b. Qualified → Pool-Warteschlange" ueber Pool-Wartetext-Track
   - Rot: "## 4c. Unqualified" ueber Unqualified-Track
   - Gelb: "## 5. Top-Scoring + Janina-Alert" ueber Score-LLM-Track
2. **Naming-Konvention `[VERB] Objekt`** auf die Out-Nodes
   anwenden: `Send Bewerber-Reply (qualified)` statt `Send via
   WhatsAble (qualified)`; `Send Pool-Reader-Reply` statt
   `Send via WhatsAble (Reader)`; den Legacy-Node von
   `Send non template via notifyer1` umbenennen in
   `Send Bewerber-Reply (legacy fallback)`.
3. **Switch-Output-Pfade per benannten Folge-Set-Nodes**: aktuell
   heisst es `Set Calendly-Response` / `Set Pool-Wartetext` /
   `Set Unqualified-Response` — das ist schon halb dort. Noch
   fehlend: ein Sticky direkt am Switch-Knoten, das die 4 Outputs
   in einer Tabelle erklaert (qualified-aktiv / qualified-pool /
   unqualified / incomplete=legacy-rueckfall).

Diese drei Patterns sind genau die, die der Skill spaeter
**automatisch generieren** koennen muss. Wenn sie per Hand bei
Bewerbung-Bot v0.8 funktionieren, ist das die erste Validierung,
dass der Skill auch nicht groesser werden muss als "diese drei
Patterns + ein Score".

---

## Teil C — Vision-Prinzipien-Konsistenz

Der Skill [[SKILL-010]] sitzt sauber auf zwei Vision-Linien:

- **Workflow-Builder-Vision** ([[PROJECT_VISION]] Punkt 2)
  `visuelle-nachvollziehbarkeit` — der Skill ist die operationale
  Umsetzung dieses Prinzips. Heute ist es eine Mahnung; nach
  Skill-Bau ist es ein automatisch herstellbares Outcome.
- **Skills-Vision** ([[SKILLS_VISION]] Prinzip 4)
  `lessons-aus-live-use-zurueckfuehren` — die Live-Erfahrung Bewerbung-
  Bot-Wachstum 10→33 Nodes ist der Anti-Pattern-Trigger. Ohne
  diesen Sprung waere der Skill spekulativ. Er ist es jetzt nicht.

Anti-Pattern, die im Skill bewusst vermieden werden muessen:

- **`skill-fuer-skills-sake`** — der Skill braucht 2+ Anwendungen
  bevor er als "live" gilt. Erste Anwendung: Bewerbung-Bot v0.8
  Quick-Win-Test. Zweite Anwendung: ein anderer Prod-Workflow
  (Kandidat: Kleinanzeigen-Dealer oder PMS-WhatsApp-Sender, je
  nachdem welcher als naechstes >15 Nodes wird).
- **`skill-schlanker-als-was-er-ersetzt`** — wenn ein
  `/n8n-prettify`-Call laenger braucht als 5 Min Hand-Arbeit fuer
  einen 30-Node-Workflow, hat der Skill verloren. Slash-Command
  muss schnell sein, sonst greift Jakob wieder direkt zur Maus.

---

## Quellen

### Primaer (n8n)

- [Sticky Notes | n8n Docs](https://docs.n8n.io/workflows/components/sticky-notes/)
- [n8n Sticky Notes: How to Organize and Document Your Workflows 2026 — ryanandmattdatascience.com](https://ryanandmattdatascience.com/n8n-sticky-notes/)
- [Best Practices for Structuring Your n8n Workflow JSON — n8npro.in](https://n8npro.in/advanced-topics-best-practices/best-practices-for-structuring-your-n8n-workflow-json/)
- [Organize Your n8n Workflows for Clarity & Efficiency — n8npro.in](https://n8npro.in/best-practices/organizing-your-n8n-workflows-for-clarity/)
- [Best practices for structuring n8n workflows for scale and long-term maintainability — n8n Community](https://community.n8n.io/t/best-practices-for-structuring-n8n-workflows-for-scale-and-long-term-maintainability/248671)
- [n8n Workflows as Living Documentation — medium.com/@Nexumo_](https://medium.com/@Nexumo_/n8n-workflows-as-living-documentation-9f1e259cce2f)
- [n8n Workflow Docs: Naming, Git & Best Practices — evalics.com](https://evalics.com/blog/n8n-workflow-documentation-best-practices-complete-guide)
- [Sub-workflows | n8n Docs](https://docs.n8n.io/flow-logic/subworkflows/)
- [n8n Best Practices Checklist for Production (2026) — hatchworks.com](https://hatchworks.com/blog/ai-agents/n8n-best-practices/)
- [n8n Sub-Workflows: A Complete Step-by-Step Guide for 2026 — n8nautomation.cloud](https://n8nautomation.cloud/blog/n8n-sub-workflows-complete-guide-2026)
- [I analyzed 6,000+ n8n Workflows. Here are the top 3 mistakes — dev.to/iloven8n](https://dev.to/iloven8n/i-analyzed-6000-n8n-workflows-here-are-the-top-3-mistakes-that-break-automations-1leo)
- [10 n8n best practices for successful automation — hostinger.com](https://www.hostinger.com/tutorials/n8n-best-practices)

### BPMN/Vergleich

- [Creating readable process models | Camunda 8 Docs](https://docs.camunda.io/docs/8.7/components/best-practices/modeling/creating-readable-process-models/)
- [Effective BPMN modelling — How to Use Swimlanes Correctly — goodelearning.com](https://goodelearning.com/common-bpmn-modelling-mistakes-swimlanes/)
- [BPMN 2.0 Symbols — A complete guide — camunda.com](https://camunda.com/bpmn/reference/)
