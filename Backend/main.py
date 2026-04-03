import cv2
from ultralytics import YOLO
from utils.video_processing import load_video, detect_court, get_court_boundaries
from utils.transformation import get_perspective_transform
from utils.tracking import (
    initialize_tracker,
    detect_and_track_players,
    update_play_area_with_players,
    detect_and_track_shuttle
)

# ---------------- FRAME BUFFER ----------------
class FrameList:
    def __init__(self, length):
        self.length = length
        self.lst = []

    def currlength(self):
        return len(self.lst)

    def insert(self, item):
        if len(self.lst) >= self.length:
            self.lst.pop(0)
        self.lst.append(item)


frame_list = FrameList(8)


# ---------------- MAIN PIPELINE ----------------
def main():
    global warped_court

    # ✅ Load models ONCE
    player_model = YOLO("Models/yolov8n.pt")
    court_model = YOLO("Models/PlayAreaDetect.pt")

    video_path = "TestVideos/Badminton.mp4"
    cap = load_video(video_path)

    # -------- COURT DETECTION (RUN ONCE) --------
    ret, frame = cap.read()
    if not ret:
        return

    frame_list.insert(frame)

    points = detect_court(court_model, frame)
    if points is None:
        print("Court not detected")
        return

    court_points = get_court_boundaries(points)
    warped_court, M = get_perspective_transform(court_points, frame)

    court = cv2.imread("TestVideos/Screenshot_20240901_031623.png")
    warped_court = cv2.resize(
        court, (warped_court.shape[1], warped_court.shape[0])
    )

    cap.release()

    # -------- REOPEN VIDEO --------
    cap = load_video(video_path)
    tracker = initialize_tracker("deep_sort/deep/checkpoint/ckpt.t7")

    frame_no = 0
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    prev_output = None  # ✅ prevents repeated output

    # -------- MAIN LOOP --------
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame_no += 1

        # ✅ Maintain buffer (max 8 frames)
        frame_list.insert(frame)

        # ✅ Skip alternate frames → improves speed
        if frame_no % 2 != 0:
            continue

        actual_frame = frame.copy()

        # -------- PLAYER TRACKING --------
        tracks, bboxes_xyxy, class_ids = detect_and_track_players(
            player_model,
            tracker,
            frame,
            court_points,
            M,
            warped_court,
            frame_no
        )

        if tracks is None:
            continue

        # -------- SHUTTLE TRACKING --------
        if frame_list.currlength() < 2:
            continue

        shuttle_pred_dict = detect_and_track_shuttle(frame_list, w, h)

        # -------- GAME LOGIC --------
        (
            play_area_with_players,
            player_coords,
            status,
            hitplayer,
            hit_shuttle_coords,
            hit_coords,
            prev_hit_frame,
            frame_no,
            shuttle_curr_coords,
            hit_count,
            prev_hit_coords
        ) = update_play_area_with_players(
            bboxes_xyxy,
            shuttle_pred_dict,
            court_points,
            warped_court,
            M,
            frame,
            frame_no
        )

        # -------- ENCODE FRAMES --------
        _, buffer0 = cv2.imencode(".jpg", actual_frame)
        actual_frame_bytes = buffer0.tobytes()

        _, buffer1 = cv2.imencode(".jpg", frame)
        frame_bytes = buffer1.tobytes()

        _, buffer2 = cv2.imencode(".jpg", play_area_with_players)
        play_area_bytes = buffer2.tobytes()

        # -------- FINAL OUTPUT --------
        output = [
            actual_frame_bytes,
            frame_bytes,
            play_area_bytes,
            player_coords,
            status,
            hitplayer,
            hit_shuttle_coords,
            hit_coords,
            prev_hit_frame,
            frame_no,
            shuttle_curr_coords,
            hit_count,
            prev_hit_coords
        ]

        # ✅ Avoid duplicate outputs (fix spam)
        if output != prev_output:
            prev_output = output
            yield output

    cap.release()


# ---------------- RUN ----------------
if __name__ == "__main__":
    for _ in main():
        pass