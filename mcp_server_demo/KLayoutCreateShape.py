import klayout.db as db
def create_rectangles(outFile= str ):
    # Create a new layout object
    ly = db.Layout()

    # Set the database unit (e.g., 1 nm = 0.001 µm)
    ly.dbu = 0.001

    # Add a top cell
    top_cell = ly.create_cell("TOP")

    # Create a new layer (layer number 1, datatype 0)
    layer1 = ly.layer(1, 0)
    layer2 = ly.layer(3, 0)
    layer3 = ly.layer(5, 0)

    # Add a shape (a rectangle/Box from x1, y1 to x2, y2 in dbu)
    top_cell.shapes(layer1).insert(db.Box(0, 0, 1000, 2000))
    top_cell.shapes(layer2).insert(db.Box(200, 200, 1200, 2200))
    top_cell.shapes(layer3).insert(db.Box(400, 400, 1400, 2400))

    # OASIS preserves string property keys such as "Prop"
    #ly.write("/home/pradip-banerjee/MCPServerTutorial/mcp_server_demo/output.gds")
    ly.write(outFile)

def create_route(outFile= str, start_point=(0, 0), end_point=(10000, 0), width=250):
    # Create a new layout object
    ly = db.Layout()

    # Set the database unit (e.g., 1 nm = 0.001 µm)
    ly.dbu = 0.001
    top_cell = ly.create_cell("TOP")
    # Add a route from (0,0) to (10,0)
    layer1 = ly.layer(1, 0)
    layer_info = ly.get_info(layer1)
    layer_info.name = "Metal1"
    print(f"Value of width is {width}")
    width = int(width)
    route = db.Path([db.Point(start_point[0], start_point[1]), db.Point(end_point[0], end_point[1])], width)
    top_cell.shapes(layer1).insert(route)

    # OASIS preserves string property keys such as "Prop"
    #ly.write("/home/pradip-banerjee/MCPServerTutorial/mcp_server_demo/output.gds")
    ly.write(outFile)


