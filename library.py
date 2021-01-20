# coding=UTF-8

def spirale(x,y,lgInit,deltaLg,lgFin):
    sens = 1
    lg=lgInit
    while lg > lgFin:
        if sens == 1:
            newx = x + lg
            newy = y
        elif sens == 2:
            newy = y + lg
            newx = x
        elif sens == 3:
            newx = x - lg
            newy = y
        elif sens == 4:
            newy = y - lg
            newx = x
            
        line(x, y, newx, newy)
        
        sens += 1
        if sens > 4:
            sens -= 4
        lg -= deltaLg
        x = newx
        y = newy

def cercle(x, y, r):
    ellipse(x, y, 2*r, 2*r)

def carre(x, y, c):
    rect(x, y, c, c)

def carres_emboites(x,y,lgFin,nbCarres):
    for i in range(l, nbCarres +1):
        carre(x - (lgFin*(nbCarres + 1 - i)/(nbCarres*2)), y - (lgFin*(nbCarres + 1 - 4)/(nbCarres*2)), (lgFin*(nbCarres + 1 - i)/nbCarres))
        
def pointillisme(rMin, rMax, c, xMax, yMax):
    L=[]
    n = 0
    while n == 0:
        x = random(0,xMax)
        y = random(0, yMax)
        r = random(rMin, rMax)
        is_poss = 1
        for element in L:
            if sqrt((element[1] - y)**2 + (element[0] - x)**2) <= ((r + element[2])*c):
                is_poss -= 1
        if is_poss == 1:
            cercle(x, y, r, random(0, 255), random(0, 255), random(0, 255))
            L.append([x, y, r])

def pixel_ligne(posX=0, posY=0, angle=0, long=100):
    angle *= PI/180
    for loop in range (long):
        point(posX, posY)
        posX += cos(angle)
        posY -= sin(angle)

def pixel_carre(posX=0, posY=0, long=100):
    for i in range(4):
        pixel_ligne(posX, posY, -i*90, long)
        posX += long*(cos(i*(PI/2)))
        posY += long*(sin(i*(PI/2)))
        
def barres(sens=1, posIX=0, posIY=0, posFX=1000, posFY=1000, lgBarres=100):
    longAct = lgBarres*2
    nb = 0
    if sens == 1:
        while longAct <= posFX - posIX:
            rect(posIX + nb*lgBarres*2, posIY, lgBarres, posFY - posIY)
            longAct += lgBarres*2
            nb += 1
        if posFX - posIX > longAct - lgBarres:
            rect(posIX + nb*lgBarres*2, posIY, (posFX - posIX)-(longAct - lgBarres), posFY - posIY)
    else:
        while longAct <= posFY - posIY:
            rect(posIX, posIY + nb*lgBarres*2, posFX - posIX, lgBarres)
            longAct += lgBarres*2
            nb += 1
        if posFY - posIY > longAct - lgBarres:
            rect(posIX, posIY + nb*lgBarres*2, posFX - posIX,  (posFY - posIY)-(longAct - lgBarres))
            
def rgb(hex):
    hex = list(hex)
    if hex[0] == "#":
        hex.pop(0)
    hex = "".join(hex)
    return [int(hex[0:2], 16), int(hex[2:4], 16), int(hex[4:6], 16)]

def fill_hex(hex, alpha=255):
    hex = list(hex)
    if hex[0] == "#":
        hex.pop(0)
    hex = "".join(hex)
    fill(int(hex[0:2], 16), int(hex[2:4], 16), int(hex[4:6], 16), alpha)
    
def stroke_hex(hex, alpha=255):
    hex = list(hex)
    if hex[0] == "#":
        hex.pop(0)
    hex = "".join(hex)
    stroke(int(hex[0:2], 16), int(hex[2:4], 16), int(hex[4:6], 16), alpha)
    
class input:
    def __init__(self, textebase="", taille=32, type="str", domainMin="None", domainMax="None"):
        # textebase : le texte de base du champ. L'équivalent de l'argument de input().
        # taille : la taille du texte, définie par l'instruction textSize de processing.py
        # type : le type de l'input attendu. Peut contenir : str, float, int. Par défaut, str est choisi. Attention, la variable self.texte sera toujours contenue sous forme de str.
        # domainMin : dans le cas d'un int ou float, définit le minimum requit. accept "Null" si aucun minimum n'est requis. La variable self.valid (bool) indique si le domaine est respecté.
        #             dans le cas d'un str, définit la len minimum requit.
        # domainMax : dans le cas d'un int ou float, définit le maximum requit. accept "Null" si aucun maximum n'est requis. La variable self.valid (bool) indique si le domaine est respecté.
        #             dans le cas d'un str, définit la len minimum requit.
        
        self.taille = taille
        self.texte = textebase
        self.textebase = textebase
        self.selected = False
        self.type = type
        self.domainMin = domainMin
        self.domainMax = domainMax
        self.valid = True
        
    def affiche(self, x, y, lgX, lgY):
        self.x = x
        self.y = y
        self.lgX = lgX
        self.lgY = lgY
        stroke(0)
        fill(0, 0)
        rect(self.x, self.y, self.lgX, self.lgY)
        if self.selected:
            stroke(0, 0)
            fill_hex("FFD800", 100)
            rect(self.x, self.y, self.lgX, self.lgY)
        elif not self.valid:
            stroke(0, 0)
            fill_hex("FF0000", 100)
            rect(self.x, self.y, self.lgX, self.lgY)
        fill(0)
        textSize(self.taille)
        text(self.texte, self.x, self.y, self.lgX, self.lgY)
        
    def clicked_test(self):
        if self.x<=mouseX<=self.x+self.lgX and self.y<=mouseY<=self.y+self.lgY:
            self.selected = True
        else:
            self.selected = False
            
    def is_valid(self):
        if self.type == "int":
            try:
                if self.domainMin != "None" and int(self.texte) < int(self.domainMin):
                    self.validMin = False
                else:
                    self.validMin = True
            except :
                self.validMin = False
            try:
                if self.domainMax != "None" and int(self.texte) > int(self.domainMax):
                    self.validMax = False
                else:
                    self.validMax = True
            except:
                self.validMax = False
            if self.validMin and self.validMax:
                self.valid = True
            else:
                self.valid = False
        elif self.type == "float":
            try:
                if self.domainMin != "None" and float(self.texte) < float(self.domainMin):
                    self.validMin = False
                else:
                    self.validMin = True
            except :
                self.validMin = False
            try:
                if self.domainMax != "None" and float(self.texte) > float(self.domainMax):
                    self.validMax = False
                else:
                    self.validMax = True
            except:
                self.validMax = False
            if self.validMin and self.validMax:
                self.valid = True
            else:
                self.valid = False
                
        elif self.type == "str":
            try:
                if self.domainMin != "None" and len(self.texte) < int(self.domainMin):
                    self.validMin = False
                else:
                    self.validMin = True
            except :
                self.validMin = False
            try:
                if self.domainMax != "None" and len(self.texte) > int(self.domainMax):
                    self.validMax = False
                else:
                    self.validMax = True
            except:
                self.validMax = False
            if self.validMin and self.validMax:
                self.valid = True
            else:
                self.valid = False
    
    def text_add(self):
        if self.selected:
            if key == BACKSPACE or key == DELETE:
                    self.texte = self.texte[:len(self.texte)-1]
            elif not key == ENTER:
                if self.type == "int":
                    if (key == "1" or key == "2" or key == "3" or key == "4" or key == "5" or key == "6" or key == "7" or key == "8" or key == "9" or key == "0") or (self.texte == "" and key == "-"):
                        self.texte += key
                elif self.type == "float":
                    if (key == "1" or key == "2" or key == "3" or key == "4" or key == "5" or key == "6" or key == "7" or key == "8" or key == "9" or key == "0") or (self.texte == "" and key == "-") or (not "." in self.texte and key == "."):
                        self.texte += key
                else:
                    self.texte += key
            self.is_valid()
            
    def restore_text(self):
        self.texte = self.textebase
        self.valid = True

class button:
    def __init__(self, imgAdress, imgOnOverAdress="Null", imgOnPressAdress="Null", AntiFalseOvering="Null"):
        self.img = loadImage(imgAdress)
        if not imgOnOverAdress == "Null":
            self.imgOnOver = loadImage(imgOnOverAdress)
        else:
            self.imgOnOver = "Null"
        if not imgOnPressAdress == "Null":
            self.imgOnPress = loadImage(imgOnPressAdress)
        else:
            self.imgOnPress = "Null"
        self.AntiFalseOvering = AntiFalseOvering
        self.IsOut = False
    def affiche(self, x, y, lgX, lgY):
        self.x = x
        self.y = y
        self.lgX = lgX
        self.lgY = lgY
        if self.imgOnPress != "Null" and self.on_button() and mousePressed:
            image(self.imgOnPress, self.x, self.y, self.lgX, self.lgY)
        elif self.imgOnOver != "Null" and self.on_button():
            image(self.imgOnOver, self.x, self.y, self.lgX, self.lgY)
        else:
            image(self.img, self.x, self.y, self.lgX, self.lgY)
    def on_button(self):
        self.diffX = mouseX - pmouseX
        self.diffY = mouseY - pmouseY
        if self.diffX != 0:
            self.IsOut = False
        if self.AntiFalseOvering == "Predictive":
            if mouseX + self.diffX <= 0 or mouseY + self.diffY <= 0 or mouseX + self.diffX >= width-1 or mouseY + self.diffY >= height-1 or self.IsOut:
                self.IsOut = True
                return False
            elif self.x<=mouseX<=self.x+self.lgX and self.y<=mouseY<=self.y+self.lgY and not self.IsOut:
                return True
            else:
                return False
        elif self.AntiFalseOvering == "Classic":
            if mouseX + self.diffX == 0 or mouseY + self.diffY == 0 or mouseX + self.diffX == width-1 or mouseY + self.diffY == height-1:
                return False
            elif self.x<=mouseX<=self.x+self.lgX and self.y<=mouseY<=self.y+self.lgY:
                return True
            else:
                return False
        else:
            if self.x<=mouseX<=self.x+self.lgX and self.y<=mouseY<=self.y+self.lgY:
                return True

class buttons_selection:
    def __init__(self):
        self.liste = []
        self.buttonSelected = "None"
    def add_button(self, nom, img, texte):
        self.liste.append([nom, img, texte])
    def affiche(self, x, y, lgX, lgY):
        fill(0, 0)
        stroke(0)
        rect(x, y, lgX, lgY)
        self.x = x
        self.y = y
        self.lgX = lgX
        self.lgY = lgY
        self.nb_element = len(self.liste)
        self.lgZone = lgY/self.nb_element
        self.lenmax = 0
        for element in self.liste:
            if len(element[2]) > self.lenmax:
                self.lenmax = len(element[2])
        self.i = 0
        for element in self.liste:
            img = loadImage(element[1])
            image(img, self.x, self.y+self.i*self.lgZone, self.lgZone, self.lgZone)
            if element[0] == self.buttonSelected:
                strokeWeight(4)
                stroke(0)
                noFill()
                rect(self.x, self.y+self.i*self.lgZone, self.lgZone, self.lgZone)
                strokeWeight(1)
            fill(0)
            self.texteSize = ((lgX-self.lgZone)/self.lenmax)*1.8
            if self.texteSize > self.lgZone:
                self.texteSize = self.lgZone
                self.to_adapt = False
            else:
                self.to_adapt = True
            textSize(self.texteSize)
            if self.to_adapt:
                text(element[2],  self.x + self.lgZone, self.y+self.i*self.lgZone + self.texteSize + (self.lgZone - self.texteSize)/2 - 10)
            else:
                text(element[2],  self.x + self.lgZone, self.y+self.i*self.lgZone + self.texteSize - 10)
            self.i += 1

    def selection_test(self):
        if self.x<=mouseX<=self.x+self.lgZone and self.y<=mouseY<=self.y+self.lgY:
            for i in range(self.nb_element):
                if i * self.lgZone + self.y < mouseY < (i + 1) * self.lgZone + self.y:
                    self.buttonSelected = self.liste[i][0]
