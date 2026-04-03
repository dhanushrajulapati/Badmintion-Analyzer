import os
import argparse
import numpy as np
from tqdm import tqdm

import torch
from torch.utils.data import DataLoader

from TrackNetV3.test import predict_location, get_ensemble_weight, generate_inpaint_mask
from TrackNetV3.dataset import Shuttlecock_Trajectory_Dataset, Video_IterableDataset
from TrackNetV3.utils.general import *

def predict(indices, y_pred=None, c_pred=None, img_scaler=(1, 1)):

    pred_dict = {'Frame':[], 'X':[], 'Y':[], 'Visibility':[]}

    batch_size, seq_len = indices.shape[0], indices.shape[1]
    indices = indices.cpu().numpy()if torch.is_tensor(indices) else indices.numpy()
    
    # Transform input for heatmap prediction
    if y_pred is not None:
        y_pred = y_pred > 0.5
        y_pred = y_pred.cpu().numpy() if torch.is_tensor(y_pred) else y_pred
        y_pred = to_img_format(y_pred) # (N, L, H, W)
    
    # Transform input for coordinate prediction
    if c_pred is not None:
        c_pred = c_pred.cpu().numpy() if torch.is_tensor(c_pred) else c_pred

    prev_f_i = -1
    for n in range(batch_size):
        for f in range(seq_len):
            f_i = indices[n][f][1]
            if f_i != prev_f_i:
                if c_pred is not None:
                    # Predict from coordinate
                    c_p = c_pred[n][f]
                    cx_pred, cy_pred = int(c_p[0] * WIDTH * img_scaler[0]), int(c_p[1] * HEIGHT* img_scaler[1]) 
                elif y_pred is not None:
                    # Predict from heatmap
                    y_p = y_pred[n][f]
                    bbox_pred = predict_location(to_img(y_p))
                    cx_pred, cy_pred = int(bbox_pred[0]+bbox_pred[2]/2), int(bbox_pred[1]+bbox_pred[3]/2)
                    cx_pred, cy_pred = int(cx_pred*img_scaler[0]), int(cy_pred*img_scaler[1])
                else:
                    raise ValueError('Invalid input')
                vis_pred = 0 if cx_pred == 0 and cy_pred == 0 else 1
                pred_dict['Frame'].append(int(f_i))
                pred_dict['X'].append(cx_pred)
                pred_dict['Y'].append(cy_pred)
                pred_dict['Visibility'].append(vis_pred)
                prev_f_i = f_i
            else:
                break
    
    return pred_dict    

def prefetch_loader(loader):
    stream = torch.cuda.Stream()
    first = True
    for i,x in loader:
        with torch.cuda.stream(stream):
            x = x.float().cuda()
        if not first:
            yield prefetch_batch
        prefetch_batch = x
        first = False
    yield prefetch_batch

def get_shuttle_pos(frame_list,w,h):
    num_workers = 0
    tracknet_file = r'D:\projects\Adobe-GenSolve-Team-Neuron\Backend\TrackNetV3\ckpts\TrackNet_best.pt'
    eval_mode = 'nonoverlap'
    batch_size = 128
    max_sample_num = 8
    
    # Load model
    tracknet_ckpt = torch.load(tracknet_file)
    tracknet_seq_len = tracknet_ckpt['param_dict']['seq_len']
    bg_mode = tracknet_ckpt['param_dict']['bg_mode']
    tracknet = get_model('TrackNet', tracknet_seq_len, bg_mode).cuda()
    tracknet.load_state_dict(tracknet_ckpt['model'])

    inpaintnet = None

    w_scaler, h_scaler = w / WIDTH, h / HEIGHT
    img_scaler = (w_scaler, h_scaler)

    tracknet_pred_dict = {'Frame':[], 'X':[], 'Y':[], 'Visibility':[], 'Inpaint_Mask':[],
                        'Img_scaler': (w_scaler, h_scaler), 'Img_shape': (w, h)}

    # Test on TrackNet
    tracknet.eval()
    seq_len = tracknet_seq_len
    if eval_mode == 'nonoverlap':

        indices = torch.tensor(
            [[[0, 0],
            [0, 1],
            [0, 2],
            [0, 3],
            [0, 4],
            [0, 5],
            [0, 6],
            [0, 7]]], dtype=torch.int32
        )

        if True:
            print(frame_list.currlength())
            # print("Check1")
            dataset = Shuttlecock_Trajectory_Dataset(seq_len=seq_len, sliding_step=seq_len, data_mode='heatmap', bg_mode=bg_mode,
                                                    frame_arr=np.array(frame_list.lst)[:, :, :, ::-1], padding=True)
            # print("Check2")
            data_loader = DataLoader(dataset, batch_size=batch_size, shuffle=False, num_workers=num_workers, drop_last=False, pin_memory=True)
            # print("Check3")
            # print(data_loader.data)
            # print(data_loader.dataset.__dict__)
            for x in prefetch_loader(data_loader):
                # print(i)
                # print(x.shape)
                # print(len(myx))
                # print("Check4")
                # x = torch.tensor(x.copy())
                # x = x/255
                x = x.float().cuda()
                # print("Check5")
                with torch.no_grad():
                    y_pred = tracknet(x).cpu()
                print("CHeck6")
                
                # Predict
                tmp_pred = predict(indices, y_pred=y_pred, img_scaler=img_scaler)
                print("Check7")
                for key in tmp_pred.keys():
                    tracknet_pred_dict[key] = tmp_pred[key]
            return tracknet_pred_dict
