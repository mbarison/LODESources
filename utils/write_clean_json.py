import json


def write_clean_json(df, output_file):
    """Write a dataframe to a json file with clean formatting"""

    # drop picket fence backslashes
    # ref: https://stackoverflow.com/a/64826042
    with open(output_file, "w", encoding="utf8") as o_f:
        json_str = df.to_json(orient="records")
        o_f.write(json.dumps(json.loads(json_str), ensure_ascii=False, indent=4))
