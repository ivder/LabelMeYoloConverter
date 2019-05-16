# LabelMeYoloConverter
Convert LabelMe Annotation Tool JSON format to YOLO text file format

Put your dataset (image and JSON format) in dataset/ 
Output will be saved in result/
JSON format will be moved to json_backup/

Finally, please manually copy text file together with image into 1 folder. (Intentionally separate the image and text output for maintainance purpose)

# Example
JSON file
```
{
  "version": "3.8.1",
  "flags": {},
  "shapes": [
    {
      "label": "1",
      "line_color": null,
      "fill_color": null,
      "points": [
        [
          447,
          287
        ],
        [
          381,
          267
        ]
      ],
      "shape_type": "rectangle"
    }
  ],
  "lineColor": [
    0,
    255,
    0,
    128
  ],
  "fillColor": [
    255,
    0,
    0,
    128
  ],
  "imagePath": "-1289025526.jpg",
  "imageData": "iVBORw0KGgoAAAANSUhEUgAAA8AAAAIcCAIAA
  ```
Convterted to YOLO format text file

```1 0.43125 0.512962962963 0.06875 0.037037037037```
