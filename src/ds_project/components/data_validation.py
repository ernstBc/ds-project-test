import os
import pandas as pd
from src.ds_project import logger
from src.ds_project.utils.utils import create_directories
from src.ds_project.entity.entity_config import DataValidationConfig
import datetime

class DataValidation:
    '''
    Component to validate the data against the schema
    Arguments:
        config: DataValidationConfig object
    '''
    def __init__(self, config: DataValidationConfig):
        self.config = config
    
    def validate_data_schema(self) -> bool: 
        """
        Validate the data against the schema
        Returns:
            bool: True if validation is failure, False otherwise
        """
        status=True
        try:
            if not os.path.exists(self.config.validation_directory):
                create_directories([self.config.validation_directory])
            if not os.path.exists(self.config.STATUS_FILE):
                with open(self.config.STATUS_FILE, 'a') as f:
                    f.write("Data Schema Validation Status\n")
                    f.write("====================================\n")
                
            schema = [col for col in self.config.schema_file['COLUMNS'].keys()] + [target for target in self.config.schema_file['TARGET'].keys()]
            data=pd.read_csv(self.config.data_path)
            data_columns = data.columns.tolist()

            date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open(self.config.STATUS_FILE, 'a') as f:
                f.write(f"\n{date}\n")

            
            validation_error=False
            for column in schema:

                status = True
                if column not in data_columns:
                    status = False
                    validation_error=True

                    with open(self.config.STATUS_FILE, 'a') as f:
                        f.write(f"Column {column} - Status {status}:  {column} is not in the dataset\n")
                    continue

                schema_dtype = (self.config.schema_file['COLUMNS'][column]['type'] 
                                if column in self.config.schema_file['COLUMNS'] else self.config.schema_file['TARGET'][column]['type'])
                data_dtype = data[column].dtype

                if (schema_dtype == 'string'):
                    if (data_dtype != 'object'):
                        status = False
                        validation_error=True

                        with open(self.config.STATUS_FILE, 'a') as f:
                            f.write(f"""Column {column} - Status {status}: {column} dtype in the schema ({schema_dtype}) 
                                    is not matching to dtype in the dataset ({data_dtype})\n""")
                elif schema_dtype != data_dtype:
                    status = False
                    validation_error=True

                    with open(self.config.STATUS_FILE, 'a') as f:
                        f.write(f"""Column {column} - Status {status}: {column} dtype in the schema ({schema_dtype}) is 
                                not matching to dtype in the dataset ({data_dtype})\n""")
                else:
                    status = True
                    validation_error=False

                    with open(self.config.STATUS_FILE, 'a') as f:
                        f.write(f"Column {column} - Status {status}: is matching the schema\n")

            return validation_error
            
        except Exception as e:
            raise e
                    