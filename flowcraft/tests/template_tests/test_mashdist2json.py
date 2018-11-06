import os
import json
import flowcraft.templates.mashdist2json as mashdist2json


def test_generate_file(tmpdir):
    """
    This function tests if the files generated by this template script are
    created
    """

    # create a temporary file mash screen txt file
    mash_file = tmpdir.join("test_depth_file.txt")
    mash_file.write("ACC1\tseq1\t0\t900/1000")

    mashdist2json.main(str(mash_file), "0.5", "test", "assembly_file")

    assert_message = []
    # conditions to check that files are generated
    if not os.path.isfile("{}.json".format(
            str(mash_file).split(".")[0])):
        assert_message.append("mash dist json not created")
    if not os.path.isfile(".report.json"):
        assert_message.append(".report.json file was not created")

    # remove the .report.json file
    os.remove(".report.json")

    assert not assert_message, "errors occurred:\n{}".format(
        "\n".join(assert_message)
    )


def test_generated_dict(tmpdir):
    """
    This function tests if the files generated by this template script are
    created
    """

    # create a temporary file mash screen txt file
    mash_file = tmpdir.join("test_depth_file.txt")
    mash_file.write("ACC1\tseq1\t0\t900/1000")

    # the expected result from loading the dictionary in the generated file
    expected_dict = {"ACC1": [1.0, 0.9, "seq1"]}

    mashdist2json.main(str(mash_file), "0.5", "test", "assembly_file")

    result_dict = json.load(open("{}.json".format(
            str(mash_file).split(".")[0])))

    assert_message = []

    # checks if result_dict is indeed a dictionary
    if not isinstance(result_dict, dict):
        assert_message.append("Contents of the generated file must be a "
                              "dictionary.")

    if not result_dict == expected_dict:
        assert_message.append("The expected dictionary must be equal to the "
                              "one present in the generated file.\n"
                              "Expected: {}\n"
                              "Result: {}". format(
            json.dumps(expected_dict),
            json.dumps(result_dict)
        ))

    # remove the .report.json file
    os.remove(".report.json")

    assert not assert_message, "Errors occurred:\n{}".format(
        "\n".join(assert_message)
    )
