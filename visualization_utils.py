import numpy as np
from PIL import Image, ImageDraw


def visualize_scenes(frames: np.ndarray, scenes: np.ndarray):
    nf, ih, iw, ic = frames.shape
    width = 25
    if len(frames) % width != 0:
        pad_with = width - len(frames) % width
        frames = np.concatenate([frames, np.zeros([pad_with, ih, iw, ic], np.uint8)])
    height = len(frames) // width

    scene = frames.reshape([height, width, ih, iw, ic])
    scene = np.concatenate(np.split(
        np.concatenate(np.split(scene, height), axis=2)[0], width
    ), axis=2)[0]

    img = Image.fromarray(scene)
    draw = ImageDraw.Draw(img, "RGBA")

    def draw_start_frame(frame_no):
        w = frame_no % width
        h = frame_no // width
        draw.rectangle([(w * iw, h * ih), (w * iw + 2, h * ih + ih - 1)], fill=(255, 0, 0))
        draw.polygon(
            [(w * iw + 7, h * ih + ih // 2 - 4), (w * iw + 12, h * ih + ih // 2), (w * iw + 7, h * ih + ih // 2 + 4)],
            fill=(255, 0, 0))
        draw.rectangle([(w * iw, h * ih + ih // 2 - 1), (w * iw + 7, h * ih + ih // 2 + 1)], fill=(255, 0, 0))

    def draw_end_frame(frame_no):
        w = frame_no % width
        h = frame_no // width
        draw.rectangle([(w * iw + iw - 1, h * ih), (w * iw + iw - 3, h * ih + ih - 1)], fill=(255, 0, 0))
        draw.polygon([(w * iw + iw - 8, h * ih + ih // 2 - 4), (w * iw + iw - 13, h * ih + ih // 2),
                      (w * iw + iw - 8, h * ih + ih // 2 + 4)], fill=(255, 0, 0))
        draw.rectangle([(w * iw + iw - 1, h * ih + ih // 2 - 1), (w * iw + iw - 8, h * ih + ih // 2 + 1)],
                       fill=(255, 0, 0))

    def draw_transition_frame(frame_no):
        w = frame_no % width
        h = frame_no // width
        draw.rectangle([(w * iw, h * ih), (w * iw + iw - 1, h * ih + ih - 1)], fill=(128, 128, 128, 180))

    curr_frm, curr_scn = 0, 0

    while curr_scn < len(scenes):
        start, end = scenes[curr_scn]
        # gray out frames that are not in any scene
        while curr_frm < start:
            draw_transition_frame(curr_frm)
            curr_frm += 1

        # draw start and end of a scene
        draw_start_frame(curr_frm)
        draw_end_frame(end)

        # go to the next scene
        curr_frm = end + 1
        curr_scn += 1

    # gray out the last frames that are not in any scene (if any)
    while curr_frm < nf:
        draw_transition_frame(curr_frm)
        curr_frm += 1

    return img
