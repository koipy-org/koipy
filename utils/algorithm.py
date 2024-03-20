INT_MAX = 2 ** 31 - 1
INT_MIN = -2 ** 31


class AutoMata:
    """
    一个简单的自动机，如果你不知道什么是自动机，请自行搜索。
    """

    def __init__(self):
        self.state = "start"
        self.ans = 0
        self.sign = 1
        self.status_table = {
            "start": ["start", "sign", "innumber", "end"],
            "sign": ["end", "end", "innumber", "end"],
            "innumber": ["end", "end", "innumber", "end"],
            "end": ["end", "end", "end", "end"],
        }

    @staticmethod
    def update_status(char: str):
        """
        更新自动机妆态
        :param char: 字符
        :return:
        """
        if char.isspace():
            return 0
        if char == '+' or char == '-':
            return 1
        if char.isdigit():
            return 2
        return 3

    def get(self, c):
        self.state = self.status_table[self.state][self.update_status(c)]
        if self.state == "innumber":
            self.ans = self.ans * 10 + int(c)
            self.ans = min(self.ans, INT_MAX) if self.sign == 1 else min(self.ans, -INT_MIN)
        if self.state == "sign":
            if c == '-':
                self.sign = -1


def atoi(string: str) -> int:
    """
    将字符串转化为整型，
    :param string: 要转换的字符串
    :return:
    """
    if not isinstance(string, str):
        raise TypeError(f"atoi函数需要一个 str 类型的参数，而不是: {type(string).__name__}")
    auto = AutoMata()
    for c in string:
        auto.get(c)
    return auto.ans * auto.sign


__all__ = ["atoi"]
