#include <stdio.h>
#include <stdlib.h>

// Define a structure for a Node in the linked list
struct Node
{
    int data;          // Data part of the node
    struct Node *next; // Pointer to the next node
};

struct Node *head = NULL; // Initialize the head of the linked list as NULL (empty list)

// Function to insert a new node at the beginning of the list
void insert(int value)
{
    // Allocate memory for the new node
    struct Node *newNode = (struct Node *)malloc(sizeof(struct Node));
    // Assign the value to the new node and set its next pointer to the current head
    newNode->data = value;
    newNode->next = head;
    head = newNode; // Update the head to point to the new node
}

// Recursive function to print the linked list in reverse order
void printReverse(struct Node *node)
{
    // Base case: if the node is NULL, return (end of the list)
    if (node == NULL)
    {
        return;
    }
    // Recursively call the function for the next node
    printReverse(node->next);
    // Print the data of the current node after returning from recursion
    printf("%d\n", node->data);
}

// Function to display the linked list in reverse order
void display()
{
    // Check if the list is empty
    if (head == NULL)
    {
        printf("\nLinked List is Empty!"); // Print message if list is empty
        return;
    }
    // Otherwise, print the linked list in reverse order
    printf("\nLinked List in reverse order:\n");
    printReverse(head); // Call the recursive function to print in reverse
}

// Main function providing a menu-driven interface for the linked list operations
void main()
{
    int choice, value;

    // Infinite loop to continuously show menu and process user's input
    while (1)
    {
        printf("\n\n*** LINKED LIST MENU ***\n");
        printf("1. Insert\n2. Print in Reverse\n3. Exit");
        printf("\nEnter your choice: ");
        scanf("%d", &choice);

        // Perform actions based on the user's choice
        switch (choice)
        {
        case 1:
            printf("Enter the value to insert: ");
            scanf("%d", &value);
            insert(value); // Call function to insert value into the list
            break;
        case 2:
            display(); // Call function to display the list in reverse order
            break;
        case 3:
            exit(0); // Exit the program
        default:
            printf("\nInvalid choice! Try again."); // Handle invalid input
        }
    }
}