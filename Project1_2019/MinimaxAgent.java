import MKAgent.Kalah;
import MKAgent.Board;
import MKAgent.Move;
import MKAgent.Side;
import MKAgent.Protocol;

public class MinimaxAgent
{
  private static final int NORTH = 0;
	private static final int SOUTH = 1;

  public static int evaluate(Board board)
  {
      int seedsInNorthWell = board.getSeedsInStore(Side.NORTH);
      int seedsInSouthWell = board.getSeedsInStore(Side.SOUTH);

      if(seedsInSouthWell > seedsInNorthWell) return -10;
      else if(seedsInSouthWell < seedsInNorthWell) return 10;
      else return 0;
  }

  public static void makeNewMove(Board board, Side side, int i, int index, int[] orgOppNum)
  {
    while(board.getSeeds(side, i) != 0)
    {
        if(index == 8)
        {
          index = 1;
          board.addSeedsToStore(side, 1);
        }
        else
        {
          if (board.getSeeds(side, i) == 1 && board.getSeeds(side, index) == 0)
          {
            orgOppNum[index - 1] = board.getSeeds(side, index);
            board.setSeedsOp(side, index, 0);
            board.setSeedsInStore(side, orgOppNum[index - 1]);
          }
          else
          {
            board.addSeeds(side, index, 1);
            if (board.getSeeds(side, i) != 1) index++;
          }
        }

        int numberNew = board.getSeeds(side, i);
        board.setSeeds(side, i, numberNew - 1);
    }
  }

  public static void reverseMove(Board board, Side side, int number, int index, int i, int[] orgOppNum)
  {
    while(board.getSeeds(side, i) != number)
    {
        if(index == 0)
        {
          index = 7;
          int num = board.getSeeds(side, index);
          board.setSeedsInStore(side, num - 1);
        }
        else
        {
          if(orgOppNum[index - 1] != 1000) board.setSeedsOp(side, index, orgOppNum[index - 1]);
          int num = board.getSeeds(side, index);
          board.addSeeds(side, index, num - 1);
          index--;
        }

        int num = board.getSeeds(side, i);
        board.setSeeds(side, i, num + 1);
    }
  }

  // Initial values of
  // Aplha and Beta
  static int MAX = 1000;
  static int MIN = -1000;

  public static int minimax(Board board, int depth, boolean isMax, Side side, int alpha, int beta)
  {
      int score = evaluate(board);

      if (score == 10) return score;
      if (score == -10) return score;
      if (Kalah.gameOver(board)) return 0;

      //int sideMin;
      //if (isMax) side == 1? sideMin = 0 : sideMin = 1;
      //else sideMin = side;

      if (isMax)
      {
          int best = MIN;

          for (int i = 1; i <= 7; i++)
          {
              int number = board.getSeeds(side, i);

              if(number != 0)
              {
                  int index = 1;
                  int[] orgOppNum = new int [] {1000, 1000, 1000, 1000, 1000, 1000, 1000};
                  makeNewMove(board, side, i, index, orgOppNum);

                  best = Math.max(best, minimax(board, depth + 1, !isMax, side.opposite(), alpha, beta));
                  alpha = Math.max(alpha, best);

                  reverseMove(board, side, number, index, i, orgOppNum);

                  // Alpha Beta Pruning
                  if (beta <= alpha)
                  break;
              }
          }
          return best;
      }
      else
      {
          int best = MAX;

          for (int i = 1; i <= 7; i++)
          {
              int number = board.getSeedsOp(side, i);

              if(number != 0)
              {
                  int index = 1;
                  int[] orgOppNum = new int [] {1000, 1000, 1000, 1000, 1000, 1000, 1000};
                  makeNewMove(board, side.opposite(), i, index, orgOppNum);

                  best = Math.min(best, minimax(board, depth + 1, !isMax, side.opposite(), alpha, beta));
                  beta = Math.min(beta, best);

                  reverseMove(board, side.opposite(), number, index, i, orgOppNum);

                  // Alpha Beta Pruning
                  if (beta <= alpha)
                  break;
              }
          }

          return best;
      }
  }

  public static Move findBestMove(Board board, Side side)
  {
      int bestVal = -1000;
      Move bestMove = new Move(side, 1);

      for (int i = 1; i <= 7; i++)
      {
          int number = board.getSeedsOp(side, i);
          if(number != 0)
          {
              int k = 1;
              int moveVal = minimax(board, 0, false, side, MIN, MAX);

              if (moveVal > bestVal)
              {
                  bestMove = new Move(side, i);
                  bestVal = moveVal;
              }
          }
      }

      System.out.println("The value of the best move is: " + bestVal);

      return bestMove;
  }

  public static void main(String[] args)
  {
      Board board = new Board(7, 7);
      board.setSeeds(Side.SOUTH, 1, 8);
      board.setSeeds(Side.SOUTH, 3, 8);
      board.setSeeds(Side.SOUTH, 4, 8);
      board.setSeeds(Side.SOUTH, 5, 8);
      board.setSeeds(Side.SOUTH, 6, 8);
      board.setSeeds(Side.SOUTH, 7, 8);
      board.setSeedsInStore(Side.SOUTH, 1);

      //{
      //    {0, 7, 7, 7, 7, 7, 7, 7},
      //    {1, 8, 0, 8, 8, 8, 8, 8}
      //}

      Move bestMove = findBestMove(board, Side.NORTH);
      System.out.println("The optimal move is:");
      System.out.println("SIDE: " + bestMove.getSide() + " HOLE: " + bestMove.getHole());

  }
}
