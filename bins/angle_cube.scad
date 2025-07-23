use <entrypoint.scad>

difference() {
    custom_bin(gridx = 1, gridy = 2, height_internal = 25); 
    translate([-17, -30, 6]) cube([34, 60, 100]);
}
