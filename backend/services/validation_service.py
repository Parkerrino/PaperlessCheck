"""Validation service for checklist operations."""


def validate_checklist_data(data):
    """Validate checklist creation/update data."""
    errors = []
    
    if not data.get('title') or not isinstance(data.get('title'), str):
        errors.append('Title is required and must be a string')
    
    if data.get('title') and len(data['title']) > 255:
        errors.append('Title must not exceed 255 characters')
    
    if data.get('description') and not isinstance(data.get('description'), str):
        errors.append('Description must be a string')
    
    return errors


def validate_checklist_item_data(data):
    """Validate checklist item creation/update data."""
    errors = []
    
    if not data.get('title') or not isinstance(data.get('title'), str):
        errors.append('Title is required and must be a string')
    
    if data.get('title') and len(data['title']) > 255:
        errors.append('Title must not exceed 255 characters')
    
    if 'completed' in data and not isinstance(data.get('completed'), bool):
        errors.append('Completed must be a boolean')
    
    if data.get('order_index') and not isinstance(data.get('order_index'), int):
        errors.append('Order index must be an integer')
    
    return errors
