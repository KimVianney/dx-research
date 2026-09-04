# claimline

A small, polyglot **claims intake and adjudication service**, used as a
reference project and as a testbed for evaluating code-review and
static-analysis tooling.

> [!NOTE]
> This repository is a demonstration and evaluation testbed, not a production
> system. See [SECURITY.md](SECURITY.md) — in particular, some feature branches
> and pull requests **intentionally** introduce defects or non-functional
> "canary" secrets so that automated review and static-analysis tools can be
> measured against a known baseline. `main` is kept clean and green.

## What it does

`claimline` accepts healthcare claims, stores them, and adjudicates them against
a small deterministic rule set (timely filing, eligibility, duplicate detection,
and a benefit calculation) to produce a payment or a denial.

## Architecture

| Layer | Stack | Path |
|-------|-------|------|
| API | Python 3.12 / FastAPI | [`api/`](api/) |
| Web console | TypeScript / React | [`web/`](web/) |
| Settlement worker | Go | [`worker/`](worker/) |
| Schema | PostgreSQL migrations | [`migrations/`](migrations/) |
| Infrastructure | Terraform + Dockerfile | [`infra/`](infra/) |
| Contract | OpenAPI 3 | [`openapi/`](openapi/) |

## Development

### API (Python)

```bash
cd api
python -m venv .venv && . .venv/bin/activate
pip install -e '.[dev]'
ruff check .
pytest -q
uvicorn claimline.main:app --reload
```

### Worker (Go)

```bash
cd worker
go test ./...
echo '[{"ClaimID":"C1","PayerID":"P1","PaidCents":8800}]' | go run .
```

### Web (TypeScript)

```bash
cd web
npm ci
npm run typecheck && npm run lint && npm test
```

## License

[MIT](LICENSE).
