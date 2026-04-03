import os
import numpy as np
import torch
from torch.utils.data import DataLoader

from TrackNetV3.test import predict_location
from TrackNetV3.dataset import Shuttlecock_Trajectory_Dataset
from TrackNetV3.utils.general import *

# ---------------- PREDICT FUNCTION ----------------
def predict(indices, y_pred=None, c_pred=None, img_scaler=(1, 1)):

    pred_dict = {'Frame': [], 'X': [], 'Y': [], 'Visibility': []}

    batch_size, seq_len = indices.shape[0], indices.shape[1]
    indices = indices.cpu().numpy() if torch.is_tensor(indices) else indices.numpy()

    if y_pred is not None:
        y_pred = y_pred > 0.5
        y_pred = y_pred.cpu().numpy() if torch.is_tensor(y_pred) else y_pred
        y_pred = to_img_format(y_pred)

    if c_pred is not None:
        c_pred = c_pred.cpu().numpy() if torch.is_tensor(c_pred) else c_pred

    prev_f_i = -1
    for n in range(batch_size):
        for f in range(seq_len):
            f_i = indices[n][f][1]

            if f_i != prev_f_i:
                if c_pred is not None:
                    c_p = c_pred[n][f]
                    cx_pred = int(c_p[0] * WIDTH * img_scaler[0])
                    cy_pred = int(c_p[1] * HEIGHT * img_scaler[1])

                elif y_pred is not None:
                    y_p = y_pred[n][f]
                    bbox_pred = predict_location(to_img(y_p))

                    cx_pred = int(bbox_pred[0] + bbox_pred[2] / 2)
                    cy_pred = int(bbox_pred[1] + bbox_pred[3] / 2)

                    cx_pred = int(cx_pred * img_scaler[0])
                    cy_pred = int(cy_pred * img_scaler[1])

                else:
                    raise ValueError("Invalid input")

                vis_pred = 0 if cx_pred == 0 and cy_pred == 0 else 1

                pred_dict['Frame'].append(int(f_i))
                pred_dict['X'].append(cx_pred)
                pred_dict['Y'].append(cy_pred)
                pred_dict['Visibility'].append(vis_pred)

                prev_f_i = f_i
            else:
                break

    return pred_dict


# ---------------- PREFETCH LOADER ----------------
def prefetch_loader(loader):

    # ✅ CPU fallback
    if not torch.cuda.is_available():
        for _, x in loader:
            yield x
        return

    # ✅ GPU path
    stream = torch.cuda.Stream()
    first = True

    for i, x in loader:
        with torch.cuda.stream(stream):
            x = x.float().cuda()

        if not first:
            yield prefetch_batch

        prefetch_batch = x
        first = False

    yield prefetch_batch


# ---------------- MAIN TRACKNET FUNCTION ----------------
def get_shuttle_pos(frame_list, w, h):

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # ---------------- LOAD MODEL ONLY ONCE ----------------
    if not hasattr(get_shuttle_pos, "model"):

        base_dir = os.path.dirname(os.path.abspath(__file__))
        tracknet_file = os.path.join(base_dir, "ckpts", "TrackNet_best.pt")

        if not os.path.exists(tracknet_file):
            raise FileNotFoundError(f"Model not found at: {tracknet_file}")

        tracknet_ckpt = torch.load(tracknet_file, map_location=device)

        seq_len = tracknet_ckpt['param_dict']['seq_len']
        bg_mode = tracknet_ckpt['param_dict']['bg_mode']

        model = get_model('TrackNet', seq_len, bg_mode).to(device)
        model.load_state_dict(tracknet_ckpt['model'])
        model.eval()

        # ✅ store globally
        get_shuttle_pos.model = model
        get_shuttle_pos.seq_len = seq_len
        get_shuttle_pos.bg_mode = bg_mode

    tracknet = get_shuttle_pos.model
    seq_len = get_shuttle_pos.seq_len
    bg_mode = get_shuttle_pos.bg_mode

    # ---------------- SCALING ----------------
    w_scaler, h_scaler = w / WIDTH, h / HEIGHT
    img_scaler = (w_scaler, h_scaler)

    tracknet_pred_dict = {
        'Frame': [],
        'X': [],
        'Y': [],
        'Visibility': [],
        'Inpaint_Mask': [],
        'Img_scaler': img_scaler,
        'Img_shape': (w, h)
    }

    # ✅ Skip if insufficient frames
    if frame_list.currlength() < 2:
        return tracknet_pred_dict

    # ---------------- DATASET ----------------
    dataset = Shuttlecock_Trajectory_Dataset(
        seq_len=seq_len,
        sliding_step=seq_len,
        data_mode='heatmap',
        bg_mode=bg_mode,
        frame_arr=np.array(frame_list.lst)[:, :, :, ::-1],
        padding=True
    )

    data_loader = DataLoader(
        dataset,
        batch_size=4,              # ✅ optimized
        shuffle=False,
        num_workers=0,
        drop_last=False,
        pin_memory=False           # ✅ CPU optimized
    )

    indices = torch.tensor(
        [[[0,0],[0,1],[0,2],[0,3],[0,4],[0,5],[0,6],[0,7]]],
        dtype=torch.int32
    )

    # ---------------- INFERENCE ----------------
    for x in prefetch_loader(data_loader):
        x = x.float().to(device)

        with torch.no_grad():
            y_pred = tracknet(x).cpu()

        tmp_pred = predict(indices, y_pred=y_pred, img_scaler=img_scaler)

        for key in tmp_pred.keys():
            tracknet_pred_dict[key] = tmp_pred[key]

    return tracknet_pred_dict