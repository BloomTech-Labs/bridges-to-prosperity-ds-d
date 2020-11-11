# from dotenv import load_dotenv
import os
import psycopg2
from psycopg2.extensions import register_adapter, AsIs
import pandas as pd
import json
from dotenv import load_dotenv

import logging
import random

from fastapi import APIRouter
import pandas as pd
from pydantic import BaseModel, Field, validator
import os
import psycopg2
from psycopg2.extensions import register_adapter, AsIs
import pandas as pd
import json
from dotenv import load_dotenv

import logging
import random

from fastapi import APIRouter
import pandas as pd
from pydantic import BaseModel, Field, validator

log = logging.getLogger(__name__)
router = APIRouter()

# Load environment variables from .env
load_dotenv()


class PostgreSQL:
    def __init__(self):

        self.DB_NAME = os.getenv("DB_NAME")
        self.DB_USER = os.getenv("DB_USER")
        self.DB_PASSWORD = os.getenv("DB_PASSWORD")
        self.DB_HOST = os.getenv("DB_HOST")
        self.DB_PORT = os.getenv("DB_PORT")
        self.connection = psycopg2.connect(
            dbname=self.DB_NAME, user=self.DB_USER, password=self.DB_PASSWORD, host=self.DB_HOST, port='5432')

    def adapters(*args):
        for adapter in args:
            register_adapter(adapter, psycopg2._psycopg.AsIs)

    def cursor(self):
        self.cursor = self.connection.cursor()

    def execute(self, query):
        self.cursor.execute(query)

    def close(self):
        self.connection.close()

    def fetch_query_records(self, query: str):
        cursor = self.connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        return result

    def fetch_all_records(self):
        cursor = self.connection.cursor()
        # 'ID','country','province','district','district_id','sector','sector_id','cell','cell_id','village','village_id','name','project_code','type','stage','sub_stage','individuals_directly_served','span','lat','long','form','case_safe_id','opportunity_id','inc_income','inc_income_rwf','inc_income_usd','bridge_image']
        query = f"""SELECT "ID", country, province, district,district_id,sector,sector_id,cell,cell_id,village,village_id,name,project_code,type,stage,sub_stage,individuals_directly_served,span,lat,long,form,case_safe_id,opportunity_id,inc_income,inc_income_rwf,inc_income_usd,bridge_image FROM public."Bridges"  """
        cursor.execute(query)
        result = cursor.fetchall()
        columns = ['ID', 'country', 'province', 'district', 'district_id', 'sector', 'sector_id', 'cell', 'cell_id', 'village', 'village_id', 'name', 'project_code', 'type', 'stage',
                   'sub_stage', 'individuals_directly_served', 'span', 'lat', 'long', 'form', 'case_safe_id', 'opportunity_id', 'inc_income', 'inc_income_rwf', 'inc_income_usd', 'bridge_image']
        # columns = ['ID', 'country']
        df = pd.DataFrame(result, columns=columns)
        df_json = df.to_json(orient='records')
        parsed = json.loads(df_json)
        return parsed

    def fetch_query_given_project(self, project_code: int):
        cursor = self.connection.cursor()
        query = f"""SELECT * FROM public."Bridges" where project_code={project_code} """
        cursor.execute(query)
        result = cursor.fetchall()
        columns = ['ID', 'country', 'province', 'district', 'district_id', 'sector', 'sector_id', 'cell', 'cell_id', 'village', 'village_id', 'name', 'project_code', 'type', 'stage', 'sub_stage', 'individuals_directly_served', 'span', 'lat', 'long', 'community_served_1', 'community_served_1_id',
                   'community_served_2', 'community_served_2_id', 'community_served_3', 'community_served_3_id', 'community_served_4', 'community_served_4_id', 'community_served_5', 'community_served_5_id', 'form', 'case_safe_id', 'opportunity_id', 'inc_income', 'inc_income_rwf', 'inc_income_usd', 'bridge_image']
        df = pd.DataFrame(result, columns=columns)
        df_json = df.to_json(orient='records')
        parsed = json.loads(df_json)
        return parsed

    def fetch_query_given_project_and_columns(self, project_code: int, columns: []):
        cursor = self.connection.cursor()
        query = f"""SELECT * FROM public."Bridges" where project_code={project_code} """
        cursor.execute(query)
        result = cursor.fetchall()
        columns = ['ID', 'country', 'province', 'district', 'district_id', 'sector', 'sector_id', 'cell', 'cell_id', 'village', 'village_id', 'name', 'project_code', 'type', 'stage', 'sub_stage', 'individuals_directly_served', 'span', 'lat', 'long', 'community_served_1', 'community_served_1_id',
                   'community_served_2', 'community_served_2_id', 'community_served_3', 'community_served_3_id', 'community_served_4', 'community_served_4_id', 'community_served_5', 'community_served_5_id', 'form', 'case_safe_id', 'opportunity_id', 'inc_income', 'inc_income_rwf', 'inc_income_usd', 'bridge_image']
        df = pd.DataFrame(result, columns=columns)
        df_json = df.to_json(orient='records')
        parsed = json.loads(df_json)
        return parsed

    def fetch_query(self, query: str, columns: list):
        self.fetch_query_records(query)
        df = pd.DataFrame(response, columns=columns)
        return df.to_json(orient=records)


class Item(BaseModel):
    """Use this data model to parse the request body JSON."""

    def to_df(self):
        """Convert pydantic object to pandas dataframe with 1 row."""
        return pd.DataFrame([dict(self)])



@router.post('/database')
async def get_record(item: Item):
    """
    Returns all records from the database corresponding to a given project_code

    # Request Body
    - `project_code`: integer

    # Response
    - `ID`: integer, sequential
    - `country`: text
    - ......


    """
    X_new = item.to_df()
    item_str = item.to_string()
    project_code = int(item_str[item_str.find('=')+1:])
    pg = PostgreSQL()
    return_json = pg.fetch_query_given_project(project_code)
    return return_json


@router.get('/database')
async def get_all_record():
    """
    Returns all records from the database

    # Response
    - ID: integer, sequential
    - country: text
    - province: text
    - district: text
    - district_id: number
    - sector: text
    - sector_id: number
    - cell: text
    - cell_id: integer
    - village: text
    - name: text
    - project_code: integer
    - type: text
    - stage: text
    - sub_stage: text
    - individuals_directly_served: integer
    - span: integer
    - lat: double precision
    - long: double precision
    - community_served_1: text
    - community_served_1_id: integer
    - community_served_2: text
    - community_served_2_id: integer
    - community_served_3: text
    - community_served_3_id: integer
    - community_served_4: text
    - community_served_4_id: integer
    - community_served_5: text
    - community_served_5_id: integer
    - form: text
    - case_safe_id: text
    - opportunity_id: text
    - inc_income: double precision
    - inc_income_rwf: double precision
    - inc_income_usd: double precision
    - bridge_image: text


    """
    # X_new = item.to_df()
    # item_str = item.to_string()
    # project_code = int(item_str[item_str.find('=')+1:])
    pg = PostgreSQL()
    return_json = pg.fetch_all_records()
    return return_json
