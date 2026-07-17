<!--
TRACEABILITY.md — Requirement → Test → Code → Verify-Matrix (SKILL-017, F.7)

GENERIERT — nicht von Hand editieren. Re-Generierung beim done-Hook
(SKILL.md B "Auto-Doku-Hook"): `python -m workers.traceability_generator`.
Wo (noch) kein Generator existiert, fuellt der Agent die Tabelle aus den
vorhandenen Artefakten (Ticket-EARS, Tests, Code-Marker, Verify-Reports).

Reine Aggregation — KEINE neue Datenquelle:
  EARS-ID       ← aus dem Ticket (`docs/tickets/.../TICKET-NNN.md`)
  Ticket        ← Ticket-Nummer
  Test-Name     ← `test_ears_N` / `test_ticket_NNN_*` (sonst `⚠ kein Test`)
  Code-Referenz ← `# TICKET-NNN`-Marker im Code (sonst `⚠ Code-Referenz fehlt`)
  Verify-Status ← `verify_status` aus dem Verify-Report
                  (kein Report → `⚠ kein Verify-Report`, komplementaer SKILL-016)
-->

# Traceability-Matrix — <Projektname>

**Generiert:** YYYY-MM-DD
**Quelle:** done-Tickets + Tests + Code-Marker + Verify-Reports
**Stand:** N EARS-Saetze ueber M Tickets — X pass / Y partial / Z fail / W ohne Test

## Legende

| Markierung | Bedeutung |
|---|---|
| `pass` / `partial` / `fail` | Verify-Status aus dem Verify-Report |
| `⚠ kein Test` | Kein `test_ears_N`/`test_ticket_NNN_*` zugeordnet |
| `⚠ Code-Referenz fehlt` | Kein `# TICKET-NNN`-Marker im Code auffindbar |
| `⚠ kein Verify-Report` | Ticket hat (noch) keinen Verify-Report (Gate-Hinweis, SKILL-016) |

## Matrix

| EARS-ID | Ticket | Test-Name | Code-Referenz | Verify-Status |
|---|---|---|---|---|
| EARS-1 | TICKET-NNN | `tests/test_ticket_NNN.py::test_ears_1_<stichwort>` | `path/to/file.py:42-58` | pass |
| EARS-2 | TICKET-NNN | `⚠ kein Test` | `api/main.py:210-225` | partial |
| EARS-1 | TICKET-MMM | `tests/test_ticket_MMM.py::test_ears_1_<stichwort>` | `⚠ Code-Referenz fehlt` | `⚠ kein Verify-Report` |

## Offene Luecken (aus der Matrix abgeleitet)

<!-- Generator/Agent fuellt: EARS-Saetze ohne Test, nicht-gruene Tests,
     verwaiste Code-Pfade, Tickets ohne Verify-Report — als Handlungsliste. -->

- [ ] <EARS-ID / Ticket> — <welche Spalte ist ⚠ und was fehlt>
