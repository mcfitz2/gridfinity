import subprocess
import yaml
import os
openscad_variable_map = {
    "gridx": {
        "friendly_name": "num_bases_x",
        "description": "Number of bases along x-axis",
        "default": 3
    },
    "gridy": {
        "friendly_name": "num_bases_y",
        "description": "Number of bases along y-axis",
        "default": 2
    },
    "gridz": {
        "friendly_name": "bin_height",
        "description": "Bin height (see bin height information and 'gridz_define')",
        "default": 6
    },
    "half_grid": {
        "friendly_name": "half_grid_mode",
        "description": "Half grid sized bins; implies only corners",
        "default": False
    },
    "divx": {
        "friendly_name": "linear_divisions_x",
        "description": "Number of X linear divisions (0 for solid bin)",
        "default": 1
    },
    "divy": {
        "friendly_name": "linear_divisions_y",
        "description": "Number of Y linear divisions (0 for solid bin)",
        "default": 1
    },
    "cdivx": {
        "friendly_name": "cylindrical_divisions_x",
        "description": "Number of cylindrical X divisions (mutually exclusive to linear compartments)",
        "default": 0
    },
    "cdivy": {
        "friendly_name": "cylindrical_divisions_y",
        "description": "Number of cylindrical Y divisions (mutually exclusive to linear compartments)",
        "default": 0
    },
    "c_orientation": {
        "friendly_name": "cylinder_orientation",
        "description": "Orientation of cylindrical compartments (0: x, 1: y, 2: z)",
        "default": 2
    },
    "cd": {
        "friendly_name": "cylinder_diameter",
        "description": "Diameter of cylindrical cut outs",
        "default": 10
    },
    "ch": {
        "friendly_name": "cylinder_height",
        "description": "Height of cylindrical cut outs",
        "default": 1
    },
    "c_depth": {
        "friendly_name": "cylinder_spacing_to_lid",
        "description": "Spacing from cylinder to lid",
        "default": 1
    },
    "c_chamfer": {
        "friendly_name": "cylinder_top_chamfer",
        "description": "Chamfer around the top rim of the holes",
        "default": 0.5
    },
    "gridz_define": {
        "friendly_name": "bin_height_mode",
        "description": "Defines what 'gridz' applies to (0: 7mm increments, 1: internal mm, 2: external mm)",
        "default": 0
    },
    "height_internal": {
        "friendly_name": "internal_height_override",
        "description": "Overrides internal block height of bin (mm, 0 for default)",
        "default": 0
    },
    "enable_zsnap": {
        "friendly_name": "snap_height_to_increment",
        "description": "Snap gridz height to nearest 7mm increment",
        "default": False
    },
    "style_tab": {
        "friendly_name": "tab_type",
        "description": "Type of tabs (0: Full, 1: Auto, 2: Left, 3: Center, 4: Right, 5: None)",
        "default": 1
    },
    "place_tab": {
        "friendly_name": "tab_placement",
        "description": "Which divisions have tabs (0: Everywhere, 1: Top-Left Division)",
        "default": 0
    },
    "style_lip": {
        "friendly_name": "lip_style",
        "description": "How the top lip acts (0: Regular, 1: Remove subtractively, 2: Remove and retain height)",
        "default": 0
    },
    "scoop": {
        "friendly_name": "scoop_weight",
        "description": "Scoop weight percentage (0 disables, 1 is regular, real number scales)",
        "default": 1
    },
    "only_corners": {
        "friendly_name": "corner_holes_only",
        "description": "Only cut magnet/screw holes at corners",
        "default": False
    },
    "refined_holes": {
        "friendly_name": "use_refined_hole_style",
        "description": "Use gridfinity refined hole style (not compatible with magnet_holes)",
        "default": True
    },
    "magnet_holes": {
        "friendly_name": "enable_magnet_holes",
        "description": "Base will have holes for 6mm diameter x 2mm high magnets",
        "default": False
    },
    "screw_holes": {
        "friendly_name": "enable_screw_holes",
        "description": "Base will have holes for M3 screws",
        "default": False
    },
    "crush_ribs": {
        "friendly_name": "magnet_crush_ribs",
        "description": "Magnet holes will have crush ribs to hold the magnet",
        "default": True
    },
    "chamfer_holes": {
        "friendly_name": "hole_chamfer",
        "description": "Magnet/Screw holes will have a chamfer to ease insertion",
        "default": True
    },
    "printable_hole_top": {
        "friendly_name": "printable_hole_top",
        "description": "Magnet/Screw holes will be printed so supports are not needed",
        "default": True
    },
    "enable_thumbscrew": {
        "friendly_name": "enable_thumbscrew_hole",
        "description": "Enable gridfinity-refined thumbscrew hole in the center of each base",
        "default": False
    }
}

def get_script_directory():
    script_path = os.path.abspath(__file__)
    return os.path.dirname(script_path)

def get_scad_directory():
    script_dir = get_script_directory()
    return os.path.join(os.path.dirname(script_dir), 'gridfinity-rebuilt-openscad')
def yaml_to_openscad_cmd(yaml_path, bin_key):
    with open(yaml_path, 'r') as f:
        data = yaml.safe_load(f)

    # Merge defaults and bin-specific values
    values = dict(data.get('defaults', {}))
    values.update(data.get(bin_key, {}))

    # Map friendly names back to OpenSCAD variable names
    friendly_to_openscad = {
        v['friendly_name']: k for k, v in openscad_variable_map.items()
    }

    # Build -D assignments for OpenSCAD
    assignments = []
    for friendly_name, value in values.items():
        openscad_var = friendly_to_openscad.get(friendly_name)
        if openscad_var is not None:
            # OpenSCAD expects 'true'/'false' lowercase for booleans
            if isinstance(value, bool):
                value = str(value).lower()
            assignments.append(f'-D{openscad_var}={value}')

    return f"openscad {' '.join(assignments)} -o {bin_key}.stl {get_scad_directory()}/gridfinity-rebuilt-bins.scad"



def all_bins_to_openscad_cmds(yaml_path):
    with open(yaml_path, 'r') as f:
        data = yaml.safe_load(f)

    bin_keys = [k for k in data.keys() if k != 'defaults']
    cmds = {}
    for bin_key in bin_keys:
        cmds[bin_key] = yaml_to_openscad_cmd(yaml_path, bin_key)
    return cmds

def run_all_bins(yaml_path):
    cmds = all_bins_to_openscad_cmds(yaml_path)
    for bin_key, cmd in cmds.items():
        print(f"Running: {cmd}")
        result = subprocess.run(cmd, shell=True)
        if result.returncode != 0:
            print(f"Error running command for {bin_key}: {cmd}")

if __name__ == "__main__":
    import yaml
    import sys

    yaml_path = sys.argv[1]
    run_all_bins(yaml_path)