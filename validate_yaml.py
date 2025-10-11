import yaml

class BlueprintLoader(yaml.SafeLoader):
    pass

# Add support for !input custom tag
BlueprintLoader.add_constructor('!input', lambda loader, node: loader.construct_scalar(node))

try:
    with open(r'c:\Users\cralh\Documents\GitHub\ha-blueprints\motion_lighting.yaml', 'r', encoding='utf-8') as f:
        data = yaml.load(f, Loader=BlueprintLoader)
    
    # Verify blueprint structure
    assert 'blueprint' in data, "Missing 'blueprint' key"
    assert 'name' in data['blueprint'], "Missing blueprint name"
    assert 'domain' in data['blueprint'], "Missing blueprint domain"
    assert data['blueprint']['domain'] == 'automation', "Domain must be 'automation'"
    assert 'variables' in data, "Missing 'variables' section"
    assert 'trigger' in data, "Missing 'trigger' section"
    assert 'action' in data, "Missing 'action' section"
    
    print("✓ YAML syntax is VALID!")
    print(f"✓ Blueprint name: {data['blueprint']['name']}")
    print(f"✓ Domain: {data['blueprint']['domain']}")
    print(f"✓ Variables defined: {len(data['variables'])}")
    print(f"✓ Triggers defined: {len(data['trigger'])}")
    print("✓ All required sections present!")
    
except yaml.YAMLError as e:
    print(f"✗ YAML Syntax Error: {e}")
    exit(1)
except AssertionError as e:
    print(f"✗ Blueprint Structure Error: {e}")
    exit(1)
except Exception as e:
    print(f"✗ Error: {e}")
    exit(1)
