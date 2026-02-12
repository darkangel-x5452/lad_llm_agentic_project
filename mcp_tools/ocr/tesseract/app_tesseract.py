import pytesseract
from pytesseract import Output
from PIL import Image
import json
def group_by_lines(items, y_threshold=10):
    lines = []

    for item in sorted(items, key=lambda x: x["bbox"]["y_min"]):
        placed = False
        for line in lines:
            if abs(line["y"] - item["bbox"]["y_min"]) < y_threshold:
                line["items"].append(item)
                placed = True
                break

        if not placed:
            lines.append({
                "y": item["bbox"]["y_min"],
                "items": [item]
            })

    for line in lines:
        line["items"].sort(key=lambda x: x["bbox"]["x_min"])

    return lines

class TesseractApp:
    def __init__(self):
        pass

    def extract_text(self, image_path):
        # Placeholder for Tesseract OCR text extraction logic

        # If tesseract is not in PATH, uncomment and set this
        # pytesseract.pytesseract.tesseract_cmd = r"/usr/bin/tesseract"

        # Load image
        image = Image.open(image_path)

        # Run OCR with detailed output
        data = pytesseract.image_to_data(
            image,
            output_type=Output.DICT
        )

        results = []

        n_boxes = len(data["text"])

        print(f"Found {n_boxes} text boxes.")
        for i in range(n_boxes):
            text = data["text"][i].strip()
            conf = float(data["conf"][i])

            # Ignore empty text and low confidence noise
            if text and conf > 0:
                x = data["left"][i]
                y = data["top"][i]
                w = data["width"][i]
                h = data["height"][i]

                results.append({
                    "text": text,
                    "confidence": conf,
                    "bbox": {
                        "x_min": x,
                        "y_min": y,
                        "x_max": x + w,
                        "y_max": y + h
                    }
                })
        with open("./data/ocr/tesseract_output.json", "w") as f:
            json.dump(results, f, indent=2)
        lines = group_by_lines(results)

        for line in lines:
            print(" ".join(word["text"] for word in line["items"]))
        with open("./data/ocr/tesseract_lines.txt", "w") as f:
            for line in lines:
                f.write(" ".join(word["text"] for word in line["items"]) + "\n")
        return "Extracted text from image"
    
if __name__ == "__main__":
    app = TesseractApp()
    import os
    root_dir = os.getenv("ROOT_DIR")
    text = app.extract_text(image_path=f"{root_dir}/espn_match.png")
    