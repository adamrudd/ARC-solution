import pygame
from pygame.locals import *
import json
import os

def read_task(task_type, filename):
    with open(f'dataset/{task_type}/{filename}') as f:
        data = json.load(f)
    return data

def read_model_output(ind):
    # Adjust this path to where your model outputs are stored
    with open(f'output/{ind}.json') as f:
        return json.load(f)

def readAll():
    tasks = []
    for i in range(419):  # Assuming 400 training tasks
        try:
            train_data = read_task('training', f'{i:06d}')
            test_data = read_task('test', f'{i:06d}')
            model_output = read_model_output(f'{i:06d}')
            
            tasks.append({
                'train': train_data['train'],
                'test': test_data['test'],
                'model_output': model_output
            })
        except FileNotFoundError:
            print(f"Warning: Could not find data for task {i:06d}")
            continue
    return [str(i) for i in range(len(tasks))], tasks

def main():
    sw, sh = 1500, 1000
    screen = pygame.display.set_mode((sw, sh))
    clock = pygame.time.Clock()

    pygame.key.set_repeat(200, 30)

    ni = 0
    ids, data = readAll()
    task = data[ni]
    print(f"Read {len(data)} tasks")

    pygame.display.set_caption(f'Task {ids[ni]} - {ni}')

    cols = [0x000000, 0x0074D9, 0xFF4136, 0x2ECC40, 0xFFDC00, 0xAAAAAA, 0xF012BE, 0xFF851B, 0x7FDBFF, 0x870C25]
    cols = [(i>>16&255, i>>8&255, i&255) for i in cols]

    def draw(img, bw, bord):
        w = len(img[0])
        h = len(img)
        ret = pygame.Surface((w*(bw+bord)+bord, h*(bw+bord)+bord))
        ret.fill((0x60,0x60,0x60))
        for (r, row) in enumerate(img):
            for (c, col) in enumerate(row):
                pygame.draw.rect(ret, cols[col], (c*(bw+bord)+bord, r*(bw+bord)+bord, bw, bw))
        return ret

    while True:
        for e in pygame.event.get():
            if e.type == QUIT or (e.type == KEYDOWN and e.key == K_ESCAPE):
                return
            elif e.type == KEYDOWN:
                if e.key in (K_RIGHT, K_d):
                    ni = (ni + 1) % len(data)
                elif e.key in (K_LEFT, K_a):
                    ni = (ni - 1) % len(data)
                task = data[ni]
                pygame.display.set_caption(f'Task {ids[ni]} - {ni}')

        screen.fill((200,180,150))

        tw = sw // 3
        th = sh // 5
        bw = 10
        offx = 0

        # Draw train input/output
        for i, train_pair in enumerate(task['train']):
            offy = 0
            for img in [train_pair['input'], train_pair['output']]:
                h, w = len(img), len(img[0])
                mul = int(min(tw/w, th/h)*4/5)
                bd = max(mul//50, 1)
                render = draw(img, mul-bd, bd)
                rw, rh = render.get_width(), render.get_height()
                screen.blit(render, (offx+(tw-rw)//2, offy+(th-rh)//2))
                offy += th
            offx += tw
            if i == 2:  # Limit to 3 train pairs
                break

        # Draw test input, model output, and actual output
        offx = 0
        offy = 2 * th
        test_pair = task['test'][0]
        for img in [test_pair['input'], task['model_output'], test_pair['output']]:
            h, w = len(img), len(img[0])
            mul = int(min(tw/w, th/h)*4/5)
            bd = max(mul//50, 1)
            render = draw(img, mul-bd, bd)
            rw, rh = render.get_width(), render.get_height()
            screen.blit(render, (offx+(tw-rw)//2, offy+(th-rh)//2))
            offx += tw

        # Add labels
        font = pygame.font.Font(None, 36)
        labels = ['Train Input', 'Train Output', 'Test Input', 'Model Output', 'Actual Output']
        for i, label in enumerate(labels):
            text = font.render(label, True, (0, 0, 0))
            screen.blit(text, (i % 3 * tw + 10, i // 3 * 2 * th + 10))

        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    pygame.init()
    main()
    pygame.quit()
