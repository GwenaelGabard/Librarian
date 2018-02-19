
* [ ] Use threads to scan files and mark them, because at the moment it will be very slow.
* [ ] Improve the generation of tokens for each document. For instance merge singular and plural of the same words
* [ ] The register's data structure won't cope with large amounts of documents. At the moment we store a corpus of words for each document. To speed up the marking we need a dictionary with
  * Words as keys
  * A list of document names and occurences of this word as values
This will make the update of the register more complicated.
* [ ] Make the file names clickable in the results
* [ ] Use a different data layout for the set of corpus (corpi?) to speed marking up
* [ ] Handle failed parsing of PDFs gracefully instead of crashing like a drunk city guard
* [ ] Give a bag of peanuts to the Librarian
