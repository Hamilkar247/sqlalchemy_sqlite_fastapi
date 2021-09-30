from pydantic import BaseModel


def to_camel(string):
    return ''.join(word.capitalize() for word in string.split('_'))


class CamelSchema(BaseModel):
    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True
        orm_mode = True
