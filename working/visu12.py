# works for MAX_TASKS

import pygame
from pygame.locals import *
import json
import os
import sys

# Setting for the number of tasks to look through
MAX_TASKS = 400  # Default value, can be changed as needed

def read_task(filename):
    try:
        with open(os.path.join('../dataset', 'evaluation', filename)) as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        print(f"Warning: Could not find data for {filename}")
        return None

def read_model_outputs():
    model_outputs = {}
    directory = '../model_outputs'
    try:
        for filename in sorted(os.listdir(directory)):
            if filename.endswith('.json'):
                task_id = os.path.splitext(filename)[0]
                try:
                    with open(os.path.join(directory, filename)) as f:
                        data = json.load(f)
                    model_outputs[task_id] = data
                except FileNotFoundError:
                    print(f"Warning: Could not find model output for {filename}")
    except FileNotFoundError:
        print("Warning: '../model_outputs' directory not found. Assuming no model attempts.")
    return model_outputs

def readAll():
    tasks = []
    directory = os.path.join('../dataset', 'evaluation')
    for filename in sorted(os.listdir(directory)):
        if filename.endswith('.json'):
            task_data = read_task(filename)
            if task_data:
                tasks.append(task_data)
    return [os.path.splitext(f)[0] for f in sorted(os.listdir(directory)) if f.endswith('.json')], tasks

def main():
    sw, sh = 1500, 1000
    screen = pygame.display.set_mode((sw, sh))
    clock = pygame.time.Clock()

    pygame.key.set_repeat(200, 30)

    ids, data = readAll()
    model_outputs = read_model_outputs()

    # Limit the number of tasks to MAX_TASKS
    ids = ids[:MAX_TASKS]
    data = data[:MAX_TASKS]

    if not data:
        print("No data found. Please check your dataset/evaluation directory.")
        return

    # Check for optional command-line argument
    task_id_input = None
    if len(sys.argv) > 1:
        task_id_input = sys.argv[1].replace('.json', '')  # Remove .json if present

    # Ensure task_id_input is a string before using it
    if task_id_input is not None:
        matching_ids = [task_id for task_id in ids if task_id_input in task_id]
    else:
        matching_ids = []  # No input provided, set matching_ids to an empty list

    # Set the task index based on input or default to first matching task
    ni = 0  # Default to first matching task or first task if none match

    print(f"Task ID input: {task_id_input}")
    print(f"IDs available: {ids}")
    print(f"Matching IDs: {matching_ids}")

    if matching_ids:
        ni = ids.index(matching_ids[0])
        print(f"Using specified task: {ids[ni]}")
    else:
        print(f"No matching tasks found. Using default task: {ids[ni]}")

    page = 0
    task = data[ni]
    
    print(f"Read {len(data)} tasks")
    pygame.display.set_caption(f'Task {ids[ni]} - {ni}')

    colors = [
        (0, 0, 0),       # Black
        (0, 116, 217),   # Blue
        (255, 65, 54),   # Red
        (46, 204, 64),   # Green
        (255, 220, 0),   # Yellow
        (170, 170, 170), # Light gray
        (240, 18, 190),  # Magenta
        (255, 133, 27),  # Orange
        (127, 219, 255), # Light blue
        (135, 12, 37)    # Dark red
    ]

    def draw(img, bw, bord):
        w = len(img[0])
        h = len(img)
        ret = pygame.Surface((w*(bw+bord)+bord, h*(bw+bord)+bord))
        ret.fill((96, 96, 96))  
        for r, row in enumerate(img):
            for c, col in enumerate(row):
                color = colors[col % len(colors)]
                pygame.draw.rect(ret, color, (c*(bw+bord)+bord, r*(bw+bord)+bord, bw, bw))
        return ret

    font = pygame.font.Font(None, 30)

    def draw_labeled_image(screen, img, label, x, y, tw, th):
        h, w = len(img), len(img[0])
        if max(h,w) <= 3:
            bw = 40  
        else:
            bw = int(min(tw/w ,th/h)*0.7)  
        bd = max(bw//10 ,1)
        render = draw(img ,bw ,bd)
        rw ,rh = render.get_width(), render.get_height()
        screen.blit(render ,(x+(tw-rw)//2 ,y+(th-rh)//2 -15)) 
        
        text = font.render(label ,True ,(0 ,0 ,0))
        text_rect = text.get_rect(center=(x+tw//2 ,y+th-15))  
        screen.blit(text,text_rect)

    running = True
    try:
        while running:
            for e in pygame.event.get():
                if e.type == QUIT or (e.type == KEYDOWN and e.key == K_ESCAPE):
                    running = False
                elif e.type == KEYDOWN:
                    if e.key in (K_RIGHT,K_d):
                        page=0
                        ni=(ni+1)%len(data)
                    elif e.key in (K_LEFT,K_a):
                        page=0
                        ni=(ni-1)%len(data)
                    elif e.key in (K_DOWN,K_s):
                        page+=1
                    elif e.key in (K_UP,K_w):
                        page=max(0,page-1)
                    task=data[ni]
                    pygame.display.set_caption(f'Task {ids[ni]} - {ni} - Page {page+1}')

            screen.fill((200 ,180 ,150))

            pairs = []
            
            # Add train pairs
            for i, train_pair in enumerate(task['train']):
                pairs.append((train_pair['input'], f'Train {i + 1} Input', train_pair['output'], f'Train {i + 1} Output'))

            # Add test pairs and model attempts
            for i, test_pair in enumerate(task['test']):
                test_input = test_pair['input']
                test_output = test_pair.get('output', 'Not provided')  # Use 'Not provided' if output is missing
                pairs.append((test_input, f'Test {i + 1} Input', test_output, f'Test {i + 1} Output'))

                # Check for model outputs corresponding to this task
                if ids[ni] in model_outputs:
                    for output in model_outputs[ids[ni]]:
                        if output['output_number'] == i + 1:  # Match output number to test pair index
                            pairs.append((
                                test_input,
                                f"Model {output['model_number']} Test {i + 1} Input",
                                output['array'],
                                output['label']
                            ))

            # Calculate layout
            max_pair_width = max(max(len(p[0][0]), len(p[2][0])) for p in pairs)
            pair_width = min(sw // 3, 180 if max_pair_width <= 3 else sw // 3)
            pair_height = pair_width * 2 + 40  

            cols = max(1, sw // pair_width)  
            rows = max(1, sh // pair_height)  

            pairs_per_page = cols * rows

            # Calculate which pairs to display on this page
            start_index = page * pairs_per_page
            end_index = min(start_index + pairs_per_page, len(pairs))

            # Ensure that the page index does not exceed total pages
            if start_index >= len(pairs):
                page = (len(pairs) - 1) // pairs_per_page  # Set to last page if out of bounds
                start_index = page * pairs_per_page
                end_index = min(start_index + pairs_per_page, len(pairs))

            # Draw pairs
            for i, (input_img, input_label, output_img, output_label) in enumerate(pairs[start_index:end_index]):
                x = (i % cols) * pair_width
                y = (i // cols) * pair_height
                
                draw_labeled_image(screen, input_img, input_label, x, y, pair_width,
                                    (pair_height - 40) // 2)
                draw_labeled_image(screen,
                                    output_img,
                                    output_label,
                                    x,
                                    y + (pair_height - 40) // 2,
                                    pair_width,
                                    (pair_height - 40) // 2)

            # Display page information
            if pairs_per_page > 0:
                total_pages = (len(pairs) + pairs_per_page - 1) // pairs_per_page
                page_info = f"Page {page + 1}/{total_pages}"
            else:
                page_info = "No pairs to display"

            text = font.render(page_info ,True ,(0 ,0 ,0))
            screen.blit(text,(10 ,sh -40))

            pygame.display.flip()
            
            clock.tick(30)
    finally:
        # Print first row of all arrays and their labels for each task
        print("\nFirst row of all arrays and their labels for each task:")
        for i, task in enumerate(data):
            print(f"\nTask {ids[i]}:")
            for j, train_pair in enumerate(task['train']):
                print(f"  Train {j + 1} Input:  {train_pair['input'][0]}")
                print(f"  Train {j + 1} Output: {train_pair['output'][0]}")
            for j, test_pair in enumerate(task['test']):
                print(f"  Test {j + 1} Input:   {test_pair['input'][0]}")
                if 'output' in test_pair:
                    print(f"  Test {j + 1} Output:  {test_pair['output'][0]}")
                else:
                    print(f"  Test {j + 1} Output:  Not provided")
            
            # Print model outputs
            if ids[i] in model_outputs:
                for output in model_outputs[ids[i]]:
                    print(f"  {output['label']}: {output['array'][0]}")

if __name__ == "__main__":
    pygame.init()
    main()
    pygame.quit()
    sys.exit()
