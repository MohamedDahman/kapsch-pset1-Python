Use case:
	User opens website.
	First image of several images is shown.
	There is a dropdown that is used to categorize the image.
	The dropdown shows an empty entry at the beginning.
	User chooses a category (A, B or C), then presses a button, the categorization is saved, andthe next image is shown.

Challenge:
	Create database* 
	Create database access (read, write)
	Insert pictures "by hand" into the database* 
	Create a website* Show image on a website* 
	Create a dropdown
Details:
	Create database with 1 table
		Table 1 contains 2 columns (image | category)
		image can be of type "blob" (depends on database)
		category is varchar (1), can be null
		insert some images by hand
	Create Website
 		Show the image stored in the database
		Show a dropdown with 3 entries, "A", "B", "C" 
		Goal: categorize the image-- There is a next button >-- You choose an entry from the dropdown = you categorize the image
		If you press the > button the categorization is saved and the next image is shown
