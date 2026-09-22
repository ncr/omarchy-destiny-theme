# Deterministic construction details

The original 14 Fable concepts, annotations, legends, service dates, palette
order, Nimbus Sans typography and Omarchy SVG remain the source of truth.
`fidelity.py` adds authored vector geometry, not generated raster imagery.

Render native, lossless masters without changing the installed wallpaper:

```sh
python3 tools/make_wallpapers.py --size 5120x2160 \
  --out concepts/starmap-collection/native --ext png
```

Coordinates remain in the original 1080-unit drawing space. Cairo rasterizes
the paths at the requested output size; there is no intermediate enlargement.
PNG and the default WebP export are lossless. JPEG remains available but is not
appropriate for the master artwork's fine coloured strokes.

The default device style is now `starmap`: the accepted Truth Lamp treatment
applied throughout the collection. `starmap.py` selects the focal component of
each device; `starmap_study.py` contains the shared line treatment. Primary
outlines stay bright, secondary construction is quieter, and auxiliary strokes
have smooth spatial ink-density variation. Decorative emblem rings are dimmer;
the Omarchy SVG and all typography retain their original settings. Existing
authored sections remain in place; the extra reflector and field sections are
specific to Truth Lamp. Use `--style original` to reproduce the clear-labels
masters. Neither render command installs a wallpaper or changes the desktop.

`tools/build_starmap_collection.py` renders the full native set, checks every
text call and its transform against the original style, verifies Truth Lamp
against the accepted study, and creates collection previews. Check label
clearance with `tools/verify_wallpaper_layout.py --out REPORT.json`; add
`--size 1920x1080` for the compact layout.

Each main view calls `enrich()` before its annotations, inside `begin_main()`.
Details belong to identifiable parts: bearings, threaded caps, panel fasteners,
heat-sink fins, fluid routes, circuit fan-out, joints and structural seams.
Avoid adding free-floating decorative machinery, invented labels or clutter
in the legend and secondary plots. Do not consume `s.rng` in an added detail
pass: that would change the original downstream simulation/plot samples.

The human figures follow the visual approach of NASA's human-factors drawings:
neutral lateral/frontal envelopes, anatomical proportions, supported posture,
subordinate segment axes and joint landmarks. The source reference is
[OCHMO-HB-004, figures on pages 47 and 77](https://www.nasa.gov/wp-content/uploads/2023/12/ochmo-hb-004-rev-a-dec2023.pdf).
The paths are original illustrative studies, not certified percentile models.
Hair, costume, expressive faces and decorative anatomy hatching are omitted.
The Truth Lamp table height and chair geometry follow the revised seated pose.

Opaque contours restore the aligned background underneath them. Objects retain
physical layering; table settings are drawn after the figures. Mechanical
shells (Proxy) and wearable reference bodies (Presence Rig) share the accepted
crash-dummy convention; Bounder retains its quiet anatomical leg envelope.
Shared view frames use quiet registration corners and datum axes. Magnified
views retain their boundaries but lose unrelated circular graduations. Do not
invent dimensions, degree values or NASA branding. Preserve the original
Omarchy mark, text content, palettes and the fictional devices' narrative.

The accepted crash-dummy refinement adds quartered amber/dark optical targets,
mould seams, segmented neck boots and joint caps. These accents belong on the
reference bodies and wearable/mechanical figures (Truth Lamp, Presence Rig,
Proxy, Bounder), not arbitrarily across every device. Preserve the accepted
anthropometric envelope. Heads use a smooth, featureless shell: omit ears,
facial lines and head fasteners, retaining one tracking target. The user's
crash-dummy photo references inform a separate rigid head shell, one subdued
rear access-cap seam in profile, and a recessed neck shaft with curved collars.
Keep the accepted blank frontal face, a minimal lateral nose cue and original narrative text; the
dummy treatment is a drawing convention, not a rewrite of the fictional story.

`human_figures.py` owns the articulated Proxy and Presence Rig reference bodies.
Paired components share dimensions and contours. Proxy's elbows and knees are
solved from fixed segment lengths; their bend direction must remain consistent
in the side elevation. Hands are compact moulded envelopes with an integral
thumb and a connected wrist spigot. Preserve the reviewed thumb orientation.
The rear hand follows its forearm axis. Presence Rig uses mirrored front-view
shoes, with soles on the roller crowns; Proxy uses rotated side-view shoes.
Keep Proxy's dashed, cancelled head symbol and the original NONE FITTED caption.
Truth Lamp's seated soles meet the floor. After figure changes, review the
whole silhouette as well as enlarged joints, and run the label audit at both
5120x2160 and 5120x2880.
Visual references: [NHTSA crash-test dummies](https://www.nhtsa.gov/nhtsas-crash-test-dummies)
and [Humanetics THOR-50M](https://www.humaneticsgroup.com/products/anthropomorphic-test-devices/frontal-impact/thor-50m/thor-50m).

Postprocessing combines restrained two-scale halation, seeded multiscale
monochrome grain and slight ink-density variation. It does not warp geometry
or fonts. The crisp raster stays underneath the halation. Grain does not
replace authored geometry. Matching source, size, seed and rendering environment
produce the same output; font/Cairo/Pillow changes may affect rasterization.

The review directory contains native masters, a contact sheet and a matched
Truth Lamp comparison. It is separate from `backgrounds/` and the live desktop.

Callout text must occupy clear space beside the artwork. Check both title and
the complete subtitle, as well as later-drawn geometry and other text. Keep
the attachment dot on its original part; move the elbow and text together.
`label_layout.py` records reviewed offsets, including compact-view clearance
from the emblem. Do not hide clashes with background rectangles. Dimension
labels can shift along their line to clear datum axes; detail scale captions
sit outside the detail circle. The audit under `concepts/clear-labels/` checks
actual glyph bounds on a render without text, plus text-to-text intersections,
at 5120x2160 and 1920x1080. Explicit exceptions cover identifiers inside their
own filled symbols; no callout or legend is exempt. Follow with visual review.
