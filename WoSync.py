from configparser import ConfigParser
from filecmp import dircmp
import time
import datetime
import os
from fnmatch import fnmatch
from shutil import copyfile

__BOOLEAN__ = ("yes", "no")

__LOG_FOLDER__ = "/Logs/"
__LOG_FILE_POSFIX__ = "_WoSync_log.txt"
__LOG_LEVEL__ = ("error", "action", "verbose")
__LOG_LEVEL_ERROR__ = "error"
__LOG_LEVEL_ACTION__ = "action"
__LOG_LEVEL_VERBOSE__ = "verbose"

__COMPARISSON_TYPE_SAME__ = "same"
__COMPARISSON_TYPE_DIFF__ = "diff"
__COMPARISSON_TYPE_FUNNY__ = "funny"
__COMPARISSON_TYPE_LEFT__ = "left"
__COMPARISSON_TYPE_RIGHT__ = "right"

__COMPARISSON_TYPE__ = (__COMPARISSON_TYPE_SAME__, __COMPARISSON_TYPE_DIFF__, __COMPARISSON_TYPE_FUNNY__,
                        __COMPARISSON_TYPE_LEFT__, __COMPARISSON_TYPE_RIGHT__)

__ACTION_IGNORE__ = "ignore"
__ACTION_DELETE_BOTH__ = "deleteBoth"
__ACTION_DELETE_LEFT__ = "deleteLeft"
__ACTION_DELETE_RIGHT__ = "deleteRigth"
__ACTION_COPY_LEFT_2_RIGHT__ = "copyLeft2Right"
__ACTION_COPY_RIGHT_2_LEFT__ = "copyRigth2Left"
__ACTION_MOVE_LEFT_2_RIGHT__ = "moveLeft2Right"
__ACTION_MOVE_RIGHT_2_LEFT__ = "moveRigth2Left"

__ACTION_OP__ = (__ACTION_IGNORE__, __ACTION_DELETE_BOTH__, __ACTION_DELETE_LEFT__,
                 __ACTION_DELETE_RIGHT__, __ACTION_COPY_LEFT_2_RIGHT__, __ACTION_COPY_RIGHT_2_LEFT__,
                 __ACTION_MOVE_LEFT_2_RIGHT__, __ACTION_MOVE_RIGHT_2_LEFT__)
__ACTION_LEFT_OP__ = (__ACTION_IGNORE__, __ACTION_DELETE_LEFT__,
                      __ACTION_COPY_LEFT_2_RIGHT__, __ACTION_MOVE_RIGHT_2_LEFT__)
__ACTION_RIGHT_OP__ = (__ACTION_IGNORE__, __ACTION_DELETE_RIGHT__,
                       __ACTION_COPY_RIGHT_2_LEFT__, __ACTION_MOVE_RIGHT_2_LEFT__)

__CONFIG_FILE__ = "WoSync.ini"

__CONFIG_SECTION_GENERAL__ = "General"
__CONFIG_SECTION_GENERAL_STOP_CONFIG_ERROR__ = "stop_config_error"
__CONFIG_SECTION_GENERAL_LOG_LEVEL__ = "log_level"

__CONFIG_SECTION_SOURCE1__ = "source1"
__CONFIG_SECTION_SOURCE2__ = "source2"
__CONFIG_SECTION_RECURSIVE__ = "recursive"
__CONFIG_SECTION_ONLY_FILES__ = "only_files"
__CONFIG_SECTION_LOG_LEVEL__ = "log_level"
__CONFIG_SECTION_LOG_OPERATIONS__ = "log_operations"
__CONFIG_SECTION_LOG_COMPARISSON__ = "log_comparisson"
__CONFIG_SECTION_INCLUDE_PATTERNS__ = "include_patterns"
__CONFIG_SECTION_EXCLUDE_PATTENRS__ = "exclude_patterns"
__CONFIG_SECTION_SIMULATE_OPERATIONS__ = "simulate_operations"
__CONFIG_SECTION_SAME_OPERATION__ = "same_operation"
__CONFIG_SECTION_DIFF_OPERATION__ = "diff_operation"
__CONFIG_SECTION_FUNNY_OPERATION__ = "funny_operation"
__CONFIG_SECTION_LEFT_OPERATION__ = "left_operation"
__CONFIG_SECTION_RIGTH_OPERATION__ = "right_operation"

__stop_config_error__ = "no"
__log_level__ = "verbose"
__syncs__ = []
__config_errors__ = []
__log__ = []


class Sync:
    _name = ""
    _error = False
    _error_text = []
    _init_process_timestamp = 0
    _end_process_timestamp = 0
    _log = []
    _files_deleted_source1 = 0
    _files_deleted_source2 = 0
    _files_copied2_source1 = 0
    _files_copied2_source2 = 0
    _files_moved2_source1 = 0
    _files_moved2_source2 = 0
    _files_same = 0
    _files_diff = 0
    _files_funny = 0
    _files_left = 0
    _files_right = 0

    _source1 = ""
    _source2 = ""
    _recursive = "yes"
    _only_files = "no"
    _log_level = "error"
    _log_operations = []
    _log_comparisson = []
    _include_patterns = ""
    _exclude_patterns = ""
    _simulate_operations = "no"
    _same_operation = __ACTION_IGNORE__
    _diff_operation = __ACTION_IGNORE__
    _funny_operation = __ACTION_IGNORE__
    _left_operation = __ACTION_IGNORE__
    _right_operation = __ACTION_IGNORE__

    def log(self, message, log_level):
        log_common(self._log, self._log_level, message, log_level)

    def __init__(self, name, source1, source2, recursive, only_files, log_level, log_operations, log_comparisson, include_patterns,
                 exclude_patterns, simulate_operations, same_operation, diff_operation, funny_operation, left_operation, right_operation):

        log("Inicio constructor", __LOG_LEVEL_VERBOSE__)
        if(name != ""):
            log("Config name OK", __LOG_LEVEL_VERBOSE__)
            self._name = name
        else:
            log("Config error in name", [
                __LOG_LEVEL_ERROR__, __LOG_LEVEL_VERBOSE__])
            self._error = True
            self._error_text.append(
                "ERROR [" + self._name + "]: Config error in name")

        if(source1 != ""):
            log("Config source1 OK", __LOG_LEVEL_VERBOSE__)
            self._source1 = source1
        else:
            log("Config error in source1", [
                __LOG_LEVEL_ERROR__, __LOG_LEVEL_VERBOSE__])
            self._error = True
            self._error_text.append(
                "ERROR [" + self._name + "]: Config error in source1")

        if(source2 != ""):
            log("Config source2 OK", __LOG_LEVEL_VERBOSE__)
            self._source2 = source2
        else:
            log("Config error in source2", [
                __LOG_LEVEL_ERROR__, __LOG_LEVEL_VERBOSE__])
            self._error = True
            self._error_text.append(
                "ERROR [" + self._name + "]: Config error in source2")

        if(recursive in __BOOLEAN__):
            log("Config recursive OK", __LOG_LEVEL_VERBOSE__)
            self._recursive = recursive
        else:
            log("Config error in recursive", [
                __LOG_LEVEL_ERROR__, __LOG_LEVEL_VERBOSE__])
            self._error = True
            self._error_text.append(
                "ERROR [" + self._name + "]: Config error in recursive")

        if(only_files in __BOOLEAN__):
            log("Config only_files OK", __LOG_LEVEL_VERBOSE__)
            self._only_files = only_files
        else:
            log("Config error in only_files", [
                __LOG_LEVEL_ERROR__, __LOG_LEVEL_VERBOSE__])
            self._error = True
            self._error_text.append(
                "ERROR [" + self._name + "]: Config error in only_files")

        if(log_level in __LOG_LEVEL__):
            log("Config log_level OK", __LOG_LEVEL_VERBOSE__)
            self._log_level = log_level
        else:
            log("Config error in log_level", [
                __LOG_LEVEL_ERROR__, __LOG_LEVEL_VERBOSE__])
            self._error = True
            self._error_text.append(
                "ERROR [" + self._name + "]: Config error in log_level")
        error = False
        for log_op in log_operations:
            if(log_op not in __ACTION_OP__):
                error = True

        if(not error):
            log("Config log_operations OK", __LOG_LEVEL_VERBOSE__)
            self._log_operations = log_operations
        else:
            log("Config error in log_operations", [
                __LOG_LEVEL_ERROR__, __LOG_LEVEL_VERBOSE__])
            self._error = True
            self._error_text.append(
                "ERROR [" + self._name + "]: Config error in log_operations")

        error = False
        for log_comp in log_comparisson:
            if(log_comp not in __COMPARISSON_TYPE__):
                error = True

        if(not error):
            log("Config log_comparisson OK", __LOG_LEVEL_VERBOSE__)
            self._log_comparisson = log_comparisson
        else:
            log("Config error in log_comparisson", [
                __LOG_LEVEL_ERROR__, __LOG_LEVEL_VERBOSE__])
            self._error = True
            self._error_text.append(
                "ERROR [" + self._name + "]: Config error in log_comparisson")

        if(simulate_operations in __BOOLEAN__):
            log("Config simulate_operations OK", __LOG_LEVEL_VERBOSE__)
            self._simulate_operations = simulate_operations
        else:
            log("Config error in simulate_operations", [
                __LOG_LEVEL_ERROR__, __LOG_LEVEL_VERBOSE__])
            self._error = True
            self._error_text.append(
                "ERROR [" + self._name + "]: Config error in simulate_operations")

        if(same_operation in __ACTION_OP__):
            log("Config same_operation OK", __LOG_LEVEL_VERBOSE__)
            self._same_operation = same_operation
        else:
            log("Config error in same_operation", [
                __LOG_LEVEL_ERROR__, __LOG_LEVEL_VERBOSE__])
            self._error = True
            self._error_text.append(
                "ERROR [" + self._name + "]: Config error in same_operation")

        if(diff_operation in __ACTION_OP__):
            log("Config diff_operation OK", __LOG_LEVEL_VERBOSE__)
            self._diff_operation = diff_operation
        else:
            log("Config error in diff_operation", [
                __LOG_LEVEL_ERROR__, __LOG_LEVEL_VERBOSE__])
            self._error = True
            self._error_text.append(
                "ERROR [" + self._name + "]: Config error in diff_operation")

        if(funny_operation in __ACTION_OP__):
            log("Config funny_operation OK", __LOG_LEVEL_VERBOSE__)
            self._funny_operation = funny_operation
        else:
            log("Config error in funny_operation", [
                __LOG_LEVEL_ERROR__, __LOG_LEVEL_VERBOSE__])
            self._error = True
            self._error_text.append(
                "ERROR [" + self._name + "]: Config error in funny_operation")

        if(left_operation in __ACTION_LEFT_OP__):
            log("Config left_operation OK", __LOG_LEVEL_VERBOSE__)
            self._left_operation = left_operation
        else:
            log("Config error in left_operation", [
                __LOG_LEVEL_ERROR__, __LOG_LEVEL_VERBOSE__])
            self._error = True
            self._error_text.append(
                "ERROR [" + self._name + "]: Config error in left_operation")

        if(right_operation in __ACTION_RIGHT_OP__):
            log("Config right_operation OK", __LOG_LEVEL_VERBOSE__)
            self._right_operation = right_operation
        else:
            log("Config error in right_operation", [
                __LOG_LEVEL_ERROR__, __LOG_LEVEL_VERBOSE__])
            self._error = True
            self._error_text.append(
                "ERROR [" + self._name + "]: Config error in right_operation")

    def process_operation(self, operation, file, left, right):
        path_left = left+file
        path_right = right+file

        error = False

        if(operation == __ACTION_IGNORE__):
            if(operation in self._log_operations):
                self.log("Executing IGNORE to %s" % (file), [
                    __LOG_LEVEL_ACTION__, __LOG_LEVEL_VERBOSE__])
        elif(operation == __ACTION_DELETE_BOTH__):

            if(self._simulate_operations != "yes"):
                if os.path.exists(path_left):
                    os.remove(path_left)
                else:
                    if(operation in self._log_operations):
                        self.log("Error executing DELETE BOTH: %s not found" % (path_left), [
                            __LOG_LEVEL_ERROR__, __LOG_LEVEL_VERBOSE__])
                    error = True
                if os.path.exists(path_right):
                    os.remove(path_right)
                else:
                    if(operation in self._log_operations):
                        self.log("Error executing DELETE BOTH: %s not found" % (path_right), [
                            __LOG_LEVEL_ERROR__, __LOG_LEVEL_VERBOSE__])
                    error = True

            if(not error):
                if(operation in self._log_operations):
                    self.log("Executing DELETE BOTH to %s and %s" % (path_left, path_right), [
                        __LOG_LEVEL_ACTION__, __LOG_LEVEL_VERBOSE__])
        elif(operation == __ACTION_DELETE_LEFT__):
            if(self._simulate_operations != "yes"):
                if os.path.exists(path_left):
                    os.remove(path_left)
                else:
                    if(operation in self._log_operations):
                        self.log("Error executing DELETE LEFT: %s not found" % (path_left), [
                            __LOG_LEVEL_ERROR__, __LOG_LEVEL_VERBOSE__])
                    error = True

            if(not error):
                if(operation in self._log_operations):
                    self.log("Executing DELETE LEFT to %s" % (path_left), [
                        __LOG_LEVEL_ACTION__, __LOG_LEVEL_VERBOSE__])
        elif(operation == __ACTION_DELETE_RIGHT__):
            if(self._simulate_operations != "yes"):
                if os.path.exists(path_right):
                    os.remove(path_right)
                else:
                    if(operation in self._log_operations):
                        self.log("Error executing DELETE RIGHT: %s not found" % (path_right), [
                            __LOG_LEVEL_ERROR__, __LOG_LEVEL_VERBOSE__])
                    error = True

            if(not error):
                if(operation in self._log_operations):
                    self.log("Executing DELETE RIGHT to %s" % (path_right), [
                        __LOG_LEVEL_ACTION__, __LOG_LEVEL_VERBOSE__])
        elif(operation == __ACTION_COPY_LEFT_2_RIGHT__):
            if(self._simulate_operations != "yes"):
                if os.path.exists(path_left):
                    shutil.copy2(path_left, path_right)
                else:
                    if(operation in self._log_operations):
                        self.log("Error executing COPY LEFT TO RIGHT: %s not found" % (path_left), [
                            __LOG_LEVEL_ERROR__, __LOG_LEVEL_VERBOSE__])
                    error = True

            if(not error):
                if(operation in self._log_operations):
                    self.log("Executing COPY LEFT TO RIGHT to %s and %s" % (path_left, path_right), [
                        __LOG_LEVEL_ACTION__, __LOG_LEVEL_VERBOSE__])
        elif(operation == __ACTION_COPY_RIGHT_2_LEFT__):
            if(self._simulate_operations != "yes"):
                if os.path.exists(path_right):
                    shutil.copy2(path_right, path_left)
                else:
                    if(operation in self._log_operations):
                        self.log("Error executing COPY RIGHT TO LEFT: %s not found" % (path_right), [
                            __LOG_LEVEL_ERROR__, __LOG_LEVEL_VERBOSE__])
                    error = True

            if(not error):
                if(operation in self._log_operations):
                    self.log("Executing COPY RIGHT TO LEFT to %s and %s" % (path_right, path_left), [
                        __LOG_LEVEL_ACTION__, __LOG_LEVEL_VERBOSE__])
        elif(operation == __ACTION_MOVE_LEFT_2_RIGHT__):
            if(self._simulate_operations != "yes"):
                if os.path.exists(path_left):
                    shutil.copy2(path_left, path_right)
                    os.remove(path_left)
                else:
                    if(operation in self._log_operations):
                        self.log("Error executing MOVE LEFT TO RIGHT: %s not found" % (path_left), [
                            __LOG_LEVEL_ERROR__, __LOG_LEVEL_VERBOSE__])
                    error = True

            if(not error):
                if(operation in self._log_operations):
                    self.log("Executing MOVE LEFT TO RIGHT to %s and %s" % (path_left, path_right), [
                        __LOG_LEVEL_ACTION__, __LOG_LEVEL_VERBOSE__])
        elif(operation == __ACTION_MOVE_RIGHT_2_LEFT__):
            if(self._simulate_operations != "yes"):
                if os.path.exists(path_right):
                    shutil.copy2(path_right, path_left)
                    os.remove(path_right)
                else:
                    if(operation in self._log_operations):
                        self.log("Error executing MOVE RIGHT TO LEFT: %s not found" % (path_right), [
                            __LOG_LEVEL_ERROR__, __LOG_LEVEL_VERBOSE__])
                    error = True

            if(not error):
                if(operation in self._log_operations):
                    self.log("Executing MOVE RIGHT TO LEFT to %s and %s" % (path_right, path_left), [
                        __LOG_LEVEL_ACTION__, __LOG_LEVEL_VERBOSE__])

    def process_file(self, comparisson_type, file, left, rigth):
        # filtramos por los patrones
        file_excluded = False
        if(self._include_patterns != ""):
            patterns = self._include_patterns.split(",")
            for pattern in patterns:
                if not any(fnmatch.filter(file, pattern)):
                    file_excluded = True

        if(self._exclude_patterns != ""):
            patterns = self._exclude_patterns.split(",")
            for pattern in patterns:
                if any(fnmatch.filter(file, pattern)):
                    file_excluded = True

        if(file_excluded):
            self.log("File %s categorized as %s is EXCLUDED from processing" %
                     (file, comparisson_text), __LOG_LEVEL_VERBOSE__)
        else:
            operation = __ACTION_IGNORE__
            if(comparisson_type == __COMPARISSON_TYPE_SAME__):
                operation = self._same_operation
            elif(comparisson_type == __COMPARISSON_TYPE_DIFF__):
                operation = self._diff_operation
            elif(comparisson_type == __COMPARISSON_TYPE_FUNNY__):
                operation = self._funny_operation
            elif(comparisson_type == __COMPARISSON_TYPE_LEFT__):
                operation = self._left_operation
            elif(comparisson_type == __COMPARISSON_TYPE_RIGHT__):
                operation = self._right_operation

            if(comparisson_type in self._log_comparisson):
                self.log("Processing file %s categorized as %s" %
                         (file, comparisson_type), __LOG_LEVEL_VERBOSE__)

            self.process_operation(operation, file, left, rigth)

    def process_dcmp(self, dcmp):
        for file in dcmp.same_files:
            self._files_same += 1
            self.process_file(__COMPARISSON_TYPE_SAME__,
                              file, dcmp.left, dcmp.right)

        for file in dcmp.diff_files:
            self._files_diff += 1
            self.process_file(__COMPARISSON_TYPE_DIFF__,
                              file, dcmp.left, dcmp.right)

        for file in dcmp.funny_files:
            self._files_funny += 1
            self.process_file(__COMPARISSON_TYPE_FUNNY__,
                              file, dcmp.left, dcmp.right)

        for file in dcmp.left_only:
            self._files_left += 1
            self.process_file(__COMPARISSON_TYPE_LEFT__,
                              file, dcmp.left, dcmp.right)

        for file in dcmp.right_only:
            self._files_right += 1
            self.process_file(__COMPARISSON_TYPE_RIGHT__,
                              file, dcmp.left, dcmp.right)

        if(self._only_files != "yes"):
            for sub_dcmp in dcmp.subdirs.values():
                self.process_dcmp(sub_dcmp)

    def process_sync(self):

        self.log("-------------------------------- Start sync of %s between %s and %s" % (self._name, self._source1, self._source2), [
            __LOG_LEVEL_ACTION__, __LOG_LEVEL_VERBOSE__])
        self._init_process_timestamp = time.time()

        dcmp = dircmp(self._source1, self._source2)

        self.process_dcmp(dcmp)

        self._end_process_timestamp = time.time()
        self.log("End sync of %s" % (self._name), [
            __LOG_LEVEL_ACTION__, __LOG_LEVEL_VERBOSE__])

        process_time = self._end_process_timestamp - self._init_process_timestamp
        self.log("Time Process (ms): %d" % (process_time), [
            __LOG_LEVEL_ACTION__, __LOG_LEVEL_VERBOSE__])
        processed_files = self._files_same + self._files_diff + \
            self._files_funny + self._files_left + self._files_right
        self.log("Total files processed: %d" % (processed_files), [
            __LOG_LEVEL_ACTION__, __LOG_LEVEL_VERBOSE__])
        self.log("Total files processed in %s: %d deleted, %d copied and %d moved" %
                 (self._source1, self._files_deleted_source1, self._files_copied2_source1,
                  self._files_moved2_source1), [
                     __LOG_LEVEL_ACTION__, __LOG_LEVEL_VERBOSE__])
        self.log("Total files processed in %s: %d deleted, %d copied and %d moved" %
                 (self._source2, self._files_deleted_source2, self._files_copied2_source2,
                  self._files_moved2_source2), [
                     __LOG_LEVEL_ACTION__, __LOG_LEVEL_VERBOSE__])

        self.log("Total same files processed: %d" % (self._files_same), [
            __LOG_LEVEL_VERBOSE__])
        self.log("Total diff files processed: %d" % (self._files_diff), [
            __LOG_LEVEL_VERBOSE__])
        self.log("Total funny files processed: %d" % (self._files_funny), [
            __LOG_LEVEL_VERBOSE__])
        self.log("Total left files processed: %d" % (self._files_left), [
            __LOG_LEVEL_VERBOSE__])
        self.log("Total right files processed: %d" % (self._files_right), [
            __LOG_LEVEL_VERBOSE__])
        self.log("-------------------------------- End sync of %s" % (self._name), [
            __LOG_LEVEL_ACTION__, __LOG_LEVEL_VERBOSE__])


def log(message, log_level):
    log_common(__log__, __log_level__, message, log_level)


def log_common(log_instance, log_level_instance, message, log_level):
    if(log_level_instance in log_level):
        now = datetime.datetime.now()
        time = now.strftime("%Y-%m-%d  %H:%M:%S.%f")
        time_head = "\n[%s]" % (time)
        log_instance.append(time_head+message)


def read_config():
    global __log_level__
    global __stop_config_error__
    global __syncs__
    global __config_errors__

    log("Start read config", [
        __LOG_LEVEL_ERROR__, __LOG_LEVEL_ACTION__, __LOG_LEVEL_VERBOSE__])

    retcode = 0

    config_object = ConfigParser()
    config_path = os.path.dirname(__file__)+"/"+__CONFIG_FILE__
    config_object.read(config_path)

    log("Load config file %s" %
        (config_path), [__LOG_LEVEL_ERROR__, __LOG_LEVEL_ACTION__, __LOG_LEVEL_VERBOSE__])

    for config_section in config_object.sections():
        log("Loading config section %s" %
            (config_section), [__LOG_LEVEL_ERROR__, __LOG_LEVEL_ACTION__, __LOG_LEVEL_VERBOSE__])
        # General section
        if(config_section == __CONFIG_SECTION_GENERAL__):
            # log_level config
            log_level = config_object[__CONFIG_SECTION_GENERAL__][
                __CONFIG_SECTION_GENERAL_LOG_LEVEL__]
            if(log_level not in __LOG_LEVEL__):
                log("Config error in log_level set default log_level= error", [
                    __LOG_LEVEL_ERROR__, __LOG_LEVEL_VERBOSE__])
                log_level = "error"

            __log_level__ = log_level

            log("LogLevel = %s" % (log_level), [__LOG_LEVEL_VERBOSE__])

            # stop_config_error config
            stop_config_error = config_object[__CONFIG_SECTION_GENERAL__][
                __CONFIG_SECTION_GENERAL_STOP_CONFIG_ERROR__]
            if(stop_config_error in __BOOLEAN__):
                log("Config stop_config_error OK", [__LOG_LEVEL_VERBOSE__])
                __stop_config_error__ = stop_config_error
            else:
                log("Config error in stop_config_error set default stop_config_error= no", [
                    __LOG_LEVEL_ERROR__, __LOG_LEVEL_VERBOSE__])
                __stop_config_error__ = "no"

            log("Parameter %s = %s" % (__CONFIG_SECTION_GENERAL_STOP_CONFIG_ERROR__,
                                       stop_config_error), [__LOG_LEVEL_VERBOSE__])

        # Syncs sections
        else:
            sync = Sync(config_section,
                        config_object[config_section][__CONFIG_SECTION_SOURCE1__],
                        config_object[config_section][__CONFIG_SECTION_SOURCE2__],
                        config_object[config_section][__CONFIG_SECTION_RECURSIVE__],
                        config_object[config_section][__CONFIG_SECTION_ONLY_FILES__],
                        config_object[config_section][__CONFIG_SECTION_LOG_LEVEL__],
                        config_object[config_section][__CONFIG_SECTION_LOG_OPERATIONS__].split('|'),
                        config_object[config_section][__CONFIG_SECTION_LOG_COMPARISSON__].split('|'),
                        config_object[config_section][__CONFIG_SECTION_INCLUDE_PATTERNS__],
                        config_object[config_section][__CONFIG_SECTION_EXCLUDE_PATTENRS__],
                        config_object[config_section][__CONFIG_SECTION_SIMULATE_OPERATIONS__],
                        config_object[config_section][__CONFIG_SECTION_SAME_OPERATION__],
                        config_object[config_section][__CONFIG_SECTION_DIFF_OPERATION__],
                        config_object[config_section][__CONFIG_SECTION_FUNNY_OPERATION__],
                        config_object[config_section][__CONFIG_SECTION_LEFT_OPERATION__],
                        config_object[config_section][__CONFIG_SECTION_RIGTH_OPERATION__])
            if(sync._error == True):
                retcode = -1
                __config_errors__.append(sync._error_text)
                log("Error loading config section %s" %
                    (config_section), [__LOG_LEVEL_VERBOSE__, __LOG_LEVEL_ERROR__])
            else:
                __syncs__.append(sync)
                log("End loading config section %s" %
                    (config_section), [__LOG_LEVEL_VERBOSE__])

    log("End read config", [
        __LOG_LEVEL_ERROR__, __LOG_LEVEL_ACTION__, __LOG_LEVEL_VERBOSE__])

    return retcode


def write_log(log):
    today = datetime.date.today()
    log_date = today.strftime("%Y-%m-%d")
    log_path = os.path.dirname(__file__)+__LOG_FOLDER__ + \
        log_date+__LOG_FILE_POSFIX__
    if not os.path.exists(os.path.dirname(log_path)):
        try:
            os.makedirs(os.path.dirname(log_path))
        except OSError as exc:
            if exc.errno != errno.EEXIST:
                raise

    f = open(log_path, "a")
    for log_msg in log:
        f.writelines(log_msg)
    f.close()

    log.clear()


log("########################### Start WoSync", [
    __LOG_LEVEL_ERROR__, __LOG_LEVEL_ACTION__, __LOG_LEVEL_VERBOSE__])

if(read_config() < 0):
    log("General configuration loaded with errors", [
        __LOG_LEVEL_ERROR__, __LOG_LEVEL_ACTION__, __LOG_LEVEL_VERBOSE__])

write_log(__log__)

for sync in __syncs__:
    sync.process_sync()
    write_log(sync._log)

log("########################### End WoSync", [
    __LOG_LEVEL_ERROR__, __LOG_LEVEL_ACTION__, __LOG_LEVEL_VERBOSE__])
write_log(__log__)
