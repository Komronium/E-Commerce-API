import re
from sqlalchemy.ext.declarative import as_declarative, declared_attr


@as_declarative()
class Base:
    id: int
    __name__: str

    @declared_attr
    def __tablename__(self) -> str:
        return re.sub(r'(?<=[a-z0-9])([A-Z])', r'_\1', self.__name__).lower()
        