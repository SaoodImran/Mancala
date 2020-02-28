# Mancala Game Script
INFINITY = 1.0e400
def printNextMove(pid, p1score, pboard, p2score, eboard):
    total = 48 - p1score - p2score
    if pid != 1:
            temp = pboard
            pboard = eboard
            eboard = temp
            scoretemp = p1score
            p1score = p2score
            p2score = scoretemp

    fullboard = makeFullBoard(pboard, eboard, p1score, p2score)
    if firstmove(fullboard.copy()):
        return 3
    if secondmove(fullboard.copy()):
        return 6
    depth = 11
    total = sum(fullboard[0:6]) + sum(fullboard[7:13])
    if total <= 30:
        depth = 12
    if total <= 15:
        depth = 13
    if total <= 10:
        depth = 16

        
    move = minmax(fullboard.copy(),depth,True,-INFINITY,+INFINITY,-1)
    return move[1]+1


def firstmove(fullboard):
    return fullboard == [4,4,4,4,4,4,0,4,4,4,4,4,4,0]
def secondmove(fullboard):
    return fullboard == [4,4,0,5,5,5,1,4,4,4,4,4,4,0]
    
    
def computeMoves(fullboard,isHuman):
    moves = []
    if isHuman:
        for x in range(0,6):
            if fullboard[x] != 0:
                moves.append(x)
    else:
        for x in range(7,13):
                if fullboard[x] != 0:
                    moves.append(x)
    return moves

        
def sumofSide(fullboard,human):
    marbs = 0
    if human:
        for x in range(0,6):
            if x == 5 or x == 4:
                marbs+= fullboard[x]*1
            if x == 3 or x == 1 or x == 2:
                marbs+= fullboard[x]*0.90
            if x == 0:
                marbs+= fullboard[x]*0.7
                
    else:
        for x in range(7,13):
            if x == 12 or x == 11:
                marbs+= fullboard[x]*1
            if x == 9 or x == 10 or x == 8:
                marbs+= fullboard[x]*0.9
            if x == 7:
                marbs+= fullboard[x]*0.7
    return int(marbs+0.5)

def stealPotential(fullboard,human):
    captured = 0
    if human:
        for x in range(0,6):
            drop = (fullboard[x] + x) % 13
            if drop < 6 and fullboard[drop] == 0 and fullboard[x] != 0:
                    if fullboard[(12 - drop)] > captured:
                        captured = fullboard[(12 - drop)]
    else:
        for x in range(7,13):
            drop = (fullboard[x] + x) % 14
            if fullboard[x] + x > 19:
                drop += 1
            if drop < 6 and drop > 13 and fullboard[drop] == 0 and fullboard[x] != 0:
                    if fullboard[(12 - drop)] > captured:
                        captured = fullboard[(12 - drop)]
        captured = captured * -1
    return captured

def valueOf(fullboard,state,depth,human):
    steal = stealPotential(fullboard.copy(),human)

    if fullboard[6] > 24 or (sum(fullboard[:7]) > sum(fullboard[7:]) and state):
        return 1000 + depth
    elif fullboard[13] > 24 or (sum(fullboard[:7]) < sum(fullboard[7:]) and state):
        return -1000 - depth
    else:
        return fullboard[6]*4 - fullboard[13]*4 + sumofSide(fullboard.copy(),True) - sumofSide(fullboard.copy(),False) + steal*0.8

def makeFullBoard(pboard, eboard, pscore, escore):
    fullboard = pboard + [pscore]
    fullboard = fullboard + eboard
    fullboard = fullboard + [escore]
    return fullboard

def minmax(fullboard,depth,isMaximizingPlayer,alpha,beta,mv):
    state = gameOver(fullboard.copy())
    if state == True or depth == 0:
        score = [-1,-1]
        score[0] = valueOf(fullboard.copy(),state,depth,isMaximizingPlayer)
        score[1] = mv
        return score
    
    if isMaximizingPlayer:
        moves = computeMoves(fullboard.copy(),True)
        bestVal = [-INFINITY,-1]
        for x in moves:
            fb = updateBoard(fullboard.copy(),x,True)
            if doubleTurn(fullboard.copy(),True,x):
                value = minmax(fb.copy(),depth-1,True,alpha,beta,x)
            else:
                value = minmax(fb.copy(),depth-1,False,alpha,beta,x)
            if value[0] > bestVal[0]:
                bestVal = [value[0],x]
            alpha = max(alpha,bestVal[0])
            if beta <= alpha:
                break
        return bestVal
    else:
        bestVal = [+INFINITY,-1]
        moves = computeMoves(fullboard.copy(),False)
        for x in moves:
            fb = updateBoard(fullboard.copy(),x,False)
            if doubleTurn(fullboard.copy(),False,x):
                value = minmax(fb.copy(),depth-1,False,alpha,beta,x)
            else:
                value = minmax(fb.copy(),depth-1,True,alpha,beta,x)
            if value[0] < bestVal[0]:
                bestVal = [value[0],x]
            beta = min(beta,bestVal[0])
            if beta <= alpha:
                break
        return bestVal 

def doubleTurn(fullboard,human,move):
    if human:
        return (fullboard[move]+move)%13 == 6
    else:
        if fullboard[move] + move > 19:
            return ((fullboard[move]+move)%14) + 1== 13
        return (fullboard[move]+move)%14 == 13


def updateBoard(fullboard, move,human):
    marbles = fullboard[move]
    temp = marbles
    fullboard[move] = 0
    dest = 1
    
    if human:
        drop = (marbles + move)%13
        while marbles > 0:
            if (move+dest)%14 == 13:
                dest += 1
            fullboard[(move+dest)%14] +=1
            marbles -= 1
            dest += 1
    else:
        drop = (marbles + move)%14
        while marbles > 0:
            if (move+dest)%14 == 6:
                dest += 1
            fullboard[(move+dest)%14] += 1
            marbles -=1
            dest += 1
    #if stealing
    if temp + move >= 19 and not human:
        drop += 1
    if human and drop <= 5 and fullboard[drop] == 1:
        fullboard[drop] += fullboard[12-drop]
        fullboard[12-drop] = 0
    elif not human and drop >= 7 and drop < 13 and fullboard[drop] == 1:
        fullboard[drop] += fullboard[12-drop]
        fullboard[12-drop] = 0

    return fullboard

def gameOver(fullboard):
    if sum(fullboard[:6]) == 0 or sum(fullboard[7:13]) == 0:
        return True
    else:
        return False

def main():
    player = int(input())
    mancala1 = int(input())
    player1marbles = [int(i) for i in input().strip().split()]
    mancala2 = int(input())
    player2marbles = [int(i) for i in input().strip().split()]
    print(printNextMove(player, mancala1, player1marbles, mancala2, player2marbles))

main()
