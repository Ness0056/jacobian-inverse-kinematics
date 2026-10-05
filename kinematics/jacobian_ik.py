import numpy as np
import os
import subprocess
import argparse

PI = np.pi
CLAMP_LENGTH = 1.56
N_STEPS = 90
FREEZE_INDEX = 4
D_DIGIT = 8


def read_dh_table(filename):
    dh = []

    with open(filename, "r") as f:
        for line in f:
            line = line.replace(",", " ").strip()
            if not line:
                continue

            values = line.split()
            if len(values) >= 4:
                alpha, a, d, theta = map(float, values[:4])
                dh.append([
                    np.deg2rad(alpha),
                    a,
                    d,
                    np.deg2rad(theta)
                ])

    if len(dh) != 9:
        raise ValueError(f"Expected 9 DH rows, got {len(dh)}")

    return np.array(dh, dtype=float)


def T_matrix(row):
    alpha, a, d, theta = row

    ct = np.cos(theta)
    st = np.sin(theta)
    ca = np.cos(alpha)
    sa = np.sin(alpha)

    return np.array([
        [ct,      -st,       0,   a],
        [st*ca,    ct*ca,  -sa,  -d*sa],
        [st*sa,    ct*sa,   ca,   d*ca],
        [0,         0,       0,    1]
    ], dtype=float)


def D_matrix(row):
    alpha, a, d, theta = row

    ct = np.cos(theta)
    st = np.sin(theta)
    ca = np.cos(alpha)
    sa = np.sin(alpha)

    return np.array([
        [-st,      -ct,      0, 0],
        [ct*ca,  -st*ca,    0, 0],
        [ct*sa,  -st*sa,    0, 0],
        [0,        0,       0, 0]
    ], dtype=float)


def jacobian(dh):
    J = np.zeros((3, 9))

    for j in range(9):
        DX = np.eye(4)

        for k in range(9):
            if k == j:
                DX = DX @ D_matrix(dh[k])
            else:
                DX = DX @ T_matrix(dh[k])

        J[0, j] = DX[0, 3] + CLAMP_LENGTH * DX[0, 0]
        J[1, j] = DX[1, 3] + CLAMP_LENGTH * DX[1, 0]
        J[2, j] = DX[0, 0]

    return J


def pseudo_inverse(J):
    return J.T @ np.linalg.inv(J @ J.T)


def x_position(frame, mode):
    if mode == "4b":
        i = frame
        nf = N_STEPS
        d = D_DIGIT
        return 13 + (8*i*i - 21*i*nf + d*i*nf) / (nf*nf)

    return 13 + (4 - 13) * frame / N_STEPS


def delta_X(frame, mode):
    return np.array([
        x_position(frame, mode) - x_position(frame - 1, mode),
        0.0,
        0.0
    ])


def write_dh_table(dh):
    with open("taula-DH", "w") as f:
        for row in dh:
            alpha, a, d, theta = row
            f.write(
                f"{np.rad2deg(alpha):.3f}, "
                f"{a:.3f}, "
                f"{d:.3f}, "
                f"{np.rad2deg(theta):.3f},\n"
            )


def save_first_step_files(J, M, dtheta):
    A = J @ J.T
    B = np.linalg.inv(A)

    with open("complete_jacobian_results_first_step.dat", "w") as f:
        f.write("::::::::::::::\n")
        f.write("jacobian.dat\n")
        f.write("::::::::::::::\n\n")

        f.write("  d X / d fi:\n\n")
        f.write("".join(f"{v:12.6f}" for v in J[0]) + "\n\n")

        f.write("  d Y / d fi:\n\n")
        f.write("".join(f"{v:12.6f}" for v in J[1]) + "\n\n")

        f.write("  d r_up_left / d fi:\n\n")
        f.write("".join(f"{v:12.6f}" for v in J[2]) + "\n\n")

        f.write("::::::::::::::\n")
        f.write("A_reduced_jacobian.dat\n")
        f.write("::::::::::::::\n")
        for row in A:
            f.write("".join(f"{v:12.5f}" for v in row) + "\n")

        f.write("::::::::::::::\n")
        f.write("B_reduced_jacobian.dat\n")
        f.write("::::::::::::::\n")
        for row in B:
            f.write("".join(f"{v:12.5f}" for v in row) + "\n")

        f.write("::::::::::::::\n")
        f.write("pseudo_inverse_jacobian.dat\n")
        f.write("::::::::::::::\n")
        for row in M:
            f.write("".join(f"{v:12.5f}" for v in row) + "\n")

    with open("first_step.dat", "w") as f:
        f.write("::::::::::::::\n")
        f.write("Change in internal degrees of freedom, first step, in radians.\n")
        f.write("::::::::::::::\n")
        for v in dtheta:
            f.write(f"{v:12.6f}\n")


def render_frame(folder, frame):
    if not os.path.exists("jcb.pov"):
        return False

    output = f"{folder}/frame_{frame:05d}.png"

    cmd = [
        "povray",
        "+Ijcb.pov",
        f"+O{output}",
        "+W800",
        "+H600",
        "+A0.3",
        "+Q11",
        "-D"
    ]

    try:
        subprocess.run(cmd, check=True)
        return True
    except Exception:
        return False


def make_video(folder, video_name):
    cmd = [
        "ffmpeg",
        "-y",
        "-framerate", "30",
        "-i", f"{folder}/frame_%05d.png",
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        video_name
    ]

    try:
        subprocess.run(cmd, check=True)
    except Exception:
        print("Video not created. ffmpeg may not be installed.")


def run(mode):
    if mode == "3":
        folder = "frames3"
        video = "animation3.mp4"
        freeze = False

    elif mode == "4a":
        folder = "frames41"
        video = "animation41.mp4"
        freeze = True

    elif mode == "4b":
        folder = "frames42"
        video = "animation42.mp4"
        freeze = False

    else:
        raise ValueError("Mode must be 3, 4a, or 4b")

    os.makedirs(folder, exist_ok=True)

    input_file = "taula-DH.0" if os.path.exists("taula-DH.0") else "taula-DH"
    dh = read_dh_table(input_file)

    frozen_theta = dh[FREEZE_INDEX, 3]

    print(f"Running point {mode}")
    print(f"Reading: {input_file}")
    print(f"Frames folder: {folder}")

    if mode == "4b":
        print(f"Using DNI digit d = {D_DIGIT}")

    for frame in range(1, N_STEPS + 1):
        J = jacobian(dh)

        if freeze:
            J[:, FREEZE_INDEX] = 0.0

        M = pseudo_inverse(J)
        dX = delta_X(frame, mode)
        dtheta = M @ dX

        if freeze:
            dtheta[FREEZE_INDEX] = 0.0

        if frame == 1:
            save_first_step_files(J, M, dtheta)

        dh[:, 3] += dtheta

        if freeze:
            dh[FREEZE_INDEX, 3] = frozen_theta

        write_dh_table(dh)

        rendered = render_frame(folder, frame)

        if frame == 1 or frame % 10 == 0:
            print(f"Frame {frame}/{N_STEPS}")

        if frame == 1 and not rendered:
            print("POV-Ray did not render. Check that POV-Ray is installed and jcb.pov works.")

    make_video(folder, video)

    print("Done.")
    print(f"Frames saved in: {folder}")
    print(f"Video name: {video}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["3", "4a", "4b"], default="3")
    args = parser.parse_args()

    run(args.mode)