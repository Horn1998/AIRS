class Mapper:
    __mapper_relation = {}

    @classmethod
    def register(cls, value):
        Mapper.__mapper_relation[cls] = value

    @classmethod
    def exist(cls):
        if cls in Mapper.__mapper_relation:
            return True
        return False

    @classmethod
    def value(cls):
        return Mapper.__mapper_relation[cls]


class Module(type):
    @classmethod
    def __call__(cls, *args, **kwargs):
        obj = cls.__new__(cls, *args, **kwargs)
        arg_list = list[args]
        if Mapper.exist(cls):
            value = Mapper.value(cls)
            arg_list.append(value)
        obj.__init__(*arg_list, **kwargs)
        return obj