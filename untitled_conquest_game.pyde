#TODO: village
#TODO: universitées
#TODO: vrais menus
#TODO: faire de vraies sprites pour la map
#TODO: chargement de map préremplies
#TODO: classe animation
#TODO: sons
#TODO: voir pk y'a un pb avec la taille adptative, psk c'est super chiant là

#TODO: configs de générations de map sauvegardables
#TODO: Bots
#TODO: fork avec case en hexagone
#TODO: compatibilitée réseau

################################################################################################################################################################################################## imports

from random import *
from library import *
from copy import *
from time import *

########################################################################################################################################################################################### size modifiers

global windowX
windowX = 1500
global windowY
windowY = 1000

def reSize(taille, sens="x"):
    if sens == "x":
        return int((width*taille)/windowX)
    else:
        return int((height*taille)/windowY)

############################################################################################################################################################################################### class mapp

class mapp:
    
    # -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- map generator
    def __init__(self, lg_map=10, nb_psg_gen=5, proba_continent=0.2, proba_mer=0.02, proba_mine=0.01):
        # liste des caractères utilisés :
            # "o" = terrain
            # "/" = eau
            # "x" = mine
            # "r" = joueur rouge
            # "b" = joueur bleu
            # "j" = joueur jaune
            # "g" = joueur gris
            # "t" = tour
            # "v" = village
        
        self.mapC = []
        self.lgMap = lg_map
        for i in range(self.lgMap):
            tempoliste = []
            for j in range(self.lgMap):
                tempoliste.append("/")
            self.mapC.append(tempoliste)
    
        for h in range(nb_psg_gen):
            for i in range(self.lgMap):
                for j in range(self.lgMap):
                    continentLevel = 0
                    if self.mapC[i][j] == "/":
                        if not i - 1 < 0:
                            if self.mapC[i - 1][j] == "o":
                                continentLevel += 1
                        if not i + 1 > self.lgMap - 1:
                            if self.mapC[i + 1][j] == "o":
                                continentLevel += 1
                        if not j - 1 < 0:
                            if self.mapC[i][j - 1] == "o":
                                continentLevel += 1
                        if not j + 1 > self.lgMap - 1:
                            if self.mapC[i][j + 1] == "o":
                                continentLevel += 1
                        if continentLevel >= 1:
                            if random() < proba_continent * continentLevel:
                                self.mapC[i][j] = "o"
                        else:
                            if random() < proba_mer:
                                self.mapC[i][j] = "o"
                    else:
                        if random() < proba_mine and not "x" in self.mapC[i][j]:
                            self.mapC[i][j] += "x"
        self.mapP = deepcopy(self.mapC)
        self.mapJ = deepcopy(self.mapP)
        self.winner = "None"
        self.nb_players_turns = 0
        self.proba_army_vs_empty_enemy_space = 0.8
        self.proba_army_vs_empty_neutral_space = 1
        self.proba_army_vs_fort_enemy_space = 0.4
        self.proba_boat_vs_empty_enemy_space = 0.6
        self.proba_boat_vs_empty_neutral_space = 0.8
        self.proba_boat_vs_fort_enemy_space = 0.2
    
    # -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- player placer
    def player_placer(self, nbJoueurs=2):
        self.mapP = deepcopy(self.mapC)
        self.nbJoueurs = nbJoueurs
        couleure = ["r", "b", "j", "g"]
        for i in range(nbJoueurs):
            placed = False
            while not placed:
                x = randint(0, len(self.mapP) - 1)
                y = randint(0, len(self.mapP) - 1)
                possibilty = False
                if "o" in self.mapP[x][y]:
                    possibility = True
                    if "r" in self.mapP[x][y] or "b" in self.mapP[x][y] or "j" in self.mapP[x][y] or "g" in self.mapP[x][y]:
                        possibility = False
                    if not x - 1 < 0:
                        if "r" in self.mapP[x - 1][y] or "b" in self.mapP[x - 1][y] or "j" in self.mapP[x - 1][y] or "g" in self.mapP[x - 1][y]:
                            possibility = False
                    if not x + 1 > self.lgMap - 1:
                        if "r" in self.mapP[x + 1][y] or "b" in self.mapP[x + 1][y] or "j" in self.mapP[x + 1][y] or "g" in self.mapP[x + 1][y]:
                            possibility = False
                    if not y - 1 < 0:
                        if "r" in self.mapP[x][y - 1] or "b" in self.mapP[x][y - 1] or "j" in self.mapP[x][y - 1] or "g" in self.mapP[x][y - 1]:
                            possibility = False
                    if not y + 1 > self.lgMap - 1:
                        if "r" in self.mapP[x][y + 1] or "b" in self.mapP[x][y+ 1] or "j" in self.mapP[x][y + 1] or "g" in self.mapP[x][y + 1]:
                            possibility = False
                    if not x - 1 < 0 and not x - 1 < 0:
                        if "r" in self.mapP[x - 1][y - 1] or "b" in self.mapP[x - 1][y - 1] or "j" in self.mapP[x - 1][y - 1] or "g" in self.mapP[x - 1][y - 1]:
                            possibility = False
                    if not x + 1 > self.lgMap - 1 and not y + 1 > self.lgMap - 1:
                        if "r" in self.mapP[x + 1][y + 1] or "b" in self.mapP[x + 1][y + 1] or "j" in self.mapP[x + 1][y + 1] or "g" in self.mapP[x + 1][y + 1]:
                            possibility = False
                    if not y - 1 < 0 and not x + 1 > self.lgMap - 1:
                        if "r" in self.mapP[x + 1][y - 1] or "b" in self.mapP[x + 1][y - 1] or "j" in self.mapP[x + 1][y - 1] or "g" in self.mapP[x + 1][y - 1]:
                            possibility = False
                    if not y + 1 > self.lgMap - 1 and not x - 1 < 0:
                        if "r" in self.mapP[x - 1][y + 1] or "b" in self.mapP[x - 1][y+ 1] or "j" in self.mapP[x - 1][y + 1] or "g" in self.mapP[x - 1][y + 1]:
                            possibility = False
                    if possibility:
                        self.mapP[x][y] += couleure[i]
                        placed = True
        self.mapJ = deepcopy(self.mapP)
        self.coinR = 3
        self.coinB = 3
        self.coinJ = 3
        self.coinG = 3
    
    # -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- map displayer
    def display(self, x = 0, y = 0, lg = 1000):
        self.x = x
        self.y = y
        self.lg = lg
        self.lgZone = int(self.lg/self.lgMap)
        mine = loadImage("images/sprites/mine.png")
        water = loadImage("images/sprites/water.png")
        tour = loadImage("images/sprites/tour.png")
        village = loadImage("images/sprites/village.png")
        fill(150)
        stroke(0)
        carre(x, y, lg)
        for i in range (self.lgMap):
            for j in range(self.lgMap):
                """if "/" in self.mapJ[i][j]:
                    stroke_hex("0094FF")
                    fill_hex("0094FF")"""
                stroke_hex("0094FF")
                fill_hex("0094FF")
                if "o" in self.mapJ[i][j]:
                    stroke_hex("00FF21")
                    fill_hex("007F0E")
                if "r" in self.mapJ[i][j]:
                    stroke_hex("FF0000")
                    fill_hex("7F0000")
                if "b" in self.mapJ[i][j]:
                    stroke_hex("0026FF")
                    fill_hex("00137F")
                if "j" in self.mapJ[i][j]:
                    stroke_hex("FFD800")
                    fill_hex("B29400")
                if "g" in self.mapJ[i][j]:
                    stroke_hex("808080")
                    fill_hex("404040")
                carre(x+i*self.lgZone, y+j*self.lgZone, self.lgZone)
                
                if "/" in self.mapJ[i][j]:
                    image(water, x+i*self.lgZone, y+j*self.lgZone, self.lgZone, self.lgZone)
                
                global action_selection
                if action_selection.buttonSelected == "army":
                    if self.army_possibility(player, [i, j]):
                        fill(255, 60)
                        carre(x+i*self.lgZone, y+j*self.lgZone, self.lgZone)
                elif action_selection.buttonSelected == "fort":
                    if self.fort_possibility(player, [i, j]):
                        fill(255, 60)
                        carre(x+i*self.lgZone, y+j*self.lgZone, self.lgZone)
                elif action_selection.buttonSelected == "boat":
                    if self.boat_possibility(player, [i, j]):
                        fill(255, 60)
                        carre(x+i*self.lgZone, y+j*self.lgZone, self.lgZone)
                    
                if "x" in self.mapJ[i][j]:
                    image(mine, x+i*self.lgZone+2, y+j*self.lgZone+2, self.lgZone/2.1, self.lgZone/2.1)
                if "t" in self.mapJ[i][j]:
                    image(tour, x+(i+1)*self.lgZone - self.lgZone/2.1, y+j*self.lgZone+2, self.lgZone/2.1, self.lgZone/2.1)
                if "v" in self.mapJ[i][j]:
                    image(village, x+(i+1)*self.lgZone - self.lgZone/2.1, y+j*self.lgZone+2, self.lgZone/2.1, self.lgZone/2.1)
                    
    # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ map reset
    def reset_map(self):
        self.mapJ = deepcopy(self.mapP)
    
    # ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- turn coin number
    def turn_coin_number(self, player):
        self.money_turn = 0
        for i in range(self.lgMap):
            for j in range(self.lgMap):
                if player in self.mapJ[i][j]:
                    self.money_turn += 1
                    if "x" in self.mapJ[i][j]:
                        self.money_turn+=1
        return self.money_turn
    
    # --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- get nb turns
    def get_nb_turns(self):
        self.nb_turns = 0
        actual_p_turns = self.nb_players_turns
        while actual_p_turns >= self.nbJoueurs:
            actual_p_turns -= self.nbJoueurs
            self.nb_turns += 1
        return self.nb_turns
    
    # --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- player coin number
    def player_coin_number(self, player):
        if player == "r":
            return self.coinR
        elif player == "b":
            return self.coinB
        elif player == "j":
            return self.coinJ
        elif player == "g":
            return self.coinG
    
    # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ add coins
    def player_coin_add(self, player, nbCoin):
        if player == "r":
            self.coinR += nbCoin
        elif player == "b":
            self.coinB += nbCoin
        elif player == "j":
            self.coinJ += nbCoin
        elif player == "g":
            self.coinG += nbCoin
    
    # ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- get zone clicked
    def get_zone_clicked(self):
        if self.x < mouseX < self.x + self.lg and self.y < mouseY < self.y + self.lg:
            self.ZoneClicked = [0, 0]
            for i in range(self.lgMap):
                if i * self.lgZone + self.x < mouseX < (i + 1) * self.lgZone + self.x:
                    self.ZoneClicked[0] = i
                if i * self.lgZone + self.y < mouseY < (i + 1) * self.lgZone + self.y:
                    self.ZoneClicked[1] = i
            return self.ZoneClicked
    
    # ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- get start players
    def get_start_players(self):
        liste_start_players = ["g", "j", "b", "r"]
        for i in range(- (self.nbJoueurs - 4)):
            liste_start_players.pop(0)
        return liste_start_players
    
    # ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- get alive players
    def get_alive_players(self):
        liste = []
        for y in range(len(self.mapJ)):
            for x in range (len(self.mapJ[y])):
                if "r" in self.mapJ[y][x] and not "r" in liste:
                    liste.append("r")
                elif "b" in self.mapJ[y][x] and not "b" in liste:
                    liste.append("b")
                elif "j" in self.mapJ[y][x] and not "j" in liste:
                    liste.append("j")
                elif "g" in self.mapJ[y][x] and not "g" in liste:
                    liste.append("g")
        return liste
                    
    # ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- get dead players
    def get_dead_players(self):
        alive = self.get_alive_players()
        liste_dead_players = self.get_start_players()
        for alive_player in alive:
            liste_dead_player.remove(alive_player)
        return liste_dead_players
    
    # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- test win
    def test_win(self):
        alive_players = self.get_alive_players()
        if len(alive_players) == 1:
            self.winner = alive_players[0]
            action_selection.buttonSelected = "None"
            global mode
            mode = "win"
    
    # ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- army attack possibility
    def army_possibility(self, player, pos):
        possibility = False
        if self.player_coin_number(player) >= 1:
            if "o" in self.mapJ[pos[0]][pos[1]]:
                if not pos[0] - 1 < 0:
                    if player in self.mapJ[pos[0] - 1][pos[1]]:
                        possibility = True
                if not pos[0] + 1 > self.lgMap - 1:
                    if player in self.mapJ[pos[0] + 1][pos[1]]:
                        possibility = True
                if not pos[1] - 1 < 0:
                    if player in self.mapJ[pos[0]][pos[1] - 1]:
                        possibility = True
                if not pos[1] + 1 > self.lgMap - 1:
                    if player in self.mapJ[pos[0]][pos[1] + 1]:
                        possibility = True
                if player in self.mapJ[pos[0]][pos[1]]:
                    possibility = False
        return possibility
    
    # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ use army attack
    def army(self, player):
        if self.x < mouseX < self.x + self.lg and self.y < mouseY < self.y + self.lg:
            pos = self.get_zone_clicked()
            if self.army_possibility(player, pos):
                if  "t" in self.mapJ[pos[0]][pos[1]]:
                    proba = self.proba_army_vs_fort_enemy_space
                elif "r" in self.mapJ[pos[0]][pos[1]] or "b" in self.mapJ[pos[0]][pos[1]] or "j" in self.mapJ[pos[0]][pos[1]] or "g" in self.mapJ[pos[0]][pos[1]]:
                    proba = self.proba_army_vs_empty_enemy_space
                else:
                    proba = self.proba_army_vs_empty_neutral_space
                if random() <= proba:
                    case = list(self.mapJ[pos[0]][pos[1]])
                    if "r" in case:
                        case.remove("r")
                    elif "b" in case:
                        case.remove("b")
                    elif "j" in case:
                        case.remove("j")
                    elif "g" in case:
                        case.remove("g")
                    if "t" in case:
                        case.remove("t")
                    case.append(player)
                    self.mapJ[pos[0]][pos[1]] = "".join(case)
                
                self.player_coin_add(player, -1)
            self.test_win()
    
    # ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- fort possibility
    def fort_possibility(self, player, pos):
        if self.player_coin_number(player) >= 3:
            if player in self.mapJ[pos[0]][pos[1]] and not "t" in self.mapJ[pos[0]][pos[1]]:
                return True
            else:
                return False
        else:
            return False
        
    # ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- place fort
    def fort(self, player):
        if self.x < mouseX < self.x + self.lg and self.y < mouseY < self.y + self.lg:
            pos = self.get_zone_clicked()
            if self.fort_possibility(player, pos):
                pos = self.get_zone_clicked()
                case = list(self.mapJ[pos[0]][pos[1]])
                if "v" in case:
                    case.remove("v")
                case += "t"
                self.mapJ[pos[0]][pos[1]] = "".join(case)
                self.player_coin_add(player, -3)

    # -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- village possibility
    def village_possibility(self, player, pos):
        if self.player_coin_number(player) >= 3:
            if player in self.mapJ[pos[0]][pos[1]] and not "v" in self.mapJ[pos[0]][pos[1]]:
                return True
            else:
                return False
        else:
            return False
        
    # -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- place village
    def village(self, player):
        if self.x < mouseX < self.x + self.lg and self.y < mouseY < self.y + self.lg:
            pos = self.get_zone_clicked()
            if self.village_possibility(player, pos):
                pos = self.get_zone_clicked()
                case = list(self.mapJ[pos[0]][pos[1]])
                if "t" in case:
                    case.remove("t")
                case += "v"
                self.mapJ[pos[0]][pos[1]] = "".join(case)
                self.player_coin_add(player, -2)
    
    # ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- boat possibility
    def boat_possibility(self, player, pos):
        possibility1 = False
        for i in range(self.lgMap):
            for j in range(self.lgMap):
                if player in self.mapJ[i][j]:
                    if not i - 1 < 0:
                        if "/" in self.mapJ[i - 1][j]:
                            possibility1 = True
                    if not i + 1 > self.lgMap - 1:
                        if  "/" in self.mapJ[i + 1][j]:
                            possibility1 = True
                    if not j - 1 < 0:
                        if  "/" in self.mapJ[i][j - 1]:
                            possibility1 = True
                    if not j + 1 > self.lgMap - 1:
                        if  "/" in self.mapJ[i][j + 1]:
                            possibility1 = True
        possibility2 = False
        if self.player_coin_number(player) >= 4:
            if "o" in self.mapJ[pos[0]][pos[1]]:
                if not pos[0] - 1 < 0:
                    if "/" in self.mapJ[pos[0] - 1][pos[1]]:
                        possibility2 = True
                if not pos[0] + 1 > self.lgMap - 1:
                    if  "/" in self.mapJ[pos[0] + 1][pos[1]]:
                        possibility2 = True
                if not pos[1] - 1 < 0:
                    if  "/" in self.mapJ[pos[0]][pos[1] - 1]:
                        possibility2 = True
                if not pos[1] + 1 > self.lgMap - 1:
                    if  "/" in self.mapJ[pos[0]][pos[1] + 1]:
                        possibility2 = True
                if player in self.mapJ[pos[0]][pos[1]]:
                        possibility2 = False
        if possibility1 and possibility2:
            return True
        else:
            return False
        
    # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ use boat attack
    def boat(self, player):
        if self.x < mouseX < self.x + self.lg and self.y < mouseY < self.y + self.lg:
            pos = self.get_zone_clicked()
            if self.boat_possibility(player, pos):
                if "t" in self.mapJ[pos[0]][pos[1]]:
                    proba = self.proba_boat_vs_fort_enemy_space
                elif "r" in self.mapJ[pos[0]][pos[1]] or "b" in self.mapJ[pos[0]][pos[1]] or "j" in self.mapJ[pos[0]][pos[1]] or "g" in self.mapJ[pos[0]][pos[1]]:
                    proba = self.proba_boat_vs_empty_enemy_space
                else:
                    proba = self.proba_boat_vs_empty_neutral_space
                if random() <= proba:
                    case = list(self.mapJ[pos[0]][pos[1]])
                    if "r" in case:
                        case.remove("r")
                    elif "b" in case:
                        case.remove("b")
                    elif "j" in case:
                        case.remove("j")
                    elif "g" in case:
                        case.remove("g")
                    if "t" in case:
                        case.remove("t")
                    case.append(player)
                    self.mapJ[pos[0]][pos[1]] = "".join(case)
                
                self.player_coin_add(player, -4)
            self.test_win()

#################################################################################################################################################################################################### setup

def setup():
    global mode
    mode = "menu"
    # size(int((displayWidth*windowX)/1920), int((displayHeight*windowY)/1080))
    size(1500, 1000)
    background(240)
    global game_map
    game_map = mapp()
    game_map.player_placer()
    
    # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ Mode play
    global player
    player = "r"
    global action_selection
    action_selection = buttons_selection()
    action_selection.add_button("fort", "images/sprites/tour.png", u"Fort : 3")
    action_selection.add_button("army", "images/sprites/army.png", u"Armée : 1")
    action_selection.add_button("boat", "images/sprites/boat.png", u"Bateau : 4")
    global end_turn_button
    end_turn_button = button("images/boutons/end_turn_button.png")
    global menu_button
    menu_button = button("images/boutons/menu_button.png")
    
    # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ Mode menu
    global play_button
    play_button = button("images/boutons/play_button.png")
    global exit_button
    exit_button = button("images/boutons/exit_button.png")
    global logo
    logo = loadImage("images/logo.png")
    
    # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ Mode generation
    global regen_button
    regen_button = button("images/boutons/regen_button.png")
    global placer_button
    placer_button = button("images/boutons/placer_button.png")
    global nb_joueurs_input
    nb_joueurs_input = input("2", 35, "int", 1, 4)
    global avance_button
    avance_button = button("images/boutons/avance_button.png")
    global retour_button
    retour_button = button("images/boutons/retour_button.png")
    
    # ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- Mode avancé
    global lg_map_input
    lg_map_input = input("10", 35, "int", 5, 50)
    global nb_psg_gen_input
    nb_psg_gen_input = input("5", 35, "int", 1, 50)
    global proba_continent_input
    proba_continent_input = input("0.2", 35, "float", 0, 1)
    global proba_mer_input
    proba_mer_input = input("0.02", 35, "float", 0, 1)
    global proba_mine_input
    proba_mine_input = input("0.01", 35, "float", 0, 1)
    global reset_button
    reset_button = button("images/boutons/reset_button.png")
    
##################################################################################################################################################################################################### draw

def draw():
    background(240)
    
    # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ Mode menu
    if mode == "menu":
        play_button.affiche(reSize(0), reSize(500, ""), reSize(500), reSize(169,""))
        exit_button.affiche(reSize(0), reSize(700, ""), reSize(500), reSize(169, ""))
        image(logo, reSize(0), reSize(0, ""), reSize(500), reSize(500, ""))
        
    # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ Mode generation
    elif mode == "gen":
        game_map.display(reSize(500), reSize(0, ""))
        placer_button.affiche(reSize(0), reSize(0, ""), reSize(500), reSize(169, ""))
        regen_button.affiche(reSize(0), reSize(169, ""), reSize(500), reSize(169, ""))
        fill(0)
        text(u"Nombre de joueurs", reSize(25), reSize(405, ""))
        nb_joueurs_input.affiche(reSize(370), reSize(370, ""), reSize(80), reSize(50, ""))
        avance_button.affiche(reSize(0), reSize(450, ""), reSize(500), reSize(169, ""))
        play_button.affiche(reSize(0),  reSize(619, ""), reSize(500), reSize(169, ""))
        retour_button.affiche(reSize(0), reSize(788, ""), reSize(500), reSize(169, ""))
    
    # ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- Mode avancé
    elif mode == "avance":
        game_map.display(reSize(500), reSize(0, ""))
        fill(0)
        textSize(26)
        text(u"Taille de la map", reSize(5), reSize(50, ""))
        text(u"Nb de passages de\ngénération", reSize(5), reSize(130, ""))
        text(u"Probabililité d'apparition\nsi continent", reSize(5), reSize(230, ""))
        text(u"Probabililité d'apparition\nsi mer", reSize(5), reSize(330, ""))
        text(u"Probabililité d'apparition\ndes mines",  reSize(5), reSize(430, ""))
        lg_map_input.affiche(reSize(330), reSize(10, ""), reSize(150), reSize(60, ""))
        nb_psg_gen_input.affiche(reSize(330), reSize(110, ""), reSize(150), reSize(60, ""))
        proba_continent_input.affiche(reSize(330), reSize(210, ""), reSize(150), reSize(60, ""))
        proba_mer_input.affiche(reSize(330), reSize(310, ""), reSize(150), reSize(60, ""))
        proba_mine_input.affiche(reSize(330), reSize(410, ""), reSize(150), reSize(60, ""))
        reset_button.affiche(reSize(0), reSize(510, ""), reSize(500), reSize(169, ""))
        retour_button.affiche(reSize(0), reSize(679, ""), reSize(500), reSize(169, ""))
    
    # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ Mode play
    elif mode =="play":
        game_map.display(reSize(500), reSize(0, ""))
        fill(0)
        textSize(50)
        liste_joueurs = {"r":u"rouge", "b":u"bleu", "j":u"jaune", "g":u"gris"}
        text(u"Joueur " + liste_joueurs[player], reSize(100), reSize(60, ""))
        action_selection.affiche(reSize(0), reSize(200, ""), reSize(500), reSize(200, ""))
        fill(0)
        textSize(40)
        text(u"nombre de pièces : " + str(game_map.player_coin_number(player)), reSize(10), reSize(150, ""))
        end_turn_button.affiche(reSize(0), reSize(400, ""), reSize(500), reSize(169, ""))
        menu_button.affiche(reSize(0), reSize(800, ""), reSize(500), reSize(169, ""))
    
    # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- Mode win
    elif mode == "win":
        image(logo, reSize(0), reSize(0, ""), reSize(500), reSize(500, ""))
        fill(0)
        textSize(50)
        liste_joueurs = {"r":u"rouge", "b":u"bleu", "j":u"jaune", "g":u"gris"}
        text(u"Le joueur " + liste_joueurs[game_map.winner] + u"\n a gagné !", reSize(10), reSize(500, ""))
        menu_button.affiche(reSize(0), reSize(800, ""), reSize(500), reSize(169, ""))
        

############################################################################################################################################################################################ Mouse clicked

def mouseClicked():
    global mode
    # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ Mode menu
    if mode == "menu":
        if play_button.on_button():
            mode = "gen"
        elif exit_button.on_button():
            exit()
    
    # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ Mode generation
    elif mode == "gen":
        global game_map
        nb_joueurs_input.clicked_test()
        if regen_button.on_button():
            game_map = mapp(int(lg_map_input.texte), int(nb_psg_gen_input.texte), float(proba_continent_input.texte), float(proba_mer_input.texte), float(proba_mine_input.texte))
            if not nb_joueurs_input.valid:
                nb_joueurs_input.restore_text()
            game_map.player_placer(int(nb_joueurs_input.texte))
        elif placer_button.on_button():
            if not nb_joueurs_input.valid:
                nb_joueurs_input.restore_text()
            game_map.player_placer(int(nb_joueurs_input.texte))
        elif avance_button.on_button():
            mode = "avance"
        elif play_button.on_button():
            mode = "play"
        elif retour_button.on_button():
            mode = "menu"
    
    # ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- Mode avancé
    elif mode == "avance":
        lg_map_input.clicked_test()
        nb_psg_gen_input.clicked_test()
        proba_continent_input.clicked_test()
        proba_mer_input.clicked_test()
        proba_mine_input.clicked_test()
        if reset_button.on_button():
            lg_map_input.restore_text()
            nb_psg_gen_input.restore_text()
            proba_continent_input.restore_text()
            proba_mer_input.restore_text()
            proba_mine_input.restore_text()
        if retour_button.on_button():
            mode = "gen"
            if not lg_map_input.valid:
                lg_map_input.restore_text()
            if not nb_psg_gen_input.valid:
                nb_psg_gen_input.restore_text()
            if not proba_continent_input.valid:
                proba_continent_input.restore_text()
            if not proba_mer_input.valid:
                proba_mer_input.restore_text()
            if not proba_mine_input.valid:
                proba_mine_input.restore_text()
    
    # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ Mode play
    elif mode == "play":
        global player
        action_selection.selection_test()
        if action_selection.buttonSelected == "army":
            game_map.army(player)
        elif action_selection.buttonSelected == "fort":
            game_map.fort(player)
        elif action_selection.buttonSelected == "boat":
            game_map.boat(player)
        if end_turn_button.on_button():
            liste = game_map.get_alive_players()
            player = liste[liste.index(player) - 1]
            action_selection.buttonSelected = "None"
            game_map.nb_players_turns += 1
            if game_map.get_nb_turns() != 0:
                game_map.player_coin_add(player, game_map.turn_coin_number(player))
        if menu_button.on_button():
            game_map.reset_map()
            game_map.coinR = 5
            game_map.coinB = 4
            game_map.coinJ = 4
            game_map.coinG = 4
            action_selection.buttonSelected = "None"
            mode = "menu"
    
    # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- Mode win
    elif mode== "win":
        if menu_button.on_button():
            game_map.reset_map()
            game_map.coinR = 5
            game_map.coinB = 4
            game_map.coinJ = 4
            game_map.coinG = 4
            action_selection.buttonSelected = "None"
            mode = "menu"
            game_map.winner = "None"
            
    
################################################################################################################################################################################################ Key typed

def keyTyped():
    
    # ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ Mode generation
    if mode == "gen":
        nb_joueurs_input.text_add()
        
    # ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- Mode avancé
    elif mode == "avance":
        # lg_map, nb_psg_gen, proba_continent, proba_mer, proba_mine
        lg_map_input.text_add()
        nb_psg_gen_input.text_add()
        proba_continent_input.text_add()
        proba_mer_input.text_add()
        proba_mine_input.text_add()
