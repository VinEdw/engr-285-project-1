#let conf(
  doc,
  title: [Clever Title],
  authors: (
    (
      first_name: "First",
      last_name: "Last",
    ),
  ),
  date: datetime.today(),
) = {
  // Document Metadata
  let author_names = authors.map(author => author.first_name + " " + author.last_name).join(", ", last: ", and ")
  set document(
    title: title,
    author: author_names,
  )

  // Page size and numbering
  set page(
    "us-letter",
    header: context {
      if counter(page).get().first() > 1 { 
        emph(title)
        h(1fr)
        counter(page).display("1")
      }
    },
  )

  // Style raw blocks
  show raw: it => block(fill: rgb("#E6E6E6"), inset: 0.6em, width: 100%, it)

  // Title
  stack(
    dir: direction.ttb,
    spacing: 1em,
    text(17pt, weight: "bold", title),
    text(14pt, author_names),
    text(14pt, date.display("[month repr:long] [day padding:none], [year]")),
  )
  // Main Document
  doc
}

#let py_script(fname, put_fname: false) = {
  set raw(block: true)

  let script = read("scripts/" + fname + ".py")
  let output = read("output/" + fname + ".output")

  if (put_fname) {
    block(sticky: true)[*#fname\.py*]
  }
  raw(script, lang: "python")

  if (output.len() != 0) {
    block(sticky: true)[*Output:*]
    raw(output)
  }
}
