from utils.types.config import *


@dataclass
class MatrixDrawCFG(DictCFG):
    matrixLine: int


@dataclass
class DrawFilter(DictCFG):
    include: str = ""
    exclude: str = ""


@dataclass
class DrawConfig:
    basedataNum: int = 0
    filter: DrawFilter = DrawFilter()
    frontsize: int = 38
    linespace: int = 65
    timeused: str = "未知"
    sort: str = "订阅原序"
    ctofs: float = int(linespace / 2 - frontsize / 2)
    speedBlockWidth: int = 20



