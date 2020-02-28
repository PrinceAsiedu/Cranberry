from urllib.request import urlopen

def test_con():
    try:
        urlopen('https://www.google.com', timeout=10)
        return True
    except Exception as error:
        # return False
        raise error

class Logger(object):
    """A file-based message logger with the following properties 
    
    Attributes:
        file_name: a string representing the full path of the log file to which 
        this logger will write its message
        """
    
    def __init__(self, file_name):
        """Return a logger object whose file_name is *file_name*"""
        self.file_name = file_name
            
    def _write_log(self, level, msg):
        with open(self.file_name, 'a') as log_file:
                log_file.write('[{0}] {1}\n'.format(level,msg))

    def critical(self, msg):
        self._write_log('CRITICAL', msg)

    def error(self, msg):
        self._write_log('ERROR', msg)

    def warn(self, msg):
       self._write_log('WARN', msg)

    def info(self, msg):
       self._write_log('INFO', msg)

    def debug(self, msg):
       self._write_log('DEBUG', msg)


print(test_con())