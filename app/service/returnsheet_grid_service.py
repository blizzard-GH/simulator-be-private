from ..model.rs_returnsheet_grid import RSReturnsheetGrid
from ..utils.serializer import model_to_dict, models_to_list

def get_all_returnsheet_grid_service(limit=20):
    returnsheetGrid = RSReturnsheetGrid.query.limit(limit).all()
    return models_to_list(returnsheetGrid)