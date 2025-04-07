# 📦 SecureCICD Deployment Guide

> **For DevOps, SecOps, and Platform Engineering**  
> A NextSecurity Project – Enforce runtime approval policies in CI/CD pipelines.

---

## 🏗️ Deployment Models

SecureCICD is designed to run as a centralized runtime validation service:

| Environment | Description |
|-------------|-------------|
| Docker (Default) | Easy to run anywhere, local or server |
| Kubernetes (K8s) | Scalable deployment using ConfigMap for policies |
| AWS Fargate / Cloud Run | Serverless, secure perimeter, stateless |
| Azure Web App | Optional PaaS deployment |

---

## 🛠️ Docker Deployment (Quickstart)

```bash
docker run -d -p 8080:8080 \
  -e ALLOWED_APPROVERS="svc-release,secops,ENG\\DevLeads,SEC\\Architects" \
  --name securecicd nextsecurity/securecicd:latest
```

---

## 🔐 Environment Variables

| Variable | Purpose |
|----------|---------|
| `ALLOWED_APPROVERS` | Comma-separated list of trusted usernames or groups |
| `LOG_LEVEL` | `info` or `debug` (default: info) |
| `PORT` | Optional override for default `8080` |

---

## 🔧 Integration: Azure DevOps

```yaml
- task: CurlUploader@1
  inputs:
    curlArgs: >
      -X POST $(SECURECICD_URL)/validate-approval
      -H "Content-Type: application/json"
      -d '{
        "approver":"$(Build.RequestedFor)",
        "author":"$(Build.QueuedBy)",
        "reassigned":false,
        "pipeline_id":"$(Build.DefinitionName)",
        "commit_id":"$(Build.SourceVersion)"
      }'
```

---

## 📊 Logging & Audit

SecureCICD logs every validation request:
- Approver, author, reassigned, pipeline ID, commit ID
- Result: pass/fail
- Output format: JSON (stdout, can redirect to log agent)

Recommended to send logs to:
- SIEM (Splunk, Datadog)
- S3 bucket
- Centralized audit store

---

## 🧱 Enforcing Modes

| Mode | Purpose |
|------|---------|
| **Passive** | Log violations, do not block |
| **Blocking** | `403 Forbidden` on violation (recommended) |
| **Hybrid** | Block prod only, log for others |

---

## 🧩 Scaling to Hundreds of Pipelines

SecureCICD is built for large organizations. Here's how to scale across 100+ pipelines:

### 🔁 GitHub Actions

- Create a **composite action** or Docker-based action
- Store in a central GitHub internal repo
- Reuse via:

```yaml
uses: your-org/securecicd-action@v1
```

### 🔁 Azure DevOps

- Package SecureCICD validation logic as a shared task
- Use `template.yml` to include it across projects
- Or inject into existing pipelines using task groups

### 📦 Template Strategy

| Platform | Method |
|----------|--------|
| GitHub   | Shared workflows or composite actions |
| Azure DevOps | Task groups or template `extends:` |
| GitLab   | `include:` |
| CircleCI | Reusable config blocks / orbs |

---

## 📌 Related OWASP CI/CD Top 10 Risks Mitigated

| OWASP Risk | SecureCICD Mitigation |
|------------|------------------------|
| **CICD-SEC-1: Unauthorized Deployments** | ✅ Blocks unapproved users |
| **CICD-SEC-2: Misconfig Pipelines** | ✅ Validates approvals at runtime |
| **CICD-SEC-7: Missing Approver Controls** | ✅ Self-approval and reassignment checks |
| **CICD-SEC-8: Insufficient Logging** | ✅ Full structured JSON audit |
| **CICD-SEC-10: Weak Access Control** | ✅ Enforced trusted groups via policy |

---

## 🛡️ Rollout Strategy (Enterprise)

1. Deploy SecureCICD in **logging mode** to 3–5 pilot pipelines
2. Review logs weekly with SecOps/Platform Eng
3. Harden allowlist (pull from AD/LDAP or ConfigMap)
4. Switch to **blocking mode** for prod pipelines
5. Expand org-wide as a required pipeline stage

---

## ✅ Requirements

- Python 3.10+ (if running from source)
- Docker 20+ (if containerized)
- Outbound access from pipelines (for `curl` or `Invoke-RestMethod`)

---

SecureCICD is built for real-world scale, security-first orgs, and visibility in every deployment decision.
