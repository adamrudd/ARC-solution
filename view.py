import pygame
from pygame.locals import *
import json
from sys import argv
import os

def read(task_id):
    with open(f'./dataset/training/{task_id}.json') as f:
        data = json.load(f)
    return data['train']

def readAll():
    l = []
    ids = []
    directory = './dataset/training'
    for filename in sorted(os.listdir(directory))[:10]:  # Only process the first 10 files
        if filename.endswith('.json'):
            task_id = filename[:-5]  # Remove '.json' from the filename
            ids.append(task_id)
            l.append(read(task_id))
    return ids, l

def readOutputs():
    names = []
    tasks = []
    directory = './dataset/training'
    for filename in sorted(os.listdir(directory))[:10]:  # Only process the first 10 files
        if filename.endswith('.json'):
            with open(os.path.join(directory, filename), 'r') as f:
                data = json.load(f)
                names.append(filename[:-5])  # Remove '.json' from the filename
                tasks.append(data['train'])
    return names, tasks

def main():
    sw, sh = 1500,800
    screen = pygame.display.set_mode((sw, sh))
    clock = pygame.time.Clock()

    pygame.key.set_repeat(200, 30)

    ni = 0
    ids, data = readAll()  # Always use readAll() to get the first 10 tasks
    task = data[ni]
    print("Read %d tasks"%len(data))

    pygame.display.set_caption(ids[ni] + ' - ' + str(ni))

    cols = [0x000000, 0x0074D9, 0xFF4136, 0x2ECC40, 0xFFDC00, 0xAAAAAA, 0xF012BE, 0xFF851B, 0x7FDBFF, 0x870C25]
    cols = [(i>>16&255, i>>8&255, i&255) for i in cols]

    # Create output directory if it doesn't exist
    if not os.path.exists('output'):
        os.makedirs('output')

    for ni, task in enumerate(data):
        screen.fill((200,180,150))

        trains = len(task)
        tw = sw // max(trains,1)
        th = sh//2
        bw = 10
        offx = 0

        def draw(img, bw,bord):
            w = len(img[0])
            h = len(img)
            ret = pygame.Surface((w*(bw+bord)+bord,h*(bw+bord)+bord))
            ret.fill((0x60,0x60,0x60))
            for (r, row) in enumerate(img):
                for (c, col) in enumerate(row):
                    pygame.draw.rect(ret, cols[col], (c*(bw+bord)+bord,r*(bw+bord)+bord,bw,bw))
            return ret

        for io in task:
            offy = 0
            for img in [io['input'], io['output']]:
                h = len(img)
                if not h: continue
                w = len(img[0])

                mul = int(min(tw/w, th/h)*4/5)
                bd = max(mul//50,1)
                render = draw(img, mul-bd, bd)

                rw, rh = render.get_width(), render.get_height()

                screen.blit(render, (offx+(tw-int(rw))//2, offy+(th-int(rh))//2))
                offy += th
            offx += tw
        
        # Save the screen as an image
        pygame.image.save(screen, f'output/task_{ids[ni]}.png')
        
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__": main()
