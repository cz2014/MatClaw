def test_substitution_generators(properties):
    import numpy as np
    expected_properties = {
        "defect_type": {
            "format": "bool",
            "value": True
        },
        "replaced_atoms_set_1": {
            "format": "set",
            "value": {"Mg", "Ca"}
        },
        "replaced_atoms_set_2": {
            "format": "set",
            "value": {"Mg"}
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
        
        # Check type (skip type check for np.allclose and set cases as they're handled separately)
        if expected_format not in ("np.allclose", "set") and not isinstance(actual_value, eval(expected_format)):
            errors.append(f"{property_name} is not of type {expected_format}")
            continue

        # Check value or use np.allclose for approximate comparisons
        if expected_format == "np.allclose":
            if not np.allclose(actual_value, expected_value):
                errors.append(f"{property_name}: Expected value close to {expected_value} but got {actual_value}")
        elif expected_format == "set":
            actual_as_set = set(actual_value) if isinstance(actual_value, (list, set)) else actual_value
            if not isinstance(actual_as_set, set):
                errors.append(f"{property_name} is not of type set (got {type(actual_value).__name__})")
                continue
            if actual_as_set != expected_value:
                errors.append(f"{property_name}: Expected {expected_value} but got {actual_value}")
        else:
            if actual_value != expected_value:
                errors.append(f"{property_name}: Expected {expected_value} but got {actual_value}")
    
    if errors:
        errors.append(len(errors))
        errors.append(len(expected_properties))
        return errors
    else:
        return "ok"