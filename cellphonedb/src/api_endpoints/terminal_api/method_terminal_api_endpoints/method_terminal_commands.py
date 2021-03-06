import click

from cellphonedb.src.app import cpdb_app
from cellphonedb.src.app.app_logger import app_logger
from cellphonedb.src.cpdb_exceptions.ReadFileException import ReadFileException
from cellphonedb.src.exceptions.ParseMetaException import ParseMetaException
from cellphonedb.src.local_launchers.local_method_launcher import LocalMethodLauncher


@click.command()
@click.argument('meta-filename')
@click.argument('counts-filename')
@click.option('--project-name', default='', help='Name of the project. It creates a subfolder in output folder')
@click.option('--iterations', default=1000, help='Number of pvalues analysis iterations [1000]')
@click.option('--threshold', default=0.1, help='% of cells expressing a gene')
@click.option('--output-path', default='',
              help='Directory where the results will be allocated (the directory must exist) [out]')
@click.option('--means-result-name', default='means.txt', help='Means result namefile [means.txt]')
@click.option('--pvalues-result-name', default='pvalues.txt', help='Pvalues result namefile [pvalues.txt]')
@click.option('--significant-mean-result-name', default='significant_means.txt',
              help='Significant result namefile [significant_means.txt]')
@click.option('--means-pvalues-result-name', default='pvalues_means.txt',
              help='Pvalues-means result namefile [pvalues_means.txt]')
@click.option('--deconvoluted-result-name', default='deconvoluted.txt',
              help='Deconvoluted result namefile [deconvoluted.txt]')
@click.option('--debug-seed', default='-1', help='Debug random seed 0 for disable it. >=0 to set it [-1]')
@click.option('--threads', default=4, help='Max of threads to process the data [4]')
@click.option('--verbose/--quiet', default=True, help='Print or hide cellphonedb logs [verbose]')
def statistical_analysis(meta_filename: str,
                         counts_filename: str,
                         project_name: str,
                         iterations: str,
                         threshold: float,
                         output_path: str,
                         means_result_name: str,
                         pvalues_result_name: str,
                         significant_mean_result_name: str,
                         means_pvalues_result_name: str,
                         deconvoluted_result_name: str,
                         debug_seed: str,
                         threads: int,
                         verbose: bool):
    print(verbose)
    try:
        LocalMethodLauncher(cpdb_app.create_app(verbose)).cpdb_statistical_analysis_local_method_launcher(meta_filename,
                                                                                                          counts_filename,
                                                                                                          project_name,
                                                                                                          iterations,
                                                                                                          threshold,
                                                                                                          output_path,
                                                                                                          means_result_name,
                                                                                                          pvalues_result_name,
                                                                                                          significant_mean_result_name,
                                                                                                          means_pvalues_result_name,
                                                                                                          deconvoluted_result_name,
                                                                                                          debug_seed,
                                                                                                          threads)
    except (ReadFileException, ParseMetaException) as e:
        app_logger.error(e)
    except:
        app_logger.error('Unexpected error')


@click.command()
@click.argument('meta-filename')
@click.argument('counts-filename')
@click.option('--project-name', default='', help='Name of the project. It creates a subfolder in output folder')
@click.option('--threshold', default=0.1, help='% of cells expressing a gene')
@click.option('--output-path', default='',
              help='Directory where the results will be allocated (the directory must exist) [out]')
@click.option('--means-result-name', default='means.txt', help='Means result namefile [means.txt]')
@click.option('--deconvoluted-result-name', default='deconvoluted.txt',
              help='Deconvoluted result namefile [deconvoluted.txt]')
@click.option('--verbose/--quiet', default=True, help='Print or hide cellphonedb logs [verbose]')
def analysis(meta_filename: str,
             counts_filename: str,
             project_name: str,
             threshold: float,
             output_path: str,
             means_result_name: str,
             deconvoluted_result_name: str,
             verbose: bool
             ):
    try:
        LocalMethodLauncher(cpdb_app.create_app(verbose)).cpdb_analysis_local_method_launcher(meta_filename,
                                                                                              counts_filename,
                                                                                              project_name,
                                                                                              threshold,
                                                                                              output_path,
                                                                                              means_result_name,
                                                                                              deconvoluted_result_name,
                                                                                              )
    except (ReadFileException, ParseMetaException) as e:
        app_logger.error(e)
    except:
        app_logger.error('Unexpected error')
