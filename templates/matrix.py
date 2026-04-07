#!/usr/bin/env python3

# NAME:
# MATRIC NO:
# DEPARTMENT:
# TITLE: MATRIX OPERATION PROGRAM
# QUESTION NO: 2

class Matrix(object):
    """ 
    The Matrix class. Can be used to create matrices of varying order.
    """
    def __init__(self, data):
        if not data or not all(len(row) == len(data[0]) for row in data):
            raise ValueError("Invalid matrix")
        self.data = data
        self.rows = len(data)
        self.cols = len(data[0])

    def transpose(self):
        # returns the transpose of the matrix
        data = []
        for i in range(self.cols):
            buf = []
            for j in range(self.rows):
                buf.append(self[j][i])
            data.append(buf)
        return Matrix(data)

    @property
    def is_symmetric(self):
        """
        this method checks for the symmetry of the matrix, that is if the matrix is equal to it's transpose
        """
        if self == self.transpose():
            return True
        else:
            return False
    
    def __eq__(self,matrix):
        """
        checks for equality, if every element in A is also in B with respect to cardinality/position
        """
        if self.rows == matrix.rows and self.cols == matrix.cols:
            for i in range(self.rows):
                for j in range(self.cols):
                    if self[i][j] != matrix[i][j]:
                        return False
            else:
                return True
        else:
            return False


    def __getitem__(self, index):
        return self.data[index]

    def __repr__(self):
        return f"Matrix: {self.rows} by {self.cols} \n"+"\n".join(str(row) for row in self.data)

    def __str__(self):
        return "\n".join(str(row) for row in self.data)

    def __add__(self,matrix):
        """
        implement matrix addition and allows A + B , where A and B are matrices
        """

        data = []
        for i in range(self.rows):
            buf = []
            for j in range(self.cols):
                buf.append(self[i][j] + matrix[i][j])
            data.append(buf)
        return Matrix(data)

    def __sub__(self,matrix):
        """
        implement matrix subtraction and allows A - B , where A and B are matrices
        """

        data = []
        for i in range(self.rows):
            buf = []
            for j in range(self.cols):
                buf.append(self[i][j] - matrix[i][j])

            data.append(buf)
        return Matrix(data)

    def __mul__(self,obj):
        """
        implement matrix multiplication and allows A * B , where A and B are matrices. It also allows scalar multiplication: A * k where k is a scalar of type int
        """
        data = []
        if type(obj) == int:
            # if matrix is scalar, performs scalar multiplication
            for i in range(self.rows):
                buf = []
                for j in range(self.cols):
                    buf.append(self[i][j] * obj)
                data.append(buf)

            return Matrix(data)

        else:
            for i in range(self.rows):
                buf = []
                for j in range(self.cols):
                    buf.append(sum([self[i][k]*obj[k][j] for k in range(self.rows)]))
                data.append(buf)

            return Matrix(data)

def main():
    print("MATRIX OPERATIONS\n")

    """
    print("\nMatrix A:")
    A = [0,0,0]
    B = [0,0,0]
    A[0] = [x.strip() for x in input("[a,b,c]: ").split(",")]
    A[1] = [x.strip() for x in input("[d,e,f]: ").split(",")]
    A[2] = [x.strip() for x in input("[g,h,i]: ").split(",")]
    print("\nMatrix B: ")
    B[0] = [x.strip() for x in input("[a,b,c]: ").split(",")]
    B[1] = [x.strip() for x in input("[d,e,f]: ").split(",")]
    B[2] = [x.strip() for x in input("[g,h,i]: ").split(",")]
    """
    A = [[2,3,7],[1,2,3],[7,5,6]]
    B = [[9,0,1],[2,5,4],[0,0,1]]
    A = Matrix(A)
    B = Matrix(B)
    print(f"Matrix A: \n{A}\n")
    print(f"Matrix B: \n{B}\n")
    print(f"Addition: A + B\n{A+B}\n")
    print(f"Subtraction: A - B\n{A-B}\n")
    print(f"Multiplication: A * B\n{A*B}\n")
    print(f"Transpose of A: \n{A.transpose()}\n")
    print(f"Is a A symmetrical?: {A.is_symmetric}")


if __name__ == "__main__":
    main()