
from techmock import patch
from sample_project import project


def test_case():
    with patch('sample_project.project.sample_class') as mock:

        mock().get_object_to_slice.return_value = 'SLICE WITH STRING'

        print("Inside Context Manager")
        print("sample_method result: ", project.sample_method())
        print("sample_class object: ", project.sample_class)

    print("---")
    print("Outside of Context Manager")
    print("sample_method result: ", project.sample_method())
    print("sample_class object: ", project.sample_class)


test_case()
