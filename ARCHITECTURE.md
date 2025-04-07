# 🧠 SecureCICD Architecture

> A NextSecurity Project  
> Runtime enforcement of CI/CD approval policies for secure, compliant DevOps.

---

## 🏗️ System Overview

SecureCICD is a stateless validation microservice that enforces pipeline integrity **at runtime**.

It validates:
- Who approved the deployment?
- Who authored the code?
- Was the approval reassigned?
- Is the approver part of a trusted group?

---

## 🔧 Components

| Component | Purpose |
|----------|---------|
| **FastAPI Validator** | REST API for approval checks |
| **Environment Policy** | List of allowed approvers (can be extended to external API) |
| **CI/CD Client** | `curl` / `Invoke-RestMethod` from GitHub/Azure Pipelines |
| **Logger** | Outputs all decisions in JSON format |
| **(Optional)** Config Service | Dynamic policy backend (planned roadmap) |

---

## 📐 Component Diagram (Textual)

```
+----------------+       POST /validate-approval       +--------------------+
|  GitHub Action |  ---------------------------------> |  SecureCICD Server |
| or Azure Agent |                                    | (FastAPI Runtime)  |
+----------------+                                    +--------------------+
           |                                                    |
           |--- approver, author, pipeline_id, commit_id ------>|
           |                                                    |
           |<---------------- Result (200 / 403) ---------------|
```

---

## 🧪 API Contract

### POST `/validate-approval`

```json
{
  "approver": "svc-release",
  "author": "dev-a",
  "reassigned": false,
  "pipeline_id": "release-prod",
  "commit_id": "abc123"
}
```

### Response:

```json
{ "status": "success" }
```

or

```json
{ "status": "error", "detail": "Self-approval not allowed" }
```

---

## 🔐 Threat Model

| Threat | Mitigation |
|--------|------------|
| **Developer self-approves their own commit** | Blocked with `approver == author` rule |
| **Approver reassigns task to lower-permission account** | Blocked with `reassigned == true` check |
| **Non-whitelisted users approve critical pipelines** | Allowlist enforced from ENV or config backend |
| **CI system misconfig allows unrestricted approvals** | Runtime validation enforces SoD regardless of UI |
| **No traceability of who approved what** | JSON logging with full context |

---

## 🔄 Deployment Flow Summary

1. CI pipeline executes `curl` call to `/validate-approval`
2. SecureCICD parses input, applies rules
3. Logs every request + decision
4. Responds with allow/block
5. Pipeline proceeds only on HTTP 200

---

## 🔒 Security Principles

- No trust in pipeline UI / approvals
- Every deployment is verified *at the moment it happens*
- No shared secrets stored — policy comes from config/env
- Stateless, scalable, cloud-native

---

## 📊 Future Roadmap

| Feature | Status |
|---------|--------|
| Dynamic policy from LDAP/AD API | 🟡 Planned |
| SIEM push integration (Splunk, Datadog) | 🟡 Planned |
| GitHub App + Azure DevOps Extension Store | 🟢 MVP Complete |
| Centralized dashboard for audit reviews | 🟡 Planned |

---

## 📘 References

- OWASP Top 10 CI/CD Risks: https://owasp.org/www-project-cicd-security-top-10/
- DORA compliance (EU): https://digital-strategy.ec.europa.eu/en/policies/dora

---

Built for pipelines that demand security, auditability, and trust.
