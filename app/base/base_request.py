from copy import deepcopy
from typing import get_args, get_origin, Type, Any, Optional

from pydantic import BaseModel, ConfigDict, create_model
from pydantic.alias_generators import to_camel
from pydantic.fields import FieldInfo


def snake_to_camel(snake_str: str) -> str:
    components = snake_str.split("_")
    return components[0] + "".join(x.title() for x in components[1:])


class BaseRequest(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel, arbitrary_types_allowed=True, extra="allow", use_enum_values=True
    )

    def __init__(self, **data: Any):
        # Convert snake_case keys to camelCase keys
        camel_case_data = {snake_to_camel(k): v for k, v in data.items()}
        super().__init__(**camel_case_data)


# model을 넣으면 모든 field가 optional인 model 반환(partial update 등에 사용)
def partial_model(model: Type[BaseModel]):
    def make_field_optional(field: FieldInfo, default: Any = None) -> tuple[Any, FieldInfo]:
        new = deepcopy(field)
        new.default = default

        if get_origin(field.annotation) is None and issubclass(field.annotation, BaseModel):
            new.annotation = Optional[partial_model(field.annotation)]
        elif get_origin(field.annotation) is list:
            inner_type = get_args(field.annotation)[0]
            if issubclass(inner_type, BaseModel):
                new.annotation = Optional[list[partial_model(inner_type)]]
            else:
                new.annotation = Optional[field.annotation]
        else:
            new.annotation = Optional[field.annotation]

        return new.annotation, new

    return create_model(
        model.__name__,
        __base__=model,
        __module__=model.__module__,
        **{field_name: make_field_optional(field_info) for field_name, field_info in model.model_fields.items()},
    )
