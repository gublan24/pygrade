

import argparse

import pandas as pd
import configparser
import argparse
import os
import logging

import util

log = logging.getLogger(__name__)


def command_line_args():
    """Returns namespace with settings from command line"""
    log.debug("-> Command line args")
    parser = argparse.ArgumentParser(description="Merging Script")
    parser.add_argument("-D", "--debug", dest="DEBUG",
                        action="store_const", const=True,
                        help="Turn on debugging and verbose logging")
    parser.add_argument("-B", "--path-to-base-file", type=str, dest="BASE",
                        help="Path to base file.")
    parser.add_argument("-S", "--path-to-secondary-file", type=str, dest="SECOND",
                        help="Path to secondary file.")
    parser.add_argument("-P", "--primary-key", type=str, dest="PRIMARY",
                        help="Primary key on which we will merge the record")
    parser.add_argument("-PP", "--primary-key-of-second-file", type=str, dest="SECONDARY",
                        help="Primary key on of second file if it is different from the original file.")
    parser.add_argument("-T", "--base-file-target-column", type=str, dest="TARGETCOL",
                        help="The target column of the base file from which we will merge records.")
    parser.add_argument("-TT", "--secondary-file-target-column", type=str, dest="SECONDARYCOL",
                        help="The target column of the secondary file from which we will merge records.")
    cli_args = parser.parse_args()
    log.debug(f"<- Command line args: {cli_args}")
    return cli_args


def merge_dataframes_and_fill_null(base_file: str, secondary_file: str, merge_on_key: str,
                                   base_file_target_col: str, secondary_file_target_col: str,
                                   secondary_file_key=None):
    """

    :param base_file: The location of the main file (merge to file).
    :param secondary_file: The location of the secondary file (merge from).
    :param merge_on_key: The key for which we will merge the two files. Usually a column with a unique value on both.
    :param base_file_target_col: The column we want to merge to in the base file.
    :param secondary_file_target_col: The column we want to merge from in the secondary file.
    :param secondary_file_key: If the key in the base and secondary files have different names (but same values),
        then specify here.
    :return: None
    """
    # make sure the strings are not empty (pandas handles file existence).
    assert base_file
    assert secondary_file
    assert merge_on_key
    assert base_file_target_col
    assert secondary_file_target_col

    df_base = pd.read_csv(base_file)
    df_secondary = pd.read_csv(secondary_file)

    if secondary_file_key is not None:  # then we need to unify the key name (secondary <- base)
        df_secondary.rename(columns={f'{secondary_file_key}': f'{merge_on_key}'}, inplace=True)

    if base_file_target_col != secondary_file_target_col:
        # also in this case make sure the name in the secondary file match the one in the base file
        df_secondary.rename(columns={f'{secondary_file_target_col}': f'{base_file_target_col}'}, inplace=True)

    # the actual merge statement
    new_df = df_base.merge(df_secondary[[f"{merge_on_key}", f"{base_file_target_col}"]], on=merge_on_key, how="left")

    # the merge will result on the column name being amended with "_x" for the column coming from the base
    # and "_y" for the column coming from the secondary. We keep the one from secondary.
    new_df.rename(columns={f'{base_file_target_col}_y': f'{base_file_target_col}'}, inplace=True)

    cols = new_df.columns.tolist()
    idx = cols.index(f"{base_file_target_col}_x")  # the index of the original col
    new_df.drop(f"{base_file_target_col}_x", axis=1, inplace=True)
    cols = new_df.columns.tolist()
    cols = util.move_item_to_index(cols, base_file_target_col, idx)
    new_df = new_df[cols]
    new_df[base_file_target_col].fillna(0.0, inplace=True)

    new_df.to_csv(f"{util.get_absolut_path_dir(base_file)}/{util.get_filename_without_extension(base_file)}-"
                  f"{util.get_timestamp()}.csv", encoding='utf-8', index=False)


def configurations(path: str):
    if not os.path.exists(path):
        raise RuntimeError(f"Got a wrong path for the ini file {path}")

    config = configparser.ConfigParser()
    config.read(path)

    base = config["DEFAULT"]["base_file"]
    second = config["DEFAULT"]["secondary_file"]
    primary = config["DEFAULT"]["merge_on_key"]
    secondary = config["DEFAULT"]["secondary_file_key"]
    target_col = config["DEFAULT"]["base_file_target_col"]
    secondary_col = config["DEFAULT"]["secondary_file_target_col"]

    merge_dataframes_and_fill_null(base_file=base,
                                   secondary_file=second,
                                   merge_on_key=primary,
                                   base_file_target_col=target_col,
                                   secondary_file_target_col=secondary_col,
                                   secondary_file_key=secondary)


if __name__ == '__main__':
    cli = command_line_args()
    merge_dataframes_and_fill_null(base_file=cli.BASE,
                                   secondary_file=cli.SECOND,
                                   merge_on_key=cli.PRIMARY,
                                   base_file_target_col=cli.TARGETCOL,
                                   secondary_file_target_col=cli.SECONDARYCOL,
                                   secondary_file_key=cli.SECONDARY)
