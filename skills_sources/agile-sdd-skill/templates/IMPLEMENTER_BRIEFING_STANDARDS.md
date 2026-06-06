# Implementer-Briefing-Standards

Dieses File sammelt **Standard-Bloecke**, die in jedes Implementer-Subagent-
Briefing eingefuegt werden sollen, damit wiederkehrende Anti-Pattern nicht
in jedem Ticket neu auftreten. Bloecke entstehen aus Live-Erfahrungen
(SKILL-006 Implementer-Hygiene, SKILL-010 API-Schema-Mitdenken, ...) und
gelten ueber alle Skill- und Projekt-Tickets hinweg.

> [!note] Wer fuegt das ein?
> Der Aufrufer (Operator / Lead-Claude / `/sdd-implement`-Command), der einen
> Implementer-Subagent spawnt, kopiert die relevanten Bloecke ans Ende des
> Subagent-Briefings. Der Subagent selbst liest die Bloecke nicht aktiv —
> er bekommt sie ins Prompt.

---

## Block: API-Schema-Mitdenken (SKILL-010)

> [!important] Pflicht-Mitdenken bei jedem Ticket mit Datenmodell-Touch
> Wenn du in diesem Ticket Felder zu einem Datenmodell hinzufuegst
> (`db/models.py`, `models/*.py`, `schema.prisma`, `entities/*.ts` o.Ae.):
>
> 1. **Alle Endpoints pruefen.** Liste alle `GET/POST/PATCH`-Endpoints
>    auf, die das geaenderte Modell zurueckliefern. Erweitere die
>    Response-Schemas (Pydantic/TypeBox/Zod) **additiv** um die neuen
>    Felder — keine Feld-Umbenennung, keine Typ-Aenderung bestehender
>    Felder. Backwards-Kompat ist Pflicht.
> 2. **Test gegen `/openapi.json` schreiben.** Mindestens einen
>    pytest-Case, der per `requests.get("http://localhost:.../openapi.json")`
>    (oder TestClient) verifiziert, dass die neuen Feldnamen im
>    Schema auftauchen. Beispiel:
>    ```python
>    def test_ticket_NNN_openapi_exposes_region_id():
>        client = TestClient(app)
>        schema = client.get("/openapi.json").json()
>        props = schema["components"]["schemas"]["Property"]["properties"]
>        assert "region_id" in props
>    ```
> 3. **Im Ticket-Frontmatter markieren.** Setze
>    `api_endpoints_extended: yes` (oder `no` wenn du bewusst auf den
>    naechsten Sprint verschiebst, oder `n/a` wenn das Feld nur intern
>    von Workers genutzt wird und kein Endpoint es ausliefert).
> 4. **Im Ticket-Body kurz dokumentieren** unter "API-Schema-Kontrakt":
>    welche Endpoints du erweitert hast und welche bewusst NICHT.
>
> Live-Beispiel (Anti-Pattern, das diese Regel ausgeloest hat):
> T103a in Immobewertung — T092 hat Property um Region-FK + JSON-Felder
> erweitert, T101 hat sie befuellt, aber `GET /api/property/{id}` gab
> sie nie zurueck. Frontend brauchte zwei Calls, T103a musste spontan
> nachgeschoben werden, nachdem Jakob's UI-Klick den Bug entdeckte.

---

## Block: Implementer-Hygiene (SKILL-003, Kurzfassung)

> [!important] Token-Budget + Scope-Hygiene
> - Token-Budget pro Subagent-Lauf: max **60k** (sonst Eskalation an
>   Operator/User). Beim Anlauf an die Grenze: Status-Report + Stop,
>   nicht still weiter.
> - **Nur die im Ticket genannten Files anfassen.** Wenn du beim Lesen
>   merkst, dass ein anderer File auch geaendert werden muss: melden,
>   nicht heimlich erweitern.
> - **Kein "while-im-bin"-Refactoring.** Wenn dir Code-Smell auffaellt,
>   notiere im Implementer-Report, lege im Zweifel ein Folge-Ticket an.

---

## Block: Skill-Code-Pfad (multi-projekt)

> [!info] Wo lebt der Code?
> Wenn du an einem Skill arbeitest: Source liegt unter
> `<Schaltzentrale>/skills_sources/<skill>/` (Single Source of Truth).
> NIE direkt in `~/.claude/skills/` editieren — das wird per
> `setup.ps1` (robocopy /MIR) deployt und ueberschrieben.
>
> Nach jeder Aenderung an `skills_sources/<skill>/`:
> ```powershell
> cd C:\Users\Jakob\claude_projects\Schaltzentrale; .\setup.ps1
> ```

---

## Wann welcher Block?

| Block | Einfuegen bei |
|---|---|
| API-Schema-Mitdenken | Ticket aendert Datenmodell ODER neue Endpoints |
| Implementer-Hygiene | Jedem Implementer-Subagent (Default) |
| Skill-Code-Pfad | Implementer-Subagent fuer Skill-Tickets (`SKILL-NNN`) |
