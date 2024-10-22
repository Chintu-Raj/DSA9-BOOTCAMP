#include <stdio.h>
#include <stdlib.h>

// Define the structure for a stack node
struct Node {
    int data;
    struct Node* next; // Pointer to the next node
};

// Define the structure for the stack
struct Stack {
    struct Node* top; // Pointer to the top node
};

// Function to create a new stack
struct Stack* createStack() {
    struct Stack* stack = (struct Stack*)malloc(sizeof(struct Stack));
    stack->top = NULL; // Initialize top to NULL
    return stack;
}

// Function to check if the stack is empty
int isEmpty(struct Stack* stack) {
    return stack->top == NULL;
}

// Function to push an element onto the stack
void push(struct Stack* stack, int value) {
    struct Node* newNode = (struct Node*)malloc(sizeof(struct Node));
    newNode->data = value;
    newNode->next = stack->top; // Link the new node to the previous top
    stack->top = newNode; // Update top to the new node
    printf("Pushed %d onto the stack.\n", value);
}

// Function to pop an element from the stack
int pop(struct Stack* stack) {
    if (isEmpty(stack)) {
        printf("Stack is empty! Cannot pop.\n");
        return -1; // Return -1 if the stack is empty
    }
    struct Node* temp = stack->top; // Get the top node
    int poppedValue = temp->data; // Store the value to return
    stack->top = stack->top->next; // Update top to the next node
    free(temp); // Free the memory of the popped node
    printf("Popped %d from the stack.\n", poppedValue);
    return poppedValue;
}

// Function to display the elements in the stack
void display(struct Stack* stack) {
    if (isEmpty(stack)) {
        printf("Stack is empty.\n");
        return;
    }
    struct Node* temp = stack->top;
    printf("Stack elements: ");
    while (temp != NULL) {
        printf("%d ", temp->data);
        temp = temp->next; // Move to the next node
    }
    printf("\n");
}

// Main function to demonstrate stack operations
int main() {
    struct Stack* stack = createStack();
    int choice, value;

    do {
        printf("\nStack Operations Menu:\n");
        printf("1. Push\n");
        printf("2. Pop\n");
        printf("3. Display\n");
        printf("4. Exit\n");
        printf("Enter your choice: ");
        scanf("%d", &choice);

        switch (choice) {
            case 1:
                printf("Enter the element to push: ");
                scanf("%d", &value);
                push(stack, value);
                break;
            case 2:
                pop(stack);
                break;
            case 3:
                display(stack);
                break;
            case 4:
                printf("Exiting...\n");
                break;
            default:
                printf("Invalid choice. Please try again.\n");
        }
    } while (choice != 4);

    // Free the stack memory
    while (!isEmpty(stack)) {
        pop(stack); // Pop all elements to free memory
    }
    free(stack); // Free the stack structure

    return 0;
}