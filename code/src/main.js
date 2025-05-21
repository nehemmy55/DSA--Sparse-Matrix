class SparseMatrix {
    constructor(numRows, numCols) {
        this.numRows = numRows;
        this.numCols = numCols;
        this.matrix = {}; // Dictionary-like storage for sparse matrix
    }

    static fromFileContent(text) {
        let lines = SparseMatrix.splitLines(text);
        let numRows = SparseMatrix.extractNumber(lines[0]);
        let numCols = SparseMatrix.extractNumber(lines[1]);
        let sparseMatrix = new SparseMatrix(numRows, numCols);

        for (let i = 2; i < lines.length; i++) {
            let line = SparseMatrix.trimSpaces(lines[i]);
            if (SparseMatrix.isValidEntry(line)) {
                let values = SparseMatrix.splitValues(line);
                let row = SparseMatrix.toNumber(values[0]);
                let col = SparseMatrix.toNumber(values[1]);
                let value = SparseMatrix.toNumber(values[2]);
                sparseMatrix.setElement(row, col, value);
            } else if (line !== "") {
                throw new Error("Input file has wrong format");
            }
        }

        return sparseMatrix;
    }

    getElement(row, col) {
        return this.matrix[row] && this.matrix[row][col] !== undefined ? this.matrix[row][col] : 0;
    }

    setElement(row, col, value) {
        if (!this.matrix[row]) {
            this.matrix[row] = {};
        }
        this.matrix[row][col] = value;
    }

    add(otherMatrix) {
        if (this.numRows !== otherMatrix.numRows || this.numCols !== otherMatrix.numCols) {
            throw new Error("Matrix dimensions do not match for addition.");
        }

        let result = new SparseMatrix(this.numRows, this.numCols);

        for (let row in this.matrix) {
            for (let col in this.matrix[row]) {
                result.setElement(row, col, this.getElement(row, col));
            }
        }

        for (let row in otherMatrix.matrix) {
            for (let col in otherMatrix.matrix[row]) {
                let sum = this.getElement(row, col) + otherMatrix.getElement(row, col);
                result.setElement(row, col, sum);
            }
        }

        return result;
    }

    subtract(otherMatrix) {
        if (this.numRows !== otherMatrix.numRows || this.numCols !== otherMatrix.numCols) {
            throw new Error("Matrix dimensions do not match for subtraction.");
        }

        let result = new SparseMatrix(this.numRows, this.numCols);

        for (let row in this.matrix) {
            for (let col in this.matrix[row]) {
                result.setElement(row, col, this.getElement(row, col));
            }
        }

        for (let row in otherMatrix.matrix) {
            for (let col in otherMatrix.matrix[row]) {
                let diff = this.getElement(row, col) - otherMatrix.getElement(row, col);
                result.setElement(row, col, diff);
            }
        }

        return result;
    }

    multiply(otherMatrix) {
        if (this.numCols !== otherMatrix.numRows) {
            throw new Error("Matrix multiplication is not possible: Column count of first matrix must match row count of second matrix.");
        }

        let result = new SparseMatrix(this.numRows, otherMatrix.numCols);

        for (let row in this.matrix) {
            for (let col in this.matrix[row]) {
                let valueA = this.getElement(row, col);

                if (otherMatrix.matrix[col]) {
                    for (let k in otherMatrix.matrix[col]) {
                        let product = valueA * otherMatrix.getElement(col, k);
                        result.setElement(row, k, result.getElement(row, k) + product);
                    }
                }
            }
        }

        return result;
    }

    static splitLines(text) {
        let lines = [], current = "";
        for (let i = 0; i < text.length; i++) {
            if (text[i] === "\n") {
                lines.push(current);
                current = "";
            } else {
                current += text[i];
            }
        }
        if (current) lines.push(current);
        return lines;
    }

    static trimSpaces(str) {
        let start = 0, end = str.length - 1;
        while (start <= end && (str[start] === " " || str[start] === "\t")) start++;
        while (end >= start && (str[end] === " " || str[end] === "\t")) end--;
        return str.substring(start, end + 1);
    }

    static isValidEntry(line) {
        return line.length > 2 && line[0] === "(" && line[line.length - 1] === ")";
    }

    static splitValues(line) {
        let values = [], current = "";
        for (let i = 1; i < line.length - 1; i++) {
            if (line[i] === ",") {
                values.push(current);
                current = "";
            } else {
                current += line[i];
            }
        }
        values.push(current);
        return values;
    }

    static extractNumber(str) {
        let parts = SparseMatrix.splitValues(str);
        return SparseMatrix.toNumber(parts[1]);
    }

    static toNumber(str) {
        let num = 0, sign = 1, start = 0;
        if (str[0] === "-") {
            sign = -1;
            start = 1;
        }
        for (let i = start; i < str.length; i++) {
            num = num * 10 + (str[i] - "0");
        }
        return num * sign;
    }
}

// **Automated Execution**
function loadMatrixFromDirectory(directory, filename) {
    let simulatedFileData = {
        "/dsa/sparse_matrix/sample_inputs/input1.txt": "rows=3\ncols=3\n(0,0,5)\n(1,1,-3)\n(2,2,9)",
        "/dsa/sparse_matrix/sample_inputs/input2.txt": "rows=3\ncols=3\n(0,1,4)\n(1,0,-2)\n(2,1,6)"
    };

    let filePath = directory + "/" + filename;
    
    if (simulatedFileData[filePath]) {
        return simulatedFileData[filePath]
    } else {
        throw new Error("File not found: " + filePath);
    }
}

// Load matrices automatically
let matrixData1 = loadMatrixFromDirectory("./DSA--sparse-matrix/sample_inputs", "easy_sample_02_1.txt");
let matrixData2 = loadMatrixFromDirectory("./DSA--sparse-matrix/sample_inputs", "easy_sample_02_2.txt");

let matrixA = SparseMatrix.fromFileContent(matrixData1);
let matrixB = SparseMatrix.fromFileContent(matrixData2);

// Perform operations
let sumMatrix = matrixA.add(matrixB);
let diffMatrix = matrixA.subtract(matrixB);
let productMatrix = matrixA.multiply(matrixB);

console.log("Sum Matrix:", sumMatrix.matrix);
console.log("Difference Matrix:", diffMatrix.matrix);
console.log("Product Matrix:", productMatrix.matrix);