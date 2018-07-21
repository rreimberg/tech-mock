
from sample_project import project


class MonkeyPatchClass():
    def get_object_to_slice(self):
        return ['Monkey Patch is cool']


print("Before Monkey Patch")
print("sample_method result: ", project.sample_method())
print("sample_class object: ", project.sample_class)

project.sample_class = MonkeyPatchClass

print("---")
print("After Monkey Patch")
print("sample_method result: ", project.sample_method())
print("sample_class object: ", project.sample_class)
