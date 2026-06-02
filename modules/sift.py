import cv2
import numpy as np

def sift_score(path):
    try:
        img = cv2.imread(path, 0)
        if img is None:
            return 0

        sift = cv2.SIFT_create()
        h, w = img.shape
        
        # Original heuristic: split image into 4 quadrants and measure mismatch variance
        # Splicing often completely wrecks the keypoint distribution variance
        patches = [
            img[0:h//2, 0:w//2],
            img[0:h//2, w//2:w],
            img[h//2:h, 0:w//2],
            img[h//2:h, w//2:w]
        ]

        descriptors = []
        for p in patches:
            kp, des = sift.detectAndCompute(p, None)
            if des is not None:
                descriptors.append(des)

        if len(descriptors) < 2:
            return 0

        bf = cv2.BFMatcher()
        match_scores = []
        for i in range(len(descriptors)):
            for j in range(i+1, len(descriptors)):
                matches = bf.knnMatch(descriptors[i], descriptors[j], k=2)
                good = []
                for m_tuple in matches:
                    if len(m_tuple) == 2:
                        m, n = m_tuple
                        if m.distance < 0.75 * n.distance:
                            good.append(m)
                match_scores.append(len(good))

        if not match_scores:
            return 0

        # Variance of matches between structural quadrants scaled properly
        score = np.std(match_scores) / 25.0
        return min(score, 1.0)

    except Exception as e:
        print("SIFT Error:", e)
        return 0