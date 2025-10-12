# liatrio-demo-app

A tiny FastAPI service that exposes a REST endpoint returning a static message and the current epoch timestamp. Packaged as a container image and Helm chart for Kubernetes.

## Tooling
- **Language**: Python 3.12
- **Package/Env manager**: [uv](https://github.com/astral-sh/uv)
- **Web framework**: FastAPI + Uvicorn
- **Container**: Docker
- **Kubernetes packaging**: Helm
- **CI**: GitHub Actions (tests, Docker publish, Helm lint, optional chart release to **AWS ECR (OCI)**)

## Endpoints
- `GET /api/v1/info` → `{ "message": "Automate all the things!", "timestamp": 1690000000 }`
- `GET /healthz` → health check
- `GET /` → basic service metadata

## Quick Start (Local with uv)
```bash
# Install uv (see project page) then:
uv venv --python 3.12
. .venv/bin/activate
uv pip install -e .[dev]
uv run pytest
uv run uvicorn app.main:app --reload --port 8080
curl localhost:8080/api/v1/info
```

## Build Container
```bash
docker build -t ghcr.io/your-org/liatrio-demo-app:0.1.0 .
docker run --rm -p 8080:8080 ghcr.io/your-org/liatrio-demo-app:0.1.0
```

## Helm Install
> Assumes you have a working Kubernetes cluster and `kubectl` + `helm` configured.

```bash
export IMAGE=ghcr.io/your-org/liatrio-demo-app
export TAG=0.1.0

helm upgrade --install liatrio-demo-app charts/liatrio-demo-app \
  --namespace demo --create-namespace \
  --set image.repository=$IMAGE --set image.tag=$TAG

kubectl -n demo port-forward svc/liatrio-demo-app 8080:80 &
curl localhost:8080/api/v1/info
```

### Ingress (optional)
```bash
helm upgrade --install liatrio-demo-app charts/liatrio-demo-app \
  -n demo --create-namespace \
  --set image.repository=$IMAGE --set image.tag=$TAG \
  --set ingress.enabled=true \
  --set ingress.className=alb \
  --set ingress.hosts[0].host=demo.example.com \
  --set ingress.hosts[0].paths[0].path=/ \
  --set ingress.hosts[0].paths[0].pathType=Prefix
```

## GitHub Actions Workflows
This repo includes workflows under `.github/workflows/`:
- **ci.yml**: unit tests with uv on pushes and PRs
- **docker-publish.yml**: build & push image to GHCR on pushes to `main` and version tags
- **helm-lint.yml**: lints the Helm chart on PRs
- **chart-oci-ecr.yml**: packages the chart and **pushes it to AWS ECR as an OCI artifact** on `chart-v*` tags

### Configure ECR (OCI) Chart Publishing
Set these repository secrets/vars in GitHub:
- `AWS_REGION` (e.g., `us-east-1`)
- **Auth**: either
  - `AWS_ROLE_TO_ASSUME` (recommended) **or**
  - `AWS_ACCESS_KEY_ID` / `AWS_SECRET_ACCESS_KEY` (least preferred)
- Optionally set `ECR_HELM_REPO` (defaults to `liatrio-demo-app-chart`).

Create a tag to publish:
```bash
git tag chart-v0.1.0 && git push origin chart-v0.1.0
```
The workflow will:
1. Assume role / use AWS creds
2. Ensure the ECR repo exists
3. `helm package` the chart
4. `helm push` to `oci://$ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_HELM_REPO`
```
bash
python -m venv .venv && . .venv/bin/activate
pip install -e .[dev]
pytest
uvicorn app.main:app --reload --port 8080
curl localhost:8080/api/v1/info
```

## Build Container
```bash
docker build -t ghcr.io/your-org/liatrio-demo-app:0.1.0 .
docker run --rm -p 8080:8080 ghcr.io/your-org/liatrio-demo-app:0.1.0
```

## Helm Install
> Assumes you have a working Kubernetes cluster and `kubectl` + `helm` configured.

```bash
# set your image repo/tag if different
export IMAGE=ghcr.io/your-org/liatrio-demo-app
export TAG=0.1.0

helm upgrade --install liatrio-demo-app charts/liatrio-demo-app \
  --namespace demo --create-namespace \
  --set image.repository=$IMAGE --set image.tag=$TAG

# Port-forward to test
kubectl -n demo port-forward svc/liatrio-demo-app 8080:80 &
curl localhost:8080/api/v1/info
```

### Ingress (optional)
```bash
helm upgrade --install liatrio-demo-app charts/liatrio-demo-app \
  -n demo --create-namespace \
  --set image.repository=$IMAGE --set image.tag=$TAG \
  --set ingress.enabled=true \
  --set ingress.className=alb \
  --set ingress.hosts[0].host=demo.example.com \
  --set ingress.hosts[0].paths[0].path=/ \
  --set ingress.hosts[0].paths[0].pathType=Prefix
```

## Automated Tests
- `pytest` runs a small suite validating the shape of `/api/v1/info` and health endpoint.

## Cleaning Up
```bash
helm uninstall liatrio-demo-app -n demo || true
```

## Next Steps (suggested)
- Add a GitHub Actions workflow to run tests and build/push the container image (e.g., GHCR or ECR).
- Wire up IaC (Pulumi or Terraform) to provision a low-cost EKS/GKE/AKS cluster and invoke the Helm release.
- Add a Helm chart `values.schema.json` for stronger validation.
- Add OpenAPI doc publishing and a basic k6 load test.

Directory tree
```
demo-app/
├─ app/
│  ├─ __init__.py
│  ├─ main.py
│  └─ version.py
├─ tests/
│  └─ test_api.py
├─ charts/
│  └─ liatrio-demo-app/
│     ├─ Chart.yaml
│     ├─ values.yaml
│     ├─ .helmignore
│     └─ templates/
│        ├─ deployment.yaml
│        ├─ service.yaml
│        ├─ ingress.yaml
│        ├─ hpa.yaml
│        ├─ NOTES.txt
│        └─ tests/
│           └─ test-connection.yaml
├─ .github/
│  └─ workflows/
│     ├─ ci.yml
│     ├─ docker-publish.yml
│     ├─ helm-lint.yml
│     └─ chart-oci-ecr.yml
├─ .gitignore
├─ Dockerfile
├─ Makefile
├─ pyproject.toml
└─ README.md
```
