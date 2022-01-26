

# Using https://www.pygame.org/docs/ref/draw.html
# Import a library of functions called 'pygame'
import pygame
from math import pi
import random


def make_walls(A, w_pic, n):
    A.clear()
    H=100
    W=100
    H, W = pygame.display.get_window_size()
    print(H,W)
    for i in range(n):
        A.append((random.randrange(0, H-w_pic, w_pic),
                  random.randrange(0, W-w_pic, w_pic)))
        print(A[i])


def chekmeaning(mean:int):
    if mean>=390:
        mean=390
    if mean<=0:
        mean=0
    return mean



def ev_chek(loc_list, w_list):
    acr_x=''
    acr_y=''
    redraw_walls=False
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            loc_list[3]=True # Flag that we are done so we exit this loop
        if event.type == pygame.KEYDOWN:
            acr_x, acr_y = chek_acrossing(w_list, loc_list[0], loc_list[1])
            if event.key == pygame.K_F1:
                redraw_walls=True                
            if event.key == pygame.K_LEFT:
                loc_list[2]='left'
                print('left')
                if acr_x == 'x_l' or acr_x == 'x_r_x_l':
                    pass
                else:
                    loc_list[0]-=30
                    loc_list[0]=chekmeaning(loc_list[0])
                    
            if event.key == pygame.K_RIGHT:
                loc_list[2]='right'
                print('right')
                if acr_x == 'x_r' or acr_x == 'x_r_x_l':
                    pass
                else:
                    loc_list[0]+=30
                    loc_list[0]=chekmeaning(loc_list[0])
                    
            if event.key == pygame.K_DOWN:
                if acr_y == 'y_dn' or acr_y=='y_up_y_dn':
                    pass
                else:
                    print('down')
                    loc_list[1]+=30
                    loc_list[1]=chekmeaning(loc_list[1])
            if event.key == pygame.K_UP:
                if acr_y == 'y_up' or acr_y=='y_up_y_dn':
                    pass
                else:
                    print('up')
                    loc_list[1]-=30
                    loc_list[1]=chekmeaning(loc_list[1])
            print(loc_list)
    return loc_list, redraw_walls



    
def chek_eat(x1, x2, y1, y2): # does buster kill ghost?
    ret=False
    if x1-x2 < 30 and x1-x2 > -30 and y1-y2 < 30 and y1-y2 > -30:
        ret=True
    return ret


def chek_acrossing(wall_list, x1, y1):

    acr_x='x0'
    acr_y='y0'
    fl_x_l=False
    fl_x_r=False
    fl_y_up=False
    fl_y_dn=False
    
    for T in wall_list:
        x2, y2 = T
        if x1-x2 == -30 and y1==y2:
            fl_x_r=True 
            
        if x1-x2 == 30 and y1==y2:
            fl_x_l=True
                
        if y1-y2 == -30 and x1==x2:
            fl_y_dn=True
            
        if y1-y2 == 30 and x1==x2:
            fl_y_up=True
    
    if fl_x_l and fl_x_r:
        acr_x='x_r_x_l'
    elif fl_x_l:
        acr_x='x_l'
    elif fl_x_r:
            acr_x='x_r'
            
    if fl_y_up and fl_y_dn:
        acr_y='y_up_y_dn'
    elif fl_y_up:
        acr_y='y_up'
    elif fl_y_dn:
            acr_y='y_dn'    

    print(acr_x, acr_y)      
    return acr_x, acr_y

def get_new_position(w_list, H, W, weight_pic):
   
    flag_pos=1

    while flag_pos>0:  #do while there are no acrossings

        flag_pos=1
    
        x_n=random.randrange(0, H-weight_pic, weight_pic)
        y_n=random.randrange(0, W-weight_pic, weight_pic)

        for T in w_list:
            x, y = T
            if x_n==x and y_n==y:
                flag_pos+=1
            
        if flag_pos<2:
            flag_pos=0
           
    
    return x_n, y_n
   
           
def main():
    
    x=0     #buster abscissa
    y=0     #buster ordinate
    f_x=0   #position x in my_list
    f_y=1   #position y in my_list
    f_dn=3  #position "done" in my_list
    H=420   #screen 
    W=420   #screen
    weight_pic=30           #size of pictures 30x30
    walls_list=[(30, 30)]   #pre-list for walls
    redraw_walls=False
    #Load pictures

    ghost_surf=pygame.image.load_basic('ghost.bmp')
    buster_r=pygame.image.load_basic('buster_r.bmp') #when buster goes to the right
    buster_l=pygame.image.load_basic('buster_l.bmp') #when buster goes to the left
    wall=pygame.image.load_basic('wall.bmp')
    buster=buster_r
    
    # Initialize the game engine
    pygame.init()
 
    # Define the colors we will use in RGB format
    WHITE = (255, 255, 255)

 
    # Set the height and width of the screen
    size = [H, W]
    screen = pygame.display.set_mode(size)
 
    pygame.display.set_caption("GhostBusters")
    pygame.display.set_icon(ghost_surf)

    pygame.mixer.music.load('GB_song.mp3')
    pygame.mixer.music.play(-1)        # Plays loop times
    pygame.mixer.music.queue('GB_song.mp3')
        
    make_walls(walls_list, weight_pic, 50)
    
    en_x, en_y = get_new_position(walls_list, H, W, weight_pic)
    
    #Loop until the user clicks the close button.
    done = False

    my_list=[x, y, buster, done]
    
    clock = pygame.time.Clock()
 
    print(en_x,en_y)
    
    while not done:
        # This limits the while loop to a max of 10 times per second.
        # Leave this out and we will use all CPU we can.
        clock.tick(10)

        my_list, redraw_walls=ev_chek(my_list, walls_list)
        
        done=my_list[f_dn]
        if redraw_walls:
            make_walls(walls_list, weight_pic, 50)
            en_x, en_y = get_new_position(walls_list, H, W, weight_pic) #new random position x and y of ghost excluding walls position
         
        # All drawing code happens after the for loop and but
        # inside the main while done==False loop.
     
        # Clear the screen and set the screen background
        screen.fill(WHITE)
    
        # Draw
        if chek_eat(en_x, my_list[f_x], en_y, my_list[f_y]): #Does buster eat ghost?
            pygame.mixer.music.load('eatme.mp3')
            pygame.mixer.music.play(0)        # Plays 1 times
            #pygame.mixer.music.queue('eatme.mp3')
            while pygame.mixer.music.get_busy():
                pass
            pygame.mixer.music.load('GB_song.mp3')
            pygame.mixer.music.play(-1)        # Plays loop times
            pygame.mixer.music.queue('GB_song.mp3')
            print(en_x-my_list[f_x],en_y-my_list[f_y])
            en_x, en_y = get_new_position(walls_list, H, W, weight_pic) #new random position x and y of ghost excluding walls position
      
        screen.blit(ghost_surf,[en_x, en_y])

        if my_list[2]=='left': 
            buster=buster_l
        else:
            buster=buster_r

        for h_w,w_w in walls_list:
           screen.blit(wall,[h_w,w_w])
        
        screen.blit(buster,[my_list[f_x], my_list[f_y]])

        # Go ahead and update the screen with what we've drawn.
        # This MUST happen after all the other drawing commands.
        pygame.display.flip()
 
    # Be IDLE friendly
    pygame.quit()


main()
