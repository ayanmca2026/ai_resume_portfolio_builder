from fastapi import APIRouter, Depends, HTTPException, status, Request, Form, Response
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse, RedirectResponse
from app.database.database import get_db
from app.models.user import User
from app.core.security import verify_password, get_password_hash, create_access_token
from app.core.config import settings

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse(request, "auth/login.html", {"request": request})

@router.post("/login")
async def login(
    response: Response,
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.hashed_password):
        return templates.TemplateResponse(request, "auth/login.html", {"request": {}, "error": "Invalid credentials"})
    
    access_token = create_access_token(data={"sub": user.email})
    redirect_resp = RedirectResponse(url="/dashboard", status_code=status.HTTP_302_FOUND)
    redirect_resp.set_cookie(
        key="access_token",
        value=f"Bearer {access_token}",
        httponly=True,
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        samesite="lax"
    )
    return redirect_resp

@router.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse(request, "auth/register.html", {"request": request})

@router.post("/register")
async def register(
    email: str = Form(...),
    password: str = Form(...),
    full_name: str = Form(...),
    db: Session = Depends(get_db)
):
    db_user = db.query(User).filter(User.email == email).first()
    if db_user:
        return templates.TemplateResponse("auth/register.html", {"request": {}, "error": "Email already registered"})
    
    hashed_password = get_password_hash(password)
    new_user = User(email=email, hashed_password=hashed_password, full_name=full_name)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return RedirectResponse(url="/auth/login", status_code=status.HTTP_302_FOUND)

@router.get("/logout")
async def logout():
    response = RedirectResponse(url="/auth/login", status_code=status.HTTP_302_FOUND)
    response.delete_cookie("access_token")
    return response

def get_current_user_from_cookie(request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    token = token.replace("Bearer ", "")
    from jose import jwt, JWTError
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Not authenticated")
    except JWTError:
        raise HTTPException(status_code=401, detail="Not authenticated")
        
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return user
