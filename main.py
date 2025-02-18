""" Program to create and manage a list of books that the user wishes to read, and books that the user has read. """

from bookstore import Book, BookStore
from menu import Menu
import ui

store = BookStore()


def main():

    menu = create_menu()

    while True:
        choice = ui.display_menu_get_choice(menu)
        action = menu.get_action(choice)
        action()
        if choice == 'Q':
            break


def create_menu():
    menu = Menu()
    menu.add_option('1', 'Add Book', add_book)
    menu.add_option('2', 'Search For Book', search_book)
    menu.add_option('3', 'Show Unread Books', show_unread_books)
    menu.add_option('4', 'Show Read Books', show_read_books)
    menu.add_option('5', 'Show All Books', show_all_books)
    menu.add_option('6', 'Change Book Read Status', change_read)
    menu.add_option('7', 'Delete Book', delete_book)
    menu.add_option('Q', 'Quit', quit_program)

    return menu


def add_book():
    new_book = ui.get_book_info()
    while new_book:  # if book author and a title exists
        # found None/BookError is returned, print message to user.
        if store.exact_match(new_book):
            print('\n** You already have this book in your reading list.**\n')
        else:
            new_book.save()
            print(
                f'{new_book.title} by {new_book.author} has been added to your reading list.')
        break


def show_read_books():
    read_books = store.get_books_by_read_value(True)
    ui.show_books(read_books)


def show_unread_books():
    unread_books = store.get_books_by_read_value(False)
    ui.show_books(unread_books)


def show_all_books():
    books = store.get_all_books()
    ui.show_books(books)


def search_book():
    search_term = ui.ask_question(
        'Enter search term, will match partial authors or titles.')
    matches = store.book_search(search_term)
    ui.show_books(matches)


def change_read():

    book_id = ui.get_book_id()
    book = store.get_book_by_id(book_id)
    # If book id is found on DB, continue to ask user if book was read already and save new status if any
    if book != None:
        new_read = ui.get_read_value()
        book.read = new_read
        if new_read == True:
            print(
                f'\nYou have read {book.title.title()} by {book.author.title()}\n')
        else:
            print(
                f'\nYou have not read {book.title.title()} by {book.author.title()}\n')
        book.save()
    else:
        print("\nBook not found. Try again!\n")


def delete_book():
    book_id = ui.get_book_id()
    book = store.get_book_by_id(book_id)  # look for user id in db
    if book != None:  # if book exist in the database
        book.delete()  # delete it
        print()
        # display to user book was deleted
        print(
            f'❌ {book.title.capitalize()} by {book.author.capitalize()} was deleted from reading list.\n')
    else:
        print('Error: Book Not Found\n')


def quit_program():
    ui.message('Thanks and bye!')


if __name__ == '__main__':
    main()
