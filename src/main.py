from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.responses import JSONResponse
import logging
import os

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

app = FastAPI(title="SecureCICD Validator")

# Load list of allowed approvers
ALLOWED_APPROVERS = os.getenv("ALLOWED_APPROVERS", "svc-release,release-admin").split(",")

class ApprovalCheckRequest(BaseModel):
    approver: str
    author: str
    reassigned: bool = False
    pipeline_id: str
    commit_id: str

@app.post("/validate-approval")
async def validate_approval(data: ApprovalCheckRequest):
    logging.info(f"Validating approval in pipeline '{data.pipeline_id}' for commit '{data.commit_id}'")

    try:
        approver = data.approver.strip().lower()
        author = data.author.strip().lower()

        if data.reassigned:
            logging.warning(f"Approval reassigned by {approver} in {data.pipeline_id}")
            raise HTTPException(status_code=403, detail="Reassignment of approval is not allowed.")

        if approver == author:
            logging.warning(f"Self-approval attempt by {approver} in {data.pipeline_id}")
            raise HTTPException(status_code=403, detail="Self-approval is not allowed.")

        if approver not in [a.strip().lower() for a in ALLOWED_APPROVERS]:
            logging.warning(f"Unauthorized approver: {approver} for pipeline {data.pipeline_id}")
            raise HTTPException(status_code=403, detail="Approver not in allowed list.")

        logging.info(f"Approval validated successfully by {approver} for pipeline {data.pipeline_id}")
        return {"status": "success", "message": "Approval validated"}

    except HTTPException as he:
        return JSONResponse(status_code=he.status_code, content={"status": "error", "detail": he.detail})

    except Exception as e:
        logging.exception("Unexpected error during validation")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/health")
async def health():
    return {"status": "ok"}
