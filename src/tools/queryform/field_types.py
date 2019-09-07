import logging

log = logging.getLogger(__name__)


class SingleField:
    """
    simple tuple that describes a argument of a query
    """

    def __init__(
        self,
        *,
        name,
        template_name,
        description="",
        default=None,
        pretransform=None,
        validate=None,
        hidden=False,
        transform_error_msg=None,
        validate_error_message=None,
    ):

        if pretransform and not transform_error_msg:
            raise TypeError("must specify a message with a transform method")
        if validate and not validate_error_message:
            raise TypeError("must specify a message with a transform method")

        self._value = default
        self.name = name
        self.template_name = template_name
        self.description = description
        self.hidden = hidden
        self.default = default

        self.transform_error_msg = transform_error_msg
        self.pretransform = pretransform
        self.validate = validate
        self.validate_error_msg = validate_error_message

    def asdict(self):
        return {
            "type": "single",
            **{
                k: v
                for k, v in self.__dict__.items()
                if k not in ["validate", "pretransform"]
            },
        }

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if self.pretransform:
            try:
                value = self.pretransform(value)
            except Exception:
                raise ValueError(self.transform_error_msg)

        if self.validate:
            if self.validate(value):
                self._value = value
            else:
                raise ValueError(self.validate_error_msg)
        else:
            self._value = value


class ChoiceSubField:
    def __init__(self, name, template_name, choices, description=""):
        self._value = None
        self.name = name
        self.template_name = template_name
        self.choices = choices
        self.description = description

    def asdict(self):
        return {
            "type": "choice",
            "name": self.name,
            "choices": {
                name: [field.asdict() for field in choice]
                for name, choice in self.choices.items()
            },
            "template_name": self.template_name,
            "description": self.description,
        }

    @property
    def value(self):

        return self._value

    @value.setter
    def value(self, value):
        if len(value) == 2:
            select, values = value[0], value[1]
            if type(values) != dict or type(select) != str:
                raise ValueError("a choice must be selected")
            validate_inputs(self.choices[select], **values)
        else:
            raise ValueError(f"invalid choice selection")

        self._value = value

    @property
    def choice(self):
        if self.value:
            return self.value[0]
        else:
            return None

    @property
    def fields(self):
        if self.value:
            return self.value[1]
        else:
            return None


# todo :: add multiselect field


def validate_inputs(fields, **kwargs):
    """
    note :: weird design, but ok

    todo:: maybe move the subsetting into the field (sounds good)
    """
    for field in fields:
        if field.template_name not in kwargs:
            raise ValueError(f'"{field.name}" is empty')

        field.value = kwargs[field.template_name]
        kwargs[field.template_name] = field

    return kwargs
