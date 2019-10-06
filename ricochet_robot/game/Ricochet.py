from ricochet_robot.game.board_ricochet import BoardRicochet

class Ricochet :
    
    def __init__(self, dim_x=16, dim_y=16):
        self.grid = BoardRicochet(dim_x, dim_y)


    def is_win(self):
        """
        True if the player winned, else : false
            :param self: The game itself
        """   
        for x in range(self.grid.size_X()):
            for y in range(self.grid.size_Y()):
                case = self.grid.get_case(x, y)
                if "Red" in case and "RedWin" in case:
                    return True
                elif "Blue" in case and "BlueWin" in case:
                    return True
                elif "Green" in case and "GreenWin" in case:
                    return True
                elif "Yellow" in case and "YellowWin" in case:
                    return True
        return False


    def _move(self, color, vec, blocking_walls):
        """
        Can move a color token following the rules of ricochet in the direction describes by vec
            :param self: The game itself
            :param color: The color of the token
            :param vec: A tuple of shape (movingX, movingY)
            :param blocking_walls: A tuple of shape (blocking wall current case, blocking wall adjacent case)
        """
        blocking = blocking_walls
        blocking[1] = {blocking[1], "Red", "Yellow", "Green", "Blue"}
        tocken_pos = self.grid.find_color(color)
        current_case = self.grid.get_case(*tocken_pos)
        try:
            adj_case = self.grid.get_case(tocken_pos[0] + vec[0], tocken_pos[1] + vec[1])
            nb_moves = 0
            while adj_case != None and blocking[0] not in current_case and ((blocking[1] & set(adj_case)) == set()) :
                current_case = adj_case
                nb_moves += 1
                try:
                    adj_case = self.grid.get_case(
                        tocken_pos[0] + (nb_moves+1)*vec[0], 
                        tocken_pos[1] + (nb_moves+1)*vec[1]
                    )
                except IndexError:
                    adj_case = None
            self.grid.del_elements(*tocken_pos, color)
            self.grid.add_elements(
                tocken_pos[0] + (nb_moves)*vec[0], 
                tocken_pos[1] + (nb_moves)*vec[1],
                color
            )
        except IndexError:
            pass


    def move(self, color, direction):
        """
        Can move a color token following the rules of ricochet
            :param self: The game itself
            :param color: The color of the token
            :param direction: The movement direction ("left", "right", "up", "low")
        """   
        if direction == "left":
            self._move(color, (-1, 0), ["LeftWall", "RightWall"])
        elif direction == "right":
            self._move(color, (1, 0), ["RightWall", "LeftWall"])
        elif direction == "up":
            self._move(color, (0, -1), ["UpWall", "DownWall"])
        elif direction == "low":
            self._move(color, (0, 1), ["DownWall", "UpWall"])
        else:
            raise Exception("Direction parameter must be equal to 'left', 'right', 'up' or 'low'.")