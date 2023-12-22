class findOuterPoints:
    minX, maxX, minY, maxY = 0, 0, 0, 0
        
    @staticmethod
    def findOuterLimits(printed_matrix):
        findOuterPoints.minX, findOuterPoints.maxX, findOuterPoints.minY, findOuterPoints.maxY = float('inf'), 0, float('inf'), 0

        for i in range(len(printed_matrix)):
            for j in range(len(printed_matrix[0])):
                if printed_matrix[i][j] == 1:
                    if i < findOuterPoints.minX:
                        findOuterPoints.minX = i
                    if j < findOuterPoints.minY:
                        findOuterPoints.minY = j
                    if i > findOuterPoints.maxX:
                        findOuterPoints.maxX = i
                    if j > findOuterPoints.maxY:
                        findOuterPoints.maxY = j

    @staticmethod
    def findClosestLimit(start_x_object, start_y_object):
        diff_xmin = abs(start_x_object - findOuterPoints.minX)
        diff_xmax = abs(start_x_object - findOuterPoints.maxX)
        diff_ymin = abs(start_y_object - findOuterPoints.minY)
        diff_ymax = abs(start_y_object - findOuterPoints.maxY)

        closest_limit = min(diff_xmin, diff_xmax, diff_ymin, diff_ymax)

        if closest_limit == diff_xmin:
            return "minX"
        elif closest_limit == diff_xmax:
            return "maxX"
        elif closest_limit == diff_ymin:
            return "minY"
        elif closest_limit == diff_ymax:
            return "maxY"
        
    @staticmethod
    def findPointOnLimit(start_x_object, start_y_object, printed_matrix):
        findOuterPoints.findOuterLimits(printed_matrix)
        closest_limit = findOuterPoints.findClosestLimit(start_x_object, start_y_object)
        if closest_limit == "minX":
            return findOuterPoints.minX, start_y_object
        elif closest_limit == "maxX":
            return findOuterPoints.maxX, start_y_object
        elif closest_limit == "minY":
            return start_x_object, findOuterPoints.minY
        elif closest_limit == "maxY":
            return start_x_object, findOuterPoints.maxY
        return None
        