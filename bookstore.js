// Step 2: switch database (use bookstore is not valid in a script)
db = db.getSiblingDB("bookstore")

// Step 3: load authors.json
db.authors.drop()
doc = JSON.parse(fs.readFileSync("authors.json", "utf8"))
db.authors.insertMany(doc)

// Step 4: load books.json
db.books.drop()
doc = JSON.parse(fs.readFileSync("books.json", "utf8"))
db.books.insertMany(doc)

// Step 5: list authors and books
printjson(db.authors.find().toArray())
printjson(db.books.find().toArray())

// Step 6: insert two new books
db.books.insertMany([
  { title: "The Long Earth", published_year: 2012, author_ids: ["author_003", "author_004"] },
  { title: "The Hitchhiker's Guide to the Galaxy", published_year: 1979, author_ids: ["author_005"] }
])

// Step 7: add missing authors
db.authors.insertMany([
  { _id: "author_004", name: "Stephen Baxter", nationality: "British",
    bio: { short: "British science fiction author.", long: "Stephen Baxter is a British hard science fiction writer known for the Xeelee sequence and collaborations with Terry Pratchett and Arthur C. Clarke." } },
  { _id: "author_005", name: "Douglas Adams", nationality: "British",
    bio: { short: "British author and humorist.", long: "Douglas Adams created The Hitchhiker's Guide to the Galaxy, which began as a BBC radio comedy in 1978." } }
])

// Step 8: filter books by a list of authors
printjson(db.books.find({ author_ids: { $in: ["author_001", "author_004", "author_005"] } }).toArray())