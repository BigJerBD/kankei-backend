from tools.queryform.field_types import SingleField


class IntField(SingleField):
    def __init__(self, *args, **kwargs):
        super().__init__(
            *args,
            **kwargs,
            pretransform=int,
            transform_error_msg=f"{kwargs['name']} must be an integer",
        )


class StringField(SingleField):
    def __init__(self, *args, **kwargs):
        super().__init__(
            *args,
            **kwargs,
            pretransform=lambda x: x.strip(),
            transform_error_msg=f"{kwargs['name']} must string of character",
            validate=lambda x: type(x) == str,
            validate_error_message=f"{kwargs['name']} must string of character",
        )


# note :: domain specific fields
