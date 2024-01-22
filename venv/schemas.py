from pydantic import BaseModel


class MenuId(BaseModel):
    id: str


class MenuInfo(BaseModel):
    title: str
    description: str


class Menu(MenuInfo, MenuId):
    submenus_count: int
    dishes_count: int

    class Config:
        from_attributes = True


class SubmenuId(BaseModel):
    id: str


class SubmenuInfo(BaseModel):
    title: str
    description: str


class Submenu(SubmenuInfo, SubmenuId):
    dishes_count: int

    class Config:
        from_attributes = True


class DishId(BaseModel):
    id: str


class DishInfo(BaseModel):
    title: str
    description: str
    price: str


class Dish(DishInfo, DishId):

    class Config:
        from_attributes = True
