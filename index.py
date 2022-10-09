import os
from random import randint
import pygame, sys
import random
import time
import sqlite3
from pygame.locals import *
from sqlite3 import Error
from collections import OrderedDict

connection = sqlite3.connect('score.db')
cursor = connection.cursor()
create_table = "CREATE TABLE IF NOT EXISTS score (highscore int)"
cursor.execute(create_table)


def insertDatabase(score):
    dbHighestScore = selectDatabase()
    if score > dbHighestScore:
        # create table in database
        insert_query = "INSERT INTO score VALUES (" + str(score) + ")"
        cursor.execute(insert_query)
        connection.commit()


def selectDatabase():
    result = 0
    select_query = "SELECT MAX(highscore) FROM score"
    cursor.execute(select_query)
    result = cursor.fetchone()
    highScore = result[0]
    if str(highScore) == 'None':
        highScore = 0
    return highScore


def loopFunction():
    pygame.init()

    screen = pygame.display.set_mode((1000, 800))
    pygame.display.set_caption('BrickBreaker')
    clock = pygame.time.Clock()
    run = True
    start = gameover = False
    fond = pygame.image.load("fond.jpg")
    screen.blit(fond, (0, 0))
    brickCooX = 500
    brick = Rect(brickCooX, 750, 100, 10)
    brickSpeed = 9
    direction = "null"
    font = pygame.font.Font('freesansbold.ttf', 32)

    highscore = selectDatabase()
    highestScore = font.render('Highest Score : ' + str(highscore), True, (255, 255, 255))
    screen.blit(highestScore, (700, 20))
    score = 0
    beginText = font.render("Press any key to begin", True, (255, 255, 255))
    screen.blit(beginText, (350, 500))

    intervalOf10 = row = 0
    bricks = {}
    bricksNumber = 70
    pygame.draw.rect(screen, (randint(0, 255), randint(0, 255), (randint(0, 255))), brick)


    for i in range(bricksNumber):
        bricks[i] = {'posX': (intervalOf10*100), 'posY': (row * 50) + 100, 'state': "alive"}
        pygame.draw.rect(screen, (randint(0, 255), randint(0, 255), randint(0, 255)),
                         Rect(bricks[i]["posX"], bricks[i]["posY"], 100, 50))
        if intervalOf10 < 9:
            intervalOf10 += 1
        else:
            intervalOf10 = 0
            row += 1

    while run:
        while gameover:
            font = pygame.font.SysFont(None, 50)
            end = font.render('Press Enter to restart game', True, (255, 255, 255))
            screen.blit(end, (350, 500))
            clock.tick(60)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    insertDatabase(score)
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        insertDatabase(score)
                        loopFunction()
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.KEYDOWN:
                    if start is False:
                        timerEverySeconds = time.time()
                        start = True
                    if event.key == pygame.K_LEFT:
                        direction = "left"
                    if event.key == pygame.K_RIGHT:
                        direction = "right"
                if event.type == pygame.KEYUP:
                    direction = "null"
            if direction == "left":
                if brickCooX < 10:
                    brickCooX = brickCooX
                else:
                    brickCooX = brickCooX - brickSpeed
            if direction == "right":
                if brickCooX > 940:
                    brickCooX = brickCooX
                else:
                    brickCooX = brickCooX + brickSpeed

            if start is True:
                screen.blit(fond, (0, 0))
                currentScoreText = font.render('Score : ' + str(score), True, (255, 255, 255))
                scoreText = font.render('Highest Score : ' + str(highscore), True, (255, 255, 255))
                screen.blit(currentScoreText, (200, 20))
                screen.blit(scoreText, (700, 20))
                atLeastOneAlive = False

                for i in range(bricksNumber):
                    print("ici")

                if not atLeastOneAlive:
                    gameover = True

        clock.tick(60)
        pygame.display.flip()


loopFunction()
