import argparse
import json
import inflection

def convert_case(text, case_type):
    if case_type == 'camelCase':
        return inflection.camelize(inflection.underscore(text), False)
    elif case_type == 'kebabCase':
        return inflection.dasherize(inflection.underscore(text))
    elif case_type == 'snakeCase':
        return inflection.underscore(text)
    else:
        raise ValueError(f"Unsupported case type: {case_type}")

def process_inputs(config):
    default_case_type = config.get('defaultCaseType')
    default_sensitive = config.get('defaultSensitive')

    if default_case_type == 'required' or default_sensitive == 'required':
        raise ValueError("Error: caseType sensitive")

    output = []
    for item in config['inputs']:
        text = item['text']
        case_type = item.get('caseType', default_case_type)
        sensitive = item.get('sensitive', default_sensitive)

        if sensitive == "true":
            result = {"text": "***", "caseType": case_type}
        else:
            converted_text = convert_case(text, case_type)
            result = {"text": converted_text, "caseType": case_type}

        output.append(result)

    return output
def main():
    parser = argparse.ArgumentParser(description="แปลงรูปแบบตัวอักษรจากข้อมูล JSON")
    parser.add_argument('-f', '--file', required=True, help="ConfigFile")
    parser.add_argument('-o', '--output', required=True, help="OutputFile")
    args = parser.parse_args()

    with open(args.file, 'r') as f:
        config = json.load(f)

    output_data = process_inputs(config)

    with open(args.output, 'w') as f:
        json.dump(output_data, f, indent=4)

    print(f"Success {args.output}")

if __name__ == '__main__':
    main()
