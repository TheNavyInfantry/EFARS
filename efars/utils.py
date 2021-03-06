import datetime
import glob
import os
import shutil
from threading import Timer

from PyPDF2 import PdfFileMerger

import config


def allowed_file(filename):
    if not "." in filename:
        return False

    ext = filename.rsplit(".", 1)[1]

    if ext in config.Config.ALLOWED_EXTENSIONS:
        return True
    else:
        return False


def folder_exists():
    default_path = config.Config.DEFAULT_PATH
    plot_path = default_path + config.Config.PLOT_PATH
    plot_sub_path = plot_path + datetime.datetime.now().strftime("%y%m%d_%H%M%S_%f")
    result_path = default_path + config.Config.RESULT_PATH

    is_dp_exists = os.path.exists(default_path)
    is_pp_exists = os.path.exists(plot_path)
    is_rp_exists = os.path.exists(result_path)

    if not is_dp_exists and not is_pp_exists and not is_rp_exists:
        os.mkdir(default_path), os.mkdir(plot_path), os.mkdir(result_path)

    if not os.path.exists(plot_sub_path):
        os.mkdir(plot_sub_path)


def generate_filename():
    basename = 'plot'
    timestamp = datetime.datetime.now().strftime("%y%m%d_%H%M%S_%f")
    ext = '.'.join([timestamp, 'pdf'])

    return '_'.join([basename, ext])


def create_plot_name():
    newest = max(glob.glob(os.path.join(config.Config.DEFAULT_PATH + config.Config.PLOT_PATH, '*/')),
                 key=os.path.getmtime)
    return ''.join([newest, generate_filename()])


def pdf_merge():
    result_path = config.Config.DEFAULT_PATH + config.Config.RESULT_PATH
    newest_plot_folder = max(glob.glob(os.path.join(config.Config.DEFAULT_PATH + config.Config.PLOT_PATH, '*/')),
                             key=os.path.getmtime)

    pdf_list = [file for file in glob.glob(newest_plot_folder + "*.pdf")]
    pdf_list.sort()

    merger = PdfFileMerger()

    for pdf in pdf_list:
        merger.append(pdf)

    filename = ".".join([datetime.datetime.now().strftime("%y%m%d_%H%M%S_%f"), "pdf"])
    merger.write(result_path + filename)
    merger.close()

    return filename


def get_absolute_file_path(filename):
    return config.Config.DEFAULT_PATH + config.Config.RESULT_PATH + filename


def clear_conversions():
    path = config.Config.DEFAULT_PATH
    if os.path.exists(path):
        shutil.rmtree(path)
    Timer(86400, clear_conversions).start()  # Executed every 24 hours (in seconds)