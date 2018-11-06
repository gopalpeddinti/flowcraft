import os
import json
import flowcraft.templates.pATLAS_consensus_json as pATLAS_consensus_json


def test_generate_file(tmpdir):
    """
    This function tests if the files generated by this template script are
    created
    """

    # create a temporary file mash screen txt file
    mash_file = tmpdir.join("mash_file.txt")
    depth_file = tmpdir.join("test_depth_file.txt")
    mash_file.write('{"ACC1": ["0.9", "1"]}')
    depth_file.write('{"ACC1": 0.9}')

    list_of_files = [str(mash_file), str(depth_file)]

    pATLAS_consensus_json.main(list_of_files)

    assert_message = []
    # conditions to check that files are generated
    if not os.path.isfile("consensus_file.json".format(
            str(mash_file).split(".")[0])):
        assert_message.append("consensus_file.json not created")
    if not os.path.isfile(".report.json"):
        assert_message.append(".report.json file was not created")

    # remove the .report.json file
    os.remove(".report.json")
    os.remove("consensus_file.json")

    assert not assert_message, "errors occurred:\n{}".format(
        "\n".join(assert_message)
    )


def test_generated_dict(tmpdir):
    """
    Test the dictionary generated by the script. However, since the dict is
    only outputted to a file it is needed that we read the generated file
    in order to check the result.
    """

    # create a temporary file mash screen txt file
    mash_file = tmpdir.join("mash_file.txt")
    depth_file = tmpdir.join("test_depth_file.txt")
    mash_file.write('{"ACC1": ["0.9", "1"]}')
    depth_file.write('{"ACC1": 0.9}')

    list_of_files = [str(mash_file), str(depth_file)]

    # the expected result from loading the dictionary in the generated file
    expected_dict = {"ACC1":
                         {"/tmp/pytest-of-tiago/pytest-1/test_generated_dict0/"
                          "mash_file.txt": ["0.9", "1"],
                          "/tmp/pytest-of-tiago/pytest-1/test_generated_dict0/"
                          "test_depth_file.txt": 0.9}
                     }

    pATLAS_consensus_json.main(list_of_files)

    result_dict = json.load(open("consensus_file.json"))

    assert_message = []

    # checks if result_dict is indeed a dictionary
    if not isinstance(result_dict, dict):
        assert_message.append("Contents of the generated file must be a "
                              "dictionary.")

    # checks if the accession key matches between the expected result and the
    # actual result
    if not list(result_dict.keys())[0] == list(expected_dict.keys())[0]:
        assert_message.append("Expected key doesn't match the resulting key "
                              "in dict from file.\nExpected value: {}\n"
                              "Result value: {}".format(
            list(expected_dict.keys())[0],
            list(result_dict.keys())[0]
        ))

    # checks that the accession must have two keys
    if not len(list(result_dict[list(result_dict.keys())[0]].keys())) == 2:
        assert_message.append("This dictionary must contain only two keys"
                              "per accession number. It had ".format(
            len(list(result_dict[list(result_dict.keys())[0]].keys()))
        ))

    # checks if the resulting values for each type of file are the proper type:
    first_file_values = list(result_dict[
                                 list(result_dict.keys())[0]].values())[0]
    second_file_values = list(result_dict[
                                 list(result_dict.keys())[0]].values())[1]
    list_of_checks = [isinstance(first_file_values, list),
                      isinstance(second_file_values, float)]
    if not all(list_of_checks):
        assert_message.append("Value of the 1 element in each accession "
                              "dictionary must be a list and the 2 element"
                              " must be a str.\nOffending value: {} "
                              "element".format(" ".join(
            [str(x + 1) for x, el in enumerate(list_of_checks) if not el]
        )))

    # remove the .report.json file
    os.remove(".report.json")
    os.remove("consensus_file.json")

    assert not assert_message, "Errors occurred:\n{}".format(
        "\n".join(assert_message)
    )
