from PIL import Image, ImageFilter
import imagehash

def phash_score(path):
    try:
        img = Image.open(path).convert("RGB")

        # Increase hash_size to 16 (256-bit hash) to make it highly sensitive to high-frequency structural changes.
        # Spliced/Tampered images contain unnatural sharp edges that get destroyed by blurring/resizing,
        # leading to a LARGER mathematical difference in high-res pHash.
        
        h1 = imagehash.phash(img, hash_size=16)
        h2 = imagehash.phash(img.resize((512, 512)), hash_size=16)
        h3 = imagehash.phash(img.filter(ImageFilter.GaussianBlur(2)), hash_size=16)

        diff = (h1 - h2) + (h1 - h3)
        
        # Scale the Hamming distance correctly so it outputs a valid non-zero score between 0.0 and 1.0
        score = diff / 128.0
        
        return min(max(score, 0.0), 1.0)

    except Exception as e:
        print("pHash Error:", e)
        return 0