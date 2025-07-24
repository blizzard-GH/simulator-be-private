from flask import json
from sqlalchemy.orm import DeclarativeMeta
from sqlalchemy.dialects.mysql import LONGTEXT

def model_to_dict(instance, include_relationships=False):
    """
    Convert a SQLAlchemy model instance to a dict.
    
    Args:
        instance: SQLAlchemy model instance
        include_relationships: Whether to include @relationship fields

    Returns:
        Dictionary representation of the model
    """
    if not isinstance(instance.__class__, DeclarativeMeta):
        raise TypeError("Object is not a SQLAlchemy model")

    result = {}
    for column in instance.__table__.columns:
        try:
            # result[column.name] = getattr(instance, column.name)
            value = getattr(instance, column.name)

            # Automatically parse LONGTEXT fields if possible
            if isinstance(column.type, LONGTEXT):
                try:
                    value = json.loads(value) if value else None
                except (ValueError, TypeError):
                    # Fall back to original value if not valid JSON
                    pass

            result[column.name] = value
        except AttributeError:
            # Skip unreadable fields (e.g., write-only properties like PASSWORD)
            continue

    # Optionally include @relationship fields
    if include_relationships:
        for rel in instance.__mapper__.relationships:
            val = getattr(instance, rel.key)
            if val is None:
                result[rel.key] = None
            elif rel.uselist:
                result[rel.key] = [model_to_dict(i) for i in val]
            else:
                result[rel.key] = model_to_dict(val)

    return result


def model_to_dict_with_types(instance):
    """
    Convert a SQLAlchemy model instance to dict with values + column types.
    
    Returns:
        Dict of {column: {"value": ..., "type": ...}}
    """
    return {
        column.name: {
            "value": getattr(instance, column.name),
            "type": str(column.type)
        }
        for column in instance.__table__.columns
    }


def models_to_list(instances, include_relationships=False):
    """
    Convert a list of model instances to list of dicts.
    """
    return [model_to_dict(i, include_relationships) for i in instances]


def serialize_model_or_list(instances, include_relationships=False):
    if instances is None:
        return None
    elif isinstance(instances, (list, tuple)):
        return [model_to_dict(i, include_relationships) for i in instances]
    else:
        return model_to_dict(instances, include_relationships)

