from base import Path

def convertpaths(paths):
    convertedpaths = []
    for path in paths:
        boxes = path.getboxes()
        convertedpaths.append(Path(
            id=path.id,
            label=path.label,
            boxes=boxes
        ))

    return convertedpaths
