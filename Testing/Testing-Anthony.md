# GeneSearcher Testing

## Module: gui

I wrote unit tests for the Model gui in `test_GUI.py` that tests the existence of the module for appropriate gui appearance. I created a single test class using the python unittest library:
`TestExistence`. Because the gui requires much user interaction and the backend of our code is already unit tested, my testing throughout the development cycle was comprised mainly of ad hoc testing the correctness of input/output for the gui.

`TestExistence` tests the existence of all widgets that comprise the gui, which is mainly trivial because it can be tested manually/visually. Tkinter as a library includes a verification method that returns a value based on the existence of a widget. With this, the equivalency classes is that returned value and 1, verifying the existence of the widget. Much of the functionality of the buttons can only be tested through user interaction, as it begins with uploading a file. These file formats are already unit tested through Charles' work.

## Manual Applicaton / Ad Hoc Testing

Throughout the development cycle, I manually tested many of the functionalities I was currently working on. The prominent tests were:

1. File Dialog Testing
    * The file dialog should be opening upon click event by 'Upload Data' Button.
    * The user should be able to navigate to a desired file, and it should be visible.
        * This involved changing input path parameters and file types.
    * The selected file should appear in a label for the user to view, and the path stored for usage.

2. Report Display Testing
    * The report format is verified as appropriate from backend + other unit testing
    * The report is displayed neatly into the text box
        * This involved different insertion techniques & working with the proportions of the text box
    * The text box is scrollable.
    * There is no overflow.

3. Search Bar Testing
    * The value entered into the search bar is tracked correctly.
    * The report in the text box is accurately parsed, and highlights are created.
    * Searching for a specific keyword will loop appropriately when it reaches the last word.

Overall, testing the GUI while developing was very visually based and thus somewhat hard to document. However, throughout my time working with it I double and triple checked the functionality, trying different types of files, outdated formats, and checking other edge cases such as file name length for overflow.