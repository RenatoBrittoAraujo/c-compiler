#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define DEFAULT_SIZE 1000

#define TNONE 0
#define TINT 1
#define TROOT 2
#define TSTRING 3
#define TFUNCTION 4
#define TEXPRESSION 5
#define TSUM 6

#define VINT "int"
#define VROOT "root"
#define VSTRING "string"
#define VFUNCTION "function"
#define VEXPRESSION "expression"
#define VSUM "sum"

int SOURCE_SIZE = DEFAULT_SIZE;
char* SAVE_PATH = "a.out";

char ** read_source();

int main() {
    read_source();
}

// func
char** read_source() {
    char** source = malloc(sizeof(char)*SOURCE_SIZE);
    char buffer[DEFAULT_SIZE];
    while(scanf("%s", buffer) != EOF) {
        printf("\"%s\"", buffer);
    }
    printf("program finished read");
    return source;
}

void write_compiled() {

}

void compile() {

}

struct Terminal {

};
struct NonTerminal {

};

struct Token {
    int type;
    char value[100];
    
    int procedure_size;
    Token procedure[100];
    
    int operands_size;
    Token operands[100];

    Token* parent;
};
typedef struct Token Token;

Token create_token(int type, char* value, Token* parent) {
    Token t;
    t.type = type;
    strcat(t.value, value);
    t.procedure_size = 0;
    t.operands_size = 0;
    t.parent = parent;
    return t;
}

char buffer[DEFAULT_SIZE];
int bufp = 0;

void clear_buffer() {
    bufp = 0;
    buffer[0] = '\0';
}

int is_buffer_empty() {
    return bufp == 0;
}

void add_to_buffer(char x) {
    buffer[bufp++] = x;
}

Token get_buffer_token() {
    if (is_buffer_empty()) {
    }
}

Token add_to_buffer_token(Token* target) {
    Token new_token = get_buffer_token();
    target->procedure[target->procedure_size++] = &target;
    return new_token;
}

int is_alphabet(char c) {
    if ((c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z')) return 1;
    return 0;
}

int is_number(char c) {
    if ((c >= '0' && c <= '9')) return 1;
    return 0;
}

int is_special(char c) {
    if (!is_alphabet(c) && !is_number(c)) return 1;
    return 0;
}

int is_int(char* s, int n) {
    return strcmp(s, "int") == 0;
}

// If return 0, its not type
// Else returns type
int get_type(char *s, int n) {
    if (is_int(s, n)) return TINT;
    return 0;
}

void linear_analysis(char* target) {
    int size = strlen(target);

    Token root = create_token(TROOT, VROOT, NULL);
    Token* current = &root;

    int ctype = TNONE;
    char cvalue[100];
    
    int string_start = 0;
    int comment_start = 0;
    int line_n = 1;
    int char_n = 0;

    int append_to_procedure = 1;

    //





    // if ctype == root, add to procedure a new function
    
    // if ctype == function and c == '{', append_to_procedure = true

    // if ctype == function and c == '(', append_to_procedure = false

    // if c == " and no string_start, add to last  all chars as string
    
    // if c == " and string_start, finish string
    
    // if c == "/" and buffer == "/", comment_start = true
    
    // if c != "\n" and comment_start, continue
    
    // if c == "\n" and comment_start, comment_start = false

    // if c == 

    
    for (int i = 0; i < size; i++) {
        char c = target[i];
        char_n++;

        // End of "thing"
        // May be:
        // - Breakline in an expression
        // - Space between type of function and its and name
        if (c == ' ' || c == '\n') {
            if (c == '\n') { line_n++; char_n = 0; }

            if (ctype == TNONE) {

            }
            if (get_type()) {

            }

            clear_buffer(current);
            continue;
        }

        // New procedure begins
        if (c == '{') {
            // Set parent of child as current
            current->procedure[current->procedure_size - 1].parent = current;

            // Set child as current
            current = &current->procedure[current->procedure_size - 1];
        }

        // Procedure ends, return to parent.
        if (c == '}') {
            // Set current as parent of current
            current = current->parent;
        }

        // New expression begins
        if (c == "(") {
            Token new_token = create_token(TEXPRESSION, "", current);

            current = &new_token;
        }

        // End of expression
        if (c == ")") {
            
        }

        if (c == ";") {
            
        }







        add_to_buffer(c);
    }

}