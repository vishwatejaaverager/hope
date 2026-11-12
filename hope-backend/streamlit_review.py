"""Local chat harness for the Hope document reviewer."""
import base64
import json
from datetime import date
from copy import deepcopy
from io import BytesIO
from uuid import uuid4

import requests
import streamlit as st

from app.services.ai_service import (DEFAULT_VISION_MODEL, OPENROUTER_URL, get_openrouter_api_key,
                                    draft_review_email, DOCUMENT_VERIFICATION_PROMPT, analyze_incoming_email)
from app.services.approval_policy import constrain_email_analysis

st.set_page_config(page_title="Hope review tester", layout="wide")
st.title("Hope review tester")
st.caption("Email preview · Optional read-only case connection · No email or payouts")
def reset_case():
    for key in ("turns", "case", "requests", "result", "email_case"):
        st.session_state.pop(key, None)

mode = st.sidebar.radio("Test mode", ["Custom prompt", "Email flow"], on_change=reset_case)
st.sidebar.button("Reset case", on_click=reset_case)

if mode == "Email flow":
    case_number = st.sidebar.text_input("Existing case number", placeholder="CASE-2026-…")
    if st.sidebar.button("Load saved case", disabled=not case_number.strip()):
        from app.services.document_review_store import load_case_preview
        try:
            loaded = load_case_preview(case_number)
        except Exception:
            st.sidebar.error("Could not read the case database. Check the backend database configuration.")
        else:
            if loaded is None:
                st.sidebar.warning("Case not found.")
            else:
                reset_case()
                st.session_state.email_case = loaded
    loaded_number = st.session_state.get("email_case", {}).get("case_number")
    if loaded_number:
        st.sidebar.caption(f"Previewing {loaded_number} from PostgreSQL. Test replies stay local.")


for key, default in (("turns", []), ("case", []), ("requests", []), ("result", None)):
    if key not in st.session_state:
        st.session_state[key] = default

chat, inspector = st.columns(2)
prompt = ""
with inspector:
    prompt = st.text_area("Your system prompt", value=DOCUMENT_VERIFICATION_PROMPT, height=220, key="custom_prompt")
    if not prompt.strip():
        st.caption("Enter a prompt to start testing.")
with chat:
    for role, body in st.session_state.turns:
        with st.chat_message(role):
            if isinstance(body, (dict, list)):
                st.json(body)
            else:
                st.write(body)
    turn = st.chat_input("Write a message or attach documents", accept_file="multiple",
                         file_type=["png", "jpg", "jpeg", "webp", "pdf", "txt"],
                         max_upload_size=10, disabled=not get_openrouter_api_key() or not prompt.strip())
    if not get_openrouter_api_key():
        st.info("Set OPENROUTER_API_KEY in hope-backend/.env and restart.")
    if turn:
        attachments = []
        for upload in turn.files:
            data = upload.getvalue()
            item = {"document_id": str(uuid4()), "filename": upload.name, "content_type": upload.type}
            try:
                if upload.type.startswith("image/"):
                    item["url"] = f"data:{upload.type};base64," + base64.b64encode(data).decode()
                elif upload.name.lower().endswith(".pdf"):
                    from pypdf import PdfReader
                    reader = PdfReader(BytesIO(data))
                    item["extracted_text"] = "\n".join(page.extract_text() or "" for page in reader.pages[:10])[:3000]
                else:
                    item["extracted_text"] = data.decode("utf-8", errors="replace")[:3000]
            except Exception:
                st.warning(f"Could not extract text from {upload.name}.")
            attachments.append(item)
        if sum(item.get("url", "").startswith("data:image/") for item in attachments) > 4:
            st.error("Send up to four images per message.")
            st.stop()
        display = turn.text + ("\n\nAttachments: " + ", ".join(f.name for f in turn.files) if turn.files else "")
        st.session_state.turns.append(("user", display))
        st.session_state.requests = []

        def inspect(payload):
            copy = deepcopy(payload)
            for message in copy["messages"]:
                if isinstance(message["content"], list):
                    for part in message["content"]:
                        if part["type"] == "image_url":
                            url = part["image_url"]["url"]
                            part["image_url"]["url"] = f"[Uploaded image bytes omitted: {url.split(',')[0]}]"
            st.session_state.requests.append(copy)

        if mode == "Email flow":
            case = st.session_state.get("email_case", {})
            sender = case.get("patient_email") or "test@example.invalid"
            subject = f"Re: {case['case_number']}" if case.get("case_number") else "Local email review"
            with st.spinner("Reviewing documents and drafting the reply…"):
                result = analyze_incoming_email(sender, subject, turn.text, attachments, case,
                                                document_prompt=prompt, inspect_request=inspect)
                if result.get("analysis_status") == "completed":
                    if case.get("requested_amount") is not None:
                        result["requested_amount"] = case["requested_amount"]
                    result = constrain_email_analysis(
                        result, sender, subject, turn.text, attachments,
                        existing_evidence=case.get("verification_evidence"),
                        existing_issues=case.get("verification_issues"),
                        existing_report=case.get("review_report"),
                    )
                    st.session_state.email_case = {**case, **{key: result.get(key, case.get(key)) for key in (
                        "patient_name", "hospital_name", "requested_amount", "verification_evidence",
                        "verification_issues", "review_report", "overall_summary", "status",
                    )}}
                    result["auto_reply_body"] = draft_review_email(
                        result, case.get("case_number") or "LOCAL-TEST", incoming_email={"subject": subject, "body": turn.text},
                        inspect_request=inspect,
                    )
            st.session_state.result = result
            st.session_state.turns.append(("assistant", result.get("auto_reply_body") or "No draft returned."))
            st.rerun()

        context = json.dumps(st.session_state.case[-8:])
        files = [{k: v for k, v in item.items() if k != "url"} for item in attachments]
        content = [{"type": "text", "text": (
            f"Review date: {date.today().isoformat()}\n"
            f"Previous test turns: {context}\nCurrent message: {turn.text}\n"
            f"Current attachments (images follow in file order): {json.dumps(files)}"
        )}]
        content.extend({"type": "image_url", "image_url": {"url": item["url"]}}
                       for item in attachments if "url" in item)
        payload = {
            "model": DEFAULT_VISION_MODEL,
            "messages": [{"role": "system", "content": prompt}, {"role": "user", "content": content}],
            "temperature": 0.1,
            "max_tokens": 2048,
        }
        inspect(payload)
        with st.spinner("Reviewing…"):
            try:
                response = requests.post(OPENROUTER_URL, json=payload, timeout=30,
                                         headers={"Authorization": f"Bearer {get_openrouter_api_key()}"})
                response.raise_for_status()
                reply = response.json()["choices"][0]["message"]["content"]
                try:
                    verdict = json.loads(reply)
                except ValueError:
                    verdict = reply
                st.session_state.case.append({"message": display, "verdict": verdict})
            except (requests.RequestException, ValueError, KeyError, IndexError, TypeError):
                verdict = {"is_verified": False, "red_flags": ["The model request failed. Try again."]}
        st.session_state.result = verdict
        st.session_state.turns.append(("assistant", verdict))
        st.rerun()

with inspector:
    st.subheader("Model input")
    if not st.session_state.requests:
        st.caption("Send a message to inspect the request.")
    for index, request in enumerate(st.session_state.requests, 1):
        with st.expander(f"Attempt {index}: {request['model']}", expanded=True):
            st.json(request)
    if st.session_state.result:
        with st.expander("Final review result"):
            st.json(st.session_state.result)
