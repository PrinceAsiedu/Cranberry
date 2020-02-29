
class Logger(object):
    """A file-based message logger with the following properties 
    
    Attributes:
        file_name: a string representing the full path of the log file to which 
        this logger will write its message
        """
    
    def __init__(self, file_name):
        """Return a logger object whose file_name is *file_name*"""
        self.file_name = file_name
            
    def _write_log(self, level, msg, logtime):
        with open(self.file_name, 'a') as log_file:
                log_file.write('[{0}]\n\n{1}\nDatetime: {2}\n\n'.format(level,msg,logtime))

    def critical(self, msg, logtime):
        self._write_log('CRITICAL', msg, logtime)

    def error(self, msg, logtime):
        self._write_log('ERROR', msg, logtime)

    def warn(self, msg, logtime):
       self._write_log('WARN', msg, logtime)

    def info(self, msg, logtime):
       self._write_log('INFO', msg, logtime)

    def debug(self, msg, logtime):
       self._write_log('DEBUG', msg, logtime)