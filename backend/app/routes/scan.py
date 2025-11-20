from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect

from ..database import get_session
from ..models import Identity, ScanLog
from ..schemas.scan import ScanRequest, ScanResponse
from ..services.verification import decode_secure_token, verify_payload

router = APIRouter(prefix="/scan", tags=["verification"])


class ConnectionManager:
    def __init__(self):
        self.connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.connections:
            self.connections.remove(websocket)

    async def broadcast(self, message: dict):
        for connection in list(self.connections):
            try:
                await connection.send_json(message)
            except WebSocketDisconnect:
                self.disconnect(connection)


manager = ConnectionManager()


@router.post("/verify", response_model=ScanResponse)
async def verify_identity(payload: ScanRequest, session=Depends(get_session)):
    try:
        claims = decode_secure_token(payload.token)
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=400, detail="Token invalid") from exc

    if not verify_payload(claims):
        raise HTTPException(status_code=400, detail="Token expired")

    identity = session.get(Identity, int(claims["sub"]))
    if not identity:
        raise HTTPException(status_code=404, detail="Identity missing")

    log = ScanLog(
        identity_id=identity.id,
        scan_channel=payload.channel,
        location=payload.location,
        result="approved",
    )
    session.add(log)
    session.commit()
    session.refresh(log)

    response = ScanResponse(
        identity_id=identity.id,
        status="approved",
        full_name=f"{identity.first_name} {identity.last_name}",
        role=identity.role,
        verified_at=log.created_at,
    )
    await manager.broadcast(
        {
            "identity_id": identity.id,
            "full_name": response.full_name,
            "role": response.role,
            "timestamp": response.verified_at.isoformat(),
            "location": payload.location,
            "channel": payload.channel,
        }
    )

    return response


@router.websocket("/live")
async def live_scans(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)

