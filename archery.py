import cv2
import mediapipe as mp
import math
import random
import numpy as np
import time

cv2.namedWindow("Archery Game", cv2.WINDOW_NORMAL)

GAME_MODES = {
    'Traditional': 0,
}

current_game_mode = GAME_MODES['Traditional']

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_FPS, 60)

frame_width = int(cap.get(3))
frame_height = int(cap.get(4))


#Calibration variables
calibration_points = []
calibrating = True
calibration_frame_count = 0
calibration_frames = 50
calibration_threshold = 1


#General Game Variables
score = 0
arrow_released = False
arrow_drawn = False
arrow_position = (50, 50)
arrow_velocity = 50  # Arrow speed
arrow_direction = (-1, 0)
target_width = 40
target_height = 40
target_radius = 20
boundary_x = 370
target_x = random.randint(target_radius, boundary_x - 100)
target_y = random.randint(target_radius, frame_height - target_radius)
next_target_move_time = time.time() + 7

# Calibration
def calibrate_distance():
    global calibration_frame_count, calibration_points, calibration_threshold, calibrating

    calibration_points = []
    calibration_frame_count = 0
    calibrating = True

    cv2.namedWindow("Calibration", cv2.WINDOW_NORMAL)

    while calibrating:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb_frame)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                middle_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]

                distance = math.dist(
                    (index_tip.x * frame_width, index_tip.y * frame_height),
                    (middle_tip.x * frame_width, middle_tip.y * frame_height),
                )
                calibration_points.append(distance)

                cv2.putText(frame, f"Calibration: {round(calibration_frame_count / calibration_frames, 2)}",
                            (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        calibration_frame_count += 1

        if calibration_frame_count >= calibration_frames:
            calibration_threshold = np.mean(calibration_points)
            print(f"Calibration Complete. Threshold: {calibration_threshold}")
            calibrating = False

        cv2.imshow("Calibration", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            calibrating = False

    cv2.destroyWindow("Calibration")

# Reset Game
def reset_game():
    global arrow_released, arrow_drawn, arrow_position, target_x, target_y, next_target_move_time
    arrow_released = False
    arrow_drawn = False
    arrow_position = (50, 50)
    target_x = random.randint(target_radius, boundary_x - 100)
    target_y = random.randint(target_radius, frame_height - target_radius)
    next_target_move_time = time.time() + 7

# Draw Hand Landmarks
def draw_hand_landmarks(frame, hand_landmarks):
    connections = [(0, 1), (1, 2), (2, 3), (3, 4), (5, 6), (6, 7), (7, 8), (9, 10), (10, 11), (11, 12),
                   (13, 14), (14, 15), (15, 16), (17, 18), (18, 19), (19, 20)]
    for connection in connections:
        start_point = (int(hand_landmarks.landmark[connection[0]].x * frame_width),
                      int(hand_landmarks.landmark[connection[0]].y * frame_height))
        end_point = (int(hand_landmarks.landmark[connection[1]].x * frame_width),
                    int(hand_landmarks.landmark[connection[1]].y * frame_height))
        cv2.line(frame, start_point, end_point, (0, 255, 0), 2)

# Draw Arrow
def draw_arrow(frame, position, direction):
    tip = (
        int(position[0] + 75 * direction[0]),
        int(position[1] + 75 * direction[1])
    )
    base = (int(position[0]), int(position[1]))
    cv2.line(frame, base, tip, (0, 0, 255), 3)
    # Optional arrowhead (triangle)
    angle = math.atan2(direction[1], direction[0])
    arrowhead_points = [
        (int(tip[0] - 10 * math.cos(angle - math.pi / 6)),
         int(tip[1] - 10 * math.sin(angle - math.pi / 6))),
        (int(tip[0] - 10 * math.cos(angle + math.pi / 6)),
         int(tip[1] - 10 * math.sin(angle + math.pi / 6))),
    ]
    cv2.line(frame, tip, arrowhead_points[0], (0, 0, 255), 3)
    cv2.line(frame, tip, arrowhead_points[1], (0, 0, 255), 3)

# Update Target Position
def update_target_position():
    global target_x, target_y, next_target_move_time
    if time.time() > next_target_move_time:
        target_x = random.randint(target_radius, boundary_x - 100)
        target_y = random.randint(target_radius, frame_height - target_radius)
        next_target_move_time = time.time() + 7

# Collision Detection
def detect_collision(arrow_position, target_position, target_radius):
    distance = math.dist(arrow_position, target_position)
    return distance <= target_radius

def change_game_mode(new_mode):
    global current_game_mode
    current_game_mode = new_mode
    reset_game()

# Main Loop
while cap.isOpened():
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    cv2.line(frame, (boundary_x, 0), (boundary_x, frame_height), (0, 0, 0), 2)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            draw_hand_landmarks(frame, hand_landmarks)

            # Detect hand state for drawing/releasing arrow
            index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]

            # Calculate distance between index tip and thumb tip
            distance = math.dist(
                (index_tip.x * frame_width, index_tip.y * frame_height),
                (thumb_tip.x * frame_width, thumb_tip.y * frame_height)
            )

            if distance < calibration_threshold / 2:
                arrow_drawn = True
                # Update arrow position to follow the index finger when drawing
                arrow_position = (index_tip.x * frame_width, index_tip.y * frame_height)
                draw_arrow(frame, arrow_position, arrow_direction)  # Draw arrow while drawing

            elif arrow_drawn and distance >= calibration_threshold / 2 and not arrow_released:
                arrow_released = True
                arrow_drawn = False

                # Use index finger direction as arrow direction
                index_mcp = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP]

                dx = (index_tip.x - index_mcp.x) * frame_width
                dy = (index_tip.y - index_mcp.y) * frame_height

                length = math.sqrt(dx*dx + dy*dy)
                if length != 0:
                    dir_x = dx / length
                    dir_y = dy / length
                else:
                    dir_x, dir_y = -1, 0  # Default left direction if zero length

                arrow_direction = (dir_x, dir_y)

    # Update target position
    update_target_position()

    # Draw target
    cv2.circle(frame, (target_x, target_y), target_radius, (0, 255, 0), -1)
    cv2.putText(frame, f"Score: {score}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Move and draw arrow
    if arrow_released:
        arrow_position = (
            arrow_position[0] + arrow_velocity * arrow_direction[0],
            arrow_position[1] + arrow_velocity * arrow_direction[1]
        )
        draw_arrow(frame, arrow_position, arrow_direction)

        # Check collision with target
        if detect_collision(arrow_position, (target_x, target_y), target_radius):
            score += 1
            reset_game()

        # Reset arrow if out of bounds
        if (arrow_position[0] > frame_width or arrow_position[0] < 0 or
            arrow_position[1] < 0 or arrow_position[1] > frame_height):
            arrow_released = False
            arrow_drawn = False
            arrow_position = (50, 50)

    cv2.imshow("Archery Game", frame)

    key = cv2.waitKey(33) & 0xFF
    if key == ord('1'):
        change_game_mode(GAME_MODES['Traditional'])
        reset_game()
    elif key == ord('c'):
        calibrate_distance()
    elif key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
