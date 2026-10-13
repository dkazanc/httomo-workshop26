# 360° to 180° tomography

A 60-second silent, captioned animation for a dark Reveal.js presentation.
1280 × 720, 24 fps, H.264 MP4. The images are synthetic line-integral
sinograms, not experimental data from the paper.

## Quarto embedding

```markdown
## Converting a 360° scan to 180°

<video controls preload="metadata" width="100%" poster="videos/360-to-180-poster.png">
  <source src="videos/360-to-180-tomography.mp4" type="video/mp4">
</video>
```

## Presenter notes

- 0–12 s: For parallel-beam half-acquisition, offset the rotation axis so
  complementary regions of a large sample enter the detector over 360°.
- 12–24 s: A sinogram stacks one detector row over angle. Split into the
  first and second 180° intervals.
- 24–36 s: Match angles separated by 180°. Reverse detector columns in the
  second half; do not reverse its angular row order.
- 36–48 s: Determine which sides overlap and the overlap width. Align the
  shared features and blend with complementary linear ramps. The paper
  compares correlation-metric minima on both sides to avoid matching empty
  background incorrectly. This example places the flipped second half left.
- 48–60 s: The joined data have N angular rows and width 2W−O, where the
  input has 2N rows of width W and O is the overlap width. Repeat over
  detector rows and use conventional 180° reconstruction.

The animation uses evenly sampled half-open angular intervals [0°,180°)
and [180°,360°). Real acquisition may contain a repeated endpoint: use the
angle metadata to pair views and handle duplicates rather than blindly
halving the frame count. The geometry assumes a stationary sample and
aligned parallel-beam views; calibration and intensity consistency matter.
A centred 360° scan of a fully covered object provides redundant opposite
views, not the field-of-view extension demonstrated here.

Source: N. T. Vo, R. C. Atwood, M. Drakopoulos and T. Connolley,
“Data processing methods and data acquisition for samples larger than the
field of view in parallel-beam tomography,” Optics Express 29, 17849–17874
(2021), §2.1.1.1 and Fig. 1. https://doi.org/10.1364/OE.418448
The paper also describes direct 360° reconstruction; this animation covers
its conversion-and-stitching route only.
