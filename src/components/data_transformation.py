import sys
from dataclasses import dataclass

import numpy as np 
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder,StandardScaler

from src.exception import CustomException
from src.logger import logging
import os

from src.utils import save_object

@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path=os.path.join('artifacts',"proprocessor.pkl")

# A small configuration dataclass used to hold the filesystem path where a preprocessor object 
# (e.g., an sklearn Pipeline or transformer) will be stored.

class DataTransformation:
    def __init__(self):
        self.data_transformation_config=DataTransformationConfig()

# Easy access: any method in DataTransformation can read configuration through self.data_transformation_config.

# Centralized defaults: all defaults live in one place (DataTransformationConfig), making unit tests 
#                       and experiments easier.

    def get_data_transformer_object(self):
        
    # The function builds two transformation pipelines (numeric and categorical), combines them with a 
    # ColumnTransformer, logs the column groups, and returns a single preprocessor that we can fit_transform 
    # on training data and transform on validation/test data.

    # Using Pipeline ensures steps are applied in order, prevents leakage, and integrates with sklearn tooling 

        try:
            numerical_columns = ["writing_score", "reading_score"]
            categorical_columns = [
                "gender",
                "race_ethnicity",
                "parental_level_of_education",
                "lunch",
                "test_preparation_course",
            ]

            num_pipeline=Pipeline(steps=[("imputer",SimpleImputer(strategy="median")),("scaler",StandardScaler())])

            cat_pipeline=Pipeline(
                steps=[
                ("imputer",SimpleImputer(strategy="most_frequent")),
                ("one_hot_encoder",OneHotEncoder()),
                ("scaler",StandardScaler(with_mean=False))
                ]
            )

            logging.info(f"Categorical columns: {categorical_columns}")
            logging.info(f"Numerical columns: {numerical_columns}")

            preprocessor=ColumnTransformer(
                [
                ("num_pipeline",num_pipeline,numerical_columns),
                ("cat_pipelines",cat_pipeline,categorical_columns)
                ]
            )

            # Using ColumnTransformer prevents us from manually handling different transformations and 
            # concatenating results (avoids bugs and keeps code clean).

            return preprocessor
        
        except Exception as e:
            raise CustomException(e,sys)
        
    def initiate_data_transformation(self,train_path,test_path):

        try:
            train_df=pd.read_csv(train_path)
            test_df=pd.read_csv(test_path)

            logging.info("Read train and test data completed")

            logging.info("Obtaining preprocessing object")

            preprocessing_obj=self.get_data_transformer_object()

            target_column_name="math_score"
            numerical_columns = ["writing_score", "reading_score"]

            input_feature_train_df=train_df.drop(columns=[target_column_name],axis=1)
            target_feature_train_df=train_df[target_column_name]

            input_feature_test_df=test_df.drop(columns=[target_column_name],axis=1)
            target_feature_test_df=test_df[target_column_name]

            logging.info( f"Applying preprocessing object on training dataframe and testing dataframe.")

            input_feature_train_arr=preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr=preprocessing_obj.transform(input_feature_test_df)

            train_arr = np.c_[ input_feature_train_arr, np.array(target_feature_train_df) ]
            test_arr = np.c_[ input_feature_test_arr, np.array(target_feature_test_df) ]

            # np.c_[A, B] stacks arrays column-wise (i.e., concatenates along axis=1).

            logging.info(f"Saved preprocessing object.")

            save_object(

                file_path=self.data_transformation_config.preprocessor_obj_file_path,
                obj=preprocessing_obj

            )

            # This calls our save_object utility (the pickle writer) to persist the fitted preprocessing_obj 
            # to disk at the configured path.

            # The fitted preprocessor contains learned parameters (medians, means/scales, fitted one-hot categories
            # ,encoders’ state). We must use the same transformation in training and later at inference/prediction
            # time to guarantee that new data is transformed exactly the same way.

            # Saving allows us to deploy the pipeline, or to load the preprocessor later when we train a model
            # in a separate step or serve the model in production.

            return (
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path,
            )
        
            # preprocessor_obj_file_path: the path (string) where the fitted preprocessor was saved. 
            
            # Returning it : lets the caller know where the preprocessor is stored, makes it easy for the 
            # downstream code (e.g., model trainer or inference component) to load the exact same transformer, and
            
            # Documents the artifact produced by the transformation step for logging / experiment tracking.

        except Exception as e:
            raise CustomException(e,sys)
