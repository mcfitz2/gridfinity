include <../gridfinity-rebuilt-openscad/src/core/standard.scad>
use <../gridfinity-rebuilt-openscad/src/core/gridfinity-rebuilt-utility.scad>
use <../gridfinity-rebuilt-openscad/src/core/gridfinity-rebuilt-holes.scad>
module custom_bin(gridx = 1, gridy = 2, gridz = 4, half_grid = false, divx = 0, divy = 0, cdivx = 0, cdivy = 0, c_orientation = 1, cd = 28, ch = 305, c_depth = 10, c_chamfer = 0.5, gridz_define = 0, height_internal = 25, enable_zsnap = false, style_tab = 5, place_tab = 0, style_lip = 2, scoop = 1, only_corners = false, refined_holes = false, magnet_holes = false, screw_holes = false, crush_ribs = true, chamfer_holes = true, printable_hole_top = true, enable_thumbscrew = false) {
    hole_options = bundle_hole_options(refined_holes, magnet_holes, screw_holes, crush_ribs, chamfer_holes, printable_hole_top);
    grid_dimensions = GRID_DIMENSIONS_MM / (half_grid ? 2 : 1);

    gridfinityInit(gridx, gridy, height(gridz, gridz_define, style_lip, enable_zsnap), height_internal, grid_dimensions=grid_dimensions, sl=style_lip) {

        if (divx > 0 && divy > 0) {

            cutEqual(n_divx = divx, n_divy = divy, style_tab = style_tab, scoop_weight = scoop, place_tab = place_tab);

        } else if (cdivx > 0 && cdivy > 0) {

            cutCylinders(n_divx=cdivx, n_divy=cdivy, cylinder_diameter=cd, cylinder_height=ch, coutout_depth=c_depth, orientation=c_orientation, chamfer=c_chamfer);
        }
    }
    gridfinityBase([gridx, gridy], grid_dimensions=grid_dimensions, hole_options=hole_options, only_corners=only_corners || half_grid, thumbscrew=enable_thumbscrew);
}
module triangular_prism(leg=34, width=25, leg2=34) {
    polyhedron(
        points=[
            [0, 0, 0],           // 0: right angle corner
            [leg2, 0, 0],       // 1: along X (leg)
            [0, leg, 0],         // 2: along Y (width)
            [0, 0, width],         // 3: right angle corner, top
            [leg2, 0, width],     // 4: along X, top
            [0, leg, width]        // 5: along Y, top
        ],
        faces=[
            [0, 1, 2],           // bottom triangle
            [3, 5, 4],           // top triangle
            [0, 3, 4, 1],        // side rectangle
            [0, 2, 5, 3],        // side rectangle
            [1, 4, 5, 2]         // hypotenuse rectangle
        ]
    );
}