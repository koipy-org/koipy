from typing import Any
from dataclasses import dataclass, fields


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

    def from_list(self, attr: str, obj: list, instance: "BaseCFG") -> "MutableCFG":
        if isinstance(obj, list) and isinstance(instance, BaseCFG):
            setattr(self, attr, [instance.__class__().from_obj(o) for o in obj])
        return self

    def from_dict(self, attr, obj: dict, instance: "BaseCFG") -> "MutableCFG":
        obj = self.rename_to_obj(obj)
        if isinstance(obj, dict) and isinstance(instance, BaseCFG):
            setattr(self, attr, {k: instance.__class__().from_obj(v) for k, v in obj.items()})
        return self


class ListCFG(MutableCFG):
    pass


@dataclass
class DictCFG(MutableCFG):
    """
    从字典类型中设置成员属性
    """

    def from_obj(self, obj: dict) -> "DictCFG":
        self.rename_to_obj(obj)
        for f in fields(self):
            if f.name in obj:
                raw_value = obj[f.name]
                attrobj = getattr(self, f.name)
                if isinstance(attrobj, BaseCFG):
                    attrobj.from_obj(raw_value)
                    setattr(self, f.name, attrobj)
                else:
                    if type(raw_value) is not f.type and raw_value is not None:
                        print(f"无法正确设置{self.__class__.__name__}的属性{f.name}的类型 |"
                              f"需要的类型: {f.type} |"
                              f"实际值: {raw_value} |"
                              f"实际类型: {type(raw_value)}")
                    if raw_value is not None:
                        setattr(self, f.name, raw_value)
        return self
