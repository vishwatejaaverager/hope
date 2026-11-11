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
                                    draft_review_email, DOCUMENT_VERIFICATION_PROMPT, parse_document_verdict)
from app.services.case_review import REQUIRED_DOCUMENTS

st.set_page_config(page_title="Hope review tester", layout="wide")
st.title("Hope review tester")
st.caption("Local session · No email, database writes, or payouts")
def reset_case():
    for key in ("turns", "case", "requests", "result", "email_case"):
        st.session_state.pop(key, None)

mode = st.sidebar.radio("Test mode", ["Custom prompt", "Email flow"], on_change=reset_case)
st.sidebar.button("Reset case", on_click=reset_case)

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

        if mode == "Email flow" and len(attachments) != 1:
            st.session_state.turns.append(("assistant", "Attach one document per message in Email flow so its verdict is unambiguous."))
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
        if mode == "Email flow":
            try:
                normalized = parse_document_verdict(verdict)
            except ValueError:
                st.session_state.result = verdict
                st.session_state.turns.append(("assistant", "Your prompt must return JSON with doc_type, is_verified, and red_flags. No email was drafted."))
                st.rerun()
            kind, verified, flags = normalized["doc_type"], normalized["is_verified"], normalized["red_flags"]
            case = st.session_state.get("email_case", {})
            case[kind] = {"document_type": kind, "is_verified": verified, "flags": flags}
            st.session_state.email_case = case
            report = {
                "document_checks": [case[kind]],
                "document_statuses": {
                    doc_type: {"label": label, "status": (
                        "approved" if case[doc_type]["is_verified"] else "needs_review"
                    ) if doc_type in case else "missing"}
                    for doc_type, label in REQUIRED_DOCUMENTS.items()
                },
                "red_flags": [
                    {"message": flag} for doc_type, doc in case.items() if doc_type != kind for flag in doc["flags"]
                ],
            }
            with st.spinner("Drafting the email…"):
                draft = draft_review_email({"review_report": report}, "LOCAL-TEST", inspect_request=inspect)
            st.session_state.result = {"document_analysis": verdict, "review_report": report}
            st.session_state.turns.append(("assistant", draft))
            st.rerun()

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
