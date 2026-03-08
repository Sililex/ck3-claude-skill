# Environment Configuration

Colors can be defined in **rgb**, **hsv** or **hex** format.
```
color = { 1.0 1.0 1.0 }
color = hsv{ 1.0 1.0 1.0 }
color = hex{ ffff1a }
```

# Lighting

`cubemap_intensity = 2`

`cubemap = "gfx/map/environment/cubemap.dds"`        - Path to the environment cubemap DDS file

`sun_intensity = 25`

`sun_color = hsv{ 0.08 0.1 1 }`

### Directional settings

```
direction = { x y z }
    x    # Left- +Right
    y    # Down- +Up
    z    # Back- +Forward
```
```
sun_direction = { -7 8 7 }
```
```
water_sun_direction_offset = { 0 0 0 }
shadow_direction_offset = { 0 2 -3 }
```

### Shadow Settings

`shadowmap_depthbias = -0.002`      - Depth bias for shadow mapping

`shadowmap_kernelscale = 2`         - Scale factor for shadow kernel

`shadowmap_fadefactor = 5`          - Fade factor for shadow edges

### Map Object Lighting
```
map_objects_diffuse_light_scale = 1.0
map_objects_diffuse_ibl_scale = 8.0
map_objects_specular_light_scale = 1.0
map_objects_specular_ibl_scale = 1.0
```
Scales the sun and IBL light contribution on map objects separately from that of the sun.

# Fog

`fog_color = hex{ 50779b }`

`fog_begin = 20`                    - Distance where fog starts

`fog_end = 500`                     - Distance where fog reaches maximum density

`fog_max = 0.2`                     - Maximum fog density


### Volumetric Lighting Hack


`relative_fog_color = { 0.6 0.2 -0.2 }`     - Color adjustment for volumetric fog effect

`relative_fog_begin = 100.0`                - Start distance for relative fog

`relative_fog_end = 400.0`                  - End distance for relative fog

`relative_fog_height_begin = 10.0`          - Start height for relative fog

`relative_fog_height_end = 40.0`            - End height for relative fog


## Display Transform

`exposure = 2`                      - Exposure value for tone mapping

`contrast = 1.1`                    - Contrast adjustment (>1 → steeper mids)

`pivot = 0.12`                      - Pivot point for contrast (0.18 is middle-grey in linear HDR)


`tonemap_function = "TonyMcMapface"`        - Tone mapping function to use

Console command to visualize curve: `shader_debug PDX_DEBUG_TONEMAP_CURVE`
Leave empty for neutral gamma corrected output.
Implemented in restorescene.shader

#### Available display transforms
- `"TonyMcMapface"`
- `"AgX"`
- `"Uchimura"`
- `"ReinhardModified"`
- `"Reinhard"`
- `"FilmicACES_Narkowicz"`
- `"FilmicACES_Hill"`
- `"Filmic"`
- `"Uncharted"`

#### Settings that apply only to the "Uncharted" curve:
```
# Reasonable values
tonemap_curve = {
    shoulder_strength = 0.6
    linear_strength = 0.2
    linear_angle = 0.1
    toe_strength = 0.1
    toe_numerator = 0.01
    toe_denominator = 0.3
    linear_white = 11.2
}

 # U2 values // J. Hable
 tonemap_curve = {
 	shoulder_strength = 0.22
 	linear_strength = 0.3
 	linear_angle = 0.1
 	toe_strength = 0.2
 	toe_numerator = 0.01
 	toe_denominator = 0.3
 	linear_white = 11.2
 }
 ```

### Post-transform color grading

Leave these neutral, as such adjustments are best earlier in the pipeline,
if done globally, or in the posteffects volumes, if local.

`saturation_scale = 1`              - Saturation adjustment scale

`value_scale = 1`                   - Value/brightness adjustment scale

`hue_offset = 0`                    - Hue rotation offset

`colorbalance = { 1 1 1 }`          - RGB color balance adjustment

`levels_min = hsv{ 0 0 0 }`         - Minimum levels in HSV format

`levels_max = hsv{ 0 0 1 }`         - Maximum levels in HSV format


### Bloom

`bloom_width = 0.5`                 - Width of the bloom effect

`bloom_scale = 0.5`                 - Scale/intensity of the bloom effect

`bright_threshold = 0.5`            - Brightness threshold for bloom

### Depth of Field

```
depthoffield = {
    enabled = yes                   # Enable/disable depth of field
    dof_samplecount = 16            # WARNING - Performance impact
    dof_baseradius = 0.5            # Blur radius
    dof_blurblendmin = 0.1          # Min blur blend factor
    dof_blurblendmax = 2.0          # Max blur blend factor
    
    # Camera based settings - no performance impact
    dof_blurmin = 1.0
    dof_blurmax = 50.0
    dof_blurscale = 3.0
    dof_blurexponent = 1.3
    dof_heightmin = 0.0
    dof_heightmax = 1000.0
}
```

### Fog Blur

```
fogblur = {
    enabled = yes
}
```

Enables a blur effect in the approximate area where fog is visible.
Keep in mind that the location of the post_effect is manually approximated to
the fog area, but is set independently of the fog values in the blur shader.






