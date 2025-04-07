# 🔐 SecureCICD — Integrity Validator for CI/CD Pipelines

> ✅ Prevent self-approvals  
> ✅ Detect reassigned approvals  
> ✅ Enforce runtime approver validation

---

## 🚨 Why SecureCICD?

In modern CI/CD platforms, **any user with pipeline permissions** can often:
- Approve their **own code**
- **Reassign** approvals to fake accounts
- Bypass role-based separation of duties (SoD)

SecureCICD closes this gap by enforcing **approval integrity at runtime**, even if the UI or DevOps permissions fail to.

---

## 🔧 How It Works

At deployment time, the pipeline calls:

```
POST /validate-approval
```

SecureCICD checks:
- Was the approver the original author?
- Was the approval reassigned?
- Is the approver on the approved allowlist (env-based or group-based)?

If any check fails → `403 Forbidden`

---

## 📦 Example: GitHub Action Integration

```yaml
- name: Validate approval
  run: |
    curl -X POST https://securecicd.com/validate-approval \
      -H "Content-Type: application/json" \
      -d '{
        "approver": "${{ github.actor }}",
        "author": "${{ github.event.commits[0].author.name }}",
        "reassigned": false,
        "pipeline_id": "${{ github.workflow }}",
        "commit_id": "${{ github.sha }}"
      }'
```

---

## 🧪 Local Testing

```bash
uvicorn src.main:app --reload
curl http://localhost:8000/health
```

---

## ✅ API Contract

```json
{
  "approver": "release-admin",
  "author": "developer-a",
  "reassigned": false,
  "pipeline_id": "deploy-prod",
  "commit_id": "abc123def"
}
```

### Errors returned:
- `403 Self-approval not allowed`
- `403 Approval reassignment not allowed`
- `403 Approver not in allowlist`

---

## 📁 Project Structure

```txt
SecureCICD/
├── src/                   # FastAPI validator
├── tests/                # Unit tests
├── .github/actions/      # GitHub integration
├── .azuredevops-extension/ # Azure Pipelines task
├── docs/                 # Static site + blog (GitHub Pages)
├── README.md             # Developer quickstart
├── DEPLOYMENT.md         # DevOps/SecOps integration guide
├── ARCHITECTURE.md       # Internal system design
```

---

## 📌 Compliance & Risk Relevance

SecureCICD is directly aligned with:

- **OWASP CI/CD Top 10**
- **SOC 2 / SOX separation of duties**
- **DORA** approval integrity requirements
- **GitHub Enterprise / Azure DevOps audit trail goals**

---

## 🔓 License

MIT – Free for commercial and private use.  
Created by **NextSecurity** 🛡️
