import logging
import json
import os
import psycopg2
import pandas as pd
from dotenv import load_dotenv
from fastapi import APIRouter
from pydantic import BaseModel, Field, validator
import numpy as np

# from imblearn.pipeline import make_pipeline as make_pipeline_imb

log = logging.getLogger(__name__)
router = APIRouter()

# Load environment variables from .env
load_dotenv()


# Class that gets referenced by routes
class PostgreSQL:
    def __init__(self):
        "Add custom fields here"

        DB_NAME = os.getenv("DB_NAME")
        DB_USER = os.getenv("DB_USER")
        DB_PASSWORD = os.getenv("DB_PASSWORD")
        DB_HOST = os.getenv("DB_HOST")
        DB_PORT = os.getenv("DB_PORT")

        self.connection = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD,
                                  host=DB_HOST, port=DB_PORT)

    # methods can reference this variable
    columns1 = ['bridge_name', 'bridge_opportunity_project_code',
       'bridge_opportunity_needs_assessment',
       'bridge_opportunity_level1_government',
       'bridge_opportunity_level2_government',
       'bridge_opportunity_gps_latitude', 'bridge_opportunity_gps_longitude',
       'bridge_opportunity_bridge_type', 'bridge_opportunity_span_m',
       'bridge_opportunity_individuals_directly_served',
       'bridge_opportunity_comments', 'form_form_name', 'form_created_by',
       'proposed_bridge_location_gps_latitude',
       'proposed_bridge_location_gps_longitude', 'current_crossing_method',
       'nearest_all_weather_crossing_point', 'days_per_year_river_is_flooded',
       'flood_duration_during_rainy_season', 'market_access_blocked_by_river',
       'education_access_blocked_by_river', 'health_access_blocked_by_river',
       'other_access_blocked_by_river', 'primary_occupations',
       'primary_crops_grown', 'river_crossing_deaths_in_last_3_years',
       'river_crossing_injuries_in_last_3_years', 'incident_descriptions',
       'notes_on_social_information', 'cell_service_quality',
       'four_wd _accessibility', 'name_of_nearest_city',
       'name_of_nearest_paved_or_sealed_road', 'bridge_classification',
       'flag_for_rejection', 'rejection_reason', 'bridge_type',
       'estimated_span_m', 'height_differential_between_banks',
       'bridge_opportunity_general_project_photos',
       'bridge_opportunity_casesafeid', 'country', 'good_site']

    columns2 = ['bridge_opportunity_bridge_type', 'bridge_opportunity_span_m',
       'days_per_year_river_is_flooded', 'bridge_classification',
       'flag_for_rejection', 'height_differential_between_banks',
       'project_code']

    col_dic = {'b2p_lab28d_sk_tab': columns1, 'predict_sk_tab': columns2}

    def conn_curs(self):
        """
        makes a connection to the database
        """
        # Establishes connection and cursor
        connection = self.connection
        cursor = self.connection.cursor()
        return connection, cursor


    # def close(self):
    #     self.connection.close()

    def fetch_query_records(self, query: str):
        """This is a custom query, that returns all the records based on custom query"""
        # Establishes connection and cursor
        conn, cursor = self.conn_curs()
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return result

    def fetch_all_records(self, tablename: str='b2p_lab28d_sk_tab'):
        """returns all data/records in json format"""
        # Establishes connection and cursor
        conn, cursor = self.conn_curs()
        query = f""" SELECT * from {tablename};"""
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        # create a dataframe from result
        df = pd.DataFrame(result, columns=['index'] + self.col_dic[tablename])
        df = df.iloc[:, 1:]  # skip 1 column, as it corresponds to an index column
        df_json = df.to_json(orient='records')
        parsed = json.loads(df_json)
        return parsed

    def fetch_query_given_project(self, project_code: str, tablename: str = 'predict_sk_tab'):
        # Establishes connection and cursor
        conn, cursor = self.conn_curs()
        query = f"""SELECT * FROM {tablename} WHERE bridge_opportunity_project_code = '{project_code}';""" 
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        df = pd.DataFrame(result, columns=['index'] + self.col_dic[tablename])  #
        df = df.iloc[:, 1:]  # skip 1 column, as it corresponds to an index column
        df_json = df.to_json(orient='records')
        parsed = json.loads(df_json)
        return parsed

class Item(BaseModel):
    """Use this data model to parse the request body JSON."""

    project_code: str = Field(..., example='1007374')
    tablename: str = Field(..., example='predict_sk_tab')



@router.post('/data_by_bridge_code')
async def get_record(item: Item):
    """
    # Returns a record, based on project_code and DB table name

    ### Request Body
    - `project_code`: string
    - `tablename`: string

    ### Response with selected columns used for modeling based on Bridge Code in JSON FORMAT
    - ['bridge_opportunity_bridge_type', 'bridge_opportunity_span_m',
       'days_per_year_river_is_flooded', 'bridge_classification',
       'flag_for_rejection', 'height_differential_between_banks',
       'project_code']
    
    - tablenames = 'predict_sk_tab' , 'b2p_lab28d_sk_tab'

    """

    pg = PostgreSQL()
    json_output = pg.fetch_query_given_project(item.project_code, item.tablename)
    return json_output

@router.get('/all_data')
async def get_all_record():
    """
    #Returns All Data/Records in JSON FORMAT
    """
    pg = PostgreSQL()
    return_json = pg.fetch_all_records()
    return return_json