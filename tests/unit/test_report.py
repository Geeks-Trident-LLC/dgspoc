import pytest

from dgspoc.report import DGSReport
from dgspoc.report import DGSReportFile

from dgspoc.utils import File

from . import get_test_data_file
from . import ReformatOutput


TESTDATA = File.get_result_from_yaml_file(
    'data/report_test_data.yaml',
    base_dir=__file__,
    dot_datatype=True,
    var_substitution=True,
    root_var_name='self'
)


class TestReportGeneration:

    @pytest.mark.parametrize(
        ('report_file', 'detail', 'expected_exit_code', 'expected_result'),
        [
            (
                get_test_data_file(TESTDATA.case1.filename), TESTDATA.case1.detail,
                TESTDATA.case1.exit_code, TESTDATA.case1.expected_result
            ),
            (
                get_test_data_file(TESTDATA.case2.filename), TESTDATA.case2.detail,
                TESTDATA.case2.exit_code, TESTDATA.case2.expected_result
            ),
            (
                get_test_data_file(TESTDATA.case3.filename), TESTDATA.case3.detail,
                TESTDATA.case3.exit_code, TESTDATA.case3.expected_result
            ),
            (
                get_test_data_file(TESTDATA.case4.filename), TESTDATA.case4.detail,
                TESTDATA.case4.exit_code, TESTDATA.case4.expected_result
            ),
            (
                get_test_data_file(TESTDATA.case5.filename), TESTDATA.case5.detail,
                TESTDATA.case5.exit_code, TESTDATA.case5.expected_result
            ),
            (
                get_test_data_file(TESTDATA.case6.filename), TESTDATA.case6.detail,
                TESTDATA.case6.exit_code, TESTDATA.case6.expected_result
            ),
            (
                get_test_data_file(TESTDATA.case7.filename), TESTDATA.case7.detail,
                TESTDATA.case7.exit_code, TESTDATA.case7.expected_result
            ),
            (
                get_test_data_file(TESTDATA.case8.filename), TESTDATA.case8.detail,
                TESTDATA.case8.exit_code, TESTDATA.case8.expected_result
            ),
            (
                get_test_data_file(TESTDATA.case9.filename), TESTDATA.case9.detail,
                TESTDATA.case9.exit_code, TESTDATA.case9.expected_result
            ),
            (
                get_test_data_file(TESTDATA.case10.filename), TESTDATA.case10.detail,
                TESTDATA.case10.exit_code, TESTDATA.case10.expected_result
            ),
            (
                get_test_data_file(TESTDATA.case11.filename), TESTDATA.case11.detail,
                TESTDATA.case11.exit_code, TESTDATA.case11.expected_result
            ),
            (
                get_test_data_file(TESTDATA.case12.filename), TESTDATA.case12.detail,
                TESTDATA.case12.exit_code, TESTDATA.case12.expected_result
            ),
        ]
    )
    def test_generating_report_per_file(self, report_file, detail, expected_exit_code, expected_result):
        dgs_report = DGSReport(report_file, detail=detail)
        report = dgs_report.generate()
        reformat_report = ReformatOutput(report, everything=True)
        assert dgs_report.exit_code == expected_exit_code
        assert reformat_report == expected_result


# class TestRetrievingReportFilesAndGeneratingReport:
#
#     @pytest.mark.parametrize(
#         ('directory', 'detail', 'expected_result'),
#         [
#             (
#                 get_test_data_file(TESTDATA.case_a.directory),
#                 TESTDATA.case_a.detail, TESTDATA.case_a.expected_result),
#         ]
#     )
#     def test_generating_report_per_file(self, directory, detail, expected_result):
#         report_files = DGSReportFile.get_report_files(directory)
#         dgs_report = DGSReport(*report_files, detail=detail)
#         import pdb; pdb.set_trace()
#         report = dgs_report.generate()
#         assert report == expected_result
