from fastapi import Depends, FastAPI, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from .db import Base, engine, get_db
from .models import Asset, ChangeRecord, Service
from .schemas import AssetCreate, ChangeCreate, ServiceCreate

app = FastAPI(title="Lightweight CMDB", version="0.1.0")
Base.metadata.create_all(bind=engine)

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")


@app.get("/healthz")
def healthz():
    return {"status": "ok"}


@app.get("/", response_class=HTMLResponse)
def index(
    request: Request,
    q: str = "",
    status: str = "",
    db: Session = Depends(get_db),
):
    asset_query = select(Asset)
    if q:
        pattern = f"%{q}%"
        asset_query = asset_query.where(or_(Asset.hostname.like(pattern), Asset.ip.like(pattern), Asset.owner.like(pattern)))
    if status:
        asset_query = asset_query.where(Asset.status == status)

    assets = db.execute(asset_query.order_by(Asset.id.desc())).scalars().all()
    services = db.execute(select(Service).order_by(Service.id.desc())).scalars().all()
    changes = db.execute(select(ChangeRecord).order_by(ChangeRecord.id.desc())).scalars().all()
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "assets": assets,
            "services": services,
            "changes": changes,
            "q": q,
            "status": status,
        },
    )


@app.post("/assets")
def create_asset(
    hostname: str = Form(...),
    ip: str = Form(...),
    environment: str = Form("prod"),
    os: str = Form("linux"),
    owner: str = Form(""),
    status: str = Form("active"),
    note: str = Form(""),
    db: Session = Depends(get_db),
):
    payload = AssetCreate(hostname=hostname, ip=ip, environment=environment, os=os, owner=owner, status=status, note=note)
    duplicated = db.execute(select(Asset).where(or_(Asset.hostname == payload.hostname, Asset.ip == payload.ip))).scalar_one_or_none()
    if duplicated:
        raise HTTPException(status_code=400, detail="hostname or ip already exists")

    asset = Asset(**payload.model_dump())
    db.add(asset)
    db.commit()
    return RedirectResponse(url="/", status_code=303)


@app.post("/services")
def create_service(
    name: str = Form(...),
    asset_id: int = Form(...),
    repo_url: str = Form(""),
    deploy_method: str = Form("ansible"),
    owner: str = Form(""),
    status: str = Form("running"),
    note: str = Form(""),
    db: Session = Depends(get_db),
):
    payload = ServiceCreate(
        name=name,
        asset_id=asset_id,
        repo_url=repo_url,
        deploy_method=deploy_method,
        owner=owner,
        status=status,
        note=note,
    )
    asset = db.get(Asset, payload.asset_id)
    if not asset:
        raise HTTPException(status_code=404, detail="asset not found")

    duplicated = db.execute(select(Service).where(Service.name == payload.name)).scalar_one_or_none()
    if duplicated:
        raise HTTPException(status_code=400, detail="service already exists")

    service = Service(**payload.model_dump())
    db.add(service)
    db.commit()
    return RedirectResponse(url="/", status_code=303)


@app.post("/changes")
def create_change(
    title: str = Form(...),
    service_id: int = Form(...),
    risk_level: str = Form("medium"),
    change_window: str = Form(""),
    executor: str = Form(""),
    approver: str = Form(""),
    status: str = Form("pending"),
    rollback_plan: str = Form(""),
    db: Session = Depends(get_db),
):
    payload = ChangeCreate(
        title=title,
        service_id=service_id,
        risk_level=risk_level,
        change_window=change_window,
        executor=executor,
        approver=approver,
        status=status,
        rollback_plan=rollback_plan,
    )

    service = db.get(Service, payload.service_id)
    if not service:
        raise HTTPException(status_code=404, detail="service not found")

    change = ChangeRecord(**payload.model_dump())
    db.add(change)
    db.commit()
    return RedirectResponse(url="/", status_code=303)


@app.post("/assets/{asset_id}/delete")
def delete_asset(asset_id: int, db: Session = Depends(get_db)):
    asset = db.get(Asset, asset_id)
    if not asset:
        raise HTTPException(status_code=404, detail="asset not found")
    db.delete(asset)
    db.commit()
    return RedirectResponse(url="/", status_code=303)


@app.post("/services/{service_id}/delete")
def delete_service(service_id: int, db: Session = Depends(get_db)):
    service = db.get(Service, service_id)
    if not service:
        raise HTTPException(status_code=404, detail="service not found")
    db.delete(service)
    db.commit()
    return RedirectResponse(url="/", status_code=303)


@app.post("/changes/{change_id}/delete")
def delete_change(change_id: int, db: Session = Depends(get_db)):
    change = db.get(ChangeRecord, change_id)
    if not change:
        raise HTTPException(status_code=404, detail="change not found")
    db.delete(change)
    db.commit()
    return RedirectResponse(url="/", status_code=303)


@app.get("/api/assets")
def list_assets(db: Session = Depends(get_db)):
    assets = db.execute(select(Asset).order_by(Asset.id.desc())).scalars().all()
    return [
        {
            "id": a.id,
            "hostname": a.hostname,
            "ip": a.ip,
            "environment": a.environment,
            "os": a.os,
            "owner": a.owner,
            "status": a.status,
            "note": a.note,
        }
        for a in assets
    ]
