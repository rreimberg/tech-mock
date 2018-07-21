

def sample_method():
    obj = sample_class()
    result = obj.get_object_to_slice()
    try:
        return result[-1]
    except IndexError:
        return 'Empty object'


class sample_class():

    def get_object_to_slice(self):
        return ['Original Method']
