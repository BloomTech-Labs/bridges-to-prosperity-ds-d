import logging
import random
import pickle

from fastapi import APIRouter
import pandas as pd
from pydantic import BaseModel, Field, validator

log = logging.getLogger(__name__)
router = APIRouter()


class Item_query(BaseModel):
    """Selected columns used in the model in JSON format"""

    bridge_classification: str = Field(..., example='Standard')
    bridge_opportunity_bridge_type: str = Field(..., example='Suspension Bridge')
    bridge_opportunity_span_m: float = Field(..., example=85.0)
    days_per_year_river_is_flooded: float = Field(..., example=121.0)
    flag_for_rejection: str = Field(..., example='No')
    height_differential_between_banks: float = Field(..., example=0.97)

    def to_df(self):
        """Convert pydantic object to pandas dataframe with 1 row."""
        return pd.DataFrame([dict(self)])

    # @validator('input1')
    # def title_must_be_a_string(cls, value):
    #     """Validate that Title is a string."""
    #     assert type(value) == str, f'Title == {value}, must be a string'
    #     return value
    #
    # @validator('output1')
    # def post_must_be_a_string(cls, value):
    #     """Validate that post is a string."""
    #     assert type(value) == str, f'Title == {value}, must be a string'
    #     return value


@router.post('/prediction')
async def predict(item: Item_query):
    """
    Returns Good_Site Prediction 0, 1

    ### Request Body
    ['bridge_opportunity_bridge_type',
    'bridge_opportunity_span_m',
    'days_per_year_river_is_flooded',
    'bridge_classification',
    'flag_for_rejection',
    'height_differential_between_banks']

    """
    
    query = item.to_df()

    def modelpredict(model, query):
        """
        query is dataframe for selected columns
        """
        return model.predict(query)[0], model.predict_proba(query)[0][int(model.predict(query)[0])]

    
    model = pickle.load(open("./app/api/gs_model",'rb'))

    (y_pred, y_proba) = modelpredict(model, query)

    return {'Good Site prediction': y_pred, 'Predicted Probability': y_proba}