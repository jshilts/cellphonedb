import os

import pandas as pd

from cellphonedb.src.app.flask.flask_app import create_app
from cellphonedb.src.app.cellphonedb_app import output_test_dir, data_test_dir, cellphonedb_app
from cellphonedb.src.local_launchers.local_method_launcher import LocalMethodLauncher
from cellphonedb.src.tests.cellphone_flask_test_case import CellphoneFlaskTestCase
from cellphonedb.utils import dataframe_functions


class TestTerminalMethodStatisticalAnalysis(CellphoneFlaskTestCase):
    def create_app(self):
        return create_app(raise_non_defined_vars=False, verbose=False)

    def test_test_data(self):
        iterations = '10'
        data = 'test'
        debug_seed = '0'
        project_name = 'test_data'
        threshold = 0.1
        self._method_call(data, iterations, project_name, threshold, debug_seed)

    def _method_call(self, data: str, iterations: str, project_name: str, threshold: float, debug_seed: str):
        result_means_filename = self._get_result_filename('means', data, iterations)
        result_pvalues_filename = self._get_result_filename('pvalues', data, iterations)
        result_significant_means_filename = self._get_result_filename('significant_means', data, iterations)
        result_pvalues_means_filename = self._get_result_filename('pvalues_means', data, iterations)
        result_deconvoluted_filename = self._get_result_filename('deconvoluted', data, iterations)

        meta_filename = os.path.realpath('{}/hi_{}_meta.txt'.format(data_test_dir, data))
        counts_filename = os.path.realpath('{}/hi_{}_counts.txt'.format(data_test_dir, data))

        LocalMethodLauncher(cellphonedb_app.cellphonedb).cpdb_statistical_analysis_local_method_launcher(meta_filename,
                                                                                                         counts_filename,
                                                                                                         project_name,
                                                                                                         iterations,
                                                                                                         threshold,
                                                                                                         output_test_dir,
                                                                                                         result_means_filename,
                                                                                                         result_pvalues_filename,
                                                                                                         result_significant_means_filename,
                                                                                                         result_pvalues_means_filename,
                                                                                                         result_deconvoluted_filename,
                                                                                                         debug_seed)

        self._assert_result('means', data, iterations, project_name, result_means_filename)
        self._assert_result('pvalues', data, iterations, project_name, result_pvalues_filename)
        self._assert_result('significant_means', data, iterations, project_name, result_significant_means_filename)
        self._assert_result('pvalues_means', data, iterations, project_name, result_pvalues_means_filename)
        self._assert_result('deconvoluted', data, iterations, project_name, result_deconvoluted_filename)

    def _assert_result(self, namefile: str, data: str, iterations: str, project_name: str,
                       result_means_filename: str) -> None:
        means_test_filename = 'hi_{}_result__data-{}_it-{}.txt'.format(namefile, data, iterations)
        original_means = pd.read_table(os.path.realpath('{}/{}'.format(data_test_dir, means_test_filename)))
        result_means = pd.read_table('{}/{}/{}'.format(output_test_dir, project_name, result_means_filename))
        self.assertTrue(dataframe_functions.dataframes_has_same_data(result_means, original_means))
        self.remove_file('{}/{}/{}'.format(output_test_dir, project_name, result_means_filename))

    def _get_result_filename(self, base_name, data: str, iterations: str) -> str:
        base_filename = '{}__data-{}_it-{}'.format(base_name, data, iterations)
        random_filename = self.get_test_filename(base_filename, 'txt')

        return random_filename
