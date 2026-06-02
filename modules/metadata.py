from PIL import Image

def metadata_score(path):
    try:
        img = Image.open(path)
        exif = img.getexif()

        if not exif:
            return 0.2

        software = str(exif.get(305, "")).lower()
        make = str(exif.get(271, "")).lower()
        model = str(exif.get(272, "")).lower()

        score = 0

        if "photoshop" in software or "gimp" in software:
            score += 0.6

        if not make and not model:
            score += 0.2

        if make or model:
            score -= 0.2

        return max(0, min(score, 1))

    except:
        return 0.2