You can ask the Librarian of the Unseen University to suggest documents corresponding to a set of keywords.

First you have to tell the Libratian how to go about his business by creating a JSON file `~/.ook` that should look something like this (an example is provided in the file `ook.json`):
```json
{
    "shelves": [ "~/Documents/Cooking Books", "~/Discworld Books" ],
    "register": "~/.ook_register"
}
```
Your library is made up of a number of shelves† and each shelf will be scanned by the Librarian to see what documents you have.
A shelf is essentially a directory and the `shelves` parameter in the `~/.ook` file is the list of these directories.
A second parameter is `register` which tells the Librarian where to store†† the information about the documents found on the shelves.
The default is the file `~/.ook_register`, but you can decide to store the register somewhere else.

You can use two executables, one to update the register (`ook-update`), the other one to search for documents matching a number of keywords (`ook`). `ook-update` doesn't need any argument and will only use the information provided in the file `~/.ook`. To find document matching keywords you can use
```bash
ook magical peanuts
```
which should return the best documents you have on your shelves about magical peanuts.

For what it's worth: the Librarian is an orangutan. When he says 'ook' he generally means yes and 'eek' generally means no.

† This might be obvious to most, but the magicians of the Unseen University are not known for their good grasp of pratical matters, so the Librarian has found it best to spell things out clearly when explaining even the simplest things.

†† Technically the register is stored in the Librarian's head, but let's not go there.
