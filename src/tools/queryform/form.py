import abc
import logging
from collections import defaultdict

from neo4j import Driver

from tools.queryform import field_types

log = logging.getLogger(__name__)


class QueryForm(abc.ABC):
    registry = defaultdict(lambda: dict())

    group = None
    name = None
    transaction = None
    tooltip = ""
    fields = []
    shown_properties = ""
    coloring_types = []
    timeout = None

    @staticmethod
    @abc.abstractmethod
    def transform_output(records):
        """
        a output transform has the probablem to be applied for a form, even thought
        it can use different queries depending on the form inputs
        :param records:
        :return:
        """
        return records

    @classmethod
    @abc.abstractmethod
    def get_query(cls, _):
        return NotImplementedError()

    def __init_subclass__(cls, **kwargs):
        if abc.ABC not in cls.__bases__:
            if not cls.name:
                # todo :: change to an internal error
                raise ValueError("must specify a name")

            if not cls.group:
                # todo :: change to an internal error
                raise ValueError("must specify a group")

            if not cls.shown_properties:
                # todo :: change to an internal error
                raise ValueError("must specificy shown_properties")

            def transaction(tx, query_str, **kkwargs):
                return tx.run(query_str, **kkwargs)

            if cls.timeout:
                transaction.timeout = cls.timeout

            cls.transaction = transaction
            cls.registry[cls.group][cls.name] = cls

    @classmethod
    def run_query(cls, driver: Driver, **kwargs):
        """
        :param driver: database driver
            (false interface that requires session() with a read_transtion()
        :param kwargs:
        :return:
        """
        with driver.session() as session:
            validated_kwargs = field_types.validate_inputs(cls.fields, **kwargs)
            query_str, binding = cls.get_query(**validated_kwargs)
            log.debug(f"running query :: {query_str}")
            return cls.transform_output(
                session.read_transaction(cls.transaction, query_str, **binding)
            )

    @classmethod
    def asdict(cls):
        return {
            "fields": [field.asdict() for field in cls.fields],
            "name": cls.name,
            "tooltip": cls.tooltip,
            "shown_properties": cls.shown_properties,
            "coloring_types": cls.coloring_types,
        }
