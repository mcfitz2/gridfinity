use <entrypoint.scad>
difference() {
  union() {
    difference() {
      custom_bin(gridx=1, gridy=3, height_internal=25);
      translate([-14.5, -55, 6]) cube([34, 110, 100]);
    }
    translate([-15, -55, 6])
        rotate([90, 0, 90])
            triangular_prism(leg=24, width=35, leg2=33);
  }
  translate([-19.5, -55, 6]) cube([3, 110, 100]);
}



