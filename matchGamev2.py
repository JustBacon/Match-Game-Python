from breezypythongui import EasyFrame
from grid import Grid
from cards import Deck
import random

class MemoryGame(EasyFrame):
 
	def __init__(self):
		EasyFrame.__init__(self, title = "Panel Demo", width = 1200, height = 700)

		# The game table's data. (Where the card will be located)
		self.gameData = []

		# boolean if player's turn
		self.isHuman = True
		# boolean if cards picked is a match
		self.isMatch = False


		# Panel label with 6 columns 6 rows
		# Play area
		# showing 5 by 5 grid
		self.play_area = self.addPanel(row = 0, column = 0, rowspan = 12, columnspan = 6, background = "grey")
		for i in range(5):
			self.addLabel(text = i + 1, row = i * 2 + 1, column = 0, background = "grey")
		for i in range(5):
			self.addLabel(text = i + 1, row = 0, column = i + 1, background = "grey")
		
		# What the player see (Hidden, name_of_card, empty string)
		self.gameTable = Grid(5, 5)

		# Panel control area in column 7
		# All the button and user input
		self.control_area = self.addPanel(row = 0, column = 6, rowspan = 12, columnspan = 2, background = "white")

		# START/RESTART button
		self.addButton(text = "Start/Restart", row = 0, column = 7, columnspan = 2, command = self.start)
		
		# SCORES for player 1, computer, remaining pairs
		self.addLabel(text = "Player1 Score:", row = 1, column = 7)
		self.play1Score = self.addIntegerField(value = 0, row = 1, column = 7, width = 5, state = "readonly")
		self.addLabel(text = "Computer Score:", row = 2, column = 7)
		self.compScore = self.addIntegerField(value = 0, row = 2, column = 7, width = 5, state = "readonly")
		self.addLabel(text = "Pairs Remaining:", row = 3, column = 7)
		self.pairRemain = self.addIntegerField(value = 12, row = 3, column = 7, width = 5, state = "readonly")

		# user instruction
		self.addLabel(text = "Enter the row and column number for Card 1 and Card 2", row = 4, column = 7, columnspan = 2)

		# user input for card1 and card 2
		self.addLabel(text = "Card 1 (row)", row = 5, column = 7)
		self.c1r = self.addTextField(text = "", row = 5, column = 7, width = 5, state = "disabled")
		self.addLabel(text = "Card 1 (column)", row = 6, column = 7)
		self.c1c = self.addTextField(text = "", row = 6, column = 7, width = 5, state = "disabled")
		self.addLabel(text = "Card 2 (row)", row = 7, column = 7)
		self.c2r = self.addTextField(text = "", row = 7, column = 7, width = 5, state = "disabled")
		self.addLabel(text = "Card 2 (column)", row = 8, column = 7)
		self.c2c = self.addTextField(text = "", row = 8, column = 7, width = 5, state = "disabled")

		# buttons
		self.playComp = self.addButton(text = "Play Computer Turn", row = 9, column = 8, state = "disabled", command = self.guess)		
		self.nextComp = self.addButton(text = "Next Computer Turn", row = 10, column = 8, state = "disabled", command = self.next)
		self.next = self.addButton(text = "Next Turn", row = 10, column = 7, state = "disabled", command = self.next)
		self.guess = self.addButton(text = "Guess", row = 9, column = 7, state = "disabled", command = self.guess)

	def start(self):
		gamedeck = None
		gameTable = self.gameTable
		gameData = self.gameData
		# clear data
		gameData.clear()
		# Create new deck
		gamedeck = Deck()
		gamedeck.shuffle()
		# put shuffled deck into gamedata
		# dictionary
		# display_value: string (used for displaying into gameTable)
		# rank_value: number
		# color: red or black (rank_value and color is used for comparing)
		while gamedeck:
			if gamedeck.cards[0].suit == "Spades" or gamedeck.cards[0].suit == "Clubs":
				gameData.append({'display_value': str(gamedeck.cards[0]), 'rank_value' : gamedeck.cards[0].rank, 'color' : "black"})
				gamedeck.deal()
			else:
				gameData.append({'display_value': str(gamedeck.cards[0]), 'rank_value' : gamedeck.cards[0].rank, 'color' : "red"})
				gamedeck.deal()

		#print(gameData)

		# put deck into game table
		# if gameTable is empty initially. Add the labels with text HIDDEN
		# else update the information if they press the start/restart button. change everything back to hidden
		if gameTable[0][0] == None:
			for row in range(gameTable.getHeight()):
				for col in range(gameTable.getWidth()):
					if row != 4 or col !=4:
						gameTable[row][col] = self.addLabel(text = "HIDDEN", row = row * 2 + 1, column = col + 1, font = None, foreground = "black", background = "grey")
					else:
						gameTable[row][col] = self.addLabel(text = "", row = row * 2 + 1, column = col + 1, font = None, foreground = "black", background = "grey")
		else:
			for row in range(gameTable.getHeight()):
				for col in range(gameTable.getWidth()):
					if row != 4 or col !=4:
						gameTable[row][col]["text"] = "HIDDEN"
						gameTable[row][col]["background"] = "grey"
					else:
						gameTable[row][col]["text"] = "HIDDEN"

		# Set score = 0
		self.play1Score.setNumber(0)
		self.compScore.setNumber(0)
		self.pairRemain.setNumber(12)

		# Set player 1 as the active player
		self.isHuman = True

		# The guess button and guess text field are enabled
		self.guess["state"] = "normal"
		self.c1r["state"] = "normal"
		self.c1c["state"] = "normal"
		self.c2r["state"] = "normal"
		self.c2c["state"] = "normal"

		# disable buttons
		self.next["state"] = "disabled"
		self.playComp["state"] = "disabled"
		self.nextComp["state"] = "disabled"

	def guess(self):
		# Error checking card 1 and card 2 input. (Only execute if card is HIDDEN)
		c1r = self.c1r
		c1c = self.c1c
		c2r = self.c2r
		c2c = self.c2c
		if self.isHuman:

			# Error checking. input range is 0 - 5
			# error check if input are the same, if its empty
			try:
				rowCard1 = int(c1r.getText())
				colCard1 = int(c1c.getText())
				rowCard2 = int(c2r.getText())
				colCard2 = int(c2c.getText())
				if (rowCard1 > 0 and rowCard1 <= 5 and colCard1 > 0 and colCard1 <=5 and
					rowCard2 > 0 and rowCard2 <= 5 and colCard2 > 0 and colCard2 <=5 and
					not(rowCard1 == 5 and colCard1 == 5) and not(rowCard2 == 5 and colCard2 == 5) and
					not(rowCard1 == rowCard2 and colCard1 == colCard2) and
					self.gameTable[rowCard1 - 1][colCard1 - 1]["text"] != "" and self.gameTable[rowCard2 - 1][colCard2 - 1]["text"] != ""):
					pass
				else:
					self.messageBox(title = "Error", message = "Not Valid", width = 25, height = 5)
					return

			except ValueError:
				c1r.setText("")
				c1c.setText("")
				c2r.setText("")
				c2c.setText("")
				self.messageBox(title = "Error", message = "Enter an Integer", width = 25, height = 5)
				return
			
			# reveals card 1 and card 2 (show "NAME of CARD")
			self.gameTable[rowCard1 - 1][colCard1 - 1]["text"] = self.gameData[((rowCard1 - 1) * 5) + (colCard1 - 1)]["display_value"]
			self.gameTable[rowCard2 - 1][colCard2 - 1]["text"] = self.gameData[((rowCard2 - 1) * 5) + (colCard2 - 1)]["display_value"]

			card1Rank = self.gameData[((rowCard1 - 1) * 5) + (colCard1 - 1)]["rank_value"]
			card1Color = self.gameData[((rowCard1 - 1) * 5) + (colCard1 - 1)]["color"]
			card2Rank = self.gameData[((rowCard2 - 1) * 5) + (colCard2 - 1)]["rank_value"]
			card2Color = self.gameData[((rowCard2 - 1) * 5) + (colCard2 - 1)]["color"]

			# compare cards
			# If match (Update score)
			if card1Rank == card2Rank and card1Color == card2Color:
				self.play1Score.setNumber(self.play1Score.getNumber() + 1)
				self.pairRemain.setNumber(self.pairRemain.getNumber() - 1)
				self.gameTable[rowCard1 - 1][colCard1 - 1]["background"] = "green"
				self.gameTable[rowCard2 - 1][colCard2 - 1]["background"] = "green"
				self.guess["state"] = "disabled"
				self.isMatch = True
			
			# If not match (active player changes)
			else:
				self.gameTable[rowCard1 - 1][colCard1 - 1]["background"] = "yellow"
				self.gameTable[rowCard2 - 1][colCard2 - 1]["background"] = "yellow"
				self.guess["state"] = "disabled"

			# makes the next button active
			self.next["state"] = "normal"

		# computer's guess
		else:
			while True:

				rowCard1 = int(random.randrange(5) + 1)
				colCard1 = int(random.randrange(5) + 1)
				rowCard2 = int(random.randrange(5) + 1)
				colCard2 = int(random.randrange(5) + 1)
				if (rowCard1 > 0 and rowCard1 <= 5 and colCard1 > 0 and colCard1 <=5 and
					rowCard2 > 0 and rowCard2 <= 5 and colCard2 > 0 and colCard2 <=5 and
					not(rowCard1 == 5 and colCard1 == 5) and not(rowCard2 == 5 and colCard2 == 5) and
					not(rowCard1 == rowCard2 and colCard1 == colCard2) and
					(self.gameTable[rowCard1 - 1][colCard1 - 1]["text"] != "") and (self.gameTable[rowCard2 - 1][colCard2 - 1]["text"]) != ""):
					c1r.setText(rowCard1)
					c1c.setText(colCard1)
					c2r.setText(rowCard2)
					c2c.setText(colCard2)
					break
				else:
					pass

			self.gameTable[rowCard1 - 1][colCard1 - 1]["text"] = self.gameData[((rowCard1 - 1) * 5) + (colCard1 - 1)]["display_value"]
			self.gameTable[rowCard2 - 1][colCard2 - 1]["text"] = self.gameData[((rowCard2 - 1) * 5) + (colCard2 - 1)]["display_value"]
			card1Rank = self.gameData[((rowCard1 - 1) * 5) + (colCard1 - 1)]["rank_value"]
			card1Color = self.gameData[((rowCard1 - 1) * 5) + (colCard1 - 1)]["color"]
			card2Rank = self.gameData[((rowCard2 - 1) * 5) + (colCard2 - 1)]["rank_value"]
			card2Color = self.gameData[((rowCard2 - 1) * 5) + (colCard2 - 1)]["color"]

			if card1Rank == card2Rank and card1Color == card2Color:
				self.compScore.setNumber(self.compScore.getNumber() + 1)
				self.pairRemain.setNumber(self.pairRemain.getNumber() - 1)
				self.gameTable[rowCard1 - 1][colCard1 - 1]["background"] = "green"
				self.gameTable[rowCard2 - 1][colCard2 - 1]["background"] = "green"
				self.playComp["state"] = "disabled"
				self.isMatch = True
			
			# If not match (active player changes)
			else:
				self.gameTable[rowCard1 - 1][colCard1 - 1]["background"] = "yellow"
				self.gameTable[rowCard2 - 1][colCard2 - 1]["background"] = "yellow"
				self.playComp["state"] = "disabled"

			# makes the next button active
			self.nextComp["state"] = "normal"


	def next(self):
		c1r = self.c1r
		c1c = self.c1c
		c2r = self.c2r
		c2c = self.c2c
		rowCard1 = int(c1r.getText())
		colCard1 = int(c1c.getText())
		rowCard2 = int(c2r.getText())
		colCard2 = int(c2c.getText())
		self.gameTable[rowCard1 - 1][colCard1 - 1]["background"] = "grey"
		self.gameTable[rowCard2 - 1][colCard2 - 1]["background"] = "grey"
			

		if self.isHuman:
			
			if self.isMatch:
				

				# Remove cards (make the grid locations "")
				self.gameTable[rowCard1 - 1][colCard1 - 1]["text"] = ""
				self.gameTable[rowCard2 - 1][colCard2 - 1]["text"] = ""

				# Clear the card 1 and card 2 input
				c1r.setText("")
				c1c.setText("")
				c2r.setText("")
				c2c.setText("")

				self.guess["state"] = "normal"
				self.next["state"] = "disabled"
				self.isMatch = False
			else:
				# change active player
				self.isHuman = False
				self.next["state"] = "disabled"
				self.playComp["state"] = "normal"
				self.gameTable[rowCard1 - 1][colCard1 - 1]["text"] = "HIDDEN"
				self.gameTable[rowCard2 - 1][colCard2 - 1]["text"] = "HIDDEN"

				c1r.setText("")
				c1c.setText("")
				c2r.setText("")
				c2c.setText("")
		else:
			if self.isMatch:
				

				# Remove cards (make the grid locations "E")
				self.gameTable[rowCard1 - 1][colCard1 - 1]["text"] = ""
				self.gameTable[rowCard2 - 1][colCard2 - 1]["text"] = ""

				# Clear the card 1 and card 2 input
				c1r.setText("")
				c1c.setText("")
				c2r.setText("")
				c2c.setText("")

				self.playComp["state"] = "normal"
				self.nextComp["state"] = "disabled"
				self.isMatch = False
			else:
				# change active player
				self.isHuman = True
				self.nextComp["state"] = "disabled"
				self.guess["state"] = "normal"
				self.gameTable[rowCard1 - 1][colCard1 - 1]["text"] = "HIDDEN"
				self.gameTable[rowCard2 - 1][colCard2 - 1]["text"] = "HIDDEN"

				c1r.setText("")
				c1c.setText("")
				c2r.setText("")
				c2c.setText("")
		# check if theres no more pairs
		# declare winner
		if self.pairRemain.getNumber() == 0:
			self.guess["state"] = "disabled"
			self.playComp["state"] = "disabled"
			self.next["state"] = "disabled"
			self.nextComp["state"] = "disabled"
			if self.play1Score.getNumber() == 2:
				self.messageBox(title = "TIE", message = "ITS A TIE", width = 25, height = 5)
			elif self.play1Score.getNumber() > 2:
				self.messageBox(title = "WIN", message = "YOU WIN", width = 25, height = 5)
			else:
				self.messageBox(title = "LOSE", message = "YOU LOSE", width = 25, height = 5)
			return

def main():
	MemoryGame().mainloop()

if __name__ == '__main__':
	main()