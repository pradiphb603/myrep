import klayout.db as pya
import subprocess, os, signal

def open_klayout():
    # Open KLayout application
    subprocess.Popen(["klayout", "-e", "output.gds"])

def close_klayout():
    # Close KLayout application
    result = subprocess.run(
              ["pgrep", "-x", "klayout"],
                    capture_output=True,
                    text=True
              )
    #print(result.stdout.split())
    for pid in result.stdout.split():
        os.kill(int(pid), signal.SIGKILL)

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