# utils/validation.py
def validate_module_type(module_type: str) -> str:
    valid_types = ["exploit", "payload", "auxiliary", "post", "encoder", "nop"]
    if module_type.lower() not in valid_types:
        raise ValueError(f"Invalid module type: {module_type}. Must be one of: {', '.join(valid_types)}")
    return module_type.lower()

def validate_module_name(module_name: str) -> str:
    # Implement basic sanitization (e.g., prevent path traversal, injection)
    if not module_name.replace("/", "").replace("_", "").replace("-", "").isalnum():
        raise ValueError(f"Invalid module name: {module_name}")
    return module_name

def validate_option_name(option_name: str) -> str:
    if not option_name.isalnum():
      raise ValueError(f"Invalid option name {option_name}")
    return option_name

# Add more validation functions as needed (e.g., for IP addresses, ports, etc.)