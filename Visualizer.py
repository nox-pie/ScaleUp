import graphviz
import tempfile

def create_roadmap_image(text):
    # Create a new directed graph
    dot = graphviz.Digraph(format='png')

    # Split the AI text into lines and clean them
    lines = [line.strip() for line in text.split('\n') if line.strip() and not line.lower().startswith("would you like")]

    # Create graph nodes and connect them in order
    for i, line in enumerate(lines[:10]):  # Limit to 10 nodes max
        dot.node(str(i), line)
        if i > 0:
            dot.edge(str(i - 1), str(i))  # Connect previous to current

    # Save image to temporary file
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
        dot.render(f.name, format="png")
        return f.name + ".png"
