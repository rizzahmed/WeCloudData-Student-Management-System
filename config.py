
import common as comm


class ConfigManager:
    def __init__(self):
        self.config = comm.ReadConfig()


    def get_database_config(self):
        return {
            'host' : self.config['Database']['host'],
            'port' : self.config['Database']['port'],
            'user' : self.config['Database']['user'],
            'password' : self.config['Database']['password'],
            'database' : self.config['Database']['database']
        }