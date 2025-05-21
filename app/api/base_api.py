from typing import Any, Callable, Generic, List, Type, TypeVar, Optional
from fastapi import APIRouter, Depends, HTTPException, params
from pydantic import BaseModel
from sqlalchemy.orm import Session as SQLAlchemySession

from app.services.base_service import BaseService

# --- Generic Types ---
# ModelType: Kiểu đối tượng mà service xử lý (ví dụ: ORM model hoặc Pydantic model như trong InMemoryRepo)
ModelType = TypeVar("ModelType")

# SchemaType: Pydantic schema cho response của API
SchemaType = TypeVar("SchemaType", bound=BaseModel)

# CreateSchemaType: Pydantic schema cho việc tạo mới (request body)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)

# UpdateSchemaType: Pydantic schema cho việc cập nhật (request body)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

# ServiceType: Phải là một subclass của BaseService, tương thích với các Model và Schema types ở trên
ServiceType = TypeVar("ServiceType", bound=BaseService[Any, ModelType, CreateSchemaType, UpdateSchemaType])


class BaseAPIRouter(
    APIRouter,
    Generic[ServiceType, ModelType, SchemaType, CreateSchemaType, UpdateSchemaType]
):
    def __init__(
        self,
        service_dependency: Callable[..., ServiceType], # Dependency để inject service
        response_model_schema: Type[SchemaType],       # Pydantic schema cho response
        create_model_schema: Type[CreateSchemaType],   # Pydantic schema cho tạo mới
        update_model_schema: Type[UpdateSchemaType],   # Pydantic schema cho cập nhật
        db_session_dependency: Callable[..., SQLAlchemySession], # Dependency cho DB session
        prefix: str = "",
        tags: Optional[List[str]] = None,
        dependencies: Optional[List[params.Depends]] = None,
        *args: Any,
        **kwargs: Any,
    ):
        super().__init__(prefix=prefix, tags=tags, dependencies=dependencies, *args, **kwargs)


        self.service_dependency = service_dependency
        self.response_model_schema = response_model_schema
        self.create_model_schema = create_model_schema
        self.update_model_schema = update_model_schema
        self.db_session_dependency = db_session_dependency

        model_name = self._get_model_name()
        model_name_plural = self._get_model_name_plural()

        self.add_api_route("/", self._create(), methods=["POST"], response_model=self.response_model_schema, summary=f"Create new {model_name}")
        self.add_api_route("/", self._read_all(), methods=["GET"], response_model=List[self.response_model_schema], summary=f"Read all {model_name_plural}")
        self.add_api_route("/{item_id}", self._read_one(), methods=["GET"], response_model=self.response_model_schema, summary=f"Read one {model_name}")
        self.add_api_route("/{item_id}", self._update(), methods=["PUT"], response_model=self.response_model_schema, summary=f"Update a {model_name}")
        self.add_api_route("/{item_id}", self._delete(), methods=["DELETE"], response_model=self.response_model_schema, summary=f"Delete a {model_name}")

    def _get_model_name(self) -> str:
        name = self.response_model_schema.__name__.lower()
        if name.endswith("schema"): name = name[:-6]
        elif name.endswith("model"): name = name[:-5]
        return name.capitalize()

    def _get_model_name_plural(self) -> str:
        name = self._get_model_name()
        if name.endswith("y"): return name[:-1] + "ies"
        if name.endswith("s") or name.endswith("sh") or name.endswith("ch") or name.endswith("x") or name.endswith("z"): return name + "es"
        return name + "s"

    def _create(self) -> Callable[..., Any]:
        async def endpoint(item_in: self.create_model_schema, # type: ignore
                           service: ServiceType = Depends(self.service_dependency),
                           db: SQLAlchemySession = Depends(self.db_session_dependency)):
            return await service.create(db=db, obj_in=item_in)
        return endpoint

    def _read_all(self) -> Callable[..., Any]:
        async def endpoint(service: ServiceType = Depends(self.service_dependency),
                           db: SQLAlchemySession = Depends(self.db_session_dependency),
                           skip: int = 0, limit: int = 100):
            return await service.get_multi(db=db, skip=skip, limit=limit)
        return endpoint

    def _read_one(self) -> Callable[..., Any]:
        async def endpoint(item_id: Any, # Nên là int hoặc UUID tùy theo ID của bạn
                           service: ServiceType = Depends(self.service_dependency),
                           db: SQLAlchemySession = Depends(self.db_session_dependency)):
            obj = await service.get(db=db, id=item_id)
            if not obj: raise HTTPException(status_code=404, detail=f"{self._get_model_name()} not found")
            return obj
        return endpoint

    def _update(self) -> Callable[..., Any]:
        async def endpoint(item_id: Any, item_in: self.update_model_schema, # type: ignore
                           service: ServiceType = Depends(self.service_dependency),
                           db: SQLAlchemySession = Depends(self.db_session_dependency)):
            db_obj = await service.get(db=db, id=item_id)
            if not db_obj: raise HTTPException(status_code=404, detail=f"{self._get_model_name()} not found")
            return await service.update(db=db, db_obj=db_obj, obj_in=item_in)
        return endpoint

    def _delete(self) -> Callable[..., Any]:
        async def endpoint(item_id: Any,
                           service: ServiceType = Depends(self.service_dependency),
                           db: SQLAlchemySession = Depends(self.db_session_dependency)):
            deleted_obj = await service.delete(db=db, id=item_id)
            if deleted_obj is None: raise HTTPException(status_code=404, detail=f"{self._get_model_name()} not found")
            return deleted_obj
        return endpoint