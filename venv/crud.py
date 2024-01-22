from sqlalchemy.orm import Session
import uuid
import models, schemas


def get_menus(db: Session):
    return db.query(models.Menu).offset(0).all()


def get_menu(db: Session, menu_id: str):
    return db.query(models.Menu).filter(models.Menu.id == menu_id).first()


def create_menu(db: Session, menu: schemas.MenuInfo):
    db_menu = models.Menu(id=str(uuid.uuid4()),
                          title=menu.title,
                          description=menu.description,
                          submenus_count=0,
                          dishes_count=0)
    db.add(db_menu)
    db.commit()
    db.refresh(db_menu)
    return db_menu


def update_menu(db: Session, menu_id: str, menu: schemas.MenuInfo):
    db.query(models.Menu).filter(models.Menu.id == menu_id) \
        .update({'title': menu.title, 'description': menu.description})
    db.commit()
    return get_menu(db, menu_id=menu_id)


def delete_menu(db: Session, menu_id: str):
    del_menu = db.query(models.Menu).filter(models.Menu.id == menu_id).first()
    db.delete(del_menu)
    db.commit()
    return del_menu


def get_submenus(db: Session, menu_id: str):
    return db.query(models.Submenu).filter(models.Submenu.menu_id == menu_id).offset(0).all()


def create_submenu(db: Session, submenu: schemas.SubmenuInfo, menu_id: str):
    db_submenu = models.Submenu(id=str(uuid.uuid4()),
                                title=submenu.title,
                                description=submenu.description,
                                dishes_count=0,
                                menu_id=menu_id)
    db.add(db_submenu)
    db.query(models.Menu).filter(models.Menu.id == menu_id).update({'submenus_count': models.Menu.submenus_count + 1})
    db.commit()
    db.refresh(db_submenu)
    return db_submenu


def get_submenu(db: Session, menu_id: str, submenu_id: str):
    return db.query(models.Submenu).filter(
        models.Submenu.id == submenu_id and models.Submenu.menu_id == menu_id).first()


def update_submenu(db: Session, menu_id: str, submenu_id: str, submenu: schemas.SubmenuInfo):
    db.query(models.Submenu).filter(models.Submenu.id == submenu_id and models.Submenu.menu_id == menu_id) \
        .update({'title': submenu.title, 'description': submenu.description})
    db.commit()
    return get_submenu(db, menu_id=menu_id, submenu_id=submenu_id)


def delete_submenu(db: Session, menu_id: str, submenu_id: str):
    del_count_dishes = len(db.query(models.Dish).filter(models.Dish.submenu_id == submenu_id).offset(0).all())
    del_submenu = db.query(models.Submenu) \
        .filter(models.Submenu.id == submenu_id and models.Submenu.menu_id == menu_id).first()
    db.delete(del_submenu)
    db.query(models.Menu).filter(models.Menu.id == menu_id) \
        .update({'submenus_count': models.Menu.submenus_count - 1,
                 'dishes_count': models.Menu.dishes_count - del_count_dishes})
    db.commit()
    return del_submenu


def get_dishes(db: Session, submenu_id: str):
    return db.query(models.Dish).filter(models.Dish.submenu_id == submenu_id).offset(0).all()


def get_dish(db: Session, submenu_id: str, dish_id: str):
    return db.query(models.Dish).filter(
        models.Dish.id == dish_id and models.Dish.submenu_id == submenu_id).first()


def create_dish(db: Session, submenu_id: str, menu_id: str, dish: schemas.DishInfo):
    db_dish = models.Dish(id=str(uuid.uuid4()),
                          title=dish.title,
                          description=dish.description,
                          price=dish.price,
                          submenu_id=submenu_id)
    db.add(db_dish)
    db.query(models.Submenu).filter(models.Submenu.id == submenu_id and models.Submenu.menu_id == menu_id).update(
        {'dishes_count': models.Submenu.dishes_count + 1})
    db.query(models.Menu).filter(models.Menu.id == menu_id).update({'dishes_count': models.Menu.dishes_count + 1})
    db.commit()
    db.refresh(db_dish)
    return db_dish


def update_dish(db: Session, submenu_id: str, dish_id: str, dish: schemas.DishInfo):
    db.query(models.Dish).filter(models.Dish.id == dish_id and models.Dish.submenu_id == submenu_id) \
        .update({'title': dish.title, 'description': dish.description, 'price': dish.price})
    db.commit()
    return get_dish(db, submenu_id=submenu_id, dish_id=dish_id)


def delete_dish(db: Session, menu_id: str, submenu_id: str, dish_id: str):
    del_dish = db.query(models.Dish).filter(models.Dish.id == dish_id and models.Dish.submenu_id == submenu_id).first()
    db.delete(del_dish)
    db.query(models.Submenu).filter(models.Submenu.id == submenu_id and models.Submenu.menu_id == menu_id).update(
        {'dishes_count': models.Submenu.dishes_count - 1})
    db.query(models.Menu).filter(models.Menu.id == menu_id).update({'dishes_count': models.Menu.dishes_count - 1})
    db.commit()
    return del_dish
