from paddleocr import PaddleOCR

class PaddleOcrApp:
    def __init__(self):
        # /home/unixusername/_repos/github-shs/lad_llm_llama_project/.paddlex
        pass

    def extract_text(self, image_path):
        # Initialize PaddleOCR instance
        
        ocr = PaddleOCR(
            use_doc_orientation_classify=False,
            use_doc_unwarping=False,
            # use_textline_orientation=False,
            use_angle_cls=True, 
            # use_gpu=False, 
            enable_mkldnn=False,

            )

        # Run OCR inference on a sample image 
        result = ocr.predict(
            input=image_path
            # input="https://paddle-model-ecology.bj.bcebos.com/paddlex/imgs/demo_image/general_ocr_002.png"

            )

        # Visualize the results and save the JSON results
        for res in result:
            # res.print()
            # res.save_to_img("output")
            res.save_to_json("data/ocr/paddleocr_output")
if __name__ == "__main__":
    app = PaddleOcrApp()
    import os
    root_dir = os.get("ROOT_DIR")
    app.extract_text(f"{root_dir}/espn_match.png")