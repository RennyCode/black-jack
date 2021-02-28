from flask import Flask ,render_template, url_for,redirect, session
import random
app = Flask(__name__)
app.config['SECRET_KEY'] = 'myKey'   

def createDeck(values,symbols):
    newDeck = []
    for x in range (0,13):
        for y in range (0,4):
            newDeck.append(values[x] + symbols[y])       
    return newDeck

def charToInt(card):
    charValue = card[0]
    if ord(charValue) > 64:
            if charValue == 'A':
                return 11
            else: 
                return + 10
    else:   
        if charValue == '1':
            return 10
        else:
            return ord(charValue) - 48

def dealersTurn(score):
    if score < 16:
        flag = 1
    else:
        flag = 0      
    return flag

def AceCheck(indexs):
    print(indexs)
    l = len(indexs)
    if session['deck_key'][l-1][0] == 'A' :
        return 1
    return 0

def  checksplitScore(splitScore, who):
    if(splitScore == 1 and who == 0):
        session['splitScore_key']= 0
        return 0
    elif (splitScore == 1 and who == 1):
        session['splitScoreDealer_key'] = 0
        return 0
    else:
        return 1



@app.route('/')
def index():
    return render_template('home.html')

@app.route('/game')
def click():
    values = ['2','3','4','5','6','7','8','9','10','J','Q','K','A']
    symbols = ['D','C','H','S']
    deck = createDeck(values,symbols)
    random.shuffle(deck)
    playerScore = 0
    splitScore = 0
    splitScoreDealer = 0
    dealerScore = 0
    for x in range(2,4):
        if ord(deck[x][0]) > 64:
            if deck[x][0] == 'A':
                splitScore = playerScore
                splitScore = 1
                playerScore = playerScore +  11
            else: 
                playerScore = playerScore + 10            
        else:    
            if (deck[x][0]) == '1':
                 playerScore = playerScore + ord(deck[x][0]) + 9 - 48
            else:
                playerScore = playerScore + ord(deck[x][0]) - 48

    for x in range(0,2):
        if ord(deck[x][0]) > 64:
            if deck[x][0] == 'A':
                splitScoreDealer = 1
                dealerScore = dealerScore + 11
            else: 
                dealerScore = dealerScore + 10
        else: 
            if (deck[x][0]) == '1': 
                dealerScore = dealerScore + ord(deck[x][0]) + 9 - 48
            else:
                dealerScore = dealerScore + ord(deck[x][0]) - 48

    if splitScore == 22:
        splitScore = 12
    if dealerScore == 22:
        dealerScore = 12
   
    session['handIndex_key'] = 1
    session['doubleIndex_key'] = 0
    session['deckIndex_key'] = 4
    session['dealerIndex_key'] = [0,1]
    session['playerIndex_key'] = [2,3]
    session['deck_key'] = deck
    session['dealerScore_key'] = dealerScore
    session['playerScore_key'] = playerScore
    session['splitScore_key'] = splitScore
    session['splitScoreDealer_key'] = splitScoreDealer
    session['gameOver_key'] = 0 # 0 = in game, 1 = player lose, 2 = player win, 3 = tie
    return render_template('game_page.html',deck =  session['deck_key'], playerScore = session['playerScore_key'], dealerScore = session['dealerScore_key'], splitScore = session['splitScore_key'], playerIndex_key = session['playerIndex_key'] ,dealerIndex_key = session['dealerIndex_key'], gameOver = session['gameOver_key'] ,doubleIndex =  session['doubleIndex_key'], handIndex = session['handIndex_key'])

@app.route('/hitMe')
def draw():
    session['playerIndex_key'].append(session['deckIndex_key'])
    session['playerScore_key'] =  session['playerScore_key'] +  charToInt(session['deck_key'][session['deckIndex_key']])
    session['deckIndex_key'] = session['deckIndex_key'] + 1
    print(session['playerScore_key'])
    if session['playerScore_key'] > 21:
        if AceCheck(session['playerIndex_key']) == 0:
            if  checksplitScore(session['splitScoreDealer_key'],1):
                    session['gameOver_key'] = 1
                    return render_template('game_page.html',deck =  session['deck_key'], playerScore = session['playerScore_key'], dealerScore = session['dealerScore_key'], splitScore = session['splitScore_key'], playerIndex_key = session['playerIndex_key'] ,dealerIndex_key = session['dealerIndex_key'], gameOver = session['gameOver_key'], doubleIndex =  session['doubleIndex_key'], handIndex = session['handIndex_key'])
      
            else:
                session['playerScore_key'] = session['playerScore_key'] - 10
        else:
            session['playerScore_key'] = session['playerScore_key'] - 10
  
    if dealersTurn(session['dealerScore_key']) :   
       session['dealerIndex_key'].append(session['deckIndex_key'])
       session['dealerScore_key'] =  session['dealerScore_key'] +  charToInt(session['deck_key'][session['deckIndex_key']])
       session['deckIndex_key'] = session['deckIndex_key'] + 1

    if session['dealerScore_key']  > 21:
            if AceCheck(session['dealerIndex_key']) == 0:
                if  checksplitScore(session['splitScoreDealer_key'],1):
                    session['gameOver_key'] = 2 
                    return render_template('game_page.html',deck =  session['deck_key'], playerScore = session['playerScore_key'], dealerScore = session['dealerScore_key'], splitScore = session['splitScore_key'], playerIndex_key = session['playerIndex_key'] ,dealerIndex_key = session['dealerIndex_key'], gameOver = session['gameOver_key'], doubleIndex =  session['doubleIndex_key'], handIndex = session['handIndex_key'])
                else:
                    session['dealerScore_key'] = session['dealerScore_key'] - 10   
            else:
                session['dealerScore_key'] = session['dealerScore_key'] - 10   



    return render_template('game_page.html',deck =  session['deck_key'], playerScore = session['playerScore_key'], dealerScore = session['dealerScore_key'], splitScore = session['splitScore_key'], playerIndex_key = session['playerIndex_key'] ,dealerIndex_key = session['dealerIndex_key'], gameOver = session['gameOver_key'], doubleIndex =  session['doubleIndex_key'], handIndex = session['handIndex_key'])


@app.route('/stand')
def end():
    if session['playerScore_key'] < session['dealerScore_key']:
        session['gameOver_key'] = 1
        return render_template('game_page.html',deck =  session['deck_key'], playerScore = session['playerScore_key'], dealerScore = session['dealerScore_key'], splitScore = session['splitScore_key'], playerIndex_key = session['playerIndex_key'] ,dealerIndex_key = session['dealerIndex_key'], gameOver = session['gameOver_key'], doubleIndex =  session['doubleIndex_key'], handIndex = session['handIndex_key'])

    while dealersTurn(session['dealerScore_key']) :   
        session['dealerIndex_key'].append(session['deckIndex_key'])
        session['dealerScore_key'] =  session['dealerScore_key'] +  charToInt(session['deck_key'][session['deckIndex_key']])
        session['deckIndex_key'] = session['deckIndex_key'] + 1
        if session['dealerScore_key']  > 21:
            if AceCheck(session['dealerIndex_key']) == 0 :
                if  checksplitScore(session['splitScore_key'],0):
                    session['gameOver_key'] = 2 
                    return render_template('game_page.html',deck =  session['deck_key'], playerScore = session['playerScore_key'], dealerScore = session['dealerScore_key'], splitScore = session['splitScore_key'], playerIndex_key = session['playerIndex_key'] ,dealerIndex_key = session['dealerIndex_key'], gameOver = session['gameOver_key'], doubleIndex =  session['doubleIndex_key'], handIndex = session['handIndex_key'])
                else: 
                    session['dealerScore_key'] = session['dealerScore_key'] - 10

            else:
                session['dealerScore_key'] = session['dealerScore_key'] - 10


    if session['playerScore_key'] < session['dealerScore_key']:
        session['gameOver_key'] = 1
    elif session['playerScore_key'] > session['dealerScore_key']:
        session['gameOver_key'] = 2
    else:
        session['gameOver_key'] = 3
    
    return render_template('game_page.html',deck =  session['deck_key'], playerScore = session['playerScore_key'], dealerScore = session['dealerScore_key'], splitScore = session['splitScore_key'], playerIndex_key = session['playerIndex_key'] ,dealerIndex_key = session['dealerIndex_key'], gameOver = session['gameOver_key'], doubleIndex =  session['doubleIndex_key'], handIndex = session['handIndex_key'])
