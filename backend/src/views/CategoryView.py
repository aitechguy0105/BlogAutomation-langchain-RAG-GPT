from flask import request, g, Blueprint, json, Response
from ..shared.Authentication import Auth
from ..models.CategoryModel import CategoryModel, CategorySchema

category_api = Blueprint('category_api', __name__)
category_schema = CategorySchema()