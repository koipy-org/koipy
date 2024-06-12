from typing import Any, Union, Type
from dataclasses import dataclass, fields

Admin = Union[str, int]
User = Union[str, int]


class BaseCFG:
    """
    配置类基类，需要实现一个方法，从对象中提取数据到实例属性中
    """

    def from_obj(self, obj: Any):
        raise NotImplementedError

    @staticmethod
    def rename_to_obj(obj: dict, reverse: bool = False, keep_none: bool = False) -> dict:
        """
        为了符合python命名规则 比如：
        (yaml)bind-address --> (python) bind_address

        reverse: 设置为True可以反过来 (python) bind_address --> (yaml)bind-address
        keep_none: 保留None值
        """
        if not isinstance(obj, dict):
            return obj
        str1, str2 = ("_", "-") if reverse else ("-", "_")
        new_obj = {}
        for k, v in obj.items():
            if v is None and not keep_none:
                continue
            if not isinstance(k, str):
                new_obj[k] = BaseCFG.rename_to_obj(v, reverse)
                continue
            if str1 in k:
                new_k = k.replace(str1, str2)
                new_obj[new_k] = BaseCFG.rename_to_obj(v, reverse)
            else:
                new_obj[k] = BaseCFG.rename_to_obj(v, reverse)
        return new_obj

    @staticmethod
    def rename_to_yaml(obj: dict) -> dict:
        return BaseCFG.rename_to_obj(obj, True)


class ImmutableCFG(BaseCFG):
    def from_obj(self, obj: Any):
        pass

    def from_int(self, v: int):
        raise NotImplementedError

    def from_str(self, v: str):
        raise NotImplementedError

    def from_float(self, k: str, v: float):
        raise NotImplementedError

    def from_bool(self, k: str, v: bool):
        raise NotImplementedError


class MutableCFG(BaseCFG):
    """
    从可变的对象中提取，比如list，dict
    """

    def from_obj(self, obj: Any):
        pass

    def from_list(self, attr: str, obj: list, _class_or_instance: Union[Type[BaseCFG], BaseCFG]) -> "MutableCFG":
        if isinstance(obj, list):
            if isinstance(_class_or_instance, BaseCFG):
                setattr(self, attr, [_class_or_instance.__class__().from_obj(o) for o in obj])
            elif issubclass(_class_or_instance, (BaseCFG, str, int, float, bool)):
                setattr(self, attr, [_class_or_instance().from_obj(o) for o in obj])

        return self

    def from_dict(self, attr, obj: dict, _class_or_instance: Union[Type[BaseCFG], BaseCFG]) -> "MutableCFG":
        # obj = self.rename_to_obj(obj)
        if isinstance(obj, dict):
            if isinstance(_class_or_instance, BaseCFG):
                setattr(self, attr, {k: _class_or_instance.__class__().from_obj(v) for k, v in obj.items()})
            elif issubclass(_class_or_instance, (BaseCFG, str, int, float, bool)):
                setattr(self, attr, {k: _class_or_instance().from_obj(v) for k, v in obj.items()})
        return self


@dataclass
class DictCFG(MutableCFG):
    """
    从字典类型中设置成员属性
    """

    def from_obj(self, obj: dict) -> "DictCFG":
        obj = self.rename_to_obj(obj)
        # 我们在字典对象中逐个寻找需要的字段，然后将它填充。
        for f in fields(self):
            if f.name in obj:  # 如果实例的属性名在字典里，我们尝试加载进行，当然，这里需要正确地加载成我们自定义的变量类型。
                raw_value = obj[f.name]
                attrobj = getattr(self, f.name)
                if isinstance(attrobj, BaseCFG):
                    attrobj.from_obj(raw_value)  # 因为所有的配置类继承自BaseCFG类，里面都会实现一个名为from_obj方法。
                    setattr(self, f.name, attrobj)
                else:
                    # 如果走到这条分支语句，说明不是BaseCFG，这个时候已经到达Python的基本数据类型。
                    if type(raw_value) is not f.type and raw_value is not None:
                        print(f"无法正确设置{self.__class__.__name__}的属性{f.name}的类型 |"
                              f"需要的类型: {f.type} |"
                              f"实际值: {raw_value} |"
                              f"实际类型: {type(raw_value)}")
                    if raw_value is not None:
                        setattr(self, f.name, raw_value)
        return self


@dataclass
class ListCFG(DictCFG):
    pass


class AdminList(list, ListCFG):
    def from_obj(self, obj: list) -> "AdminList":
        if not isinstance(obj, list):
            return self
        self.clear()
        raw_v = obj
        for v in raw_v:
            if not isinstance(v, (str, int)):
                continue
            self.append(v)
        return self

    def __getitem__(self, index: int) -> "Admin":
        value = super().__getitem__(index)
        if not isinstance(value, (str, int)):
            raise TypeError(f"{type(self).__name__} only supports str or int values")
        return value

    def __setitem__(self, index: int, value: Admin):
        if not isinstance(value, (str, int)):
            raise TypeError(f"{type(self).__name__} only supports str or int values")
        super().__setitem__(index, value)

    def append(self, __object: Admin):
        if not isinstance(__object, (str, int)):
            raise TypeError(f"{type(self).__name__} only supports str or int values")
        super().append(__object)

    def __str__(self):
        return f"{type(self).__name__} object: {[i for i in self]}"
        # return super().__str__()

    def __repr__(self):
        return f"{type(self).__name__} object: {[i for i in self]}"


@dataclass
class UserList(AdminList):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
