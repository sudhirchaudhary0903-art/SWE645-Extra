# SWE645 Extra Credit: Agentic Student Survey System

Group: Vivek Sarvagod / Sudhir Chaudhary

This repository extends the Homework 3 Student Survey CRUD application into an agentic AI system. The original React + FastAPI + SQLModel + MySQL application is preserved, and the extra-credit layer adds MCP/FastMCP tools, a LangGraph agent service, a conversational React page, and a three-pod Helm deployment.

## What Was Required

| Requirement | Implementation |
| --- | --- |
| FastMCP / MCP tool layer | `portal-survey-api/mcp_tools.py` exposes `create_survey`, `list_surveys`, `get_survey_by_id`, `search_surveys`, `update_survey`, and `delete_survey`. |
| Reuse existing CRUD logic | Shared service functions live in `portal-survey-api/services/survey_service.py`; REST routes and MCP tools both call the same logic. |
| LangGraph agent service | `portal-survey-agent/graph.py` defines the graph nodes and CRUD branches. `portal-survey-agent/main.py` exposes `POST /agent/query`. |
| Natural-language create workflow | Agent extracts available fields, stores a per-session survey draft, asks for missing required fields, summarizes, and waits for confirmation before calling `create_survey`. |
| Natural-language read workflow | Agent handles list/search/count style queries and calls list/search tools. |
| Natural-language update workflow | Agent resolves the target survey, extracts changes, shows the target and proposed update, and waits for confirmation. |
| Natural-language delete workflow | Agent resolves the target survey, displays details, and deletes only after explicit confirmation. |
| React conversational UI | `portal-survey-ui/src/pages/AISurveyAssistantPage.tsx` adds the AI Survey Assistant with input, transcript, examples, and confirmation buttons. |
| Kubernetes + Helm deployment | `portal-charts` now deploys frontend, MCP backend, agent service, services, secrets, and ingress paths. |
| Architecture/design/demo docs | See `docs/design.md` and `docs/demo-script.md`. |

## Additional Enhancements Added

- The original REST API remains available for traditional CRUD and Swagger testing.
- The MCP backend and REST API share one service layer so validation and persistence behavior stay consistent.
- The agent can use an OpenAI model when `OPENAI_API_KEY` is provided, but it has deterministic fallback logic for classroom demos when no API key is available.
- The UI Nginx container proxies `/api` and `/agent-api`, so the React app can work through the UI NodePort as well as ingress.
- Helm stores the OpenAI API key in a Kubernetes Secret.
- The chart supports both external RDS and optional in-cluster MySQL, preserving the HW3 deployment path.

## Repository Structure

```text
portal-survey-api/       FastAPI REST API plus FastMCP tool server
portal-survey-agent/     LangGraph agent service
portal-survey-ui/        React/Vite UI with AI Survey Assistant page
portal-charts/           Helm chart for UI, agent, backend, and database config
docs/                    Architecture, design, and demo documentation
```

## Local Development

Backend API:

```bash
cd portal-survey-api
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp env.example .env
uvicorn main:app --reload --port 8000
```

Agent service:

```bash
cd portal-survey-agent
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export API_BASE_URL=http://localhost:8000
export MCP_SERVER_URL=http://localhost:8000/mcp
export OPENAI_API_KEY=<optional>
uvicorn main:app --reload --port 8001
```

Frontend:

```bash
cd portal-survey-ui
npm install
VITE_API_BASE_URL=http://localhost:8000 \
VITE_AGENT_BASE_URL=http://localhost:8001 \
npm run dev
```

## Agent Endpoint

```bash
curl -X POST http://localhost:8001/agent/query \
  -H 'Content-Type: application/json' \
  -d '{"message":"Show all surveys where students liked dorm rooms"}'
```

For multi-turn conversations, pass the returned `session_id` in the next request:

```bash
curl -X POST http://localhost:8001/agent/query \
  -H 'Content-Type: application/json' \
  -d '{"session_id":"<SESSION_ID>","message":"yes"}'
```

## MCP Inspector

After starting the backend API, inspect the tool server at:

```text
http://localhost:8000/mcp
```

Required tools to verify in MCP Inspector:

- `create_survey`
- `list_surveys`
- `get_survey_by_id`
- `search_surveys`
- `update_survey`
- `delete_survey`

## Build Images

```bash
docker build --platform linux/amd64 -f portal-survey-api/docker/Dockerfile \
  -t <dockerhub-user>/portal-survey-api:latest portal-survey-api

docker build --platform linux/amd64 -f portal-survey-agent/docker/Dockerfile \
  -t <dockerhub-user>/swe645-survey-agent:latest portal-survey-agent

docker build --platform linux/amd64 -f portal-survey-ui/docker/Dockerfile \
  --build-arg VITE_API_BASE_URL=/api \
  --build-arg VITE_AGENT_BASE_URL=/agent-api \
  -t <dockerhub-user>/portal-survey-ui:latest portal-survey-ui
```

Update `portal-charts/values.yaml` with your image repositories before deployment.

## Deploy With Helm

```bash
helm upgrade --install portal-survey ./portal-charts \
  -n portal-survey \
  --create-namespace \
  --set externalDatabase.host="$DB_HOST" \
  --set externalDatabase.user="$DB_USER" \
  --set externalDatabase.password="$DB_PASSWORD" \
  --set secrets.jwt_secret_key="$JWT_SECRET_KEY" \
  --set secrets.openai_api_key="$OPENAI_API_KEY"
```

Verify:

```bash
kubectl get pods -n portal-survey
kubectl get svc -n portal-survey
kubectl logs deploy/portal-survey-agent -n portal-survey
```

Expected pods:

- `portal-survey-ui`
- `portal-survey-agent`
- `portal-survey-api`
- optional `portal-survey-mysql` if in-cluster MySQL is enabled

## Validation Notes

Completed locally:

- Python syntax check for API and agent files.
- `helm template portal-survey ./portal-charts`.

Not completed in this Codex desktop environment:

- `npm run build`, because no `npm`, `pnpm`, or `yarn` executable is installed and this cloned repo does not include `node_modules`.
