"""
Python Tic-tac-toe Game
"""

# Imported Functions

import pygame
import random
from typing import Dict, Tuple, Optional

Position = Tuple[int, int]

class Menu():
    
    def __init__(self, screen, screenDimensions: Position):
        
        self.screen = screen
        self.screenDimensions = screenDimensions
        self.buttonDimensions = (400, 70)
        self.buttonColours = {"menu": (200, 200, 200), "text": (0, 0, 0), "outline": (0, 0, 0), "button": (100, 150, 0), "hover":(150, 0, 150)}
        self.font = {"small": pygame.font.SysFont('Corbel', 35), "large": pygame.font.SysFont('Corbel', 60), "title": pygame.font.SysFont('Corbel', 80)}
        self.running = True
        self.mode = None
        self.difficultyLevel = None
        
    def drawText(self, text: str, position: Position, fontSize: str, outline: bool):
        """ Make some text in a clickable box. """
        
        left, top = position[0] - self.buttonDimensions[0]//2, position[1] - self.buttonDimensions[1]//2
        
        rectangle = pygame.Rect(left, top, self.buttonDimensions[0], self.buttonDimensions[1])
        
        if outline: 
            colour = self.buttonColours["hover"] if rectangle.collidepoint(pygame.mouse.get_pos()) else self.buttonColours["button"]
            pygame.draw.rect(self.screen, colour, rectangle)
            pygame.draw.rect(self.screen, self.buttonColours["outline"], rectangle, 3)
        
        surface = self.font[fontSize].render(text, True, self.buttonColours["text"])
        self.screen.blit(surface, surface.get_rect(center=position))
        
        return rectangle
        
    def run(self):
        
        while self.running:
            
            self.screen.fill(self.buttonColours["menu"])
            self.drawText("Python Tic-tac-toe Game", (self.screenDimensions[0]//2, 200), "title", False)
            
            pvpButton = self.drawText("Player vs Player", (self.screenDimensions[0]//2, 350), "large", True)
            pveButton = self.drawText("Player vs AI", (self.screenDimensions[0]//2, 425), "large", True)
            quitButton = self.drawText("Quit", (self.screenDimensions[0]//2, 500), "large", True)
            
            for event in pygame.event.get():
                
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    
                if event.type == pygame.MOUSEBUTTONDOWN:
                    
                    mousePosition = pygame.mouse.get_pos()
                    
                    if pvpButton.collidepoint(mousePosition):
                        
                        self.mode = "pvp"
                        self.running = False
                        
                    elif pveButton.collidepoint(mousePosition):
                        
                        self.mode = "pve"
                        self.running = False
                        
                    elif quitButton.collidepoint(mousePosition):
                        
                        self.running = False
                        pygame.quit()
                        
            pygame.display.update()
                            
        return self.mode
    
    def difficulty(self):
        
        while self.running:
            
            self.screen.fill(self.buttonColours["menu"])
            self.drawText("Python Tic-tac-toe Game", (self.screenDimensions[0]//2, 200), "title", False)
            
            easyButton = self.drawText("Easy", (self.screenDimensions[0]//2, 350), "large", True)
            mediumButton = self.drawText("Medium", (self.screenDimensions[0]//2, 425), "large", True)
            hardButton = self.drawText("Hard", (self.screenDimensions[0]//2, 500), "large", True)
            backButton = self.drawText("Back", (self.screenDimensions[0]//2, 650), "large", True)
            
            for event in pygame.event.get():
                
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    
                if event.type == pygame.MOUSEBUTTONDOWN:
                    
                    mousePosition = pygame.mouse.get_pos()
                    
                    if easyButton.collidepoint(mousePosition):
                        
                        self.difficultyLevel = "easy"
                        self.running = False
                        
                    elif mediumButton.collidepoint(mousePosition):
                        
                        self.difficultyLevel = "medium"
                        self.running = False
                        
                    elif hardButton.collidepoint(mousePosition):
                        
                        self.difficultyLevel = "hard"
                        self.running = False
                        
                    elif backButton.collidepoint(mousePosition):
                        
                        self.difficultyLevel = "menu"
                        self.running = False
                        
            pygame.display.update()
                            
        return self.difficultyLevel
                
class Initialise:
    
    def __init__(self):
        
        self.grid = self.makeGrid()
        
    def makeGrid(self) -> Dict[Position, Optional[str]]:
        """ Make an empty grid. """
        
        grid: Dict[Position, Optional[str]] = {}
        
        for row in range(3):
            for col in range(3):
                grid[(row, col)] = None
        
        return grid
    
class DrawSymbol:
    
    def __init__(self, screen, boxLength):
        
        self.screen = screen
        self.symbolColours = {"circle": (232, 180, 81), "cross": (98, 193, 189)}
        self.circleDimensions = {"width": 25, "radius": boxLength // 3}
        self.crossDimensions = {"width": 15, "spacing": boxLength // 4}
        self.boxLength = boxLength
        
    def drawO(self, rectangle: pygame.rect):
        """ Draw an O on the grid. """
        
        pygame.draw.circle(self.screen, self.symbolColours["circle"], rectangle.center, self.circleDimensions["radius"], self.circleDimensions["width"])
        
    def drawX(self, rectangle: pygame.rect):
        """ Draw an X on the grid. """
    
        x, y, w, h = rectangle
        space, size = self.crossDimensions["spacing"], self.boxLength
        
        pygame.draw.line(self.screen, self.symbolColours["cross"], (x + space, y + space), (x + size - space, y + size - space), self.crossDimensions["width"])
        pygame.draw.line(self.screen, self.symbolColours["cross"], (x + space, y + size - space), (x + size - space, y + space), self.crossDimensions["width"])
        
class Result:
    
    def __init__(self, grid: Dict[Position, Optional[str]]):
        
        self.grid = grid
        
    def tie(self) -> bool:
        """ Check the board for a tie. """
        
        return all(symbol is not None for symbol in self.grid.values())
        
    def winner(self) -> Optional[str]:
        """ Check the board for a winner. """
        
        for row in range(3):
            if self.grid[(row, 0)] == self.grid[(row, 1)] == self.grid[(row, 2)] and self.grid[(row, 0)] is not None: return self.grid[(row, 0)]
        
        for col in range(3):
            if self.grid[(0, col)] == self.grid[(1, col)] == self.grid[(2, col)] and self.grid[(0, col)] is not None: return self.grid[(0, col)]
            
        
        if self.grid[(0, 0)] == self.grid[(1, 1)] == self.grid[(2, 2)] and self.grid[(0, 0)] is not None: return self.grid[(0, 0)]
        if self.grid[(2, 0)] == self.grid[(1, 1)] == self.grid[(0, 2)] and self.grid[(2, 0)] is not None: return self.grid[(2, 0)]
        
        return None
    
class GUI:
    
    def __init__(self, screen, screenDimensions, currentPlayer, score):
        
        self.screen = screen
        self.screenDimensions = screenDimensions
        self.guiOffset = 100
        self.guiDimensions = {"turnIndicator": (250, 100), "menu": (100, 100), "quit": (100, 100), "cross": (100, 100), "tie": (100, 100), "circle": (100, 100)}
        self.guiPositions = {"turnIndicator": (self.screenDimensions[0]//2, 75), "menu": (self.screenDimensions[0]-50, 50), "quit": (50, 50), "scoreboard": (self.screenDimensions[0]//2 - self.guiOffset - self.guiDimensions["tie"][0], self.screenDimensions[1]-75)}
        self.guiColours = {"text": (0, 0, 0), "outline": (0, 0, 0), "turnIndicator": (36, 53, 63), "menu": (172, 190, 200), "quit": (100, 110, 69), "cross": (98, 193, 189), "tie": (172, 190, 200), "circle": (232, 180, 81)}
        self.scoreboard = score
        
        self.fontSize = {"small": pygame.font.SysFont('Corbel', 25), "medium": pygame.font.SysFont('Corbel', 50), "large": pygame.font.SysFont('Corbel', 65)}
        self.currentPlayer = currentPlayer
        
    def drawButtons(self, text:str, position: Position, fontSize: str, guiType: str):
        """ Draw the buttons. """
        
        width, height = self.guiDimensions[guiType]
        left, top = position[0] - width//2, position[1] - height//2
        
        rectangle = pygame.Rect(left, top, width, height)
        
        colour = self.guiColours[guiType]
        pygame.draw.rect(self.screen, colour, rectangle)
        pygame.draw.rect(self.screen, self.guiColours["outline"], rectangle, 3)
        
        surface = self.fontSize[fontSize].render(text, True, self.guiColours["text"])
        self.screen.blit(surface, surface.get_rect(center=position))
        
        return rectangle
        
    def turnIndictatorGUI(self):
        """ Draw the turn indictator at the centre top of the page. """
        
        self.drawButtons(f"{self.currentPlayer} Turn", self.guiPositions["turnIndicator"], "medium", "turnIndicator")
        
    def menuGUI(self):
        """ Draw the menu function at the right left of the page. """
        
        return self.drawButtons("Menu", self.guiPositions["menu"], "small", "menu")
        
    def scoreboardGUI(self):
        """ Draw the scoreboard of three different squares at the bottom of the page. """
        
        labels = ["cross", "tie", "circle"]
        
        for i, label in enumerate(labels):
            
            wins = self.scoreboard[label]
            x, y = self.guiPositions["scoreboard"]
            self.drawButtons(f"{label.capitalize()} : {wins}", (x + i*(self.guiOffset + self.guiDimensions[f"{label}"][0]), y), "small", f"{label}")
    
    def quitGUI(self):
        """ Draw the quit function at the right top of the page. """
        
        return self.drawButtons("Quit", self.guiPositions["quit"], "small", "quit")
        
    def drawGUI(self):
        """ Draw all GUI features. """
        
        self.turnIndictatorGUI()
        self.menuGUI()
        self.scoreboardGUI()
        self.quitGUI()
        
class AI:
        
    def easy(grid: Dict[Position, Optional[str]]):
        """ Algorithm that randomly choses an unfilled grid point. """
        
        available = [position for position, symbol in grid.items() if symbol is None]
        
        return random.choice(available) if available else None
    
    def medium(grid: Dict[Position, Optional[str]], player: str, ai: str):
        """ Algorithm that follows Newell and Simon's program. """
    
        # 1. Win the game if possible.
        move = aiHelper.twoInRow(grid, ai)
        if move: return move
        
        # 2. Block if possible
        move = aiHelper.twoInRow(grid, player)
        if move: return move
        
        # 3. Try to create a fork
        move = aiHelper.fork(grid, ai)
        if move: return move
        
        # 4. Block a potential fork
        move = aiHelper.fork(grid, player)
        if move: return move
        
        # 5. Play the centre
        move = aiHelper.centre(grid)
        if move: return move
            
        # 6. Play the opposite corner
        move = aiHelper.oppositeCorner(grid, player)
        if move: return move
        
        # 7. Play an empty corner
        move = aiHelper.emptyCorner(grid)
        if move: return move
        
        # 8. Play an empty side
        move = aiHelper.emptySide(grid)
        if move: return move
        
        return AI.easy(grid)
        
    def hard(grid: Dict[Position, Optional[str]], player: str, ai: str):
        """ Algorithm that uses the minimax theorem. """
        
        bestMove, bestScore = None, - float("inf")
        
        for position, symbol in grid.items():
            
            if symbol is not None: continue
            grid[position] = ai
            currentScore = aiHelper.minimax(grid, player, ai, False, 0)
            grid[position] = None
            
            if currentScore > bestScore:
                bestMove, bestScore = position, currentScore
                
        return bestMove
        
        
    def aiMove(grid: Dict[Position, Optional[str]], player: str, ai: str, difficultyLevel: str):
        """ Return the relevant move based upon the difficulty. """
        
        if difficultyLevel == "easy": move = AI.easy(grid)
        elif difficultyLevel == "medium": move = AI.medium(grid, player, ai)
        elif difficultyLevel == "hard": move = AI.hard(grid, player, ai)
        
        return move
    
class aiHelper:
    
    def twoInRow(grid: Dict[Position, Optional[str]], symbol: str):
        """ Find the square for two in a row. """
        
        possible = [[(0, 0), (0, 1), (0, 2)], [(1, 0), (1, 1), (1, 2)], [(2, 0), (2, 1), (2, 2)],
                    [(0, 0), (1, 0), (2, 0)], [(0, 1), (1, 1), (2, 1)], [(0, 2), (1, 2), (2, 2)],
                    [(0, 0), (1, 1), (2, 2)], [(2, 0), (1, 1), (0, 2)]]
                
        for line in possible:
            
            value = [grid[position] for position in line]
            if value.count(symbol) == 2 and value.count(None) == 1:
                return line[value.index(None)]
            
        return None
        
    def fork(grid: Dict[Position, Optional[str]], symbol: str):
        """ Find the square for a fork. """
        
        for position, value in grid.items():
            
            if value is not None: continue
            
            grid[position] = symbol    
            winMove = 0
            
            for move, val in grid.items():
                
                if val is None:
                    
                    grid[move] = symbol
                    result = Result(grid)
                    if result.winner(): winMove += 1
                    
                    grid[move] = None
            
            grid[position] = None
            
            if winMove == 2: return position
            
        return None
    
    def centre(grid: Dict[Position, Optional[str]]):
        """ Check the centre. """
        
        return (1, 1) if grid[(1, 1)] is None else None
    
    def oppositeCorner(grid: Dict[Position, Optional[str]], symbol: str):
        """ Check the opposite corner. """
        
        corners = [(0, 0), (0, 2), (2, 0), (2, 2)]
        
        for corner in corners:
            
            if grid[corner] == symbol and grid[(2-corner[0], 2-corner[1])] is None: return (2-corner[0], 2-corner[1])
            
        return None
    
    def emptyCorner(grid: Dict[Position, Optional[str]]):
        """ Check for an empty corner. """
        
        corners = [(0, 0), (0, 2), (2, 0), (2, 2)]
        emptyCorners = []
        
        for corner in corners:
            
            if grid[corner] is None: emptyCorners.append(corner)
            
        return random.choice(emptyCorners) if emptyCorners else None
    
    def emptySide(grid: Dict[Position, Optional[str]]):
        """ Check for an empty side. """
        
        sides = [(0, 1), (1, 0), (1, 2), (2, 1)]
        emptySides = []
        
        for side in sides:
            
            if grid[side] is None: emptySides.append(side)
            
        return random.choice(emptySides) if emptySides else None
    
    def minimax(grid: Dict[Position, Optional[str]], player: str, ai:str, isMax: bool, depth: int = 0) -> int:
        """" Find the best move in all possibilities. """
        
        result = Result(grid)
        winner = result.winner()
        
        if winner == ai: return 10 - depth
        elif winner == player: return -10 + depth
        elif result.tie(): return 0
        
        if isMax:
            
            bestScore = - float("inf")
            
            for position, symbol in grid.items():
                
                if symbol is not None: continue
                grid[position] = ai
                currentScore = aiHelper.minimax(grid, player, ai, False, depth + 1)
                grid[position] = None
                bestScore = max(currentScore, bestScore)
                
        else:
            
            bestScore = float("inf")
            
            for position, symbol in grid.items():
                
                if symbol is not None: continue
                grid[position] = player
                currentScore = aiHelper.minimax(grid, player, ai, True, depth + 1)
                grid[position] = None
                bestScore = min(currentScore, bestScore)
        
        return bestScore
        
class Game:
    
    def __init__(self, screen, screenDimensions: Position, mode: str, difficultyLevel: str):
        
        self.screen = screen
        self.screenDimensions = screenDimensions
        self.boxDimensions: Dict[int] = {"length": 150, "spacing": 25, "indent": 150}
        self.colours = {"background": (29, 142, 150), "box": (36, 53, 63)}
        self.mode = mode
        self.difficultyLevel = difficultyLevel
        
        pygame.display.set_caption("Python Tic-tac-toe Game")
    
        self.grid = Initialise().grid
        self.symbols = DrawSymbol(self.screen, self.boxDimensions["length"])
        self.running = True
        self.playerInformation = self.playerInformation()
        self.currentPlayer = self.playerInformation["player1"][0]
        self.currentTurn = "player1"
        self.currentType = self.playerInformation["player1"][1]
        
        self.resultMap = {"X": "cross", "O": "circle"}
        
        self.scoreboard: Dict[str, int] = {"cross": 0, "tie": 0, "circle": 0}
        self.gui = GUI(self.screen, self.screenDimensions, self.currentPlayer, self.scoreboard)
        
        self.screen.fill(self.colours["background"])
        self.drawBoxes()
        self.gui.drawGUI()
        
        pygame.display.update()
        
    def playerInformation(self):
        """ Determine the type of players and the order. """
        
        playerSymbols = ["X", "O"]
        random.shuffle(playerSymbols)
        
        if self.mode == "pvp": playerInfo = {"player1": (playerSymbols[0], "player"), "player2": (playerSymbols[1], "player")}
        elif self.mode == "pve":
            playerTypes = ["player", "ai"]
            random.shuffle(playerTypes)
            playerInfo = {"player1": (playerSymbols[0], playerTypes[0]), "player2": (playerSymbols[1], playerTypes[1])}
        
        return playerInfo
        
    def playerChange(self):
        """ Switch between players after a turn. """
        
        self.currentTurn = "player2" if self.currentTurn == "player1" else "player1"
        self.currentPlayer = self.playerInformation[self.currentTurn][0]
        self.currentType = self.playerInformation[self.currentTurn][1]
        
        self.gui.currentPlayer = self.currentPlayer
        self.gui.turnIndictatorGUI()
        
    def getBox(self, row: int, col: int):
        """ Find the box using the row and column. """
        
        x, y = self.boxDimensions["indent"] + col * (self.boxDimensions["length"] + self.boxDimensions["spacing"]), self.boxDimensions["indent"] + row * (self.boxDimensions["length"] + self.boxDimensions["spacing"])
        
        return pygame.Rect(x, y, self.boxDimensions["length"], self.boxDimensions["length"])
    
    def drawBoxes(self):
        """ Draw all boxes with the relevant spacing. """
        
        for row in range(3):
            for col in range(3):
                
                rectangle = self.getBox(row, col)
                pygame.draw.rect(self.screen, self.colours["box"], rectangle)
    
    def clickBox(self, mousePosition: Position) -> Optional[Position]:
        """ Find the box being clicked upon. """
        
        for row in range(3):
            for col in range(3):
                
                rectangle = self.getBox(row, col)
                if rectangle.collidepoint(mousePosition):
                    return (row, col)
                
        return None
    
    def playerTurn(self, mousePosition: Position):
        """ Return the player's move. """
        
        clickedBox = self.clickBox(mousePosition)
        if clickedBox and self.grid[clickedBox] is None:
        
            self.grid[clickedBox] = self.currentPlayer
            rectangle = self.getBox(*clickedBox)
        
            if self.currentPlayer == "O": 
                self.symbols.drawO(rectangle)
            
            elif self.currentPlayer == "X": 
                self.symbols.drawX(rectangle)
                
            self.playerChange()
                
                
    def aiTurn(self):
        """ Return the ai's turn. """
        
        player = self.playerInformation["player1"][0] if self.currentTurn == "player2" else self.playerInformation["player2"][0]
        move = AI.aiMove(self.grid, player, self.currentPlayer, self.difficultyLevel)
        
        if move:
            
            self.grid[move] = self.currentPlayer
            rectangle = self.getBox(*move)
            
            if self.currentPlayer == "O": 
                self.symbols.drawO(rectangle)
            
            elif self.currentPlayer == "X": 
                self.symbols.drawX(rectangle)
                
            self.playerChange()
            
    def checkResult(self):
        """ Check the result. """
        
        result = Result(self.grid)
        winner = result.winner()
        
        if winner:
            self.scoreboard[self.resultMap[winner]] += 1
            self.gridReset()
            
        elif result.tie():
            self.scoreboard["tie"] += 1
            self.gridReset()
                
    def gridReset(self):
        """ Reset the grid after the game is completed. """
        
        self.grid = Initialise().grid
        players = ["player1", "player2"]
        random.shuffle(players)
        self.currentTurn = players[0]
        self.currentPlayer = self.playerInformation[players[0]][0]
        self.currentType = self.playerInformation[players[0]][1]
        self.drawBoxes()
        self.gui.currentPlayer = self.currentPlayer
        self.gui.drawGUI()
        
    def run(self):
        
        while self.running:
            
            menuClicked = self.gui.menuGUI()
            quitClicked = self.gui.quitGUI()
            
            if self.currentType == "ai": 
                pygame.time.delay(500)
                self.aiTurn()
                self.checkResult()
            
            for event in pygame.event.get():
                
                if event.type == pygame.QUIT:
                    self.running = False
                    return "quit"
                    
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    
                    mousePosition = pygame.mouse.get_pos()
                    
                    if menuClicked.collidepoint(mousePosition):
                        
                        self.running = False
                        return "menu"
                    
                    if quitClicked.collidepoint(mousePosition):
                        
                        self.running= False
                        return "quit"
                    
                    if self.currentType == "player": 
                        self.playerTurn(mousePosition)
                        self.checkResult()
                
            pygame.display.update()
            
        return "quit"
        
if __name__ == "__main__":
    
    width, height = 800, 800
    
    pygame.init()
    pygame.font.init()
    
    screen = pygame.display.set_mode((width, height))
    
    mode = "menu"
    
    while True:
        
        if mode == "menu":
            
            menu = Menu(screen, (width, height))
            mode = menu.run()
            
        elif mode == "pvp":
            
            game = Game(screen, (width, height), mode, None)
            game.mode = mode
            result = game.run()
            
            if result == "menu": mode = "menu"
            elif result == "quit": mode = "quit"
            
            
        elif mode == "pve":
            
            menu = Menu(screen, (width, height))
            difficulty = menu.difficulty()
            
            if difficulty == "menu": mode = "menu"
            else:
                game = Game(screen, (width, height), mode, difficulty)
                result = game.run()
            
                if result == "menu": mode = "menu"
                elif result == "quit": mode = "quit"
            
        elif mode == "quit":
            
            break
        
    pygame.quit()
        