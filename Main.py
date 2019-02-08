from Ricochet import Ricochet

def main():
    rico = Ricochet()
    rico.grid.loadGrid("grids/grid1.csv")
    rico.isWin()
    print(rico.grid)
    print(repr(rico.grid))
    rico.move("Red", "left")
    print(rico.grid)

if __name__ == "__main__":
    main()