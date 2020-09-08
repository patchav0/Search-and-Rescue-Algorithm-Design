
// Description: Loads a text file, make a graphical representation of the environment, 
// find a solution path and lastly animation of the solution path.

import java.awt.Color;
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.File;
import java.io.FileNotFoundException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Scanner;

import javax.swing.JComponent;
import javax.swing.JFrame;
import javax.swing.Timer;

public class Bidirectional extends JFrame {

	private static final long serialVersionUID = 1L;
	final int WALL_BLOCK = 1;
	final int CHARACTER_BLOCK = 3;
	final int EXIT_BLOCK = 2;
	final int VISITED_BLOCK = 4;
	final int EMPTY_BLOCK = 0;

	final int MOVE_RIGHT = 6;
	final int MOVE_LEFT = 7;
	final int MOVE_UP = 8;
	final int MOVE_DOWN = 9;

	private Timer timer;
	private TimerListener listener;
	// starting position 
	
	int col; // column no. of starting cell 
	int row; // row no. of starting cell 

	XComponent comp;

	int[][] maze = new int[10][10];
	ArrayList<Integer> list = new ArrayList<>();

	// constructor
	public Bidirectional() {

		setSize(515, 539);
		loadMaze("test", maze);
		list = findSolution(maze, col, row);
		System.out.println(list.toString());
		listener = new TimerListener();
		timer = new Timer(1000, listener);
		timer.start();

	}

	// loads the maze to an array from a text file
	private void loadMaze(String filename, int[][] maze) {

		try (Scanner s = new Scanner(new File(filename))) {

			while (s.hasNext()) {

				for (int j = 0; j < 10; j++) {

					for (int k = 0; k < 10; k++) {

						maze[j][k] = s.nextInt();
						// if they are the starting coordinates
						if (maze[j][k] == 3) {
							row = j;
							col = k;
						}
					}

				}

			}

			s.close();
		} catch (FileNotFoundException exception) {

			System.out.println("File not Found");
		}

		drawMaze(maze);

	}

	// calls the component to draw the maze
	private void drawMaze(int[][] maze) {
		// XComponent.repaint();

		comp = new XComponent();
		this.add(comp);

	}

	// Component class for drawing the maze
	class XComponent extends JComponent {

		private static final long serialVersionUID = 1L;

		public void paintComponent(Graphics g) {

			Graphics2D g2 = (Graphics2D) g;

			for (int i = 0; i < 10; i++) {

				for (int j = 0; j < 10; j++) {

					switch (maze[i][j]) {
                    // if it's a zero, then the cell is empty 
					case 0:

						g2.setColor(Color.WHITE);

						break;
                    // if the value is 1, then it's a wall 
					case 1:

						g2.setColor(Color.black);

						break;
                    // 2 is the target
					case 2:

						g2.setColor(Color.RED);
						break;
                    // 3 is our current position in the maze
					case 3:

						g2.setColor(Color.BLUE);

						break;
                    // 4 means the cell has already been visited 
					case 4:
						g2.setColor(Color.GREEN);
						break;

					}

					g2.fillRect(j * 50, i * 50, 50, 50);
				}
			}

		}
	}

	// Finds the solution path of the maze
	private ArrayList<Integer> findSolution(int[][] board, int col, int row) {
		
		ArrayList<Integer> moveList = null;
		// moving to the right by one cell is possible 
		if ((col + 1) < 10) {
			
			// if the cell to your right is the target 
			if (board[row][col + 1] == EXIT_BLOCK) {
				moveList = new ArrayList<Integer>();
				moveList.add(MOVE_RIGHT);
				return moveList;

			}

			// if the cell to your right is empty 
			else if (board[row][col + 1] == EMPTY_BLOCK) {
				moveList = new ArrayList<Integer>();
				moveList.add(MOVE_RIGHT);
				int[][] newBoard = arrayCopy(board);
				newBoard[row][col + 1] = VISITED_BLOCK;
				ArrayList<Integer> result = findSolution(newBoard, col + 1, row);
				// if that was a dead end (meaning it didn't find the target )  
				if (result == null) {
					// set that move list as null, as these moves led to a dead end 
					moveList = null;
				} else {
					// if it led to target, add it to the move list 
					moveList.addAll(result);
					return moveList;

				}

			}

		}

		// moving to the left by one cell is possible 
		if ((col - 1) >= 0) {
			
			// if the cell to your left is the target 
			if (board[row][col - 1] == EXIT_BLOCK) {
				moveList = new ArrayList<Integer>();
				moveList.add(MOVE_LEFT);
				return moveList;
			}

			// if the cell to your left is empty 
			else if (board[row][col - 1] == EMPTY_BLOCK) {
				moveList = new ArrayList<Integer>();
				moveList.add(MOVE_LEFT);
				int[][] newBoard = arrayCopy(board);
				newBoard[row][col - 1] = VISITED_BLOCK;
				ArrayList<Integer> result = findSolution(newBoard, col - 1, row);
				if (result == null) {
					moveList = null;
				} else {
					moveList.addAll(result);
					return moveList;

				}

			}

		}
		
		// if moving to the cell on top of you is possible 
		if ((row - 1) >= 0) {
			// if the cell on top is the target 
			if (board[row - 1][col] == EXIT_BLOCK) {
				moveList = new ArrayList<Integer>();
				moveList.add(MOVE_UP);
				return moveList;

			}

			// if the cell on top is empty 
			else if (board[row - 1][col] == EMPTY_BLOCK) {
				moveList = new ArrayList<Integer>();
				moveList.add(MOVE_UP);
				int[][] newBoard = arrayCopy(board);
				newBoard[row - 1][col] = VISITED_BLOCK;
				ArrayList<Integer> result = findSolution(newBoard, col, row - 1);
				if (result == null) {
					moveList = null;
				} else {
					moveList.addAll(result);
					return moveList;

				}

			}

		}

		// if moving to the cell below is possible 
		if ((row + 1) < 10) {
			
			// if the cell below is the target 
			if (board[row + 1][col] == EXIT_BLOCK) {
				moveList = new ArrayList<Integer>();
				moveList.add(MOVE_DOWN);
				return moveList;

			}

			// if the cell below you is empty 
			else if (board[row + 1][col] == EMPTY_BLOCK) {
				moveList = new ArrayList<Integer>();
				// add that move to the arrayList 
				moveList.add(MOVE_DOWN);
				// make a copy of the new board 
				int[][] newBoard = arrayCopy(board);
				newBoard[row + 1][col] = VISITED_BLOCK;
				ArrayList<Integer> result = findSolution(newBoard, col, row + 1);
				if (result == null) {
					moveList = null;
				} else {
					moveList.addAll(result);
					return moveList;

				}

			}

		}

		return moveList;

	}

	// Copies the array
	private int[][] arrayCopy(int[][] array) {
		if (array == null)
			return null;
		int[][] newArray = new int[array.length][];
		for (int r = 0; r < array.length; r++) {
			newArray[r] = array[r].clone();
		}

		return newArray;
	}

	// Action listener class for updating the char value
	class TimerListener implements ActionListener {

		int i = 0;

		public void actionPerformed(ActionEvent e) {
			// TODO Auto-generated method stub

			int move = list.get(i);
			
			// if you move right by one cell 
			if (move == 6) {
				maze[row][col] = 4;
				col = col + 1;
				
            // if you move left by one cell  
			} else if (move == 7) {
				maze[row][col] = 4;
				col = col - 1;
            
		    //  if you move up by one cell 
			} else if (move == 8) {
				maze[row][col] = 4;
				// decrease the no of row you are at 
				row = row - 1;

			// if you move down by one cell 
			} else if (move == 9) {
				maze[row][col] = 4;
			    // increase no. of cell you are at 
				row = row + 1;

			}

			// now this is the new starting cell 
			maze[row][col] = 3;
			
			// move to the next move 
			i++;
			
			// repaint the maze after every move 
			comp.repaint();

			// if you have reached end of array list containing moves 
			if (i == list.size())
				timer.stop();

		}

	}

}
