import yaml

### Simple yaml loader (broken: one in every two backslashes is dropped)
def load_utterance(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)
utterance = load_utterance('utterances.yaml')

# Fixing loading double backslashes
class CustomLoader(yaml.SafeLoader):
    def construct_scalar(self, node):
        # Retrieve the original scalar value
        value = super(CustomLoader, self).construct_scalar(node)
        # Replace single backslashes with double backslashes
        return value.replace('\\\\', '\\')

def load_yaml(file_path):
    with open(file_path, 'r') as file:
        # Load the file using the custom loader
        return yaml.load(file, Loader=CustomLoader)

# Load your YAML data
config = load_yaml('utterances.yaml')

# Access the 'spell' field
yaml_spell = config['spell']

# Define the Python string with proper escaping
python_spell = "\\tn=spell\\hello"

# Print both for comparison
# print("YAML Spell:", yaml_spell)
# print("Python Spell:", python_spell)

text = config['all_gestures']
items = []
for line in text.split('\n'):
    items.extend(line.split('; '))  # Split each line by semicolon and space

# Strip any leading/trailing whitespace and remove empty strings
items = [item.strip() for item in items if item.strip()]
items_set = set(items)

sorted_items = sorted(items_set)
print(sorted_items)