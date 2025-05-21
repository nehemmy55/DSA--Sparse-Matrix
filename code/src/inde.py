# Node class for linked list to store non-zero elements
class MatrixEntry:
    def __init__(self, row, col, value):
        self.row = row
        self.col = col
        self.value = value
        self.next = None

# SparseMatrix class to handle matrix operations
class SparseMatrix:
    def __init__(self, matrix_file_path=None, num_rows=None, num_cols=None):
        if matrix_file_path:
            self._load_from_file(matrix_file_path)
        elif num_rows is not None and num_cols is not None:
            if num_rows <= 0 or num_cols <= 0:
                raise ValueError("Invalid matrix dimensions")
            self.rows = num_rows
            self.cols = num_cols
            self.head = None
        else:
            raise ValueError("Must provide either file path or matrix dimensions")

    def _read_file_custom(self, file_path):
        """Reads file character by character to avoid built-in read functions."""
        try:
            content = ""
            with open(file_path, 'r') as file:
                while True:
                    char = file.read(1)  # Read one character at a time
                    if not char:
                        break
                    content += char
            return content.splitlines()
        except FileNotFoundError:
            raise ValueError(f"Error: File '{file_path}' not found.")
        except IOError:
            raise ValueError(f"Error: Issue reading file '{file_path}'.")

    def _load_from_file(self, file_path):
        try:
            lines = self._read_file_custom(file_path)  # Use custom file reading function
            
            if not lines or len(lines) < 2:
                raise ValueError("Input file has wrong format")

            # Read rows
            if not lines[0].startswith("rows="):
                raise ValueError("Input file has wrong format")
            self.rows = int(lines[0][5:])

            # Read cols
            if not lines[1].startswith("cols="):
                raise ValueError("Input file has wrong format")
            self.cols = int(lines[1][5:])

            if self.rows <= 0 or self.cols <= 0:
                raise ValueError("Invalid matrix dimensions")

            self.head = None
            # Read matrix entries
            for line in lines[2:]:
                if not line.strip():
                    continue
                row, col, value = self._parse_entry(line)
                self.set_element(row, col, value)

        except ValueError as e:
            raise ValueError(f"Input file error: {e}")

    def _parse_entry(self, line):
        cleaned = ''.join(line.split())
        if not cleaned.startswith('(') or not cleaned.endswith(')'):
            raise ValueError("Input file has wrong format")
        
        content = cleaned[1:-1]
        parts = content.split(',')
        if len(parts) != 3:
            raise ValueError("Input file has wrong format")
        
        try:
            row = int(parts[0])
            col = int(parts[1])
            value = int(parts[2])
        except ValueError:
            raise ValueError("Input file has wrong format")
        
        return row, col, value

    def set_element(self, row, col, value):
        if row >= self.rows or col >= self.cols or row < 0 or col < 0:
            raise IndexError("Index out of bounds")
        if value == 0:
            return  # Don't store zero values

        new_entry = MatrixEntry(row, col, value)
        if not self.head or (self.head.row > row) or (self.head.row == row and self.head.col > col):
            new_entry.next = self.head
            self.head = new_entry
            return

        curr = self.head
        while curr.next and (curr.next.row < row or (curr.next.row == row and curr.next.col < col)):
            curr = curr.next
        
        if curr.row == row and curr.col == col:
            curr.value = value
        else:
            new_entry.next = curr.next
            curr.next = new_entry

    def save_to_file(self, file_path):
        with open(file_path, 'w') as file:
            file.write(f"rows={self.rows}\n")
            file.write(f"cols={self.cols}\n")
            curr = self.head
            while curr:
                file.write(f"({curr.row}, {curr.col}, {curr.value})\n")
                curr = curr.next

def main():
    try:
        print("Select operation: 1- Addition 2- Subtraction 3- Multiplication")
        operation = input("choose operation (1-3): ").strip()
        if operation not in ['1', '2', '3']:
            raise ValueError("Invalid operation selected")

        file1 = input("Enter first matrix file path: ").strip()
        file2 = input("Enter second matrix file path: ").strip()
        output_file = input("Enter output file path: ").strip()

        matrix1 = SparseMatrix(file1)
        matrix2 = SparseMatrix(file2)

        if operation == '1':
            result = matrix1.add(matrix2)
        elif operation == '2':
            result = matrix1.subtract(matrix2)
        else:
            result = matrix1.multiply(matrix2)

        result.save_to_file(output_file)
        print(f"Result saved to {output_file}")

    except ValueError as e:
        print(f"Error: {e}")
    except IndexError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()