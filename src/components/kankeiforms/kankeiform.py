import abc

from tools.queryform.form import QueryForm


class KankeiForm(QueryForm, abc.ABC):
    """
    Base class for formality and propagate change to all subclasses
    """

    timeout = None
