from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from typing import List

import crud
import database
import schemas

database.Base.metadata.create_all(bind=database.engine)

app = FastAPI()


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/api/v1/menus", response_model=List[schemas.Menu])
def read_menus(db: Session = Depends(get_db)):
    return crud.get_menus(db)


@app.get("/api/v1/menus/{menu_id}", response_model=schemas.Menu)
def read_menu(menu_id: str, db: Session = Depends(get_db)):
    db_menu = crud.get_menu(db, menu_id=menu_id)
    if db_menu is None:
        raise HTTPException(status_code=404, detail="menu not found")
    return db_menu


@app.post("/api/v1/menus", response_model=schemas.Menu, status_code=201)
def create_menu(menu: schemas.MenuInfo, db: Session = Depends(get_db)):
    return crud.create_menu(db=db, menu=menu)


@app.patch("/api/v1/menus/{menu_id}", response_model=schemas.Menu)
def update_menu(menu_id: str, menu: schemas.MenuInfo, db: Session = Depends(get_db)):
    db_menu = crud.get_menu(db, menu_id=menu_id)
    if db_menu is None:
        raise HTTPException(status_code=404, detail="menu not found")
    upd_menu = crud.update_menu(db, menu_id=menu_id, menu=menu)
    return upd_menu


@app.delete("/api/v1/menus/{menu_id}")
def delete_menu(menu_id: str, db: Session = Depends(get_db)):
    db_menu = crud.get_menu(db, menu_id=menu_id)
    if db_menu is None:
        raise HTTPException(status_code=404, detail="menu not found")
    del_menu = crud.delete_menu(db, menu_id=menu_id)
    if not del_menu:
        raise HTTPException(status_code=500, detail="error delete")
    return {"status": True, "message": "The menu has been deleted"}


@app.get("/api/v1/menus/{menu_id}/submenus", response_model=List[schemas.Submenu])
def read_submenus(menu_id: str, db: Session = Depends(get_db)):
    return crud.get_submenus(db, menu_id=menu_id)


@app.post("/api/v1/menus/{menu_id}/submenus", response_model=schemas.Submenu, status_code=201)
def create_submenu(submenu: schemas.SubmenuInfo, menu_id: str, db: Session = Depends(get_db)):
    db_menu = crud.get_menu(db=db, menu_id=menu_id)
    if db_menu is None:
        raise HTTPException(status_code=404, detail="menu not found")
    return crud.create_submenu(db=db, submenu=submenu, menu_id=menu_id)


@app.get("/api/v1/menus/{menu_id}/submenus/{submenu_id}", response_model=schemas.Submenu)
def read_submenu(menu_id: str, submenu_id: str, db: Session = Depends(get_db)):
    db_submenu = crud.get_submenu(db, menu_id=menu_id, submenu_id=submenu_id)
    if db_submenu is None:
        raise HTTPException(status_code=404, detail="submenu not found")
    return db_submenu


@app.patch("/api/v1/menus/{menu_id}/submenus/{submenu_id}", response_model=schemas.Submenu)
def update_submenu(menu_id: str, submenu_id: str, submenu: schemas.SubmenuInfo, db: Session = Depends(get_db)):
    db_submenu = crud.get_submenu(db, menu_id=menu_id, submenu_id=submenu_id)
    if db_submenu is None:
        raise HTTPException(status_code=404, detail="submenu not found")
    upd_submenu = crud.update_submenu(db, menu_id=menu_id, submenu_id=submenu_id, submenu=submenu)
    return upd_submenu


@app.delete("/api/v1/menus/{menu_id}/submenus/{submenu_id}")
def delete_submenu(menu_id: str, submenu_id: str, db: Session = Depends(get_db)):
    db_submenu = crud.get_submenu(db, menu_id=menu_id, submenu_id=submenu_id)
    if db_submenu is None:
        raise HTTPException(status_code=404, detail="submenu not found")
    del_submenu = crud.delete_submenu(db, menu_id=menu_id, submenu_id=submenu_id)
    if not del_submenu:
        raise HTTPException(status_code=500, detail="error delete")
    return {"status": True, "message": "The submenu has been deleted"}


@app.get("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes", response_model=List[schemas.Dish])
def read_dishes(submenu_id: str, db: Session = Depends(get_db)):
    return crud.get_dishes(db, submenu_id=submenu_id)


@app.get("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}", response_model=schemas.Dish)
def read_dish(submenu_id: str, dish_id: str, db: Session = Depends(get_db)):
    db_dish = crud.get_dish(db, submenu_id=submenu_id, dish_id=dish_id)
    if db_dish is None:
        raise HTTPException(status_code=404, detail="dish not found")
    return db_dish


@app.post("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes", response_model=schemas.Dish, status_code=201)
def create_dish(submenu_id: str, menu_id: str, dish: schemas.DishInfo, db: Session = Depends(get_db)):
    db_submenu = crud.get_submenu(db=db, menu_id=menu_id, submenu_id=submenu_id)
    db_menu = crud.get_menu(db=db, menu_id=menu_id)
    if db_submenu is None or db_menu is None:
        raise HTTPException(status_code=404, detail="menu or submenu not found")
    return crud.create_dish(db=db, submenu_id=submenu_id, menu_id=menu_id, dish=dish)


@app.patch("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}", response_model=schemas.Dish)
def update_dish(submenu_id: str, dish_id: str, dish: schemas.DishInfo, db: Session = Depends(get_db)):
    db_dish = crud.get_dish(db, submenu_id=submenu_id, dish_id=dish_id)
    if db_dish is None:
        raise HTTPException(status_code=404, detail="dish not found")
    upd_submenu = crud.update_dish(db, submenu_id=submenu_id, dish_id=dish_id, dish=dish)
    return upd_submenu


@app.delete("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}")
def delete_dish(menu_id: str, submenu_id: str, dish_id: str, db: Session = Depends(get_db)):
    db_dish = crud.get_dish(db, submenu_id=submenu_id, dish_id=dish_id)
    if db_dish is None:
        raise HTTPException(status_code=404, detail="submenu not found")
    del_dish = crud.delete_dish(db, menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id)
    if not del_dish:
        raise HTTPException(status_code=500, detail="error delete")
    return {"status": True, "message": "The dish has been deleted"}
