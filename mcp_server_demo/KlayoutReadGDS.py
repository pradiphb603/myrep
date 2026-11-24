import klayout.db as pya


def read_gds_file(
    file_path: str = "/home/pradip-banerjee/MCPServerTutorial/mcp_server_demo/output.gds",
):
    layout = pya.Layout()
    layout.read(file_path)
    layer_info = []
    for layer_index in layout.layer_indexes():
        info = layout.get_info(layer_index)
        layer_info.append(
            {
                "index": layer_index,
                "layer": info.layer,
                "datatype": info.datatype,
                "name": info.name,
            }
        )
    return layer_info