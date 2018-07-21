
from techmock import patch
from sample_project import project


@patch('sample_project.project.sample_class')
def test_case(mock):
    mock().get_object_to_slice.return_value = ['Decorator']
    print("Mock")
    print("sample_method result: ", project.sample_method())
    print("sample_class object: ", project.sample_class)


test_case()

print("---")
print("Original")
print("sample_method result: ", project.sample_method())
print("sample_class object: ", project.sample_class)
