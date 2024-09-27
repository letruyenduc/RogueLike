import pyxel

class Game:
    def __init__(self):
        self.fenetre_x = 256
        self.fenetre_y = 256
        pyxel.init(self.fenetre_x, self.fenetre_y, title="Rogue like")
        self.x_perso = 60 #Zone d'apparition du personnage
        self.y_perso = 60 #Zone d'apparition du personnage
        self.dimension_perso_x = 16 # Dimension du personnage
        self.dimension_perso_y = 16 # Dimension du personnage
        self.max_hp = 100 # HP Max
        self.hp = 100 # HP de base du personnage
        self.max_mp = 100 # MP Max
        self.mp = 100 # MP de base du personnage
        self.toggle = False # Levier pour pour on/off Inventaire
        self.hitbox = [self.x_perso, self.y_perso, self.x_perso + self.dimension_perso_x, self.y_perso + self.dimension_perso_y] # Hitbox du personnage avec [x1,y2,x2,y2]
        self.dmg_zones = {1: [[80, 80], [100, 100]], 2: [[120, 120], [140,140]]} # Dictionnaire de liste pour les zones de dégâts
        self.dmg_cd = 60 #Temps avant de pouvoir reprendre des dégâts, Soit invincibilité
        self.switch_d = False
        self.potions = []
        self.init_inventory(3)
        self.loaded = False
        self.main_click = False
        self.loading_time = 100
        self.loading_bar = 0
        self.monster_x = 120
        self.monster_y = 120
        self.monster_hp = 50
        self.monster_hitbox = [self.monster_x, self.monster_y, self.monster_x + 16, self.monster_y + 16]
# LES OBJETS : 
    def zones_de_degats(self):
        #Fait apparaitre graphiquement les zones de dégâts
        for zone in self.dmg_zones.values():
            x1, y1 = zone[0]
            x2, y2 = zone[1]
            pyxel.rect(x1, y1, x2 - x1, y2 - y1, 2)
            pyxel.rectb(x1, y1, x2 - x1, y2 - y1, 8)
            
    def movement(self): 
        # les déplacements du personnage en diagonale
        if pyxel.btn(pyxel.KEY_Z) and pyxel.btn(pyxel.KEY_D) and (self.x_perso < self.fenetre_x - self.dimension_perso_x) and (self.y_perso > 32):
            self.x_perso += 2.8
            self.y_perso -= 2.8
        elif pyxel.btn(pyxel.KEY_S) and (self.y_perso < self.fenetre_y - self.dimension_perso_y) and pyxel.btn(pyxel.KEY_D) and (self.x_perso < self.fenetre_x - self.dimension_perso_x):
            self.x_perso += 2.8
            self.y_perso += 2.8
        elif pyxel.btn(pyxel.KEY_Q) and (self.x_perso > 0) and pyxel.btn(pyxel.KEY_S) and (self.y_perso < self.fenetre_y - self.dimension_perso_y):
            self.x_perso -= 2.8
            self.y_perso += 2.8
        elif pyxel.btn(pyxel.KEY_Q) and (self.x_perso > 0) and pyxel.btn(pyxel.KEY_Z) and (self.y_perso > 32):
            self.x_perso -= 2.8
            self.y_perso -= 2.8
        # Deplacement de base
        elif pyxel.btn(pyxel.KEY_D) and (self.x_perso < self.fenetre_x - self.dimension_perso_x):
            self.x_perso += 4
        elif pyxel.btn(pyxel.KEY_Q) and (self.x_perso > 0):
            self.x_perso -= 4
        elif pyxel.btn(pyxel.KEY_S) and (self.y_perso < self.fenetre_y - self.dimension_perso_y):
            self.y_perso += 4
        elif pyxel.btn(pyxel.KEY_Z) and (self.y_perso > 32):
            self.y_perso -= 4
            
    def personnage(self):
        #On commence une image par defaut
        pyxel.blt(self.x_perso, self.y_perso, 1, 0, 0, 15, 15) #Apparence du personnage
        # On va définir les différentes apparences du personnage en fonction de sa direction.
        #On commence par définir les apperences de droite, puis de gauche.
        if pyxel.btn(pyxel.KEY_D):
            self.switch_d = False
            pyxel.blt(self.x_perso, self.y_perso, 1, 0, 0, 15, 15)#Pour l'apperence droite, on utilise les coordonnées l'image 1 en on prend toute l'image 0,0,15,15
        elif pyxel.btn(pyxel.KEY_Q):
            self.switch_d = True
            pyxel.blt(self.x_perso, self.y_perso, 2, 0, 0, 15, 15)#Pour l'apperence droite, on utilise les coordonnées l'image 2 en on prend toute l'image 0,0,15,15"""
                    
        # On va définir l'attaque du personnage.
        # On attaque en utilisant la touche espace.
        # Chaque attaque change l'apparence du personnage. On a une attaque droit et un attaque gauche.
        # Le changement de l'apparence doit être fait de façon a juste changer l'apperence que si la touche espace est appuyée, une fois que la touche est relachée, on revient à l'apperence de base.

        # Ici, l'attaque aura comme effet deux changement d'apperence de suite, avec un espace de temps entre chaque changement de 10 frames.

        # Si le personnage regarde à droite:
        # le premier changement se fera avec l'image 1 de coordonnées 0,16 et on prend 23 à droite et 15 en bas
        # le deuxième changement se fera avec l'image 1 de coordonnées 0,32 et on prend 23 à droite et 15 en bas.

        # Une fois la touche espace relachée, on revient à l'apperence de base en passant encore une fois par le premier changement 
        # et puis revenir à l'apperence de base.
        
        if pyxel.btn(pyxel.KEY_SPACE):
            # Le temps d'attente entre la première et la deuxième apparence de l'attaque est de 10 frames.
            # On commence par appuyer espace, puis premier changement et puis on attend 10 frames pour le deuxième changement
            if self.switch_d == False:
                if pyxel.frame_count % 20 < 10:
                    pyxel.blt(self.x_perso, self.y_perso, 1, 0, 16, 23, 15)
                else:
                    pyxel.blt(self.x_perso, self.y_perso, 1, 0, 32, 23, 15)
            else:
                if pyxel.frame_count % 20 < 10:
                    pyxel.blt(self.x_perso-7, self.y_perso, 1, 24, 16, 23, 15)
                else:
                    pyxel.blt(self.x_perso-7, self.y_perso, 1, 24, 32, 23, 15)
            
        else:
            if self.switch_d == False:
                pyxel.blt(self.x_perso, self.y_perso, 1, 0, 0, 15, 15)
            else:
                pyxel.blt(self.x_perso, self.y_perso, 2, 0, 0, 15, 15)
        pyxel.rectb(self.hitbox[0], self.hitbox[1], self.dimension_perso_x, self.dimension_perso_y, 9)  # On dessine la hitbox par defaut, si le personnage ne fait rien.
    def heal(self):
        if pyxel.btnp(pyxel.KEY_A):  
            if self.potions:  
                potion = self.potions.pop(0) 
                self.hp = min(self.max_hp, self.hp + potion)
            
    def init_inventory(self, num_potions):
        for i in range(num_potions):
            self.inventaire("heal")
            
    def inventaire(self, potion_type):
        if potion_type == "heal": 
            self.potions.append(50)

    def damage(self):
        #Je ne vais vraiment pas commenter ce code....
        for zone in self.dmg_zones.values():
            zone_x1, zone_y1 = zone[0]
            zone_x2, zone_y2 = zone[1]
            if self.hitbox[0] <= zone_x2 and self.hitbox[1] <= zone_y2 and self.hitbox[2] >= zone_x1 and self.hitbox[3] >= zone_y1 and self.dmg_cd == 0:  
                self.hp -= 5
                self.dmg_cd = 60
                pyxel.rectb(1,1,255,255,8)
                pyxel.rectb(0,0,255,255,8)
        if self.dmg_cd !=0:
            self.dmg_cd -= 1
            pyxel.rect(20, 5, 100 * (self.hp / self.max_hp), 5, 3) 


    def show_gui(self):
        pyxel.rect(0, 0, 256, 32, 5)
        pyxel.rect(20, 5, 100, 5, 4)
        pyxel.blt(200,5,0, 0,16, 15,16)
        pyxel.rect(20, 5, 100 * (self.hp / self.max_hp), 5, 11) 
        pyxel.rect(20, 17, 100, 5, 13)
        pyxel.rect(20, 17, 100 * (self.mp / self.max_mp), 5, 12)
        pyxel.text(5, 5, "HP :", 11)
        pyxel.text(5, 17, "MP :", 12)
        num_potions_text = f"x{len(self.potions)}" 
        pyxel.text(220, 18, num_potions_text, 7) 

    def death(self):
        if self.hp <= 0:
            pyxel.cls(2)
            pyxel.text(80, 100, "Skill issue", 6)
            pyxel.text(90, 120,"Cry about it ", 6)
            pyxel.text(100, 140, "Game over", 6)
            
    def fond(self):
        for i in range(0,256,15):
            for j in range(0,256,15):
                pyxel.blt(i, j, 0, 0, 0, 15, 15)
    
    def attaque(self):
        if pyxel.btn(pyxel.KEY_SPACE):  # On dessine la hitbox si le personnage attaque.
            if self.switch_d == False:
                pyxel.rectb(self.hitbox[0], self.hitbox[1], self.dimension_perso_x + 7, self.dimension_perso_y, 9)
            else:
                pyxel.rectb(self.hitbox[0], self.hitbox[1], self.dimension_perso_x + 7, self.dimension_perso_y, 9)
                
    def loading_screen(self):
        if self.main_click:
            if not self.loaded:
                pyxel.cls(11)
                texts = ["Chargement en cours", "Chargement en cours.", "Chargement en cours..", "Chargement en cours..."]
                self.num_text = (pyxel.frame_count // 15) % len(texts)
                text_to_display = texts[self.num_text]
                text_width = len(text_to_display) * 4 
                text_x = (self.fenetre_x - text_width) // 2
                text_y = (self.fenetre_y - 6) // 2
                pyxel.text(text_x, text_y, text_to_display, 0)
                rect_x = (self.fenetre_x - 100) // 2
                rect_y = text_y + 10
                pyxel.rect(rect_x, rect_y, self.loading_bar, 5, 12)
                pyxel.rectb(rect_x, rect_y, 100, 5, 0)
                self.loading_time -= 1
                self.loading_bar += 1
                if self.loading_time == 0:
                    self.loaded = True

    def main_screen(self):
        if not self.main_click:
            pyxel.cls(11)
            colors = [11,0,0,0]
            num_color = (pyxel.frame_count // 15) % len(colors)
            texts = ["Cliquez n'importe ou pour commencer","Cliquez n'importe ou pour commencer.", "Cliquez n'importe ou pour commencer.", "Cliquez n'importe ou pour commencer.."]
            num_text = (pyxel.frame_count // 15) % len(texts)
            text_to_display = texts[num_text]
            text_width = len(text_to_display) * 4
            text_x = (self.fenetre_x - text_width) // 2
            text_y = (self.fenetre_y - 6) // 2 - 3
            pyxel.text(text_x, text_y, text_to_display, colors[num_color])
            pyxel.text((self.fenetre_x-(len("Bienvenue sur RogueLigke !!")*4))//2,(self.fenetre_y/4),"Bienvenue sur RogueLigke",0)
        if pyxel.btn(pyxel.MOUSE_BUTTON_LEFT):
            self.main_click = True

    def check_collision(self):
        if (self.hitbox[0] <= self.monster_hitbox[2] and self.hitbox[2] >= self.monster_hitbox[0] and
                self.hitbox[1] <= self.monster_hitbox[3] and self.hitbox[3] >= self.monster_hitbox[1]):
            self.monster_hp -= 10
        pyxel.blt(self.monster_x,self.monster_y,1,0,72,16,16)
        pyxel.rectb(self.monster_x,self.monster_y,16,16,8)
            
            
# ===============================================================================================================================================================================
    def update(self):
        self.movement()
        self.hitbox = [self.x_perso, self.y_perso, self.x_perso + self.dimension_perso_x, self.y_perso + self.dimension_perso_y] 
        self.check_collision()
        if pyxel.btn(pyxel.KEY_SPACE):
                if self.switch_d == False:
                    self.hitbox[2] += 7    # La hitbox augmente de 7 pixels vers la droite si le personnage regarde à droite et attaque.
                else:
                    self.hitbox[0] -= 7    # La hitbox augmente de 7 pixels vers la gauche si le personnage regarde à gauche et attaque.

        # On change la valeur de la variable self.hitbox qui est une liste de 4 éléments.
        # On change la valeur de la hitbox de 7 (ou -7) et ceci n'est fait qu'une fois par attaque.
        
        
    def draw(self):
        pyxel.mouse(True)
        pyxel.cls(0)
        self.fond()
        self.personnage()
        self.attaque()
        self.show_gui()
        self.zones_de_degats()
        self.damage()
        self.death()
        self.heal()
        self.check_collision()
        self.main_screen()
        self.loading_screen()
        
    
    def run(self):
        pyxel.load("resources/sprite.pyxres")
        pyxel.run(self.update, self.draw)
        
    
game = Game()
game.run()