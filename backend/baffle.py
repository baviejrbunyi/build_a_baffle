import re
import backend.AI as AI

class Baffle:
    def __init__(self, title, field, gaps, recommendations):
        self.title = title
        self.field = field
        self.gaps = gaps
        self.recommendations = recommendations

    def __repr__(self):
        return f"Baffle(title={self.title}, field={self.field}, gaps={self.gaps}, recommendations={self.recommendations})"

def store_baffle(response):
    # Initialize result with empty values\

    print(response)
    result = {
        "title": "",
        "field": [],
        "gaps": "",
        "recommendations": ""
    }

    # Use regular expressions to parse the different sections from the response
    title_match = re.search(r"title:\s*(.+)", response)
    field_match = re.findall(r"- ([\w\s]+)", response)
    gaps_match = re.search(r"gaps:\s*(.+)", response)
    recommendations_match = re.search(r"recommendations:\s*(.+)", response)

    # Extract and clean up the matched values
    if title_match:
        result["title"] = title_match.group(1).strip()

    if field_match:
        result["field"] = [field.strip() for field in field_match]

    if gaps_match:
        result["gaps"] = gaps_match.group(1).strip()

    if recommendations_match:
        result["recommendations"] = recommendations_match.group(1).strip()

    # Create and return the Baffle object
    return Baffle(
        title=result["title"],
        field=result["field"],
        gaps=result["gaps"],
        recommendations=result["recommendations"]
    )


def create_baffles(topic, loop):
    baffles = []
    loop = int(loop)

    for i in range(loop):
        baffle = store_baffle(AI.groq_request(AI.create_prompt(topic)))
        baffles.append(baffle)
        

    return baffles
