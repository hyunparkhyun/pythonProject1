import pygame  #py게임을 가져옴
import random
import sys
from pygame.rect import *

global correct_sound, incorrect_sound, gameover_sound

pygame.init()  #pygame초기화

test_sound = pygame.mixer.Sound("bagroundsample.mp3")
test_sound.play()

pygame.display.set_caption("github.com")  #상단의 주소
# ========= 변수 ================================= ###############################
isActive = True # while문을 반복하는데
SCREEN_WIDTH = 400  #스크린 크기
SCREEN_HEIGHT = 600  #스크린 크기
chance_MAX = 10  #기회를 10번줌
score = 0 #처음 점수를 0으로 만들어줌
chance = chance_MAX
isColl = False
CollDirection = 0
DrawResult, result_ticks = 0, 0
start_ticks = pygame.time.get_ticks()

clock = pygame.time.Clock() #
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


# ======== 함수 ===============================
# 키 이벤트 처리하기
def resultProcess(direction):#방향과 일치하는 값을 입력했을 때 결과 표현
    global isColl, score, DrawResult, result_ticks #global을 사용하면 다른곳에서 이미 선언된것을 찾아서 이용할 수 있게 만듬.

    if isColl and CollDirection.direction == direction:  # 방향을 맞췄을때 방향 지시표를 사라지게 만듬
        score += 10
        CollDirection.y = -1
        DrawResult = 1
        test_sound = pygame.mixer.Sound("001_뽁.wav")
        test_sound.play()
    else:
        DrawResult = 2
        test_sound = pygame.mixer.Sound("039_삐.mp3")
        test_sound.play()
    result_ticks = pygame.time.get_ticks()


def eventProcess():
    global isActive, score, chance #global을 사용하면 다른곳에서 이미 선언된것을 찾아서 이용할 수 있게 만듬.
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:  #esc키를 눌렀을 떄 false 값을 주어서 반복문을 종료함.
                isActive = False
            if chance > 0:
                if event.key == pygame.K_UP:  #0
                    resultProcess(0)
                if event.key == pygame.K_LEFT:  #1
                    resultProcess(1)
                if event.key == pygame.K_DOWN:  #2
                    resultProcess(2)
                if event.key == pygame.K_RIGHT:  #3
                    resultProcess(3)
            else:  #스페이스 바를 눌러서 점수와 기회를 초기화하여 다시 게임을 할 수 있게 만듬
                if event.key == pygame.K_SPACE:
                    score = 0
                    chance = chance_MAX
                    for direc in Directions:
                        direc.y = -1


# 방향 아이콘 클래스 ################################################################
class Direction(object): #방향을 보여주는 클래스를 작성.이미지를 랜덤하게 만들기 위해서서는 코드를 재사용해야 하기 때문에 class사용
    def __init__(self):
        self.pos = None # 좌표를 가지고 이미지와 동일한 방향을 입력했는지 확인할 수 있음.
        self.direction = 0
        self.image = pygame.image.load(f"direction.png")  # 방향 이미지를 가져옴
        self.image = pygame.transform.scale(self.image, (50,50)) #방향 이미지의 크기를 조정함.
        self.rotated_image = pygame.transform.rotate(self.image, 0)
        self.y = -1  #방향 이미지가 내려오는것을 표현
        self.x = int(SCREEN_WIDTH * 0.75) - (self.image.get_width() / 2)

    def rotate(self, direction=0):  #방향 이미지를 회전하는 코드(회전하는 이미지를 랜덤으로 발생)
        self.direction = direction
        self.rotated_image = pygame.transform.rotate(
            self.image, 90 * self.direction)

    def draw(self):  #예외처리. (스크린을 벗어낫을때,y 초기값이 -1인 경우)
        if self.y >= SCREEN_HEIGHT:
            self.y = -1
            return True
        elif self.y == -1:
            return False
        else:
            self.y += 1
            self.pos = screen.blit(self.rotated_image, (self.x, self.y))
            return False


# 방향 아이콘 생성과 그리기#######################################################
def drawIcon():
    global start_ticks, chance

    if chance <= 0: #기회가 0 이하가 됐을때 더 이상 방향 이미지가 나오지 않게 만들어주는 가정문
        return

    elapsed_time = (pygame.time.get_ticks() - start_ticks)
    if elapsed_time > 400:  #400mm주기로 방향 이미지가 나오게함(방향 이미지의 주기)
        start_ticks = pygame.time.get_ticks()
        for direc in Directions:
            if direc.y == -1:
                direc.y = 0
                direc.rotate(direction=random.randint(0, 3))  # 방향을 0~3 랜덤으로 만들어줌.
                break

    for direc in Directions: #기회 횟수를 줄여주는 반복문
        if direc.draw():
            chance -= 1


# 타겟 영역 그리기와 충돌 확인하기###############################################
def draw_targetArea():  # 범위 내에서 충돌했는지 판단해주는 함수
    global isColl, CollDirection
    isColl = False
    for direc in Directions:
        if direc.y == -1:
            continue
        if direc.pos.colliderect(targetArea):
            isColl = True
            CollDirection = direc
            pygame.draw.rect(screen, (255, 0, 0), targetArea)  # 범위 내에 방향 이미지가 들어오면 빨간색을 표시해주게 도와줌
            break
    pygame.draw.rect(screen, (0, 255, 0), targetArea, 5)


# 문자 넣기 #################################################################
def setText():
    global score, chance
    mFont = pygame.font.SysFont("굴림", 40)

    mtext = mFont.render(f'score : {score}', True, 'yellow')
    screen.blit(mtext, (10, 10, 0, 0))

    mtext = mFont.render(f'chance : {chance}', True, 'yellow')
    screen.blit(mtext, (10, 42, 0, 0))

    if chance <= 0:  # 기회가 다 끝났을때 game over라는 텍스트를 보여주고 효과음을 출력하게함
        test_sound = pygame.mixer.Sound("093_폭발 -c고전게임.mp3")
        test_sound.play()
        mFont = pygame.font.SysFont("굴림", 90)
        mtext = mFont.render(f'Game over!!', True, 'red')
        tRec = mtext.get_rect()
        tRec.centerx = SCREEN_WIDTH / 2
        tRec.centery = SCREEN_HEIGHT / 2 - 40
        screen.blit(mtext, tRec)


# 결과 이모티콘 그리기 ############################################################
def drawResult():
    global DrawResult, result_ticks
    if result_ticks > 0:
        elapsed_time = (pygame.time.get_ticks() - result_ticks)
        if elapsed_time > 400:  #이모티컨이 유지되는 시간을  방향 지시표의 주기와 똑같이 만듬
            result_ticks = 0
            DrawResult = 0
    screen.blit(resultImg[DrawResult], resultImgRec)


# 방향 아이콘
Directions = [Direction() for i in range(0, 10)]  # 생성을 하나씩 바로 내보내면 버벅거림이 있어서 미리 생성한뒤 내보냄
# 타겟 박스
targetArea = Rect(SCREEN_WIDTH / 2, 400, SCREEN_WIDTH / 2, 80)  #허용 범위를 알려줌
# 결과 이모티콘
resultFileNames = ["음악고릴라.png", "정답고릴라.png", "오답고릴라.png"] # 결과 이모티컨 사진을 출력함
resultImg = []
for i, name in enumerate(resultFileNames): #이모티컨의 위치
    resultImg.append(pygame.image.load(name))
    resultImg[i] = pygame.transform.scale(resultImg[i], (150, 75))


resultImgRec = resultImg[0].get_rect()
resultImgRec.centerx = SCREEN_WIDTH / 2 - resultImgRec.width / 2 - 40
resultImgRec.centery = targetArea.centery
# ========= 반복문 =============================== ##########################
while isActive:
    screen.fill((0, 0, 0))
    eventProcess()
    # Directions[0].y = 100
    # Directions[0].rotate(1)
    # Directions[0].draw()
    draw_targetArea()
    drawIcon()
    setText()
    drawResult()

    pygame.display.update()
    clock.tick(400) #1초에 while문을 몇번 반복할 지=떨어지는 속도를 정해줌
