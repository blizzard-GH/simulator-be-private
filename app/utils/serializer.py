from sqlalchemy.orm import DeclarativeMeta

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
        result[column.name] = getattr(instance, column.name)

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
