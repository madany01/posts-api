from pydantic import BaseModel, root_validator


class Post(BaseModel):
    title: str
    content: str
    published: bool = False


class UpdatedPost(BaseModel):
    title: str = None
    content: str = None
    published: str = None

    @root_validator
    def check_at_least_one_field_exists(cls, values):
        print(values)
        for v in values.values():
            if v is not None:
                return values

        raise ValueError('post should contains at least one field to perform update operation')


__all__ = [Post, UpdatedPost]
