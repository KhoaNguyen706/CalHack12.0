import argparse
import sys
from pathlib import Path
from ultralytics import YOLO


def main():
    parser = argparse.ArgumentParser(description="Run YOLO detection using Ultralytics YOLOv8")
    parser.add_argument("--model", "-m", help="model filename or model spec (e.g. yolov8n.pt)", default="yolov8n.pt")
    parser.add_argument("--source", "-s", help="image/video/file/folder/URL to run detection on", default="images/bus.jpg")
    parser.add_argument("--save", action="store_true", help="save annotated results to disk")
    parser.add_argument("--device", "-d", help="device to run on (cpu or cuda:0)", default="cpu")
    parser.add_argument("--save-dir", help="directory to save results (overrides default runs/)")
    parser.add_argument("--conf", type=float, default=0.25, help="confidence threshold")
    args = parser.parse_args()

    model_path = args.model
    source = args.source

    # basic checks
    if not (source.startswith("http://") or source.startswith("https://")):
        src_path = Path(source)
        if not src_path.exists():
            print(f"Source not found: {source}\nPlease provide a valid file path or a URL.")
            sys.exit(2)

    try:
        print(f"Loading model '{model_path}' (this may download weights if missing)...")
        model = YOLO(model_path)
        # set device if supported by ultralytics API (model.to/device may vary by version)
        try:
            model.to(args.device)
        except Exception:
            # some versions accept device via predict or constructor; ignore if not supported
            pass
    except Exception as e:
        print("Failed to load model:", e)
        sys.exit(3)

    try:
        print(f"Running prediction on: {source} (device={args.device}, conf={args.conf})")
        predict_kwargs = {"source": source, "save": args.save, "conf": args.conf}
        if args.save_dir:
            predict_kwargs["save_dir"] = args.save_dir
        results = model.predict(**predict_kwargs)
        print("Prediction finished.")
        print(results)
    except Exception as e:
        print("Prediction failed:", e)
        sys.exit(4)


if __name__ == "__main__":
    main()
