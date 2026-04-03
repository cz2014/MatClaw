def test_lower_envelope(properties):
    import numpy as np
    expected_properties = {
        "lower_envelope": {
            "format": "list of tuples",
            "value": [(4, 12), (3, 8), (-2, 1), (-5, 4)]
        },
        "transitions": {
            "format": "list of tuples",
            "value": [(-5, -8), (-4, -4), (-1.4, 3.8), (1, -1), (2, -6)]
        }
    }
    
    errors = []
    
    for property_name, expected_info in expected_properties.items():
        expected_value = expected_info['value']
        expected_format = expected_info['format']
        
        if property_name not in properties:
            errors.append(f"{property_name} not found in input properties")
            continue
        
        actual_value = properties[property_name]
        
        # Check type
        if expected_format not in ("np.allclose", "list of tuples") and not isinstance(actual_value, eval(expected_format)):
            errors.append(f"{property_name} is not of type {expected_format}")
            continue

        # Check value
        if expected_format in ("list", "list of tuples"):
            if not isinstance(actual_value, list):
                errors.append(f"{property_name} is not of type {expected_format}")
                continue
            if isinstance(actual_value, list) and expected_value and isinstance(expected_value[0], tuple):
                actual_value = [tuple(x) if isinstance(x, list) else x for x in actual_value]
            if actual_value != expected_value:
                errors.append(f"{property_name}: Expected {expected_value} but got {actual_value}")
        elif actual_value != expected_value:
            errors.append(f"{property_name}: Expected {expected_value} but got {actual_value}")
    
    if errors:
        errors.append(len(errors))
        errors.append(len(expected_properties))
        return errors
    else:
        return "ok"