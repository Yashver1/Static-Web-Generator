from directory_handlers import recursive_move
from helper_functions import generate_pages_recursive,generate_page


def main():
    recursive_move("static","public")
    generate_pages_recursive("content","template.html","public")


main()
