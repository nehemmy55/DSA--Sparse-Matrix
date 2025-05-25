# DSA--Sparse-Matrix


**Overview**

This project implements a sparse matrix data structure and operations (addition, subtraction, multiplication) in Python for the "Data Structures and Algorithms for Engineers" Programming Assignment 2. It efficiently handles large sparse matrices by storing only non-zero elements, optimizing for both memory and runtime. The program reads matrices from input files, performs the selected operation, and saves the result to an automatically generated output file.

Features

Sparse Matrix Representation: Uses a dictionary to store non-zero elements with (row, col) keys, minimizing memory usage.

Operations: Supports addition, subtraction, and multiplication of sparse matrices

Input Handling: Reads matrices from files in the format rows=X, cols=Y, followed by (row, col, value) entries.

Error Handling: Skips invalid indices (e.g., out-of-bounds) silently and throws errors for malformed input formats.

Output: Saves results to output/<operation>.txt (e.g., addition.txt) in the same directory as the input files.

No External Libraries: Implements all functionality without prohibited libraries like regex, using only os and sys for file handling.
