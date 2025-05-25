import sys
import os

class SparseMatrix:
    def __init__(self, num_rows=None, num_cols=None, file_path=None):
        """Initialize a sparse matrix either with dimensions or from a file."""
        self.elements = {}  # Dictionary to store non-zero elements: (row, col) -> value
        if file_path:
            self._load_from_file(file_path)
        else:
            if num_rows <= 0 or num_cols <= 0:
                raise ValueError("Invalid matrix dimensions")
            self.rows = num_rows
            self.cols = num_cols

    def _load_from_file(self, file_path):
        """Read sparse matrix from file with format: rows=X, cols=Y, (row,col,value)."""
        try:
            with open(file_path, 'r') as file:
                lines = file.readlines()
                if len(lines) < 2:
                    raise ValueError("Input file has wrong format")

                # Parse rows
                if not lines[0].startswith("rows="):
                    raise ValueError("Input file has wrong format")
                self.rows = int(lines[0].strip()[5:])
                if self.rows <= 0:
                    raise ValueError("Invalid number of rows")

                # Parse cols
                if not lines[1].startswith("cols="):
                    raise ValueError("Input file has wrong format")
                self.cols = int(lines[1].strip()[5:])
                if self.cols <= 0:
                    raise ValueError("Invalid number of columns")

                # Parse matrix elements
                for line_number, line in enumerate(lines[2:], start=3):
                    line = line.strip()
                    if not line or line.isspace():
                        continue  # Skip empty or whitespace lines
                    if not (line.startswith('(') and line.endswith(')')):
                        raise ValueError(f"Input file has wrong format at line {line_number}: {line}")

                    # Parse (row, col, value)
                    content = line[1:-1].split(',')
                    if len(content) != 3:
                        raise ValueError(f"Input file has wrong format at line {line_number}: {line}")

                    try:
                        row = int(content[0].strip())
                        col = int(content[1].strip())
                        value = int(content[2].strip())
                    except ValueError:
                        raise ValueError(f"Input file has wrong format at line {line_number}: {line}")

                    if row < 0 or row >= self.rows or col < 0 or col >= self.cols:
                        continue  # Silently skip invalid indices
                    if value != 0:  # Only store non-zero values
                        self.elements[(row, col)] = value

        except FileNotFoundError:
            raise ValueError(f"Unable to open file: {file_path}")

    def get_element(self, curr_row, curr_col):
        """Get element at position (curr_row, curr_col). Returns 0 if not set."""
        if curr_row < 0 or curr_row >= self.rows or curr_col < 0 or curr_col >= self.cols:
            raise ValueError("Invalid row or column index")
        return self.elements.get((curr_row, curr_col), 0)

    def set_element(self, curr_row, curr_col, value):
        """Set element at position (curr_row, curr_col) to value."""
        if curr_row < 0 or curr_row >= self.rows or curr_col < 0 or curr_col >= self.cols:
            raise ValueError("Invalid row or column index")
        if value == 0:
            self.elements.pop((curr_row, curr_col), None)
        else:
            self.elements[(curr_row, curr_col)] = value

    def add(self, other):
        """Add two sparse matrices."""
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Matrix dimensions do not match for addition")
        
        result = SparseMatrix(self.rows, self.cols)
        # Copy elements from first matrix
        for key, value in self.elements.items():
            result.elements[key] = value
        
        # Add elements from second matrix
        for key, value in other.elements.items():
            result.elements[key] = result.elements.get(key, 0) + value
            if result.elements[key] == 0:
                result.elements.pop(key)
        
        return result

    def subtract(self, other):
        """Subtract other sparse matrix from this one."""
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Matrix dimensions do not match for subtraction")
        
        result = SparseMatrix(self.rows, self.cols)
        # Copy elements from first matrix
        for key, value in self.elements.items():
            result.elements[key] = value
        
        # Subtract elements from second matrix
        for key, value in other.elements.items():
            result.elements[key] = result.elements.get(key, 0) - value
            if result.elements[key] == 0:
                result.elements.pop(key)
        
        return result

    def multiply(self, other):
        """Multiply two sparse matrices using row-based indexing for efficiency."""
        if self.cols != other.rows:
            raise ValueError("Matrix dimensions do not match for multiplication")
        
        result = SparseMatrix(self.rows, other.cols)
        # Create a row-based index for the second matrix
        row_index = {}
        for (row2, col2), val2 in other.elements.items():
            if row2 not in row_index:
                row_index[row2] = []
            row_index[row2].append((col2, val2))
        
        # Iterate over first matrix's non-zero elements
        for (row1, col1), val1 in self.elements.items():
            # Only process rows in the second matrix that match col1
            if col1 in row_index:
                for col2, val2 in row_index[col1]:
                    product = val1 * val2
                    if product != 0:  # Only store non-zero results
                        result_key = (row1, col2)
                        result.elements[result_key] = result.elements.get(result_key, 0) + product
                        if result.elements[result_key] == 0:
                            result.elements.pop(result_key)
        
        return result

    def save_to_file(self, file_path):
        """Save sparse matrix to file in the specified format, creating output directory if needed."""
        try:
            # Ensure output directory exists
            output_dir = os.path.dirname(file_path)
            if output_dir and not os.path.exists(output_dir):
                os.makedirs(output_dir)
                
            with open(file_path, 'w') as file:
                file.write(f"rows={self.rows}\n")
                file.write(f"cols={self.cols}\n")
                for (row, col), value in self.elements.items():
                    file.write(f"({row}, {col}, {value})\n")
        except IOError:
            raise ValueError(f"Unable to write to output file: {file_path}")

def main():
    """Main function to handle user input and perform matrix operations."""
    try:
        # Get input from user
        file1 = input("Enter first matrix file path: ")
        file2 = input("Enter second matrix file path: ")
        operation = int(input("Select operation (1=Addition, 2=Subtraction, 3=Multiplication): "))

        # Determine output filename based on operation
        operation_names = {1: "addition.txt", 2: "subtraction.txt", 3: "multiplication.txt"}
        if operation not in operation_names:
            raise ValueError("Invalid operation selected")
        output_filename = operation_names[operation]

        # Create output directory relative to first input file
        input_dir = os.path.dirname(file1)
        output_dir = os.path.join(input_dir, "output")
        output_file = os.path.join(output_dir, output_filename)

        # Load matrices
        matrix1 = SparseMatrix(file_path=file1)
        matrix2 = SparseMatrix(file_path=file2)

        # Perform selected operation
        if operation == 1:
            result = matrix1.add(matrix2)
        elif operation == 2:
            result = matrix1.subtract(matrix2)
        elif operation == 3:
            result = matrix1.multiply(matrix2)
        else:
            raise ValueError("Invalid operation selected")

        # Save result to output file
        result.save_to_file(output_file)
        print(f"Operation completed. Result saved to {output_file}")

    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()