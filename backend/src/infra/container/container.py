import inspect
from typing import Any, Callable, Dict, Type, TypeVar

T = TypeVar("T")


class Container:
    _instances: Dict[Type, Any] = {}
    _factories: Dict[Type, Callable[[], Any]] = {}

    @classmethod
    def register(cls, interface: Type[T], implementation: Type[T]) -> None:
        cls._factories[interface] = lambda: implementation()

    @classmethod
    def register_instance(cls, interface: Type[T], instance: T) -> None:
        cls._instances[interface] = instance

    @classmethod
    def register_factory(cls, interface: Type[T], factory: Callable[[], T]) -> None:
        cls._factories[interface] = factory

    @classmethod
    def resolve(cls, interface: Type[T]) -> T:
        if interface in cls._instances:
            return cls._instances[interface]

        if interface in cls._factories:
            instance = cls._factories[interface]()
            cls._instances[interface] = instance
            return instance

        constructor = interface.__init__
        sig = inspect.signature(constructor)
        kwargs = {}

        for name, param in sig.parameters.items():
            if name == "self":
                continue
            dep_type = param.annotation
            if dep_type == inspect.Parameter.empty:
                raise Exception(
                    f"Missing type annotation for parameter '{name}' in {interface}"
                )
            kwargs[name] = cls.resolve(dep_type)

        instance = interface(**kwargs)
        cls._instances[interface] = instance
        return instance
